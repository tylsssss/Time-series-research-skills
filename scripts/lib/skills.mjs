// Shared helpers for the repository scripts.
//
// Kept dependency-free on purpose: `node scripts/*.mjs` must work on a fresh
// checkout with no install step.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

/** Paths that are never part of the shipped artifact. */
export const SKIP_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', '__pycache__', '.venv', 'venv',
  '.backup', '.idea', '.vscode', '.pytest_cache', '.mypy_cache', '.ruff_cache',
]);

export function readText(abs) {
  return fs.readFileSync(abs, 'utf8');
}

export function exists(abs) {
  return fs.existsSync(abs);
}

export function isDir(abs) {
  try { return fs.statSync(abs).isDirectory(); } catch { return false; }
}

export function rel(abs) {
  return path.relative(ROOT, abs).split(path.sep).join('/');
}

/** Recursively list files, skipping SKIP_DIRS. */
export function walk(dir, out = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const entry of entries) {
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      walk(abs, out);
    } else if (entry.isFile()) {
      out.push(abs);
    }
  }
  return out;
}

/** List skill directories: `<root>/skills/<name>/SKILL.md`. */
export function listSkills() {
  const skillsDir = path.join(ROOT, 'skills');
  if (!isDir(skillsDir)) return [];
  return fs.readdirSync(skillsDir, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => path.join(skillsDir, e.name))
    .filter((dir) => exists(path.join(dir, 'SKILL.md')))
    .map((dir) => loadSkill(dir))
    .filter(Boolean);
}

export function parseFrontmatter(text) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!match) return { data: {}, body: text, raw: '' };
  const data = {};
  let key = null;
  for (const line of match[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(line);
    if (kv) {
      key = kv[1];
      data[key] = kv[2].replace(/^["']|["']$/g, '').trim();
    } else if (key && /^\s+\S/.test(line)) {
      data[key] = `${data[key]} ${line.trim()}`.trim();
    }
  }
  return { data, body: text.slice(match[0].length), raw: match[1] };
}

export function loadSkill(dir) {
  const skillFile = path.join(dir, 'SKILL.md');
  const text = readText(skillFile);
  const { data, body, raw } = parseFrontmatter(text);
  const name = path.basename(dir);
  const contents = walk(dir).filter((f) => f !== skillFile);
  return {
    name, dir, skillFile, text, body, frontmatter: data, frontmatterRaw: raw,
    contents,
    refs: extractPathTokens(text, dir),
    /** Every markdown/asset file in the skill, as skill-relative paths. */
    relContents: contents.map((f) => rel(f).replace(`skills/${name}/`, '')),
  };
}

const TOKEN_RE = /`([^`\n]+)`/g;
const PATH_EXT = /\.(md|markdown|json|ya?ml|svg|txt|py|mjs|js|sh)$/i;

/**
 * Directory prefixes that mark a token as a path relative to the skill root.
 * A bare filename in prose (`run.py`, `best_config.json`, `README.md`) is not a
 * reference and must not be resolved as one — that produced a wall of false
 * positives the first time this lint ran.
 */
const SKILL_ROOT_PREFIXES = [
  'references/', 'assets/', 'agents/', 'evals/', 'scripts/', 'docs/', 'profiles/', 'skills/',
];

/**
 * Extract backticked tokens that look like repository-relative file paths.
 *
 * Resolution rule, matching how the skills actually refer to files:
 *   - `../foo/bar.md` is resolved against the containing file's directory;
 *   - `references/bar.md` is resolved against the skill root, wherever it appears;
 *   - anything else (globs, placeholders, URLs, bare filenames, prose) is ignored.
 */
export function extractPathTokens(text, rootDir, fileDir = rootDir) {
  const out = [];
  const seen = new Set();
  for (const match of text.matchAll(TOKEN_RE)) {
    const token = match[1].trim();
    if (!token || seen.has(token)) continue;
    if (/[\s*<>{}|]/.test(token)) continue;          // globs, templates, prose
    if (token.includes('://') || token.startsWith('/') || token.startsWith('~')) continue;
    if (!PATH_EXT.test(token)) continue;
    if (!/^[A-Za-z0-9._/-]+$/.test(token)) continue;

    let abs = null;
    if (token.startsWith('../')) abs = path.resolve(fileDir, token);
    else if (SKILL_ROOT_PREFIXES.some((p) => token.startsWith(p))) abs = path.resolve(rootDir, token);
    else continue;

    seen.add(token);
    const inside = abs === rootDir || abs.startsWith(rootDir + path.sep);
    out.push({ token, abs, inside, exists: inside && exists(abs) });
  }
  return out;
}

/** Byte size of a file, or 0 when unreadable. */
export function size(abs) {
  try { return fs.statSync(abs).size; } catch { return 0; }
}

export function isProbablyBinary(abs) {
  const buf = fs.readFileSync(abs);
  const sample = buf.subarray(0, 4096);
  return sample.includes(0);
}
