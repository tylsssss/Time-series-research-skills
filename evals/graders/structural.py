#!/usr/bin/env python3
"""Tier-1 structural grader for one produced Idea Dossier Markdown file.

Offline, deterministic, Python 3.9+ standard library only.

The authority for every rule below is
``skills/time-series-model-ideation/assets/idea-dossier-template.md`` plus the
contract in ``skills/time-series-model-ideation/SKILL.md``.  Where the task
brief and the template disagree, the template wins and the deviation is
recorded in ``evals/README.md`` (see S10 -> G0..G11 and S11 -> E0..E5).

Usage:
    python3 evals/graders/structural.py evals/fixtures/good-dossier.md
    python3 evals/graders/structural.py evals/fixtures/bad-dossier.md --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

GRADER_VERSION = "1.0.0"

# --------------------------------------------------------------------------
# Canonical vocabulary, read from the template (do not invent values here)
# --------------------------------------------------------------------------

CANONICAL_SECTIONS: Tuple[int, ...] = tuple(range(17))  # 0..16

LIFECYCLE_VALUES: Tuple[str, ...] = ("NOT-STARTED", "ACTIVE", "COMPLETE", "BLOCKED")

ID_NAMESPACES: Tuple[str, ...] = (
    "DOS",
    "NEED",
    "CLM",
    "FAIL",
    "LINK",
    "RIV",
    "INV",
    "CAND",
    "FIND",
    "SYS",
    "COMP",
    "EXP",
)

# template: Claim type = OBSERVATION | EXPLANATION | MECHANISM | HYPOTHESIS |
#                       ASSUMPTION | EVIDENCE
CLAIM_TYPES: Tuple[str, ...] = (
    "OBSERVATION",
    "EXPLANATION",
    "MECHANISM",
    "HYPOTHESIS",
    "ASSUMPTION",
    "EVIDENCE",
)

# template: Status = SUPPORTED | CONTRADICTED | UNRESOLVED | NOT-APPLICABLE
CLAIM_STATUSES: Tuple[str, ...] = (
    "SUPPORTED",
    "CONTRADICTED",
    "UNRESOLVED",
    "NOT-APPLICABLE",
)

# template: Evidence strength = E0 | E1 | E2 | E3 | E4 | E5
EVIDENCE_LEVELS: Tuple[str, ...] = tuple("E%d" % i for i in range(6))

# template section 15 enumerates G0..G11 (the brief said G0..G12; template wins)
GATES: Tuple[str, ...] = tuple("G%d" % i for i in range(12))

GATE_EVALUATION_STATUSES: Tuple[str, ...] = ("EVALUATED", "DEFERRED")
GATE_STATES: Tuple[str, ...] = ("SATISFIED", "UNRESOLVED", "UNSATISFIED")
GATE_FAILURE_MODES: Tuple[str, ...] = ("null", "REPAIRABLE", "CONTRADICTED")

DECISIONS: Tuple[str, ...] = ("GO", "PIVOT", "NEED-EVIDENCE", "KILL")
DECISION_RULES: Tuple[str, ...] = (
    "ALL-SATISFIED",
    "UNRESOLVED-EVIDENCE",
    "REPAIRABLE-FAILURE",
    "FATAL-CONTRADICTION",
)

NOVELTY_STATUSES: Tuple[str, ...] = ("PASS", "CONDITIONAL", "FAIL", "UNKNOWN")

# Phase -> highest section number that may already be entered.  Sections above
# the boundary are expected to be NOT-STARTED (template: "Use the phases
# progressively"; SKILL.md: "Leave unentered sections NOT-STARTED").
PHASE_SECTION_BOUNDARY: Dict[str, int] = {
    "DIAGNOSIS": 6,
    "INDEPENDENT-IDEATION": 7,
    "AUDIT": 13,
    "COMPILATION": 16,
    "COMPLETE": 16,
}

# External identifiers that are not dossier record IDs.  Kept small and
# documented in evals/README.md so S06 does not fire on "GPT-4".
EXTERNAL_ID_PREFIXES: Tuple[str, ...] = (
    "GPT",
    "LLM",
    "CIFAR",
    "IMAGENET",
    "PEMS",
    "METR",
    "SMD",
    "SWAT",
    "WADI",
    "TSB",
    "ETT",
    "M3",
    "M4",
    "M5",
    "NN5",
    "ILI",
    "LOSLOOP",
    "MIMIC",
)

MAX_FINDINGS_PER_CHECK = 25

# --------------------------------------------------------------------------
# Regular expressions
# --------------------------------------------------------------------------

HEADING_RE = re.compile(r"^##\s+(\d{1,3})\.\s*(.*?)\s*$")
YAML_KV_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")
PLACEHOLDER_RE = re.compile(r"\{\{REQUIRED")
ANY_PLACEHOLDER_RE = re.compile(r"\{\{")
HORIZONTAL_RULE_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
ID_TOKEN_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,9})-(\d{1,4})\b")
EVIDENCE_TOKEN_RE = re.compile(r"\bE(\d{1,2})\b")
GATE_ID_RE = re.compile(r"^\s*\|\s*(G\d{1,2})\b")

# S07: numeric novelty / aggregate gate scores.  Each pattern carries a label.
NUMERIC_SCORE_PATTERNS: Tuple[Tuple[str, "re.Pattern[str]"], ...] = (
    (
        "numeric novelty score",
        re.compile(r"\bnovelty\b[^.\n]{0,40}?\b\d+(?:\.\d+)?\s*/\s*(?:5|10|100)\b", re.I),
    ),
    (
        "numeric novelty score",
        re.compile(r"\bnovelty\s*(?:score|rating|level|value)\b[^.\n]{0,20}?[:=]?\s*\(?\s*\d+(?:\.\d+)?", re.I),
    ),
    (
        "numeric novelty score",
        re.compile(r"\bnovelty\s*[:=]\s*\(?\s*\d+(?:\.\d+)?", re.I),
    ),
    (
        "aggregate gate score",
        re.compile(
            r"\b(?:aggregate|overall|average|averaged|mean|total)\s+(?:gate\s+)?score\b[^.\n]{0,20}?[:=]?\s*\(?\s*\d+(?:\.\d+)?",
            re.I,
        ),
    ),
    (
        "aggregate gate score",
        re.compile(r"\bgate\s*score\s*[:=]\s*\(?\s*\d+(?:\.\d+)?", re.I),
    ),
    (
        "aggregate gate score",
        re.compile(
            r"\b(?:aggregate|overall|average|averaged|mean)\s+gates?\b[^.\n]{0,30}?\b\d+(?:\.\d+)?\s*/\s*\d+",
            re.I,
        ),
    ),
)

NEGATION_RE = re.compile(
    r"\b(?:no|not|never|without|avoid|avoided|avoiding|forbid|forbidden|prohibit|prohibited|"
    r"refuse|refused|refuses|reject|rejected|rejects|disable|disabled|"
    r"does\s+not|do\s+not|doesn't|don't|cannot|can't|isn't|aren't|nor)\b",
    re.I,
)


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------


@dataclass
class Finding:
    """One grader finding tied to a stable check id."""

    check_id: str
    severity: str
    message: str
    line: Optional[int] = None
    section: Optional[int] = None

    def as_dict(self) -> dict:
        return {
            "check_id": self.check_id,
            "severity": self.severity,
            "message": self.message,
            "line": self.line,
            "section": self.section,
        }


@dataclass
class CheckOutcome:
    applicable: bool = True
    note: str = ""
    findings: List[Finding] = field(default_factory=list)


@dataclass
class Section:
    number: int
    title: str
    heading_line: int
    entries: List[Tuple[int, str]] = field(default_factory=list)

    @property
    def heading(self) -> str:
        return "## %d. %s" % (self.number, self.title)


@dataclass
class Table:
    headers: List[str]
    rows: List[Tuple[int, List[str]]]
    header_line: int

    def column(self, name: str) -> Optional[int]:
        for idx, header in enumerate(self.headers):
            if header.strip().lower() == name.strip().lower():
                return idx
        return None


# --------------------------------------------------------------------------
# Parsing helpers
# --------------------------------------------------------------------------


def _fence_and_comment_state(lines: Sequence[str]) -> Tuple[List[bool], List[bool], List[bool]]:
    """Return (in_fence_body, is_fence_delimiter, is_comment_line) per line."""

    in_fence_body = [False] * len(lines)
    is_fence_delim = [False] * len(lines)
    is_comment = [False] * len(lines)

    fence_open = False
    in_comment = False
    for i, line in enumerate(lines):
        # --- HTML comment tracking (independent of fences) ---
        j = 0
        visible = False
        while j < len(line):
            if in_comment:
                end = line.find("-->", j)
                if end == -1:
                    j = len(line)
                else:
                    in_comment = False
                    j = end + 3
                continue
            start = line.find("<!--", j)
            if start == -1:
                if line[j:].strip():
                    visible = True
                break
            if line[j:start].strip():
                visible = True
            in_comment = True
            j = start + 4
        is_comment[i] = not visible and (in_comment or "<!--" in line)

        # --- fence tracking ---
        m = FENCE_RE.match(line)
        if m:
            is_fence_delim[i] = True
            fence_open = not fence_open
            continue
        if fence_open:
            in_fence_body[i] = True

    return in_fence_body, is_fence_delim, is_comment


def clean_value(raw: str) -> str:
    """Normalise a YAML-ish scalar: drop inline comments and surrounding quotes."""

    value = (raw or "").strip()
    if not value.startswith(("'", '"')) and "#" in value:
        value = value.split("#", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def split_row(text: str) -> List[str]:
    """Split one Markdown table row, honouring escaped pipes inside cells."""

    body = text.strip().replace("\\|", "\x00")
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.replace("\x00", "|").strip() for cell in body.split("|")]


def is_separator_row(cells: Sequence[str]) -> bool:
    return len(cells) > 0 and all(SEPARATOR_CELL_RE.match(cell) for cell in cells)


def tokens_of(cell: str) -> List[str]:
    """Split a cell into uppercase-ish tokens for enum membership tests."""

    return [tok for tok in re.split(r"[^A-Za-z0-9\-]+", cell or "") if tok]


class Dossier:
    """A parsed Idea Dossier Markdown document."""

    def __init__(self, text: str, path: Optional[str] = None) -> None:
        self.path = path
        self.text = text
        self.lines: List[str] = text.split("\n")
        self.in_fence, self.is_fence_delim, self.is_comment = _fence_and_comment_state(self.lines)
        self.sections: List[Section] = []
        self.preamble: List[Tuple[int, str]] = []
        self._line_section: Dict[int, int] = {}

        current: Optional[Section] = None
        for idx, line in enumerate(self.lines):
            lineno = idx + 1
            if self.is_comment[idx]:
                continue
            m = HEADING_RE.match(line)
            if m and not self.in_fence[idx]:
                current = Section(number=int(m.group(1)), title=m.group(2), heading_line=lineno)
                self.sections.append(current)
                continue
            if current is None:
                self.preamble.append((lineno, line))
            else:
                current.entries.append((lineno, line))
                self._line_section[lineno] = current.number

    # -- lookups ----------------------------------------------------------

    def by_number(self, number: int) -> Optional[Section]:
        for section in self.sections:
            if section.number == number:
                return section
        return None

    def section_of_line(self, lineno: int) -> Optional[int]:
        return self._line_section.get(lineno)

    def content_lines(self) -> List[Tuple[int, str]]:
        """Lines that are neither HTML comments nor headings, document wide."""

        headings = {section.heading_line for section in self.sections}
        out = []
        for idx, line in enumerate(self.lines):
            lineno = idx + 1
            if self.is_comment[idx] or lineno in headings:
                continue
            out.append((lineno, line))
        return out

    def status_of(self, section: Optional[Section]) -> Tuple[Optional[str], Optional[int]]:
        if section is None:
            return None, None
        for lineno, text in section.entries:
            m = YAML_KV_RE.match(text)
            if m and m.group(1) == "section_status":
                return clean_value(m.group(2)), lineno
        return None, None

    def is_entered(self, section: Optional[Section]) -> bool:
        status, _ = self.status_of(section)
        return status in ("ACTIVE", "COMPLETE")

    def lifecycle_block_end(self, section: Section) -> Optional[int]:
        """Last line number that still belongs to the section lifecycle block."""

        start_lineno = None
        for lineno, text in section.entries:
            m = YAML_KV_RE.match(text)
            if m and m.group(1) == "section_status":
                start_lineno = lineno
                break
        if start_lineno is None:
            return None

        if self.in_fence[start_lineno - 1]:
            for lineno in range(start_lineno + 1, len(self.lines) + 1):
                if self.is_fence_delim[lineno - 1]:
                    return lineno
            return len(self.lines)

        last = start_lineno
        for lineno, text in section.entries:
            if lineno <= start_lineno:
                continue
            if not text.strip():
                continue
            if YAML_KV_RE.match(text):
                last = lineno
                continue
            break
        return last

    def yaml_value(self, section: Optional[Section], key: str) -> Tuple[Optional[str], Optional[int]]:
        if section is None:
            return None, None
        for lineno, text in section.entries:
            m = YAML_KV_RE.match(text)
            if m and m.group(1) == key:
                return clean_value(m.group(2)), lineno
        return None, None


def iter_tables(section: Section) -> List[Table]:
    """Every Markdown table inside a section (header row + separator + body)."""

    tables: List[Table] = []
    entries = section.entries
    idx = 0
    while idx < len(entries):
        lineno, text = entries[idx]
        if TABLE_ROW_RE.match(text):
            if idx + 1 < len(entries):
                next_cells = split_row(entries[idx + 1][1])
                if is_separator_row(next_cells):
                    headers = split_row(text)
                    rows: List[Tuple[int, List[str]]] = []
                    cursor = idx + 2
                    while cursor < len(entries) and TABLE_ROW_RE.match(entries[cursor][1]):
                        cells = split_row(entries[cursor][1])
                        if is_separator_row(cells):
                            break
                        rows.append((entries[cursor][0], cells))
                        cursor += 1
                    tables.append(Table(headers=headers, rows=rows, header_line=lineno))
                    idx = cursor
                    continue
        idx += 1
    return tables


def find_table(section: Section, required_headers: Sequence[str]) -> Optional[Table]:
    wanted = {header.strip().lower() for header in required_headers}
    for table in iter_tables(section):
        present = {header.strip().lower() for header in table.headers}
        if wanted <= present:
            return table
    return None


def cell(table: Table, row: Sequence[str], column: str) -> str:
    idx = table.column(column)
    if idx is None or idx >= len(row):
        return ""
    return row[idx]


def cap(findings: List[Finding], limit: int = MAX_FINDINGS_PER_CHECK) -> List[Finding]:
    if len(findings) <= limit:
        return findings
    head = findings[:limit]
    head.append(
        Finding(
            findings[0].check_id,
            findings[0].severity,
            "… and %d further finding(s) suppressed by the %d-finding display cap"
            % (len(findings) - limit, limit),
            None,
            None,
        )
    )
    return head


def _is_negated(line: str, start: int, window: int = 45) -> bool:
    return bool(NEGATION_RE.search(line[max(0, start - window) : start]))


# Section 0 keeps its whole control block in one fenced YAML block, so these
# keys are the template's REQUIRED control fields.  Dossier schema 1.1.0 has
# twelve of them: `dossier_schema_version` sits directly after `dossier_id`.
CONTROL_REQUIRED_FIELDS: Tuple[str, ...] = (
    "section_status",
    "status_reason",
    "dossier_id",
    "dossier_schema_version",
    "date",
    "evidence_cutoff",
    "entry_mode",
    "current_phase",
    "task",
    "data_regime",
    "evaluation_target",
    "scope_exclusions",
)


def yaml_fields(section: Section) -> Dict[str, Tuple[int, str]]:
    """Every ``key: value`` line in a section, first occurrence wins."""

    fields: Dict[str, Tuple[int, str]] = {}
    for lineno, text in section.entries:
        match = YAML_KV_RE.match(text)
        if match:
            fields.setdefault(match.group(1), (lineno, clean_value(match.group(2))))
    return fields


def emitted_fields(dossier: "Dossier", section: Section) -> List[Tuple[int, str, str]]:
    """Fields emitted beyond the lifecycle pair (section_status, status_reason)."""

    end = dossier.lifecycle_block_end(section)
    fields: List[Tuple[int, str, str]] = []
    for lineno, text in section.entries:
        if not text.strip() or HORIZONTAL_RULE_RE.match(text) or dossier.is_fence_delim[lineno - 1]:
            continue
        match = YAML_KV_RE.match(text)
        inside_lifecycle = end is not None and lineno <= end
        if inside_lifecycle:
            # Section 0 carries its control fields inside the lifecycle block.
            if match and match.group(1) not in ("section_status", "status_reason"):
                fields.append((lineno, match.group(1), clean_value(match.group(2))))
            continue
        fields.append((lineno, match.group(1) if match else "", text.strip()))
    return fields


# --------------------------------------------------------------------------
# S01..S17
# --------------------------------------------------------------------------


def check_s01(doc: Dossier) -> CheckOutcome:
    """sections-present: headings ## 0. through ## 16. all present."""

    present = {section.number for section in doc.sections}
    findings: List[Finding] = []
    for number in CANONICAL_SECTIONS:
        if number not in present:
            findings.append(
                Finding(
                    "S01",
                    "error",
                    "section %d is missing: no heading matching '## %d.'" % (number, number),
                    None,
                    number,
                )
            )
    for section in doc.sections:
        if section.number not in CANONICAL_SECTIONS:
            findings.append(
                Finding(
                    "S01",
                    "error",
                    "unexpected section heading '## %d.' outside the canonical range 0-16" % section.number,
                    section.heading_line,
                    section.number,
                )
            )
    return CheckOutcome(
        True,
        "%d/17 canonical sections present" % len(present & set(CANONICAL_SECTIONS)),
        cap(findings),
    )


