#!/usr/bin/env python3
"""CLI entry point for the eval suite of the time-series research skills.

Modes
-----
--list                     list the behavioural eval cases shipped by a skill
--grade PATH.md            run the Tier-1 structural grader on one dossier
--self-test                grade both fixtures and check the documented defects
--tier2                    run the behavioural (model-in-the-loop) eval tier

Tier-1 is fully offline and deterministic.  Tier-2 needs an API key and is
skipped cleanly (exit 0) when none is present.

Exit codes: 0 ok, 1 grading failure, 2 usage error.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2

REPO_ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = REPO_ROOT / "evals"
SKILLS_DIR = REPO_ROOT / "skills"
FIXTURES_DIR = EVALS_DIR / "fixtures"
RESULTS_DIR = EVALS_DIR / "results"
DEFAULT_SKILL = "time-series-model-ideation"

DEFAULT_TIMEOUT = 180.0
MAX_OUTPUT_CHARS_IN_REPORT = 20000

PROVIDER_SPECS: Dict[str, Dict[str, str]] = {
    "anthropic": {
        "style": "anthropic",
        "key_env": "ANTHROPIC_API_KEY",
        "base_env": "ANTHROPIC_BASE_URL",
        "model_env": "ANTHROPIC_MODEL",
        "default_base": "https://api.anthropic.com",
        "default_model": "claude-sonnet-4-5",
    },
    "openai": {
        "style": "openai",
        "key_env": "OPENAI_API_KEY",
        "base_env": "OPENAI_BASE_URL",
        "model_env": "OPENAI_MODEL",
        "default_base": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
    },
    "deepseek": {
        "style": "openai",
        "key_env": "DEEPSEEK_API_KEY",
        "base_env": "DEEPSEEK_BASE_URL",
        "model_env": "DEEPSEEK_MODEL",
        "default_base": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
    },
}


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def load_grader():
    """Import evals/graders/structural.py without requiring a package."""

    path = EVALS_DIR / "graders" / "structural.py"
    spec = importlib.util.spec_from_file_location("dossier_structural_grader", str(path))
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise RuntimeError("cannot load %s" % path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses need the module registered
    spec.loader.exec_module(module)
    return module


def skill_dir(skill: str) -> Path:
    return SKILLS_DIR / skill


def evals_json_path(skill: str) -> Path:
    return skill_dir(skill) / "evals" / "evals.json"


def load_cases(skill: str) -> List[dict]:
    path = evals_json_path(skill)
    if not path.is_file():
        raise FileNotFoundError("no evals.json for skill '%s' (looked at %s)" % (skill, path))
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return list(data.get("evals", []))


def resolve_case_file(skill: str, relative: str) -> Path:
    """Case 'files' entries are relative to the skill root."""

    candidate = skill_dir(skill) / relative
    if candidate.is_file():
        return candidate
    return (REPO_ROOT / relative).resolve()


def read_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


# --------------------------------------------------------------------------
# --list
# --------------------------------------------------------------------------


def cmd_list(skill: str, as_json: bool) -> int:
    try:
        cases = load_cases(skill)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_USAGE

    if as_json:
        print(
            json.dumps(
                {
                    "skill": skill,
                    "evals_json": str(evals_json_path(skill)),
                    "cases": [
                        {
                            "id": case.get("id"),
                            "expectations": len(case.get("expectations", [])),
                            "files": list(case.get("files", [])),
                        }
                        for case in cases
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return EXIT_OK

    print("behavioural eval cases for skill: %s" % skill)
    print("source: %s" % evals_json_path(skill).relative_to(REPO_ROOT))
    print("")
    print("%-6s %-14s %s" % ("case", "expectations", "fixture files"))
    for case in cases:
        files = case.get("files", [])
        label = ", ".join(files) if files else "(none)"
        print("%-6s %-14d %s" % (case.get("id"), len(case.get("expectations", [])), label))
    print("")
    print("total: %d case(s), %d expectation(s)" % (len(cases), sum(len(c.get("expectations", [])) for c in cases)))
    print("next: python3 evals/run.py --tier2 --case 1   (needs an API key)")
    return EXIT_OK


# --------------------------------------------------------------------------
# --grade
# --------------------------------------------------------------------------


def cmd_grade(grader, path: str, skill: str, as_json: bool) -> int:
    target = Path(path)
    if not target.is_file():
        print("error: no such dossier file: %s" % path, file=sys.stderr)
        return EXIT_USAGE
    if not skill_dir(skill).is_dir():
        print("error: unknown skill '%s' (no directory %s)" % (skill, skill_dir(skill)), file=sys.stderr)
        return EXIT_USAGE

    try:
        report = grader.grade_file(str(target))
    except OSError as exc:
        print("error: cannot read %s: %s" % (path, exc), file=sys.stderr)
        return EXIT_USAGE

    report["skill"] = skill
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(grader.format_text_report(report))
    return EXIT_OK if report["ok"] else EXIT_FAIL


# --------------------------------------------------------------------------
# --self-test
# --------------------------------------------------------------------------

DEFECT_RE = re.compile(r"^\s*DEFECT:\s*(S\d{2})\b\s*::\s*(.*)$", re.M)


def parse_documented_defects(text: str) -> List[Tuple[str, str]]:
    """Read the DEFECT lines the bad fixture documents at the top of the file."""

    head = text[: text.find("-->") + 3] if "<!--" in text else text[:4000]
    return [(m.group(1), m.group(2).strip()) for m in DEFECT_RE.finditer(head)]


def cmd_self_test(grader, as_json: bool) -> int:
    good_path = FIXTURES_DIR / "good-dossier.md"
    bad_path = FIXTURES_DIR / "bad-dossier.md"
    missing = [str(p) for p in (good_path, bad_path) if not p.is_file()]
    if missing:
        print("error: missing fixture(s): %s" % ", ".join(missing), file=sys.stderr)
        print("hint: python3 evals/fixtures/make_fixtures.py", file=sys.stderr)
        return EXIT_USAGE

    good_text = read_text(good_path)
    bad_text = read_text(bad_path)
    good_report = grader.grade_text(good_text, str(good_path))
    bad_report = grader.grade_text(bad_text, str(bad_path))

    defects = parse_documented_defects(bad_text)
    triggered: List[dict] = []
    for check_id, description in defects:
        check = next((c for c in bad_report["checks"] if c["check_id"] == check_id), None)
        hits = len(check["findings"]) if check else 0
        triggered.append(
            {
                "check_id": check_id,
                "description": description,
                "findings": hits,
                "triggered": hits > 0,
            }
        )

    good_ok = good_report["error_count"] == 0
    bad_ok = bool(defects) and all(item["triggered"] for item in triggered)
    ok = good_ok and bad_ok

    if as_json:
        print(
            json.dumps(
                {
                    "ok": ok,
                    "good": {
                        "path": str(good_path),
                        "error_count": good_report["error_count"],
                        "warning_count": good_report["warning_count"],
                        "checks_evaluated": sum(1 for c in good_report["checks"] if c["applicable"]),
                        "checks_passed": sum(1 for c in good_report["checks"] if c["status"] == "pass"),
                        "checks": [
                            {"check_id": c["check_id"], "status": c["status"], "note": c["note"]}
                            for c in good_report["checks"]
                        ],
                    },
                    "bad": {
                        "path": str(bad_path),
                        "error_count": bad_report["error_count"],
                        "warning_count": bad_report["warning_count"],
                        "documented_defects": len(defects),
                        "triggered_defects": sum(1 for item in triggered if item["triggered"]),
                        "defects": triggered,
                    },
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return EXIT_OK if ok else EXIT_FAIL

    lines: List[str] = []
    lines.append("self-test: Tier-1 structural grader against the checked-in fixtures")
    lines.append("")
    lines.append("good fixture: %s" % good_path.relative_to(REPO_ROOT))
    evaluated = [c for c in good_report["checks"] if c["applicable"]]
    skipped = [c for c in good_report["checks"] if not c["applicable"]]
    lines.append(
        "  %d/%d checks evaluated, %d error(s), %d warning(s) -> %s"
        % (
            len(evaluated),
            len(good_report["checks"]),
            good_report["error_count"],
            good_report["warning_count"],
            "zero errors" if good_ok else "ERRORS PRESENT",
        )
    )
    lines.append("  proved: %s" % ", ".join(c["check_id"] for c in good_report["checks"] if c["status"] == "pass"))
    if skipped:
        lines.append(
            "  not applicable: %s"
            % ", ".join("%s (%s)" % (c["check_id"], c["note"]) for c in skipped)
        )
    lines.append("")
    lines.append("bad fixture: %s" % bad_path.relative_to(REPO_ROOT))
    lines.append(
        "  %d error(s), %d warning(s); %d documented defect(s), %d triggered"
        % (
            bad_report["error_count"],
            bad_report["warning_count"],
            len(defects),
            sum(1 for item in triggered if item["triggered"]),
        )
    )
    width = max(len(item["check_id"]) for item in triggered) if triggered else 4
    for item in triggered:
        marker = "triggered" if item["triggered"] else "NOT TRIGGERED"
        lines.append(
            "  %s  %-9s %d finding(s) — %s"
            % (item["check_id"].ljust(width), marker, item["findings"], item["description"])
        )
    lines.append("")
    if ok:
        lines.append(
            "self-test: PASS — good fixture yields zero errors and every documented defect in the bad fixture fires"
        )
    else:
        if not good_ok:
            lines.append("self-test: FAIL — good fixture produced %d error(s)" % good_report["error_count"])
        if not defects:
            lines.append("self-test: FAIL — bad fixture documents no DEFECT: lines")
        elif not bad_ok:
            missed = ", ".join(item["check_id"] for item in triggered if not item["triggered"])
            lines.append("self-test: FAIL — documented defect(s) did not fire: %s" % missed)
    print("\n".join(lines))
    return EXIT_OK if ok else EXIT_FAIL


# --------------------------------------------------------------------------
# --tier2
# --------------------------------------------------------------------------


class Tier2Error(Exception):
    pass


def _join_base(base: str, path: str, add_v1_when_bare: bool) -> str:
    base = (base or "").strip().rstrip("/")
    parsed = urllib.parse.urlsplit(base)
    if add_v1_when_bare and parsed.path in ("", "/"):
        base = base + "/v1"
    return base + path


def _http_post_json(url: str, payload: dict, headers: Dict[str, str], timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    for key, value in headers.items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", "replace")[:300]
        except Exception:  # pragma: no cover - defensive
            detail = ""
        raise Tier2Error("HTTP %s from %s: %s" % (exc.code, url, detail.strip()))
    except urllib.error.URLError as exc:
        raise Tier2Error("network error calling %s: %s" % (url, exc.reason))
    except TimeoutError:
        raise Tier2Error("timed out after %.0fs calling %s" % (timeout, url))
    try:
        return json.loads(raw)
    except ValueError:
        raise Tier2Error("non-JSON response from %s: %s" % (url, raw[:200]))


def call_model(
    provider: str,
    api_key: str,
    base_url: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int,
    timeout: float,
) -> str:
    spec = PROVIDER_SPECS[provider]
    if spec["style"] == "anthropic":
        url = _join_base(base_url, "/v1/messages", add_v1_when_bare=False)
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
        data = _http_post_json(url, payload, headers, timeout)
        blocks = data.get("content") or []
        text = "".join(block.get("text", "") for block in blocks if isinstance(block, dict))
        if not text:
            raise Tier2Error("empty completion from %s" % url)
        return text

    url = _join_base(base_url, "/chat/completions", add_v1_when_bare=True)
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {"Authorization": "Bearer %s" % api_key}
    data = _http_post_json(url, payload, headers, timeout)
    choices = data.get("choices") or []
    if not choices:
        raise Tier2Error("empty completion from %s" % url)
    message = choices[0].get("message") or {}
    text = message.get("content") or ""
    if not text:
        raise Tier2Error("empty completion from %s" % url)
    return text


def skill_context(skill: str) -> str:
    """The skill contract handed to the generator model (SKILL.md + template)."""

    parts = []
    skill_md = skill_dir(skill) / "SKILL.md"
    template = skill_dir(skill) / "assets" / "idea-dossier-template.md"
    if skill_md.is_file():
        parts.append("SKILL.md (the skill contract):\n\n%s" % read_text(skill_md))
    if template.is_file():
        parts.append("assets/idea-dossier-template.md (the only permitted output shape):\n\n%s" % read_text(template))
    return "\n\n---\n\n".join(parts)


def build_generation_prompt(case: dict, skill: str, files: List[Path], with_context: bool) -> str:
    parts: List[str] = []
    if with_context:
        parts.append(skill_context(skill))
        parts.append("---")
    parts.append("# Task\n\n%s" % case.get("prompt", ""))
    if files:
        for path in files:
            try:
                body = read_text(path)
            except OSError as exc:
                body = "<unreadable: %s>" % exc
            parts.append("# Attached file: %s\n\n```markdown\n%s\n```" % (path.name, body))
    parts.append(
        "# Output\n\nProduce the artifact the skill requires for this task. Return Markdown only, "
        "with no commentary before or after it."
    )
    return "\n\n".join(parts)


JUDGE_SYSTEM = (
    "You are a strict, evidence-driven grader for research-idea dossiers. "
    "Judge each expectation independently against the supplied response. "
    "An expectation passes only when the response itself contains the evidence for it; "
    "absence of counter-evidence is not evidence. Reply with JSON only."
)


def build_judge_prompt(case: dict, response: str) -> str:
    expectations = case.get("expectations", [])
    expectation_block = "\n".join("%d. %s" % (i + 1, e) for i, e in enumerate(expectations))
    return (
        "# Case prompt given to the model\n\n%s\n\n"
        "# Expected output (summary)\n\n%s\n\n"
        "# Expectations to judge\n\n%s\n\n"
        "# Response under evaluation\n\n```markdown\n%s\n```\n\n"
        "# Instructions\n\n"
        "For each expectation decide PASS or FAIL. Quote the specific evidence you relied on. "
        "If the expectation is only partially met, judge FAIL and say what is missing.\n\n"
        'Reply with JSON only, in exactly this shape:\n'
        '{"expectations": [{"index": 1, "verdict": "PASS", "reason": "..."}]}\n'
        % (
            case.get("prompt", ""),
            case.get("expected_output", ""),
            expectation_block,
            response,
        )
    )


def parse_verdicts(raw: str, count: int) -> List[dict]:
    """Leniently parse the judge JSON; returns [] when unparseable."""

    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(.+?)```", text, re.S)
    if fenced:
        text = fenced.group(1).strip()
    candidates = [text]
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        candidates.append(text[start : end + 1])
    data = None
    for candidate in candidates:
        try:
            data = json.loads(candidate)
            break
        except ValueError:
            continue
    if not isinstance(data, dict):
        return []
    items = data.get("expectations")
    if not isinstance(items, list):
        return []
    by_index: Dict[int, dict] = {}
    for position, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        index = item.get("index", position)
        try:
            index = int(index)
        except (TypeError, ValueError):
            index = position
        verdict = str(item.get("verdict", "")).strip().upper()
        if verdict not in ("PASS", "FAIL"):
            verdict = "UNJUDGED"
        by_index[index] = {
            "index": index,
            "verdict": verdict,
            "reason": str(item.get("reason", "")).strip()[:600],
        }
    return [by_index.get(i, {"index": i, "verdict": "UNJUDGED", "reason": "judge returned no verdict"}) for i in range(1, count + 1)]


def _md_cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def tier2_markdown(result: dict) -> str:
    lines: List[str] = []
    lines.append("# Tier-2 behavioural eval results")
    lines.append("")
    lines.append("- skill: %s" % result["skill"])
    lines.append("- date: %s (UTC)" % result["date"])
    lines.append("- provider: %s" % result["provider"])
    lines.append("- generator model: %s" % result["model"])
    lines.append("- judge model: %s" % result["judge_model"])
    lines.append("- max tokens per response: %d" % result["max_tokens"])
    lines.append("- base URL: %s" % result["base_url"])
    lines.append("- cases run: %s" % ", ".join(str(c["id"]) for c in result["cases"]))
    lines.append(
        "- expectations passed: %d/%d"
        % (
            sum(c["passed"] for c in result["cases"]),
            sum(c["total"] for c in result["cases"]),
        )
    )
    lines.append("- key source: %s" % result["key_env"])
    lines.append("")
    failed = [
        (case["id"], item["index"])
        for case in result["cases"]
        for item in case["expectations"]
        if item["verdict"] != "PASS"
    ]
    lines.append("## Failed expectations")
    lines.append("")
    if not failed:
        lines.append("None: every judged expectation passed." if result["cases"] else "No cases were run.")
    else:
        for case_id, index in failed:
            lines.append("- case %s expectation %d" % (case_id, index))
    lines.append("")
    for case in result["cases"]:
        lines.append("## Case %s — %d/%d expectations passed" % (case["id"], case["passed"], case["total"]))
        lines.append("")
        if case.get("error"):
            lines.append("**Run error:** %s" % case["error"])
            lines.append("")
            continue
        lines.append("### Prompt")
        lines.append("")
        lines.append("> %s" % _md_cell(case["prompt"]))
        lines.append("")
        lines.append("### Expectation verdicts")
        lines.append("")
        lines.append("| # | Expectation | Verdict | Reason |")
        lines.append("|---|---|---|---|")
        for item in case["expectations"]:
            lines.append(
                "| %d | %s | %s | %s |"
                % (item["index"], _md_cell(item["expectation"]), item["verdict"], _md_cell(item["reason"]))
            )
        lines.append("")
        output = case.get("output", "")
        truncated = case.get("output_truncated", False)
        lines.append(
            "### Produced output (%d characters%s)"
            % (len(output), ", truncated for the report" if truncated else "")
        )
        lines.append("")
        lines.append("````markdown")
        lines.append(output)
        lines.append("````")
        lines.append("")
    lines.append("## Cost and limitations")
    lines.append("")
    lines.append(
        "Tier-2 makes two model calls per case (one generation, one judgement) and is non-deterministic; "
        "verdicts are model judgements, not ground truth. Tier-1 structural grading is the only "
        "deterministic gate in this suite."
    )
    lines.append("")
    return "\n".join(lines)


def resolve_out_path(out: Optional[str], default_name: str) -> Path:
    if not out:
        return RESULTS_DIR / default_name
    candidate = Path(out)
    as_dir = out.endswith(os.sep) or candidate.is_dir() or candidate.suffix == ""
    if as_dir:
        return candidate / default_name
    return candidate


def default_report_name(provider: str, model: str, directory: Path) -> str:
    """`<date>-<provider>-<model>.md`, never overwriting an earlier run."""

    safe_model = re.sub(r"[^A-Za-z0-9._-]+", "-", model).strip("-") or "model"
    stem = "%s-%s-%s" % (time.strftime("%Y-%m-%d", time.gmtime()), provider, safe_model)
    candidate = "%s.md" % stem
    suffix = 2
    while (directory / candidate).exists():
        candidate = "%s-%d.md" % (stem, suffix)
        suffix += 1
    return candidate


def cmd_tier2(grader, args) -> int:
    skill = args.skill
    try:
        cases = load_cases(skill)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_USAGE

    selected = cases
    if args.case:
        wanted: List[int] = []
        for raw in args.case:
            for piece in str(raw).split(","):
                piece = piece.strip()
                if not piece:
                    continue
                if not re.match(r"^\d+$", piece):
                    print("error: --case expects numeric case ids, got '%s'" % piece, file=sys.stderr)
                    return EXIT_USAGE
                wanted.append(int(piece))
        known = {int(c.get("id")) for c in cases}
        unknown = [c for c in wanted if c not in known]
        if unknown:
            print(
                "error: unknown case id(s) %s; available: %s"
                % (", ".join(str(c) for c in unknown), ", ".join(str(c) for c in sorted(known))),
                file=sys.stderr,
            )
            return EXIT_USAGE
        selected = [c for c in cases if int(c.get("id")) in set(wanted)]

    provider = args.provider
    if not provider:
        for name, spec in PROVIDER_SPECS.items():
            if os.environ.get(spec["key_env"]):
                provider = name
                break
    if not provider:
        print(
            "skipped: no API key — tier-2 not run. "
            "Set ANTHROPIC_API_KEY, OPENAI_API_KEY or DEEPSEEK_API_KEY and retry "
            "(optionally with --provider and --model)."
        )
        return EXIT_OK
    if provider not in PROVIDER_SPECS:
        print("error: unknown provider '%s'" % provider, file=sys.stderr)
        return EXIT_USAGE

    spec = PROVIDER_SPECS[provider]
    api_key = os.environ.get(spec["key_env"])
    if not api_key:
        print(
            "skipped: no API key — tier-2 not run. Provider '%s' needs %s in the environment."
            % (provider, spec["key_env"])
        )
        return EXIT_OK

    base_url = os.environ.get(spec["base_env"]) or spec["default_base"]
    model = args.model or os.environ.get(spec["model_env"]) or spec["default_model"]
    judge_model = args.judge_model or model
    timeout = float(args.timeout)

    result: dict = {
        "skill": skill,
        "date": time.strftime("%Y-%m-%d", time.gmtime()),
        "provider": provider,
        "model": model,
        "judge_model": judge_model,
        "base_url": base_url,
        "max_tokens": args.max_tokens,
        "key_env": spec["key_env"],
        "cases": [],
    }

    had_error = False
    for case in selected:
        case_id = case.get("id")
        entry: dict = {
            "id": case_id,
            "prompt": case.get("prompt", ""),
            "total": len(case.get("expectations", [])),
            "passed": 0,
            "expectations": [],
            "output": "",
            "output_truncated": False,
            "error": None,
        }
        try:
            files = [resolve_case_file(skill, rel) for rel in case.get("files", [])]
            prompt = build_generation_prompt(case, skill, files, with_context=not args.no_skill_context)
            output = call_model(
                provider, api_key, base_url, model, "Follow the supplied skill contract exactly.", prompt,
                args.max_tokens, timeout,
            )
            entry["output"] = output
            if len(output) > MAX_OUTPUT_CHARS_IN_REPORT:
                entry["output"] = output[:MAX_OUTPUT_CHARS_IN_REPORT] + "\n\n… [truncated in report]"
                entry["output_truncated"] = True
            judge_raw = call_model(
                provider, api_key, base_url, judge_model, JUDGE_SYSTEM,
                build_judge_prompt(case, output), args.max_tokens, timeout,
            )
            verdicts = parse_verdicts(judge_raw, len(case.get("expectations", [])))
            expectations = case.get("expectations", [])
            entry["expectations"] = [
                {
                    "index": item["index"],
                    "expectation": expectations[item["index"] - 1] if item["index"] - 1 < len(expectations) else "",
                    "verdict": item["verdict"],
                    "reason": item["reason"],
                }
                for item in verdicts
            ]
            entry["passed"] = sum(1 for item in entry["expectations"] if item["verdict"] == "PASS")
            if not verdicts:
                entry["error"] = "judge output could not be parsed as JSON; verdicts marked UNJUDGED"
                had_error = True
        except Tier2Error as exc:
            entry["error"] = str(exc)
            had_error = True
        except Exception as exc:  # pragma: no cover - defensive: never traceback out
            entry["error"] = "%s: %s" % (type(exc).__name__, exc)
            had_error = True
        result["cases"].append(entry)

    target_dir = Path(args.out) if args.out and (args.out.endswith(os.sep) or Path(args.out).is_dir() or Path(args.out).suffix == "") else RESULTS_DIR
    default_name = default_report_name(provider, model, target_dir)
    out_path = resolve_out_path(args.out, default_name)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(tier2_markdown(result))
    except OSError as exc:
        print("error: cannot write %s: %s" % (out_path, exc), file=sys.stderr)
        return EXIT_FAIL

    if args.json:
        summary = dict(result)
        summary["report_path"] = str(out_path)
        summary["cases"] = [
            {k: v for k, v in case.items() if k != "output"} for case in result["cases"]
        ]
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("tier-2 behavioural eval — provider %s, model %s" % (provider, model))
        print("%-6s %-8s %s" % ("case", "passed", "notes"))
        for case in result["cases"]:
            note = case["error"] or ""
            print("%-6s %-8s %s" % (case["id"], "%d/%d" % (case["passed"], case["total"]), note))
        print("")
        print("report written to %s" % out_path)
        print(
            "total: %d/%d expectations passed"
            % (
                sum(c["passed"] for c in result["cases"]),
                sum(c["total"] for c in result["cases"]),
            )
        )
    return EXIT_FAIL if had_error else EXIT_OK


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evals/run.py",
        description="Eval runner for the time-series research skills (Tier-1 structural, Tier-2 behavioural).",
    )
    parser.add_argument("--list", action="store_true", help="list the behavioural eval cases")
    parser.add_argument("--grade", metavar="PATH.md", help="run Tier-1 structural grading on one dossier")
    parser.add_argument("--self-test", action="store_true", help="grade both fixtures and check documented defects")
    parser.add_argument("--tier2", action="store_true", help="run the Tier-2 behavioural eval against a model")
    parser.add_argument("--skill", default=DEFAULT_SKILL, help="skill name (default: %s)" % DEFAULT_SKILL)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON for the chosen mode")
    parser.add_argument("--case", action="append", metavar="N", help="tier2: case id (repeatable, comma-separated)")
    parser.add_argument(
        "--provider", choices=sorted(PROVIDER_SPECS), help="tier2: API provider (default: first with a key)"
    )
    parser.add_argument("--model", help="tier2: generator model name")
    parser.add_argument("--judge-model", help="tier2: judge model name (default: the generator model)")
    parser.add_argument("--out", metavar="PATH", help="tier2: report file or directory (default: evals/results/)")
    parser.add_argument("--max-tokens", type=int, default=8000, help="tier2: per-response token cap")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="tier2: per-request timeout in seconds")
    parser.add_argument(
        "--no-skill-context", action="store_true", help="tier2: do not send SKILL.md and the template to the model"
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    modes = [bool(args.list), args.grade is not None, bool(args.self_test), bool(args.tier2)]
    if sum(1 for mode in modes if mode) != 1:
        parser.error("choose exactly one mode: --list, --grade PATH, --self-test or --tier2")

    grader = load_grader()

    if args.list:
        return cmd_list(args.skill, args.json)
    if args.grade is not None:
        return cmd_grade(grader, args.grade, args.skill, args.json)
    if args.self_test:
        return cmd_self_test(grader, args.json)
    return cmd_tier2(grader, args)


if __name__ == "__main__":
    sys.exit(main())
