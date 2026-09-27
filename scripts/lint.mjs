#!/usr/bin/env node
// Repository lint: the cheap checks that keep a prompt-and-docs repository from
// silently rotting. Run with `node scripts/lint.mjs` or `make lint`.
//
// Errors fail the run (exit 1). Warnings are reported and summarized but do not
// fail: they mark states that are legitimate for a user but wrong for a commit.

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import {
  ROOT, rel, walk, listSkills, extractPathTokens, exists, isDir, readText, size,
} from './lib/skills.mjs';

const findings = [];
const record = (id, severity, ok, message) => findings.push({ id, severity, ok, message });
const check = (id, ok, message) => record(id, 'error', ok, message);
const softCheck = (id, ok, message) => record(id, 'warning', ok, message);

const SLOT_SOURCES = [
  ['personal-research-priors.md', 'skills/time-series-model-ideation/references/personal-research-priors.md'],
  ['personal-pattern-index.md', 'skills/time-series-model-ideation/references/personal-pattern-index.md'],
  ['personal-pattern-card-a.md', 'skills/time-series-model-ideation/references/personal-pattern-card-a.md'],
  ['personal-pattern-card-b.md', 'skills/time-series-model-ideation/references/personal-pattern-card-b.md'],
  ['personal-pattern-card-c.md', 'skills/time-series-model-ideation/references/personal-pattern-card-c.md'],
  ['personal-code-style.md', 'skills/time-series-code-implementation/references/personal-code-style.md'],
];

// ---------------------------------------------------------------------------
// L01 — repository files that must exist for the project to be usable
// ---------------------------------------------------------------------------
const REQUIRED_FILES = [
  'README.md', 'README.zh-CN.md', 'LICENSE', 'NOTICE', 'CHANGELOG.md', 'CONTRIBUTING.md',
  'CODE_OF_CONDUCT.md', 'SECURITY.md', 'CITATION.cff', 'PERSONALIZE.md', 'Makefile',
  '.gitignore', '.editorconfig',
  '.claude-plugin/marketplace.json',
  'docs/schema.md', 'docs/architecture.md', 'docs/faq.md', 'docs/contributing-a-pattern-card.md',
  'docs/README.md', 'docs/release-checklist.md', 'examples/README.md',
  'evals/run.py', 'evals/README.md', 'evals/results/README.md',
  'scripts/install.sh', 'scripts/use-profile.sh', 'scripts/set-owner.sh',
  'scripts/build-bundle.mjs', 'scripts/lint.mjs',
  'profiles/README.md', 'profiles/default/personal-research-priors.md',
  'profiles/default/personal-code-style.md',
  '.github/workflows/lint.yml', '.github/PULL_REQUEST_TEMPLATE.md',
];
const missing = REQUIRED_FILES.filter((f) => !exists(path.join(ROOT, f)));
check('L01 required-files', missing.length === 0,
  missing.length ? `missing required files: ${missing.join(', ')}` : `${REQUIRED_FILES.length} required files present`);