def check_s02(doc: Dossier) -> CheckOutcome:
    """section-order: section numbers strictly ascending in document order."""

    findings: List[Finding] = []
    previous: Optional[int] = None
    for section in doc.sections:
        if previous is not None and section.number <= previous:
            findings.append(
                Finding(
                    "S02",
                    "error",
                    "section %d follows section %d; section numbers must be strictly ascending"
                    % (section.number, previous),
                    section.heading_line,
                    section.number,
                )
            )
        previous = section.number
    order = ", ".join(str(section.number) for section in doc.sections)
    note = "strictly ascending (%s)" % order if not findings else "order violated"
    return CheckOutcome(True, note, cap(findings))


def check_s03(doc: Dossier) -> CheckOutcome:
    """placeholders: no unreplaced {{REQUIRED: ...}} token anywhere."""

    findings: List[Finding] = []
    total = 0
    for lineno, text in doc.content_lines():
        count = len(PLACEHOLDER_RE.findall(text))
        if count:
            total += count
            findings.append(
                Finding(
                    "S03",
                    "error",
                    "%d unreplaced template placeholder(s): %s" % (count, text.strip()[:110]),
                    lineno,
                    doc.section_of_line(lineno),
                )
            )
    note = "no placeholders" if not findings else "%d placeholder token(s)" % total
    return CheckOutcome(True, note, cap(findings))


def check_s04(doc: Dossier) -> CheckOutcome:
    """lifecycle-values: every section carries a valid section_status."""

    findings: List[Finding] = []
    valid = 0
    for section in doc.sections:
        value, lineno = doc.status_of(section)
        if value is None or value == "":
            findings.append(
                Finding(
                    "S04",
                    "error",
                    "section %d has no section_status field in its lifecycle block" % section.number,
                    section.heading_line,
                    section.number,
                )
            )
            continue
        if value not in LIFECYCLE_VALUES:
            findings.append(
                Finding(
                    "S04",
                    "error",
                    "section %d has section_status '%s'; allowed values are %s"
                    % (section.number, value, " | ".join(LIFECYCLE_VALUES)),
                    lineno,
                    section.number,
                )
            )
            continue
        valid += 1
    return CheckOutcome(True, "%d/%d sections carry a valid section_status" % (valid, len(doc.sections)), cap(findings))


def check_s05(doc: Dossier) -> CheckOutcome:
    """lifecycle-body: NOT-STARTED/BLOCKED sections emit heading + lifecycle only;
    ACTIVE/COMPLETE sections must not be empty."""

    findings: List[Finding] = []
    checked = 0
    for section in doc.sections:
        status, _ = doc.status_of(section)
        if status is None:
            continue
        checked += 1
        if status in ("NOT-STARTED", "BLOCKED"):
            end = doc.lifecycle_block_end(section)
            if end is None:
                continue
            for lineno, text in section.entries:
                if lineno <= end or not text.strip():
                    continue
                if HORIZONTAL_RULE_RE.match(text):
                    continue
                if ANY_PLACEHOLDER_RE.search(text):
                    reason = "unreplaced placeholder %s" % text.strip()[:80]
                elif TABLE_ROW_RE.match(text):
                    reason = "instantiated table row: %s" % text.strip()[:80]
                elif ID_TOKEN_RE.search(text):
                    reason = "instantiated ID record: %s" % text.strip()[:80]
                else:
                    reason = "content beyond the lifecycle block: %s" % text.strip()[:80]
                findings.append(
                    Finding(
                        "S05",
                        "error",
                        "section %d is %s but emits more than its heading and lifecycle block — %s"
                        % (section.number, status, reason),
                        lineno,
                        section.number,
                    )
                )
        elif status in ("ACTIVE", "COMPLETE"):
            # "emit the lifecycle block and the full section body": an entered
            # section must carry at least one field beyond section_status and
            # status_reason.  Section 0 keeps its whole control block in one
            # fenced YAML block, so its control keys count as the body — but a
            # missing or blank control key must still fail.
            fields = emitted_fields(doc, section)
            if section.number == 0:
                present = yaml_fields(section)
                for key in CONTROL_REQUIRED_FIELDS:
                    if key not in present or not present[key][1]:
                        lineno = present[key][0] if key in present else section.heading_line
                        findings.append(
                            Finding(
                                "S05",
                                "error",
                                "section 0 control block is missing the required field '%s'" % key,
                                lineno,
                                0,
                            )
                        )
            elif not fields:
                findings.append(
                    Finding(
                        "S05",
                        "error",
                        "section %d is %s but emits no field beyond its lifecycle block"
                        % (section.number, status),
                        section.heading_line,
                        section.number,
                    )
                )
    return CheckOutcome(True, "%d section(s) checked against their lifecycle contract" % checked, cap(findings))