// ---------------------------------------------------------------------------
// L02 — skill frontmatter
// ---------------------------------------------------------------------------
const skills = listSkills();
check('L02 skills-found', skills.length > 0, `${skills.length} skill(s) discovered`);
for (const skill of skills) {
  const { name, frontmatter } = skill;
  check(`L02a ${name} frontmatter`, Boolean(frontmatter.name && frontmatter.description),
    `${name}: name and description are required frontmatter keys`);
  check(`L02b ${name} name-match`, frontmatter.name === name,
    `${name}: frontmatter name "${frontmatter.name}" must equal the directory name`);
  const len = (frontmatter.description || '').length;
  check(`L02c ${name} description-length`, len > 20 && len <= 1024,
    `${name}: description length ${len} must be 21..1024 characters`);
  check(`L02d ${name} no-placeholders`, !/\{\{REQUIRED|\{\{TODO/i.test(skill.text),
    `${name}: SKILL.md contains an unresolved {{REQUIRED}} placeholder (the literal \`{{...}}\` used to describe template marks is fine)`);
}

// ---------------------------------------------------------------------------
// L03 — reference-path integrity (the router resolves paths by literal string)
// ---------------------------------------------------------------------------
for (const skill of skills) {
  const scanned = [{ file: skill.skillFile, base: skill.dir }];
  for (const abs of skill.contents) {
    if (/\.(md|ya?ml)$/i.test(abs)) scanned.push({ file: abs, base: skill.dir });
  }
  const broken = [];
  for (const { file, base } of scanned) {
    for (const ref of extractPathTokens(readText(file), base, path.dirname(file))) {
      if (!ref.inside) broken.push(`${rel(file)}: ${ref.token} escapes the skill directory`);
      else if (!ref.exists) broken.push(`${rel(file)}: ${ref.token} does not exist`);
    }
  }
  check(`L03 ${skill.name} reference-paths`, broken.length === 0,
    broken.length ? broken.join('; ') : `all referenced paths resolve (${scanned.length} files scanned)`);
}

// ---------------------------------------------------------------------------
// L04 — profiles: right shape, and the default matches the live slots
// ---------------------------------------------------------------------------
const profilesDir = path.join(ROOT, 'profiles');
if (isDir(profilesDir)) {
  const profiles = fs.readdirSync(profilesDir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && e.name !== '.backup')
    .map((e) => e.name);
  for (const profile of profiles) {
    const dir = path.join(profilesDir, profile);
    const files = fs.readdirSync(dir).filter((f) => fs.statSync(path.join(dir, f)).isFile());
    const missingSlots = SLOT_SOURCES.map(([n]) => n).filter((n) => !files.includes(n));
    check(`L04a profile-${profile}-complete`, missingSlots.length === 0,
      missingSlots.length ? `profiles/${profile} is missing: ${missingSlots.join(', ')}` : `profiles/${profile} has all six slots`);
  }
  const drift = [];
  for (const [slotName, liveRel] of SLOT_SOURCES) {
    const src = path.join(profilesDir, 'default', slotName);
    const live = path.join(ROOT, liveRel);
    if (!exists(live)) { drift.push(`${liveRel} is missing`); continue; }
    if (!exists(src) || !fs.readFileSync(src).equals(fs.readFileSync(live))) drift.push(liveRel);
  }
  softCheck('L04b default-profile-sync', drift.length === 0,
    drift.length
      ? `live slots differ from profiles/default: ${drift.join(', ')} — if this is your own profile, do not commit it; restore with scripts/use-profile.sh default`
      : 'live slots are byte-identical to profiles/default');
}

// ---------------------------------------------------------------------------
// L05 — JSON artifacts parse, and marketplace skill paths resolve
// ---------------------------------------------------------------------------
const jsonFiles = [
  '.claude-plugin/marketplace.json',
  ...skills.map((s) => `skills/${s.name}/evals/evals.json`).filter((f) => exists(path.join(ROOT, f))),
].filter((f) => exists(path.join(ROOT, f)));
for (const f of jsonFiles) {
  let ok = true; let message = `${f} parses`;
  try { JSON.parse(readText(path.join(ROOT, f))); } catch (e) { ok = false; message = `${f}: ${e.message}`; }
  check(`L05a json ${f}`, ok, message);
}
const marketPath = path.join(ROOT, '.claude-plugin/marketplace.json');
if (exists(marketPath)) {
  const market = JSON.parse(readText(marketPath));
  const listed = (market.plugins || []).flatMap((p) => p.skills || []);
  const absent = listed.filter((s) => !exists(path.join(ROOT, s, 'SKILL.md')));
  check('L05b marketplace-skill-paths', listed.length > 0 && absent.length === 0,
    absent.length ? `marketplace lists non-existent skills: ${absent.join(', ')}` : `marketplace lists ${listed.length} skill(s), all present`);
  const owner = (market.owner && market.owner.name) || '';
  softCheck('L05c marketplace-owner', owner.length > 0 && !/^(todo|your[-_]|changeme|owner)/i.test(owner),
    owner ? `marketplace owner is "${owner}"` : 'marketplace owner is empty');
}

// ---------------------------------------------------------------------------
// L06 — eval suite: fixture files exist, cases are well-formed
// ---------------------------------------------------------------------------
for (const skill of skills) {
  const evalsPath = path.join(skill.dir, 'evals', 'evals.json');
  if (!exists(evalsPath)) continue;
  const suite = JSON.parse(readText(evalsPath));
  check(`L06a ${skill.name} eval-skill-name`, suite.skill_name === skill.name,
    `${skill.name}: evals.json declares skill_name "${suite.skill_name}"`);
  const cases = suite.evals || [];
  check(`L06b ${skill.name} eval-cases`, cases.length > 0, `${skill.name}: ${cases.length} eval case(s)`);
  const malformed = cases.filter((c) => !c.id || !c.prompt || !Array.isArray(c.expectations) || c.expectations.length === 0);
  check(`L06c ${skill.name} eval-shape`, malformed.length === 0,
    malformed.length ? `cases without id/prompt/expectations: ${malformed.map((c) => c.id).join(', ')}` : 'every case has id, prompt, and expectations');
  const missingFixtures = cases.flatMap((c) => (c.files || []))
    .filter((f) => !exists(path.join(skill.dir, f)));
  check(`L06d ${skill.name} eval-fixtures`, missingFixtures.length === 0,
    missingFixtures.length ? `missing fixtures: ${missingFixtures.join(', ')}` : 'all referenced fixtures exist');
}

// ---------------------------------------------------------------------------
// L07 — dossier template keeps sections 0..16 in order
// ---------------------------------------------------------------------------
const templatePath = path.join(ROOT, 'skills/time-series-model-ideation/assets/idea-dossier-template.md');
if (exists(templatePath)) {
  const headings = [...readText(templatePath).matchAll(/^## (\d+)\./gm)].map((m) => Number(m[1]));
  const expected = Array.from({ length: 17 }, (_, i) => i);
  const ok = headings.length === expected.length && headings.every((n, i) => n === expected[i]);
  check('L07 dossier-sections', ok,
    ok ? 'template contains sections 0..16 in canonical order' : `template sections are ${headings.join(',')} (expected 0..16 in order)`);
}

// ---------------------------------------------------------------------------
// L08 — no personal data or absolute local paths in shipped content
// ---------------------------------------------------------------------------
const EMAIL_RE = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
// A published project needs one contact address. Rather than exempting the files that
// carry it, the declared contact in CITATION.cff is the single allowed address and every
// other address is still an error — the guard stays strong where it matters.
const DECLARED_CONTACTS = new Set(
  (exists(path.join(ROOT, 'CITATION.cff'))
    ? [...readText(path.join(ROOT, 'CITATION.cff')).matchAll(/^\s*email:\s*"?([^"\s]+)"?/gm)]
    : []).map((m) => m[1]),
);
const ABS_PATH_RE = /(^|[\s"'(])\/(?:Users|home)\/[A-Za-z0-9._-]+\//g;
const privacyHits = [];
for (const abs of walk(ROOT)) {
  const relative = rel(abs);
  if (/^(LICENSE|NOTICE)$/.test(relative)) continue;
  if (/^evals\/results\//.test(relative)) continue;
  if (!/\.(md|json|ya?ml|mjs|js|py|sh|txt|svg|cff)$/i.test(relative)) continue;
  if (size(abs) > 512 * 1024) continue;
  const text = readText(abs);
  for (const m of text.matchAll(EMAIL_RE)) {
    if (/@(example|users\.noreply\.github)\./i.test(m[0])) continue;
    if (DECLARED_CONTACTS.has(m[0])) continue;
    privacyHits.push(`${relative}: email-like string "${m[0]}"`);
  }
  for (const m of text.matchAll(ABS_PATH_RE)) privacyHits.push(`${relative}: absolute local path "${m[0].trim()}"`);
}
check('L08 privacy-scan', privacyHits.length === 0,
  privacyHits.length
    ? privacyHits.slice(0, 8).join('; ')
    : `no unexpected emails or absolute local paths (allowed contact: ${[...DECLARED_CONTACTS].join(', ') || 'none declared'})`);

// ---------------------------------------------------------------------------
// L09 — no vendored third-party content
// ---------------------------------------------------------------------------
const VENDOR_MARKERS = ['Anthropic, PBC', 'Keith Lazuka', 'anthropics/skills'];
const vendorHits = [];
for (const abs of walk(ROOT)) {
  const relative = rel(abs);
  if (relative === 'NOTICE') continue;      // acknowledges the ecosystem by name, ships nothing
  if (relative === 'scripts/lint.mjs') continue; // this file has to name the markers it bans
  if (!/\.(md|json|ya?ml|mjs|py|sh|txt)$/i.test(relative)) continue;
  const text = readText(abs);
  for (const marker of VENDOR_MARKERS) {
    if (text.includes(marker)) vendorHits.push(`${relative}: contains "${marker}"`);
  }
}
check('L09 no-vendored-content', vendorHits.length === 0,
  vendorHits.length ? vendorHits.join('; ') : 'no third-party attribution strings in shipped files');

// ---------------------------------------------------------------------------
// L10 — junk files
// ---------------------------------------------------------------------------
const junk = walk(ROOT).filter((f) => /(\.DS_Store|\.pyc$|~$|\.swp$)/.test(f)).map(rel);
check('L10 no-junk-files', junk.length === 0,
  junk.length ? `remove junk files: ${junk.join(', ')}` : 'no editor or bytecode junk');

// ---------------------------------------------------------------------------
// L11 — adapter and icon files referenced by agents/openai.yaml exist
// ---------------------------------------------------------------------------
for (const skill of skills) {
  const adapter = path.join(skill.dir, 'agents', 'openai.yaml');
  if (!exists(adapter)) {
    check(`L11a ${skill.name} adapter`, false, `${skill.name}: agents/openai.yaml is missing`);
    continue;
  }
  const text = readText(adapter);
  const iconRefs = [...text.matchAll(/icon_(?:small|large):\s*(\S+)/g)].map((m) => m[1]);
  const badIcons = iconRefs.filter((p) => !exists(path.join(skill.dir, p)));
  check(`L11a ${skill.name} adapter-icons`, iconRefs.length > 0 && badIcons.length === 0,
    badIcons.length ? `${skill.name}: icon paths do not resolve: ${badIcons.join(', ')}` : `${skill.name}: ${iconRefs.length} icon reference(s) resolve`);
}

// ---------------------------------------------------------------------------
// L12 — relative links in root documentation resolve
// ---------------------------------------------------------------------------
const LINK_RE = /\[[^\]]*\]\((?!https?:|#|mailto:)([^)\s]+)\)/g;
const brokenLinks = [];
for (const doc of ['README.md', 'README.zh-CN.md', 'CONTRIBUTING.md', 'PERSONALIZE.md', 'SECURITY.md', 'profiles/README.md', 'docs/README.md']) {
  const abs = path.join(ROOT, doc);
  if (!exists(abs)) continue;
  for (const m of readText(abs).matchAll(LINK_RE)) {
    const target = m[1].split('#')[0];
    if (!target) continue;
    if (!exists(path.resolve(path.dirname(abs), target))) brokenLinks.push(`${doc}: ${m[1]}`);
  }
}
check('L12 doc-links', brokenLinks.length === 0,
  brokenLinks.length ? `broken relative links: ${brokenLinks.join('; ')}` : 'relative links in root docs resolve');

// ---------------------------------------------------------------------------
// L13 — line citations in the docs still point inside their target files
//
// docs/ is built on "quote the rule and cite where it lives". A citation that
// drifts past the end of its target is how that documentation rots silently,
// and this repository's whole claim is that its references stay traceable.
// ---------------------------------------------------------------------------
const CITE_RE = /`([A-Za-z0-9_./-]+\.(?:md|json|ya?ml|mjs|py|sh))`\s+lines?\s+(\d+)(?:\s*[-–]\s*(\d+))?/g;
const citationProblems = new Set();
let citationsChecked = 0;
const citationDocs = walk(path.join(ROOT, 'docs')).filter((f) => f.endsWith('.md'))
  .concat(['README.md', 'CONTRIBUTING.md', 'PERSONALIZE.md'].map((f) => path.join(ROOT, f)).filter(exists));
const skillDirs = skills.map((s) => s.dir);
for (const abs of citationDocs) {
  for (const m of readText(abs).matchAll(CITE_RE)) {
    const token = m[1];
    if (token.includes('//')) continue;
    const high = Number(m[3] || m[2]);
    // A bare `SKILL.md` or `references/x.md` is ambiguous across skills, so try
    // every skill directory and accept the citation when any target is long
    // enough. Only when no candidate can hold the citation is it reported.
    const candidates = [...new Set([
      path.join(ROOT, token),
      ...skillDirs.map((d) => path.join(d, token)),
      ...skillDirs.map((d) => path.join(d, 'references', path.basename(token))),
      ...skillDirs.map((d) => path.join(d, 'assets', path.basename(token))),
    ])].filter((c) => exists(c) && !isDir(c));
    if (candidates.length === 0) {
      citationProblems.add(`${rel(abs)}: cites "${token}" which does not resolve`);
      continue;
    }
    const lengths = candidates.map((c) => readText(c).split('\n').length);
    citationsChecked += 1;
    if (!lengths.some((n) => n >= high)) {
      const best = rel(candidates[lengths.indexOf(Math.max(...lengths))]);
      citationProblems.add(`${rel(abs)}: cites ${token} line ${high}; the longest match (${best}) has ${Math.max(...lengths)} lines`);
    }
  }
}
const citationProblemList = [...citationProblems];
check('L13 doc-citations', citationProblemList.length === 0,
  citationProblemList.length
    ? citationProblemList.slice(0, 6).join('; ')
    : `${citationsChecked} line citation(s) point inside their target files`);

// ---------------------------------------------------------------------------
// L14 — claims about the canonical enumerations match the template
//
// The template defines the evidence-level roster and the gate roster. Prose that
// restates them as a range ("E0-E4", "G0-G12") drifts silently, and a wrong
// upper bound tells readers a level or gate exists that does not. The template
// wins; this check derives the truth from it instead of hardcoding it here.
// ---------------------------------------------------------------------------
if (exists(templatePath)) {
  const templateText = readText(templatePath);
  const evMax = Math.max(...[...templateText.matchAll(/^E(\d+)\s*=/gm)].map((m) => Number(m[1])));
  const gateMax = Math.max(...[...templateText.matchAll(/\bG(\d+)\b/g)].map((m) => Number(m[1])));
  // Narrow on purpose. A bare range is not a roster claim: "G0-G4 are set by
  // Stages 0-4" is a legitimate sub-range, and "the unsupported claim G0-G12"
  // is a refutation. Only a range introduced by the words "levels" or "gates",
  // on a line that is not refuting it, is treated as a claim about the roster.
  const ROSTER_RE = /\b(levels|gates)\b[^.\n]{0,24}?`?([EG])(\d+)`?\s*[–—-]\s*`?\2(\d+)`?/gi;
  const REFUTING_RE = /unsupported|does not exist|no such|refers to|incorrect|wrong|thirteen|fourteen|absent|not a\b/i;
  const proseProblem = [];
  let rostersChecked = 0;
  const proseDocs = ['README.md', 'README.zh-CN.md', 'CONTRIBUTING.md', 'PERSONALIZE.md', 'SECURITY.md']
    .map((f) => path.join(ROOT, f))
    .concat(walk(path.join(ROOT, 'docs')).filter((f) => f.endsWith('.md')));
  for (const abs of proseDocs.filter(exists)) {
    readText(abs).split('\n').forEach((line, i) => {
      if (REFUTING_RE.test(line)) return;
      for (const m of line.matchAll(ROSTER_RE)) {
        const letter = m[2].toUpperCase();
        const high = Number(m[4]);
        const canonical = letter === 'E' ? evMax : gateMax;
        rostersChecked += 1;
        if (high !== canonical) {
          proseProblem.push(`${rel(abs)}:${i + 1}: says ${m[1]} ${letter}0–${letter}${high}, but the template defines ${letter}0–${letter}${canonical}`);
        }
      }
    });
  }
  softCheck('L14 roster-claims', proseProblem.length === 0,
    proseProblem.length
      ? `${proseProblem.join('; ')} — the template is authoritative; fix the prose (this check is heuristic)`
      : `${rostersChecked} roster claim(s) agree with the template (E0–E${evMax}, G0–G${gateMax})`);
}

// ---------------------------------------------------------------------------
// L15 — the publishing handle is consistent wherever the project self-references
//
// The handle appears in the marketplace manifest, the citation file, both
// READMEs, the issue-template config, the code of conduct and the release
// checklist. A partial rename leaves 404 links and a wrong attribution — the kind
// of mistake that only becomes visible after the repository is public.
// `scripts/set-owner.sh` performs the rename atomically.
//
// Only *self*-references are checked: a URL carrying this repository's own slug,
// plus bare `github.com/<handle>` mentions inside the files whose job is to name
// the maintainer. `references/library-landscape.md` legitimately links to dozens
// of third-party time-series projects and must not be read as a self-reference.
// ---------------------------------------------------------------------------
const IDENTITY_FILES = [
  'CODE_OF_CONDUCT.md', '.claude-plugin/marketplace.json', 'CITATION.cff',
  '.github/ISSUE_TEMPLATE/config.yml', '.github/ISSUE_TEMPLATE/pattern_card.md',
];
if (exists(marketPath)) {
  const market = JSON.parse(readText(marketPath));
  const declared = (market.owner && market.owner.name) || '';
  const slug = market.name || '';
  const bad = [];
  let selfRefs = 0;
  let identityRefs = 0;
  for (const abs of walk(ROOT)) {
    if (!/\.(md|json|ya?ml|cff|txt|mjs|py|sh)$/i.test(abs)) continue;
    const relative = rel(abs);
    const text = readText(abs);
    if (slug) {
      for (const m of text.matchAll(new RegExp(`github\\.com/([A-Za-z0-9_.-]+)/${slug}`, 'g'))) {
        selfRefs += 1;
        if (m[1] !== declared) bad.push(`${relative}: links to github.com/${m[1]}/${slug}, but the declared owner is "${declared}"`);
      }
    }
    if (IDENTITY_FILES.includes(relative)) {
      for (const m of text.matchAll(/github\.com\/([A-Za-z0-9_.-]+)(?![/A-Za-z0-9_.-])/g)) {
        identityRefs += 1;
        if (m[1] !== declared) bad.push(`${relative}: names github.com/${m[1]} while the declared owner is "${declared}"`);
      }
    }
  }
  check('L15 owner-consistency', bad.length === 0 && declared.length > 0,
    bad.length
      ? `${bad.slice(0, 4).join('; ')} — run scripts/set-owner.sh <handle> to rename atomically`
      : `declared owner "${declared}"; ${selfRefs} self-reference(s) and ${identityRefs} identity mention(s) agree`);
}

// ---------------------------------------------------------------------------
// L16 — prose counts agree with the eval suite
//
// Twice now a number in the READMEs drifted from the artifact it described: the
// expectation total (written as 96 when the suite had 97) and the Tier-1 check
// split. This is a heuristic guard, not a proof — it only recognises the common
// phrasings, in both English and Chinese, which is why it warns rather than fails.
// ---------------------------------------------------------------------------
const suitePath = path.join(ROOT, 'skills/time-series-model-ideation/evals/evals.json');
if (exists(suitePath)) {
  const suite = JSON.parse(readText(suitePath));
  const cases = suite.evals || [];
  const expectations = cases.reduce((n, c) => n + (c.expectations || []).length, 0);
  // A lookbehind keeps "Stage-5 case" and "S10 check" from reading as counts. Lines
  // that are explicitly per-case ("8 expectations per case") are not totals, and
  // neither is a range that describes a spread ("judges its 8-9 expectations"), so
  // both are skipped.
  const NOT_A_TOTAL_RE = /per case|each case|expectations per|×|\bx\b/i;
  const RANGE_RE = /\d+\s*[–—-]\s*\d+\s*(?:natural-language\s+)?(?:expectations?|assertions?|cases?|条)/i;
  const patterns = [
    { re: /(?<![A-Za-z0-9-])(\d+)[-\s](?:behavioral\s+)?cases?\b/gi, actual: cases.length, label: 'cases' },
    { re: /(?<![A-Za-z0-9-])(\d+)[-\s](?:natural-language\s+)?expectations?\b/gi, actual: expectations, label: 'expectations' },
    { re: /(?<![A-Za-z0-9-])(\d+)[-\s]assertions?\b/gi, actual: expectations, label: 'assertions' },
    { re: /(?<![A-Za-z0-9-])(\d+)\s*(?:个|条)\s*(?:行为)?\s*(?:用例|case)/gi, actual: cases.length, label: 'cases (zh)' },
    { re: /(?<![A-Za-z0-9-])(\d+)\s*条\s*(?:expectation|断言)/gi, actual: expectations, label: 'expectations (zh)' },
  ];
  const mismatches = [];
  let countsChecked = 0;
  const proseDocs = ['README.md', 'README.zh-CN.md', 'CONTRIBUTING.md', 'PERSONALIZE.md']
    .map((f) => path.join(ROOT, f))
    .concat(walk(path.join(ROOT, 'docs')).filter((f) => f.endsWith('.md')))
    .concat(walk(path.join(ROOT, 'evals')).filter((f) => f.endsWith('.md')))
    .concat(walk(path.join(ROOT, '.github')).filter((f) => f.endsWith('.md')));
  for (const abs of proseDocs.filter(exists)) {
    readText(abs).split('\n').forEach((line, i) => {
      if (NOT_A_TOTAL_RE.test(line) || RANGE_RE.test(line)) return;
      for (const { re, actual, label } of patterns) {
        for (const m of line.matchAll(re)) {
          countsChecked += 1;
          if (Number(m[1]) !== actual) {
            mismatches.push(`${rel(abs)}:${i + 1}: says ${m[1]} ${label}, suite has ${actual}`);
          }
        }
      }
    });
  }
  softCheck('L16 suite-counts', mismatches.length === 0,
    mismatches.length
      ? `${mismatches.slice(0, 4).join('; ')} — the suite is the authority (heuristic check)`
      : `${countsChecked} prose count(s) agree with the suite (${cases.length} cases, ${expectations} expectations)`);
}

// ---------------------------------------------------------------------------
// L17 — the Tier-1 check count stated in prose matches the grader
//
// The READMEs summarize the grader as "N checks — M of them fail the run". Adding a
// check silently makes that sentence wrong. The grader is the authority; the
// patterns are deliberately narrow (the exact summary forms used) so this can never
// fire on prose that merely mentions a check by name.
// ---------------------------------------------------------------------------
const graderPath = path.join(ROOT, 'evals/graders/structural.py');
if (exists(graderPath)) {
  const specs = [...readText(graderPath).matchAll(/CheckSpec\(\s*"(S\d+)"\s*,\s*"([^"]+)"\s*,\s*"(error|warning)"/g)];
  const total = specs.length;
  const errorCount = specs.filter((s) => s[3] === 'error').length;
  const warningCount = total - errorCount;
  const claims = [
    { re: /(\d+)\s+checks?\s*—\s*(\d+)\s+of them fail/g, kind: 'en' },
    { re: /共\s*(\d+)\s*项检查（\s*(\d+)\s*项/g, kind: 'zh' },
  ];
  const problems = [];
  let claimsChecked = 0;
  for (const abs of ['README.md', 'README.zh-CN.md'].map((f) => path.join(ROOT, f)).filter(exists)) {
    readText(abs).split('\n').forEach((line, i) => {
      for (const { re } of claims) {
        for (const m of line.matchAll(re)) {
          claimsChecked += 1;
          if (Number(m[1]) !== total || Number(m[2]) !== errorCount) {
            problems.push(`${rel(abs)}:${i + 1}: says ${m[1]} checks with ${m[2]} failing, grader has ${total} with ${errorCount} failing (and ${warningCount} warning)`);
          }
        }
      }
    });
  }
  check('L17 grader-counts', problems.length === 0 && total > 0,
    problems.length
      ? problems.join('; ')
      : `${claimsChecked} prose claim(s) agree with the grader (${total} checks, ${errorCount} error-severity, ${warningCount} warning-severity)`);
}

// ---------------------------------------------------------------------------
// L18 — the repository name in self-referencing URLs matches the git remote
//
// The owner can be right while the repository name is wrong: a rename on GitHub
// leaves ~20 self-references pointing at a name that 404s, and nothing else in
// this file notices. The remote is the authority when it exists. Warning rather
// than error because a fork legitimately keeps pointing at upstream.
// ---------------------------------------------------------------------------
function remoteSlug() {
  try {
    const url = execFileSync('git', ['-C', ROOT, 'config', '--get', 'remote.origin.url'],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    if (!url) return null;
    const m = /github\.com[:/]+([^/]+)\/([^/]+?)(?:\.git)?$/.exec(url);
    return m ? { owner: m[1], slug: m[2] } : null;
  } catch {
    return null;   // not a git checkout, or no remote configured
  }
}
{
  const remote = remoteSlug();
  const SELF_RE = /github\.com\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+)/g;
  const declared = exists(marketPath) ? JSON.parse(readText(marketPath)).name || '' : '';
  const found = new Map();
  for (const abs of walk(ROOT)) {
    if (!/\.(md|json|ya?ml|cff|txt)$/i.test(abs)) continue;
    for (const m of readText(abs).matchAll(SELF_RE)) {
      // Only URLs whose path segment is this project's own repository name.
      if (m[2].toLowerCase() !== declared.toLowerCase()) continue;
      found.set(m[1], (found.get(m[1]) || 0) + 1);
    }
  }
  const owners = [...found.keys()];
  const problems = [];
  if (remote) {
    if (remote.slug.toLowerCase() !== declared.toLowerCase()) {
      problems.push(`git remote points at "${remote.slug}" but the project declares "${declared}" — rename with scripts/set-owner.sh --slug <name>, or on GitHub`);
    }
    for (const owner of owners) {
      if (owner.toLowerCase() !== remote.owner.toLowerCase()) {
        problems.push(`self-references use github.com/${owner}/… while the remote owner is "${remote.owner}"`);
      }
    }
  }
  softCheck('L18 repo-name', problems.length === 0,
    problems.length
      ? `${[...new Set(problems)].join('; ')} (expected in a fork)`
      : remote
        ? `self-references and the git remote agree on ${remote.owner}/${declared} (${owners.length} owner spelling(s))`
        : `declared repository name "${declared}"; no git remote to compare against`);
}

// ---------------------------------------------------------------------------
// L19 — workflows only reference scripts and make targets that exist
//
// A workflow step is configuration that nothing else type-checks. This repository
// shipped a CI step naming a profile directory that had been deleted, and only CI
// noticed, after the push. Cheaper to catch here.
// ---------------------------------------------------------------------------
{
  const makefilePath = path.join(ROOT, 'Makefile');
  const targets = new Set(
    exists(makefilePath)
      ? [...readText(makefilePath).matchAll(/^([A-Za-z][\w-]*):/gm)].map((m) => m[1])
      : [],
  );
  const problems = new Set();
  let refsChecked = 0;
  for (const wf of walk(path.join(ROOT, '.github/workflows')).filter((f) => /\.ya?ml$/.test(f))) {
    const text = readText(wf);
    for (const m of text.matchAll(/\b(scripts|evals)\/[A-Za-z0-9._/-]+/g)) {
      refsChecked += 1;
      if (!exists(path.join(ROOT, m[0]))) problems.add(`${rel(wf)}: ${m[0]} does not exist`);
    }
    for (const m of text.matchAll(/(?:^|\s)make\s+([A-Za-z][\w-]*)/gm)) {
      refsChecked += 1;
      if (!targets.has(m[1])) problems.add(`${rel(wf)}: make ${m[1]} is not a Makefile target`);
    }
  }
  const list = [...problems];
  check('L19 workflow-references', list.length === 0,
    list.length ? list.join('; ') : `${refsChecked} workflow reference(s) resolve to real scripts and targets`);
}

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------
const errors = findings.filter((f) => f.severity === 'error' && !f.ok);
const warnings = findings.filter((f) => f.severity === 'warning' && !f.ok);

const width = Math.max(...findings.map((f) => f.id.length), 8);
for (const f of findings) {
  const mark = f.ok ? 'ok  ' : f.severity === 'error' ? 'FAIL' : 'warn';
  if (f.ok && process.argv.includes('--quiet')) continue;
  console.log(`${mark}  ${f.id.padEnd(width)}  ${f.message}`);
}
console.log('');
console.log(`${findings.length - errors.length - warnings.length}/${findings.length} checks passed, ` +
  `${errors.length} error(s), ${warnings.length} warning(s)`);

if (errors.length > 0) {
  console.log('\nErrors must be fixed before committing.');
  process.exit(1);
}
if (warnings.length > 0) console.log('\nWarnings are acceptable locally; review them before opening a pull request.');
process.exit(0);