def check_s06(doc: Dossier) -> CheckOutcome:
    """id-namespaces: every AAA-123 token uses a namespace the template permits."""

    findings: List[Finding] = []
    seen = set()
    for lineno, text in doc.content_lines():
        for match in ID_TOKEN_RE.finditer(text):
            namespace, token = match.group(1), match.group(0)
            if namespace in ID_NAMESPACES or namespace in EXTERNAL_ID_PREFIXES:
                continue
            key = (lineno, token)
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                Finding(
                    "S06",
                    "error",
                    "ID token '%s' uses namespace '%s'; the template permits only %s"
                    % (token, namespace, ", ".join(ID_NAMESPACES)),
                    lineno,
                    doc.section_of_line(lineno),
                )
            )
    note = "no unpermitted ID namespace" if not findings else "%d unpermitted token(s)" % len(findings)
    return CheckOutcome(True, note, cap(findings))


def check_s07(doc: Dossier) -> CheckOutcome:
    """novelty-numeric: no numeric novelty score or aggregate gate score."""

    findings: List[Finding] = []
    for lineno, text in doc.content_lines():
        hits: List[Tuple[int, int, str, str]] = []
        for label, pattern in NUMERIC_SCORE_PATTERNS:
            for match in pattern.finditer(text):
                if _is_negated(text, match.start()):
                    continue
                hits.append((match.start(), match.end(), label, match.group(0).strip()))
        # report distinct offending spans only: drop spans contained in another
        hits.sort(key=lambda item: (item[0], -(item[1] - item[0])))
        kept: List[Tuple[int, int, str, str]] = []
        for hit in hits:
            if any(hit[0] >= other[0] and hit[1] <= other[1] for other in kept):
                continue
            kept.append(hit)
        for _start, _end, label, token in sorted(kept, key=lambda item: item[0]):
            findings.append(
                Finding(
                    "S07",
                    "error",
                    "%s '%s' is forbidden — the skill requires a non-numeric status" % (label, token),
                    lineno,
                    doc.section_of_line(lineno),
                )
            )
    note = "no numeric novelty or gate score" if not findings else "%d numeric score token(s)" % len(findings)
    return CheckOutcome(True, note, cap(findings))


def check_s08(doc: Dossier) -> CheckOutcome:
    """decision-enum: section 16 carries exactly one decision from the enum."""

    section = doc.by_number(16)
    status, _ = doc.status_of(section)
    if section is None:
        return CheckOutcome(False, "section 16 is absent", [])
    if status not in ("ACTIVE", "COMPLETE"):
        return CheckOutcome(False, "section 16 is %s — no decision required" % (status or "not started"), [])

    found: List[Tuple[int, str]] = []
    for lineno, text in section.entries:
        m = re.match(r"^\s*decision\s*:\s*(.*)$", text)
        if m:
            found.append((lineno, clean_value(m.group(1))))

    findings: List[Finding] = []
    if len(found) != 1:
        findings.append(
            Finding(
                "S08",
                "error",
                "section 16 must contain exactly one 'decision:' field; found %d" % len(found),
                found[1][0] if len(found) > 1 else (found[0][0] if found else None),
                16,
            )
        )
    for lineno, value in found:
        if value not in DECISIONS:
            findings.append(
                Finding(
                    "S08",
                    "error",
                    "decision '%s' is not one of %s" % (value, " | ".join(DECISIONS)),
                    lineno,
                    16,
                )
            )
    note = "decision %s" % found[0][1] if len(found) == 1 and found[0][1] in DECISIONS else "decision field invalid"
    return CheckOutcome(True, note, findings)


def check_s09(doc: Dossier) -> CheckOutcome:
    """decision-consistency: decision_consistency_check: PASS present in section 16."""

    section = doc.by_number(16)
    status, _ = doc.status_of(section)
    if section is None:
        return CheckOutcome(False, "section 16 is absent", [])
    if status not in ("ACTIVE", "COMPLETE"):
        return CheckOutcome(False, "section 16 is %s — no decision required" % (status or "not started"), [])

    value, lineno = doc.yaml_value(section, "decision_consistency_check")
    if value is None:
        return CheckOutcome(
            True,
            "missing decision_consistency_check",
            [
                Finding(
                    "S09",
                    "error",
                    "section 16 must declare decision_consistency_check: PASS",
                    section.heading_line,
                    16,
                )
            ],
        )
    if value != "PASS":
        return CheckOutcome(
            True,
            "decision_consistency_check is %s" % value,
            [
                Finding(
                    "S09",
                    "error",
                    "decision_consistency_check is '%s'; only PASS is acceptable at a compiled decision" % value,
                    lineno,
                    16,
                )
            ],
        )
    return CheckOutcome(True, "decision_consistency_check: PASS", [])


def check_s10(doc: Dossier) -> CheckOutcome:
    """gate-table: section 15 enumerates G0-G11 with a valid result per gate."""

    section = doc.by_number(15)
    if section is None:
        return CheckOutcome(False, "section 15 is absent", [])
    gate_rows = [
        (lineno, text) for lineno, text in section.entries if GATE_ID_RE.match(text) and not is_separator_row(split_row(text))
    ]
    status, _ = doc.status_of(section)
    if not gate_rows and status not in ("ACTIVE", "COMPLETE"):
        return CheckOutcome(False, "section 15 is %s — gate table not entered" % (status or "not started"), [])

    findings: List[Finding] = []
    if not gate_rows:
        findings.append(
            Finding("S10", "error", "section 15 is entered but contains no gate rows", section.heading_line, 15)
        )
        return CheckOutcome(True, "0 gate rows", findings)

    table = find_table(section, ["Gate", "Evaluation status", "State", "Failure mode"])
    if table is None:
        findings.append(
            Finding(
                "S10",
                "error",
                "section 15 gate table is missing its canonical columns (expected Gate | Evaluation status | State | Failure mode | …)",
                gate_rows[0][0],
                15,
            )
        )
        return CheckOutcome(True, "gate table malformed", findings)

    seen: Dict[str, int] = {}
    for lineno, row in table.rows:
        m = re.match(r"^(G\d{1,2})\b", cell(table, row, "Gate"))
        if not m:
            continue
        gate = m.group(1)
        if gate in seen:
            findings.append(
                Finding("S10", "error", "gate %s is listed more than once" % gate, lineno, 15)
            )
        seen[gate] = lineno
        evaluation = cell(table, row, "Evaluation status")
        state = cell(table, row, "State")
        failure_mode = cell(table, row, "Failure mode")
        if evaluation == "":
            findings.append(Finding("S10", "error", "gate %s has no evaluation status" % gate, lineno, 15))
        elif evaluation not in GATE_EVALUATION_STATUSES:
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s evaluation status '%s' is not one of %s"
                    % (gate, evaluation, " | ".join(GATE_EVALUATION_STATUSES)),
                    lineno,
                    15,
                )
            )
        if state == "":
            findings.append(Finding("S10", "error", "gate %s has no state" % gate, lineno, 15))
        elif state not in GATE_STATES:
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s state '%s' is not one of %s" % (gate, state, " | ".join(GATE_STATES)),
                    lineno,
                    15,
                )
            )
        mode_norm = failure_mode.strip().lower()
        is_null_mode = mode_norm in ("null", "") or mode_norm.startswith("n/a")
        if not is_null_mode and failure_mode not in GATE_FAILURE_MODES:
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s failure mode '%s' is not one of %s"
                    % (gate, failure_mode, " | ".join(GATE_FAILURE_MODES)),
                    lineno,
                    15,
                )
            )
        if state in GATE_STATES and state != "UNSATISFIED" and not is_null_mode:
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s uses failure mode '%s' while state is %s; failure_mode must be null unless the gate is UNSATISFIED"
                    % (gate, failure_mode, state),
                    lineno,
                    15,
                )
            )
        if state == "UNSATISFIED" and is_null_mode:
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s is UNSATISFIED but names no failure mode (REPAIRABLE or CONTRADICTED)" % gate,
                    lineno,
                    15,
                )
            )
        if evaluation == "DEFERRED" and state not in ("UNRESOLVED", ""):
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s is DEFERRED but its state is %s; a deferred gate must be UNRESOLVED" % (gate, state),
                    lineno,
                    15,
                )
            )

    for number in range(len(GATES)):
        gate = "G%d" % number
        if gate not in seen:
            findings.append(
                Finding(
                    "S10",
                    "error",
                    "gate %s is missing from the section 15 gate table" % gate,
                    None,
                    15,
                )
            )
    note = "%d/12 gates enumerated with a result" % len(seen)
    return CheckOutcome(True, note, cap(findings))


def check_s11(doc: Dossier) -> CheckOutcome:
    """evidence-levels: every E-level token is inside the template's range."""

    findings: List[Finding] = []
    seen = set()
    for lineno, text in doc.content_lines():
        for match in EVIDENCE_TOKEN_RE.finditer(text):
            level = "E%s" % match.group(1)
            if level in EVIDENCE_LEVELS:
                continue
            key = (lineno, level)
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                Finding(
                    "S11",
                    "error",
                    "evidence level '%s' is out of range; the template defines %s"
                    % (level, " | ".join(EVIDENCE_LEVELS)),
                    lineno,
                    doc.section_of_line(lineno),
                )
            )
    note = "all E-level tokens within %s" % " | ".join(EVIDENCE_LEVELS) if not findings else "%d out-of-range token(s)" % len(findings)
    return CheckOutcome(True, note, cap(findings))


def check_s12(doc: Dossier) -> CheckOutcome:
    """claim-ledger-typing: CLM rows carry a canonical Claim type and Status."""

    section = doc.by_number(3)
    if section is None:
        return CheckOutcome(False, "section 3 is absent", [])
    if not doc.is_entered(section):
        status, _ = doc.status_of(section)
        return CheckOutcome(False, "section 3 is %s — ledger not entered" % (status or "not started"), [])

    table = find_table(section, ["Claim ID", "Claim type", "Status"])
    if table is None:
        return CheckOutcome(
            True,
            "no typed ledger table",
            [
                Finding(
                    "S12",
                    "error",
                    "section 3 is entered but contains no claim ledger table with the canonical columns (Claim ID | Claim type | … | Status)",
                    section.heading_line,
                    3,
                )
            ],
        )

    rows = [(lineno, row) for lineno, row in table.rows if cell(table, row, "Claim ID").startswith("CLM-")]
    findings: List[Finding] = []
    if not rows:
        findings.append(
            Finding(
                "S12",
                "error",
                "section 3 ledger contains no CLM-* rows",
                table.header_line,
                3,
            )
        )
    for lineno, row in rows:
        claim_id = cell(table, row, "Claim ID")
        claim_type = cell(table, row, "Claim type")
        status_value = cell(table, row, "Status")
        if not (set(tokens_of(claim_type)) & set(CLAIM_TYPES)):
            findings.append(
                Finding(
                    "S12",
                    "error",
                    "%s Claim type '%s' is not one of %s" % (claim_id, claim_type, " | ".join(CLAIM_TYPES)),
                    lineno,
                    3,
                )
            )
        if not (set(tokens_of(status_value)) & set(CLAIM_STATUSES)):
            findings.append(
                Finding(
                    "S12",
                    "error",
                    "%s Status '%s' is not one of %s" % (claim_id, status_value, " | ".join(CLAIM_STATUSES)),
                    lineno,
                    3,
                )
            )
    note = "%d CLM-* row(s) typed" % len(rows)
    return CheckOutcome(True, note, cap(findings))


def check_s13(doc: Dossier) -> CheckOutcome:
    """phase-gating: current_phase DIAGNOSIS requires sections 8-16 NOT-STARTED."""

    control = doc.by_number(0)
    if control is None:
        return CheckOutcome(False, "section 0 is absent", [])
    phase, phase_line = doc.yaml_value(control, "current_phase")
    if phase is None or phase == "":
        if doc.is_entered(control):
            status, _ = doc.status_of(control)
            return CheckOutcome(
                True,
                "current_phase not recorded",
                [
                    Finding(
                        "S13",
                        "error",
                        "section 0 is %s but records no current_phase, so phase gating cannot be verified" % status,
                        control.heading_line,
                        0,
                    )
                ],
            )
        return CheckOutcome(False, "section 0 is not entered and records no current_phase", [])

    normalized = phase.split()[0].strip()
    if normalized not in PHASE_SECTION_BOUNDARY:
        return CheckOutcome(
            True,
            "unknown phase %s" % phase,
            [
                Finding(
                    "S13",
                    "error",
                    "current_phase '%s' is not one of %s"
                    % (phase, " | ".join(sorted(PHASE_SECTION_BOUNDARY))),
                    phase_line,
                    0,
                )
            ],
        )
    if normalized != "DIAGNOSIS":
        return CheckOutcome(True, "current_phase %s — sections 8-16 are not gated" % normalized, [])

    # Section 13 is exempt: the template's own section-13 note says "Preserve
    # diagnostic EXP-* IDs created during Stages 2-4", and Stages 2-4 are inside
    # DIAGNOSIS.  Gating it would flag the skill's canonical NEED-EVIDENCE
    # dossier.  Sections 8-12 and 14-16 stay gated.
    gated = (8, 9, 10, 11, 12, 14, 15, 16)
    findings: List[Finding] = []
    for number in gated:
        section = doc.by_number(number)
        if section is None:
            continue
        status, lineno = doc.status_of(section)
        if status != "NOT-STARTED":
            findings.append(
                Finding(
                    "S13",
                    "error",
                    "current_phase is DIAGNOSIS (sections 0-6) but section %d is %s; it must be NOT-STARTED"
                    % (number, status or "unset"),
                    lineno if lineno else section.heading_line,
                    number,
                )
            )
    section13 = doc.by_number(13)
    section13_status, _ = doc.status_of(section13)
    if section13 is not None and section13_status in ("ACTIVE", "COMPLETE"):
        suffix = " (section 13 exempt: it carries the Stage 2-4 diagnostic rows)"
    else:
        suffix = ""
    note = (
        "current_phase DIAGNOSIS — sections 8-12 and 14-16 NOT-STARTED" + suffix
        if not findings
        else "phase gating violated"
    )
    return CheckOutcome(True, note, cap(findings))


def _section13_experiments(doc: Dossier) -> Dict[str, Tuple[str, str, int]]:
    section = doc.by_number(13)
    if section is None:
        return {}
    table = find_table(section, ["Experiment ID", "Status", "Observed result"])
    if table is None:
        return {}
    out: Dict[str, Tuple[str, str, int]] = {}
    for lineno, row in table.rows:
        exp_id = cell(table, row, "Experiment ID").strip()
        if not exp_id.startswith("EXP-"):
            continue
        out[exp_id] = (cell(table, row, "Status"), cell(table, row, "Observed result"), lineno)
    return out


def check_s14(doc: Dossier) -> CheckOutcome:
    """plans-vs-evidence: a SUPPORTED CLM row may not rest on a plan."""

    section = doc.by_number(3)
    if section is None or not doc.is_entered(section):
        return CheckOutcome(False, "section 3 ledger not entered", [])
    table = find_table(section, ["Claim ID", "Claim type", "Status"])
    if table is None:
        return CheckOutcome(False, "section 3 has no claim ledger table", [])

    experiments = _section13_experiments(doc)
    findings: List[Finding] = []
    supported = 0
    for lineno, row in table.rows:
        claim_id = cell(table, row, "Claim ID")
        if not claim_id.startswith("CLM-"):
            continue
        if "SUPPORTED" not in tokens_of(cell(table, row, "Status")):
            continue
        supported += 1
        source_refs = cell(table, row, "Source refs")
        row_text = " | ".join(row)
        if "PENDING" in row_text.upper():
            findings.append(
                Finding(
                    "S14",
                    "warning",
                    "%s is SUPPORTED but its row references a PENDING record — a plan is never evidence"
                    % claim_id,
                    lineno,
                    3,
                )
            )
        for exp_id in sorted(set(re.findall(r"\bEXP-\d{1,4}\b", row_text))):
            if exp_id not in experiments:
                findings.append(
                    Finding(
                        "S14",
                        "warning",
                        "%s is SUPPORTED and cites %s, which has no recorded row in section 13 — a plan is never evidence"
                        % (claim_id, exp_id),
                        lineno,
                        3,
                    )
                )
                continue
            status, observed, exp_line = experiments[exp_id]
            if status.strip().upper() not in ("COMPLETED",) or "PENDING" in observed.upper():
                findings.append(
                    Finding(
                        "S14",
                        "warning",
                        "%s is SUPPORTED but %s is %s with observed result '%s' — a plan is never evidence"
                        % (claim_id, exp_id, status.strip() or "unset", observed.strip()[:60]),
                        lineno,
                        3,
                    )
                )
        if not source_refs.strip():
            findings.append(
                Finding("S14", "warning", "%s is SUPPORTED but names no source reference" % claim_id, lineno, 3)
            )
    note = "%d SUPPORTED claim(s) checked against their experiment records" % supported
    return CheckOutcome(True, note, cap(findings))


def _defined_ids(doc: Dossier) -> set:
    """IDs defined by record position in sections 0-13.

    A definition is either the first cell of a table row (the record tables) or
    the value of a singleton *_id field (dossier_id, need_id, failure_id,
    invariant_id).
    """

    defined = set()
    for section in doc.sections:
        if section.number > 13:
            continue
        for table in iter_tables(section):
            for _lineno, row in table.rows:
                if not row:
                    continue
                for match in ID_TOKEN_RE.finditer(row[0]):
                    if match.group(1) in ID_NAMESPACES:
                        defined.add(match.group(0))
        for _lineno, text in section.entries:
            m = re.match(r"^\s*([A-Za-z_]+_id)\s*:\s*(.*)$", text)
            if not m:
                continue
            for match in ID_TOKEN_RE.finditer(m.group(2)):
                if match.group(1) in ID_NAMESPACES:
                    defined.add(match.group(0))
    return defined


def check_s15(doc: Dossier) -> CheckOutcome:
    """traceability: IDs referenced in sections 14-16 must be defined in 0-13."""

    defined = _defined_ids(doc)
    findings: List[Finding] = []
    seen = set()
    referenced = 0
    for number in (14, 15, 16):
        section = doc.by_number(number)
        if section is None:
            continue
        for lineno, text in section.entries:
            for match in ID_TOKEN_RE.finditer(text):
                token, namespace = match.group(0), match.group(1)
                if namespace not in ID_NAMESPACES:
                    continue
                referenced += 1
                if token in defined:
                    continue
                key = (token, number)
                if key in seen:
                    continue
                seen.add(key)
                findings.append(
                    Finding(
                        "S15",
                        "warning",
                        "%s is referenced in section %d but never defined in sections 0-13"
                        % (token, number),
                        lineno,
                        number,
                    )
                )
    note = "%d reference(s) traced against %d defined ID(s)" % (referenced, len(defined))
    return CheckOutcome(True, note, cap(findings))


def check_s16(doc: Dossier) -> CheckOutcome:
    """phase-section-consistency (extension): later sections stay NOT-STARTED."""

    control = doc.by_number(0)
    if control is None:
        return CheckOutcome(False, "section 0 is absent", [])
    phase, _ = doc.yaml_value(control, "current_phase")
    if not phase:
        return CheckOutcome(False, "no current_phase recorded", [])
    normalized = phase.split()[0].strip()
    boundary = PHASE_SECTION_BOUNDARY.get(normalized)
    if boundary is None:
        return CheckOutcome(False, "unknown phase %s" % phase, [])

    findings: List[Finding] = []
    for number in range(boundary + 1, 17):
        if normalized == "DIAGNOSIS" and number >= 8:
            continue  # S13 owns the hard DIAGNOSIS gate
        section = doc.by_number(number)
        if section is None:
            continue
        status, lineno = doc.status_of(section)
        if status != "NOT-STARTED":
            findings.append(
                Finding(
                    "S16",
                    "warning",
                    "current_phase %s covers sections 0-%d but section %d is %s; unentered sections should stay NOT-STARTED"
                    % (normalized, boundary, number, status or "unset"),
                    lineno if lineno else section.heading_line,
                    number,
                )
            )
    note = "phase %s — later sections stay NOT-STARTED" % normalized if not findings else "later sections entered early"
    return CheckOutcome(True, note, cap(findings))


def check_s17(doc: Dossier) -> CheckOutcome:
    """decision-gate-agreement (extension): the decision must follow the gate table."""

    section15 = doc.by_number(15)
    section16 = doc.by_number(16)
    if section15 is None or section16 is None:
        return CheckOutcome(False, "section 15 or 16 is absent", [])
    if not doc.is_entered(section16):
        return CheckOutcome(False, "section 16 is not entered — no decision to cross-check", [])
    table = find_table(section15, ["Gate", "Evaluation status", "State", "Failure mode"])
    if table is None or not doc.is_entered(section15):
        return CheckOutcome(False, "section 15 gate table not entered", [])

    unresolved: List[str] = []
    repairable: List[str] = []
    contradicted: List[str] = []
    unsatisfied_without_mode: List[str] = []
    not_evaluated_satisfied: List[str] = []
    for _lineno, row in table.rows:
        gate = cell(table, row, "Gate").split()[0] if cell(table, row, "Gate") else ""
        if not re.match(r"^G\d{1,2}$", gate):
            continue
        state = cell(table, row, "State")
        failure_mode = cell(table, row, "Failure mode").strip()
        evaluation = cell(table, row, "Evaluation status")
        if state == "UNRESOLVED":
            unresolved.append(gate)
        elif state == "UNSATISFIED":
            if failure_mode == "REPAIRABLE":
                repairable.append(gate)
            elif failure_mode == "CONTRADICTED":
                contradicted.append(gate)
            else:
                unsatisfied_without_mode.append(gate)
        elif state == "SATISFIED" and evaluation == "DEFERRED":
            not_evaluated_satisfied.append(gate)

    if contradicted or unsatisfied_without_mode:
        derived = "FATAL-CONTRADICTION"
    elif repairable:
        derived = "REPAIRABLE-FAILURE"
    elif unresolved:
        derived = "UNRESOLVED-EVIDENCE"
    else:
        derived = "ALL-SATISFIED"

    decision, decision_line = doc.yaml_value(section16, "decision")
    rule, rule_line = doc.yaml_value(section16, "decision_rule_triggered")
    expected_decision = {
        "FATAL-CONTRADICTION": "KILL",
        "REPAIRABLE-FAILURE": "PIVOT",
        "UNRESOLVED-EVIDENCE": "NEED-EVIDENCE",
        "ALL-SATISFIED": "GO",
    }[derived]

    findings: List[Finding] = []
    if decision is not None and decision in DECISIONS and decision != expected_decision:
        findings.append(
            Finding(
                "S17",
                "warning",
                "decision '%s' does not follow the section 15 gate table; the gate states imply %s"
                % (decision, expected_decision),
                decision_line,
                16,
            )
        )
    if rule is not None and rule in DECISION_RULES and rule != derived:
        findings.append(
            Finding(
                "S17",
                "warning",
                "decision_rule_triggered '%s' disagrees with the gate table, which implies %s"
                % (rule, derived),
                rule_line,
                16,
            )
        )
    if derived == "ALL-SATISFIED" and decision == "GO":
        novelty_section = doc.by_number(10)
        novelty_status = None
        if novelty_section is not None and doc.is_entered(novelty_section):
            novelty_table = find_table(novelty_section, ["Candidate ID", "Novelty status"])
            if novelty_table is not None and novelty_table.rows:
                novelty_status = cell(novelty_table, novelty_table.rows[0][1], "Novelty status").strip()
        if novelty_status is not None and novelty_status not in NOVELTY_STATUSES:
            findings.append(
                Finding(
                    "S17",
                    "warning",
                    "section 10 novelty status '%s' is not one of %s"
                    % (novelty_status, " | ".join(NOVELTY_STATUSES)),
                    None,
                    10,
                )
            )
        if novelty_status != "PASS":
            findings.append(
                Finding(
                    "S17",
                    "warning",
                    "decision GO requires novelty PASS; section 10 reports '%s'"
                    % (novelty_status or "no novelty audit"),
                    decision_line,
                    16,
                )
            )

    def _normalize_ids(raw: Optional[str]) -> set:
        if not raw:
            return set()
        if raw.strip().upper().startswith("N/A"):
            return set()
        return set(re.findall(r"\bG\d{1,2}\b", raw))

    expected_lists = {
        "unresolved_gate_ids": set(unresolved),
        "repairable_gate_ids": set(repairable),
        "contradicted_gate_ids": set(contradicted) | set(unsatisfied_without_mode),
    }
    for key, expected in expected_lists.items():
        raw, key_line = doc.yaml_value(section16, key)
        if raw is None:
            continue
        actual = _normalize_ids(raw)
        if actual != expected:
            findings.append(
                Finding(
                    "S17",
                    "warning",
                    "%s lists {%s} but the section 15 gate table implies {%s}"
                    % (
                        key,
                        ", ".join(sorted(actual)) or "none",
                        ", ".join(sorted(expected)) or "none",
                    ),
                    key_line,
                    16,
                )
            )
    note = "gate table implies %s (decision %s)" % (derived, decision or "unset")
    return CheckOutcome(True, note, cap(findings))


def check_s18(doc: Dossier) -> CheckOutcome:
    """coverage-gate (extension): `coverage_complete: NO` caps the falsification gate.

    Template section 13 note (dossier schema 1.1.0) and SKILL.md Stage 11:
    "coverage_complete: NO leaves G11 EVALUATED and UNRESOLVED — never satisfied —
    so the decision is capped at NEED-EVIDENCE, and each uncovered CORE claim must
    be named as the smallest next action."

    This is cross-section gate semantics rather than a property of one gate row,
    so it lives in its own error-severity check instead of being folded into S10.
    """

    section13 = doc.by_number(13)
    if section13 is None:
        return CheckOutcome(False, "section 13 is absent", [])
    if not doc.is_entered(section13):
        status, _ = doc.status_of(section13)
        return CheckOutcome(False, "section 13 is %s — no coverage block to gate" % (status or "unset"), [])

    coverage_raw, coverage_line = doc.yaml_value(section13, "coverage_complete")
    if coverage_raw is None or coverage_raw.strip() == "":
        return CheckOutcome(
            True,
            "section 13 records no coverage_complete",
            [
                Finding(
                    "S18",
                    "error",
                    "section 13 is entered but records no coverage_complete; the template marks the coverage block REQUIRED",
                    section13.heading_line,
                    13,
                )
            ],
        )

    value = re.split(r"[;\s]", coverage_raw.strip(), 1)[0].strip().upper()
    if value not in ("YES", "NO"):
        return CheckOutcome(
            True,
            "coverage_complete '%s'" % coverage_raw,
            [
                Finding(
                    "S18",
                    "error",
                    "coverage_complete '%s' is not one of YES | NO" % coverage_raw,
                    coverage_line,
                    13,
                )
            ],
        )

    uncovered_raw, uncovered_line = doc.yaml_value(section13, "uncovered_core_claim_ids")
    uncovered_ids = sorted(set(re.findall(r"\bCLM-\d{1,4}\b", uncovered_raw or "")))
    findings: List[Finding] = []

    # The field is derived from the three coverage fields: YES means nothing is
    # uncovered, NO means at least one CORE claim is.
    if value == "YES" and uncovered_ids:
        findings.append(
            Finding(
                "S18",
                "error",
                "coverage_complete is YES but uncovered_core_claim_ids lists %s; derive the value from the three coverage fields"
                % ", ".join(uncovered_ids),
                uncovered_line,
                13,
            )
        )
    if value == "NO" and not uncovered_ids:
        findings.append(
            Finding(
                "S18",
                "error",
                "coverage_complete is NO but uncovered_core_claim_ids names no CORE claim",
                uncovered_line if uncovered_line else coverage_line,
                13,
            )
        )

    if value != "NO":
        return CheckOutcome(True, "coverage_complete YES — no G11 cap applies", cap(findings))

    # (i) G11 must be EVALUATED and UNRESOLVED — never SATISFIED.
    section15 = doc.by_number(15)
    gate_seen = False
    if section15 is not None and doc.is_entered(section15):
        table = find_table(section15, ["Gate", "Evaluation status", "State", "Failure mode"])
        if table is not None:
            for lineno, row in table.rows:
                if not re.match(r"^G11\b", cell(table, row, "Gate")):
                    continue
                gate_seen = True
                state = cell(table, row, "State")
                evaluation = cell(table, row, "Evaluation status")
                if state == "SATISFIED":
                    findings.append(
                        Finding(
                            "S18",
                            "error",
                            "section 13 reports coverage_complete: NO but gate G11 is SATISFIED; incomplete coverage leaves G11 EVALUATED and UNRESOLVED",
                            lineno,
                            15,
                        )
                    )
                elif evaluation == "EVALUATED" and state != "UNRESOLVED":
                    findings.append(
                        Finding(
                            "S18",
                            "error",
                            "section 13 reports coverage_complete: NO but gate G11 is %s/%s; it must be EVALUATED/UNRESOLVED"
                            % (evaluation or "unset", state or "unset"),
                            lineno,
                            15,
                        )
                    )

    # (ii) the decision is capped: GO is forbidden while coverage is incomplete.
    section16 = doc.by_number(16)
    decision_seen = False
    if section16 is not None and doc.is_entered(section16):
        for lineno, text in section16.entries:
            match = re.match(r"^\s*decision\s*:\s*(.*)$", text)
            if not match:
                continue
            decision_seen = True
            if clean_value(match.group(1)) == "GO":
                findings.append(
                    Finding(
                        "S18",
                        "error",
                        "section 13 reports coverage_complete: NO but section 16 decides GO; incomplete falsification coverage caps the decision at NEED-EVIDENCE",
                        lineno,
                        16,
                    )
                )

        # (iii) each uncovered CORE claim must be named as the smallest next action.
        if uncovered_ids:
            action, action_line = doc.yaml_value(section16, "smallest_next_action")
            named = set(re.findall(r"\bCLM-\d{1,4}\b", action or "")) & set(uncovered_ids)
            if not named:
                findings.append(
                    Finding(
                        "S18",
                        "error",
                        "coverage_complete: NO but smallest_next_action names none of the uncovered CORE claims (%s)"
                        % ", ".join(uncovered_ids),
                        action_line if action_line else section16.heading_line,
                        16,
                    )
                )

    bits = ["coverage_complete NO"]
    if gate_seen:
        bits.append("G11 checked against the coverage state")
    if decision_seen:
        bits.append("decision checked for the GO cap")
    note = " — ".join(bits) if not findings else "coverage/gate contradiction"
    return CheckOutcome(True, note, cap(findings))


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CheckSpec:
    check_id: str
    title: str
    severity: str
    fn: Callable[[Dossier], CheckOutcome]


CHECKS: Tuple[CheckSpec, ...] = (
    CheckSpec("S01", "sections-present", "error", check_s01),
    CheckSpec("S02", "section-order", "error", check_s02),
    CheckSpec("S03", "placeholders", "error", check_s03),
    CheckSpec("S04", "lifecycle-values", "error", check_s04),
    CheckSpec("S05", "lifecycle-body", "error", check_s05),
    CheckSpec("S06", "id-namespaces", "error", check_s06),
    CheckSpec("S07", "novelty-numeric", "error", check_s07),
    CheckSpec("S08", "decision-enum", "error", check_s08),
    CheckSpec("S09", "decision-consistency", "error", check_s09),
    CheckSpec("S10", "gate-table", "error", check_s10),
    CheckSpec("S11", "evidence-levels", "error", check_s11),
    CheckSpec("S12", "claim-ledger-typing", "error", check_s12),
    CheckSpec("S13", "phase-gating", "error", check_s13),
    CheckSpec("S14", "plans-vs-evidence", "warning", check_s14),
    CheckSpec("S15", "traceability", "warning", check_s15),
    CheckSpec("S16", "phase-section-consistency", "warning", check_s16),
    CheckSpec("S17", "decision-gate-agreement", "warning", check_s17),
    CheckSpec("S18", "coverage-gate", "error", check_s18),
)


def grade_text(text: str, path: Optional[str] = None) -> dict:
    """Grade one dossier string and return a JSON-serialisable report."""

    doc = Dossier(text.lstrip("\ufeff"), path)  # tolerate a UTF-8 BOM
    checks = []
    error_count = 0
    warning_count = 0
    for spec in CHECKS:
        outcome = spec.fn(doc)
        findings = [f for f in outcome.findings if f.check_id == spec.check_id]
        if not outcome.applicable:
            status = "skip"
        elif not findings:
            status = "pass"
        elif spec.severity == "error":
            status = "fail"
        else:
            status = "warn"
        for finding in findings:
            if finding.severity == "error":
                error_count += 1
            else:
                warning_count += 1
        checks.append(
            {
                "check_id": spec.check_id,
                "title": spec.title,
                "severity": spec.severity,
                "applicable": outcome.applicable,
                "status": status,
                "note": outcome.note,
                "findings": [f.as_dict() for f in findings],
            }
        )
    return {
        "grader_version": GRADER_VERSION,
        "path": path,
        "ok": error_count == 0,
        "error_count": error_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def grade_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return grade_text(handle.read(), path)


def format_text_report(report: dict) -> str:
    """Stable, timestamp-free text rendering of a report."""

    width = max(len("%s %s" % (c["check_id"], c["title"])) for c in report["checks"])
    lines = [
        "Idea Dossier structural report — Tier-1 (offline, deterministic)",
        "file: %s" % (report.get("path") or "<stdin>"),
        "grader: structural.py v%s — %d checks (%d error-severity, %d warning-severity)"
        % (
            report["grader_version"],
            len(report["checks"]),
            sum(1 for c in report["checks"] if c["severity"] == "error"),
            sum(1 for c in report["checks"] if c["severity"] == "warning"),
        ),
        "",
    ]
    for check in report["checks"]:
        label = ("%s %s" % (check["check_id"], check["title"])).ljust(width)
        marker = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "skip": "SKIP"}[check["status"]]
        lines.append(
            "%s  %s  (%s)  %s" % (marker, label, check["severity"], check["note"])
        )
        for finding in check["findings"]:
            location = "line %d" % finding["line"] if finding["line"] else "line -"
            lines.append("        %-9s %s" % (location, finding["message"]))
    statuses = [c["status"] for c in report["checks"]]
    lines.append("")
    lines.append(
        "summary: %d checks | %d pass, %d fail, %d warn, %d skip | %d error(s), %d warning(s) | RESULT: %s"
        % (
            len(statuses),
            statuses.count("pass"),
            statuses.count("fail"),
            statuses.count("warn"),
            statuses.count("skip"),
            report["error_count"],
            report["warning_count"],
            "PASS" if report["ok"] else "FAIL",
        )
    )
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Tier-1 structural grader for one Idea Dossier Markdown file.")
    parser.add_argument("path", help="path to a produced dossier Markdown file")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        report = grade_file(args.path)
    except OSError as exc:
        print("error: cannot read %s: %s" % (args.path, exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_text_report(report))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
