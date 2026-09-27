#!/usr/bin/env python3
"""Generate the two Tier-1 fixtures from the shipped Idea Dossier template.

    python3 evals/fixtures/make_fixtures.py            # write both fixtures
    python3 evals/fixtures/make_fixtures.py --check    # fail if they are stale

The generator walks ``skills/time-series-model-ideation/assets/idea-dossier-template.md``
section by section: section order and titles, field names, table columns and
enum alternatives all come from the template, and only the *values* come from
the CONTENT table below.  Every ``{{REQUIRED: A | B | C}}`` with alternatives
falls back to its first alternative, and the lifecycle comes from LIFECYCLE.

* ``good-dossier.md``  — a coherent COMPILATION-phase dossier that ends in
  NEED-EVIDENCE.  It must produce zero Tier-1 errors.
* ``bad-dossier.md``   — the same dossier with the defects listed in the HTML
  comment at the top of the file, each tied to the check id it must trigger.

If the template changes, this script either fails loudly (a field it does not
know about appears in a materialised section) or regenerates cleanly.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "skills" / "time-series-model-ideation" / "assets" / "idea-dossier-template.md"
FIXTURES_DIR = REPO_ROOT / "evals" / "fixtures"
GOOD_PATH = FIXTURES_DIR / "good-dossier.md"
BAD_PATH = FIXTURES_DIR / "bad-dossier.md"

SECTION_HEADING_RE = re.compile(r"^##\s+(\d{1,3})\.\s*(.*?)\s*$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")
PLACEHOLDER_RE = re.compile(r"\{\{REQUIRED\s*:?\s*(.*?)\}\}")
COMMENT_OPEN = "<!--"
COMMENT_CLOSE = "-->"

# Sections entered in the good fixture.  Everything else is NOT-STARTED, which
# is the SKILL.md contract for a dossier that enters COMPILATION early with an
# unresolved diagnosis (sections 15 and 16 may be compiled from existing IDs).
LIFECYCLE: Dict[int, str] = {
    0: "COMPLETE",
    1: "COMPLETE",
    2: "COMPLETE",
    3: "COMPLETE",
    4: "COMPLETE",
    5: "COMPLETE",
    6: "COMPLETE",
    7: "NOT-STARTED",
    8: "NOT-STARTED",
    9: "NOT-STARTED",
    10: "NOT-STARTED",
    11: "NOT-STARTED",
    12: "NOT-STARTED",
    13: "COMPLETE",
    14: "COMPLETE",
    15: "COMPLETE",
    16: "COMPLETE",
}

STATUS_REASON: Dict[int, str] = {
    0: "Control fields completed at Stage 0 and updated when COMPILATION was entered.",
    1: "Boundary recorded from the supplied request; no downstream work is assumed.",
    2: "Need stated without a preferred method name.",
    3: "Claim ledger typed and kept current as the diagnosis stayed unresolved.",
    4: "Failure localised from the supplied narrative; no direct diagnostic has been run.",
    5: "Causal link and two rival explanations recorded; all remain unresolved.",
    6: "Invariant derived from the deployment regime and stated with its measurement plan.",
    7: "Not entered: G2 to G4 are unresolved, so no candidate may be designed yet.",
    8: "Not entered: direct-use assessment requires a frozen candidate.",
    9: "Not entered: adaptation requires a Stage-6 disposition.",
    10: "Not entered: the novelty audit requires a frozen candidate or system.",
    11: "Not entered: feasibility requires a trainable candidate or system.",
    12: "Not entered: no theory-relevant subject exists before candidate freeze.",
    13: "Diagnostic and rival-discriminating experiments recorded as plans; no result exists.",
    14: "Research argument compiled from existing IDs only.",
    15: "Stage-gate summary compiled from the recorded evidence boundary.",
    16: "One decision compiled from the gate table and the typed ledger.",
}

# --------------------------------------------------------------------------
# CONTENT: values keyed by YAML field name or table column header.
# A list value fills consecutive rows of a repeating table.
# --------------------------------------------------------------------------

CONTENT: Dict[int, Dict[str, Union[str, List[str]]]] = {
    0: {
        "task": "causal multivariate forecasting for an industrial sensor fleet",
        "data_regime": "regularly sampled 1-minute multivariate sensor channels, 96-step horizon, block missingness from sensor outages, single 24 GB GPU, no future covariates",
        "evaluation_target": "horizon-specific error on affected channels inside historically observed outage windows, reported separately from aggregate error",
        "scope_exclusions": "implementation, code, paper prose, figures, and any claim of superiority over existing normalization or forecasting methods",
        "date": "2026-05-02",
        "evidence_cutoff": "2026-05-01",
        "entry_mode": "GENERATE",
        "current_phase": "COMPILATION",
        "dossier_schema_version": "1.1.0",
    },
    1: {
        "user_request": "Design a research idea for causal sensor forecasting in which long contiguous outages are underrepresented in the training windows.",
        "intended_contribution": "candidate contribution category: training-exposure correction for the state update (success is not assumed)",
        "supplied_evidence": "USER-SUPPLIED request narrative only; no measurement, ablation, or causal evidence was supplied",
        "task_constraints": "past observations only (no future covariates); single 24 GB GPU; 1-minute sampling; 96-step horizon; evaluation stays on the natural missingness distribution",
        "unknowns": "whether the symptom has ever been measured; whether a maintenance regime confounds outage windows; whether model capacity explains the effect",
        "out_of_scope": "implementation, code, paper prose, figures, and any claim about a specific architecture family",
    },
    2: {
        "task_objective": "forecast the multivariate sensor state 96 steps ahead under the deployment missingness regime",
        "operating_regime": "regular 1-minute sampling with occasional contiguous multi-minute outages in individual channels",
        "current_limitation": "training windows are drawn from clean periods, so rare contiguous outages are underrepresented in the training exposure",
        "measurable_consequence": "horizon-specific error on affected channels inside outage windows, reported separately from aggregate error",
        "solution_independent_need": "reduce horizon-specific error on affected channels under the natural outage regime without changing causal information access",
        "method_names_removed_check": "PASS",
        "claim_boundary": "the need does not imply that any specific correction, architecture, or training scheme will work",
        "related_claim_ids": "CLM-001, CLM-002",
    },
    3: {
        "Claim ID": [
            "CLM-001",
            "CLM-002",
            "CLM-003",
            "CLM-004",
            "CLM-005",
            "CLM-006",
            "CLM-007",
            "CLM-008",
            "CLM-009",
        ],
        "Claim type": [
            "OBSERVATION",
            "HYPOTHESIS",
            "MECHANISM",
            "ASSUMPTION",
            "EXPLANATION",
            "HYPOTHESIS",
            "HYPOTHESIS",
            "EXPLANATION",
            "HYPOTHESIS",
        ],
        "Centrality": [
            "CORE",
            "CORE",
            "SUPPORTING",
            "SUPPORTING",
            "SUPPORTING",
            "SUPPORTING",
            "SUPPORTING",
            "SUPPORTING",
            "SUPPORTING",
        ],
        "Statement": [
            "Horizon-specific error inflates on affected channels during contiguous outages in the natural regime.",
            "Underexposure to historically observed outage masks during training causes the brittle state update.",
            "Contiguous outages push the state update into an operating regime that clean training windows never exercise.",
            "Historically observed outage masks represent the deployment missingness regime.",
            "Rival A: affected channels are dominated by a maintenance regime shift that coincides with outage windows.",
            "Stable causal dependency locality under single-sensor dropout is task-relevant for this regime.",
            "The symptom persists when the maintenance regime is held fixed.",
            "Rival B: the symptom is explained by insufficient capacity or receptive-field size rather than mask underexposure.",
            "A capacity-matched wider forecaster leaves the symptom unchanged.",
        ],
        "Provenance": [
            "USER-SUPPLIED",
            "INFERENCE",
            "INFERENCE",
            "NONE",
            "USER-SUPPLIED",
            "INFERENCE",
            "INFERENCE",
            "USER-SUPPLIED",
            "INFERENCE",
        ],
        "Source refs": [
            "USER-SUPPLIED request narrative, 2026-04-28; no measurement recorded",
            "N/A - inferred from the supplied narrative, not measured",
            "N/A - mechanism stated but not measured",
            "N/A - assumption; no source recorded",
            "USER-SUPPLIED request narrative, 2026-04-28",
            "N/A - justified from the deployment regime, not measured",
            "N/A - discriminating prediction, not measured",
            "USER-SUPPLIED request narrative, 2026-04-28",
            "N/A - discriminating prediction, not measured",
        ],
        "Evidence strength": ["E1", "E1", "E1", "E0", "E0", "E1", "E1", "E0", "E1"],
        "Supports IDs": [
            "N/A - nothing is supported yet",
            "CLM-003",
            "N/A - no supported claim depends on it yet",
            "N/A - assumption only",
            "N/A - rival explanation",
            "N/A - invariant justification",
            "N/A - discriminating prediction",
            "N/A - rival explanation",
            "N/A - discriminating prediction",
        ],
        "Contradicts IDs": [
            "N/A - no contradicting claim recorded",
            "CLM-005, CLM-008",
            "N/A - no contradicting claim recorded",
            "N/A - no contradicting claim recorded",
            "CLM-002",
            "N/A - no contradicting claim recorded",
            "CLM-005",
            "CLM-002",
            "CLM-008",
        ],
        "Status": [
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
        ],
        "Decision impact": [
            "Blocks G2 until a direct diagnostic exists",
            "Decisive for G2 and G3",
            "Feeds EXP-001 and EXP-003",
            "Named as the highest-risk assumption",
            "Rival A in the section 5.2 comparison",
            "Justifies INV-001",
            "Discriminates RIV-001",
            "Rival B in the section 5.2 comparison",
            "Discriminates RIV-002",
        ],
    },
    4: {
        "failure_class": "INFORMATION - the training exposure omits an operating regime that is present at deployment",
        "operation_under_examination": "construction of training windows from clean periods only",
        "affected_object_or_process": "the state update of the forecasting estimator",
        "observable_symptom": "horizon-specific error inflation on affected channels during contiguous outages, described without a causal explanation",
        "condition": "outages of six or more consecutive minutes in the natural regime distribution",
        "diagnostic_measurement": "channel-level error decomposition restricted to outage windows and compared against clean windows",
        "measured_effect": "UNRESOLVED - no direct diagnostic has been run; EXP-001 will measure it",
        "intermediate_effects": "N/A - no intermediate measurement recorded",
        "task_level_effect": "unresolved - no task-level measurement recorded",
        "downstream_consequence": "unresolved - no downstream measurement recorded",
        "related_claim_ids": "CLM-001, CLM-003",
    },
    5: {
        "Link ID": "LINK-001",
        "From claim ID": "CLM-002",
        "Relation": "causes (one adjacent causal step)",
        "To claim ID": "CLM-001",
        "Supporting claim IDs": "CLM-003",
        "Contradicting claim IDs": "N/A - no contradicting claim recorded",
        "Status": "UNRESOLVED",
        "Rival ID": ["RIV-001", "RIV-002"],
        "Explanation claim ID": ["CLM-005", "CLM-008"],
        "Shared prediction": [
            "affected channels show inflated outage-window error",
            "the symptom appears with capacity-matched baselines",
        ],
        "Discriminating prediction claim ID": ["CLM-007", "CLM-009"],
        "Planned experiment ID": ["EXP-002", "EXP-002"],
    },
    6: {
        "property": "unchanged causal information access with evaluation on the natural missingness regime distribution",
        "preservation_type": "TASK-RELEVANT",
        "measurement": "report outage-window error separately from aggregate error while auditing future-observation access in both paths",
        "tolerance": "exact: zero future-observation access; the outage-window gap is reported rather than thresholded",
        "task_relevance": "the invariant is what makes the diagnosis attributable to training exposure rather than to changed information access (justified, not yet evidenced)",
        "unnecessary_or_harmful_conditions": "N/A - no exact reconstruction or invertibility requirement is imposed",
        "related_claim_ids": "CLM-006",
    },
    13: {
        "Experiment ID": ["EXP-001", "EXP-002", "EXP-003"],
        "Assessment subject IDs": [
            "NEED-001, FAIL-001",
            "FAIL-001, LINK-001",
            "INV-001, NEED-001",
        ],
        "Claim IDs": [
            "CLM-001, CLM-002",
            "CLM-005, CLM-007, CLM-008, CLM-009",
            "CLM-006",
        ],
        "Test/intervention": [
            "direct diagnostic: train two matched forecasters, one on clean windows only and one on a clean/corrupted mixture built from historically observed outage masks, and compare channel-level outage-window error",
            "rival-discriminating intervention: repeat EXP-001 while holding the maintenance regime fixed and while matching parameter count and receptive field",
            "invariant measurement: report outage-window error next to an explicit audit of future-observation access in the training and inference paths",
        ],
        "Status": ["PLANNED", "PLANNED", "PLANNED"],
        "Expected result": [
            "outage-window error falls on affected channels while aggregate error is unchanged",
            "the mask effect survives the maintenance holdout and the capacity match",
            "information access stays past-only and the outage-window gap is reported separately",
        ],
        "Falsifying result": [
            "outage-window error is unchanged or worsens",
            "the effect disappears once the maintenance regime or the capacity is controlled",
            "any future observation enters either path, or the gap cannot be separated from aggregate error",
        ],
        "Observed result": [
            "PENDING - planned; a plan is not evidence",
            "PENDING - planned; a plan is not evidence",
            "PENDING - planned; a plan is not evidence",
        ],
        "Result source refs": [
            "PENDING - no run recorded",
            "PENDING - no run recorded",
            "PENDING - no run recorded",
        ],
        "Rival explanation claim IDs": [
            "CLM-005, CLM-008",
            "CLM-005, CLM-008",
            "N/A - no rival claim recorded for the invariant",
        ],
        "Ablation": [
            "N/A - no candidate component exists before candidate freeze",
            "N/A - no candidate component exists before candidate freeze",
            "N/A - no candidate component exists before candidate freeze",
        ],
        "Fairest simple baseline": [
            "unchanged forecaster trained on clean windows only",
            "capacity-matched wider forecaster trained on clean windows",
            "unchanged forecaster trained on clean windows only",
        ],
        "What the result cannot prove": [
            "it cannot separate the mask effect from the maintenance regime or from capacity on its own",
            "it cannot establish the mechanism, only exclude the two named rivals",
            "it cannot show that the invariant is sufficient for the task, only that it was preserved",
        ],
        "Decision change if falsified": [
            "G2 stays UNRESOLVED and the decision remains NEED-EVIDENCE",
            "RIV-001 or RIV-002 survives and the diagnosis returns to Stage 2",
            "G4 stays UNRESOLVED and the decision remains NEED-EVIDENCE",
        ],
        "core_claim_ids": "CLM-001, CLM-002",
        "covered_core_claim_ids": "CLM-001, CLM-002",
        "uncovered_core_claim_ids": "N/A - every CORE claim has a planned falsifier",
        "coverage_complete": "YES",
    },
    14: {
        "Compiled statement": [
            "Causal sensor forecasting loses horizon-specific accuracy on affected channels during contiguous outages because the training windows omit that regime.",
            "FAIL-001 records the symptom without a causal explanation; no direct diagnostic has been run.",
            "LINK-001 states that training-exposure underexposure causes the brittle state update; it is UNRESOLVED, not supported.",
            "INV-001 preserves unchanged causal information access and evaluation on the natural missingness regime.",
            "N/A - no candidate has been frozen; Stage 5 was not entered while G2 to G4 remain unresolved.",
            "N/A - Stage 6 was not entered; section 8 is NOT-STARTED.",
            "N/A - Stage 7 was not entered; section 9 is NOT-STARTED.",
            "N/A - the novelty audit was not entered; section 10 is NOT-STARTED.",
            "N/A - no trainable subject exists; section 11 is NOT-STARTED.",
            "N/A - no theory-relevant subject exists; section 12 is NOT-STARTED.",
            "EXP-001 is the smallest measurement that can change the decision, and its observed result is still PENDING.",
        ],
        "Source IDs": [
            "NEED-001, FAIL-001, CLM-001",
            "FAIL-001, CLM-001",
            "LINK-001, CLM-002, CLM-003",
            "INV-001, CLM-006",
            "N/A - no candidate record exists",
            "N/A - section 8 not started",
            "N/A - section 9 not started",
            "N/A - section 10 not started",
            "N/A - section 11 not started",
            "N/A - section 12 not started",
            "EXP-001, CLM-001, CLM-002",
        ],
    },
    15: {
        "Evaluation status": [
            "EVALUATED",
            "EVALUATED",
            "EVALUATED",
            "EVALUATED",
            "EVALUATED",
            "DEFERRED",
            "DEFERRED",
            "DEFERRED",
            "DEFERRED",
            "DEFERRED",
            "DEFERRED",
            "DEFERRED",
        ],
        "State": [
            "SATISFIED",
            "SATISFIED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
            "UNRESOLVED",
        ],
        "Failure mode": ["null"] * 12,
        "Decisive ledger IDs": [
            "NEED-001, CLM-001",
            "NEED-001, CLM-002",
            "FAIL-001, CLM-001",
            "LINK-001, CLM-002",
            "INV-001, CLM-006",
            "N/A - no candidate exists",
            "N/A - no candidate exists",
            "N/A - no candidate exists",
            "N/A - no frozen subject exists",
            "N/A - no trainable subject exists",
            "N/A - no theory-relevant claim exists",
            "CLM-001, CLM-002",
        ],
        "Blocking item": [
            "N/A - no blocker",
            "N/A - no blocker",
            "no direct diagnostic has been run; EXP-001 is planned",
            "the rival-discriminating intervention EXP-002 is planned, not run",
            "the invariant measurement EXP-003 is planned, not run",
            "G2 to G4 are unresolved; Stage 5 was not entered",
            "Stage 6 depends on frozen candidates",
            "Stage 7 depends on Stage-6 dispositions",
            "Stage 8 depends on a frozen candidate or system",
            "Stage 9 depends on a frozen candidate or system",
            "Stage 10 depends on a frozen candidate or system",
            "diagnostic falsifiers are planned but not run (EXP-001 to EXP-003)",
        ],
        "Earliest return stage": [
            "N/A - no return required",
            "N/A - no return required",
            "Stage 2",
            "Stage 3",
            "Stage 4",
            "Stage 5",
            "Stage 5",
            "Stage 5",
            "Stage 5",
            "Stage 5",
            "Stage 5",
            "Stage 2",
        ],
    },
    16: {
        "decision": "NEED-EVIDENCE",
        "decision_subject_type": "DOSSIER",
        "decision_subject_id": "DOS-001",
        "decisive_ledger_ids": "CLM-001, CLM-002",
        "highest_risk_assumption_claim_id": "CLM-004",
        "smallest_next_action": "run EXP-001, the matched mask-injection diagnostic that reports outage-window error separately from aggregate error",
        "stage_to_revisit": "Stage 2",
        "reusable_observation_claim_ids": "CLM-005, CLM-008",
        "decision_rationale": "The need and boundary are stable, but the failure has no direct diagnostic, the causal link is untested, and the invariant is unmeasured; G2 to G11 are unresolved, so no candidate, novelty, feasibility, or theory work is justified yet.",
        "unresolved_gate_ids": "G2, G3, G4, G5, G6, G7, G8, G9, G10, G11",
        "repairable_gate_ids": "N/A - no gate is UNSATISFIED",
        "contradicted_gate_ids": "N/A - no decisive contradiction is recorded",
        "decision_rule_triggered": "UNRESOLVED-EVIDENCE",
        "decision_consistency_check": "PASS",
    },
}


# --------------------------------------------------------------------------
# Template parsing
# --------------------------------------------------------------------------


@dataclass
class YamlBlock:
    entries: List[Tuple[str, str]]


@dataclass
class CodeBlock:
    language: str
    lines: List[str]


@dataclass
class TableBlock:
    headers: List[str]
    rows: List[List[str]]


@dataclass
class ProseBlock:
    lines: List[str]


Element = Union[YamlBlock, CodeBlock, TableBlock, ProseBlock]


@dataclass
class TemplateSection:
    number: int
    title: str
    elements: List[Element] = field(default_factory=list)


class MissingContent(Exception):
    pass


def _strip_comments(lines: Sequence[str]) -> List[str]:
    """Remove HTML comments, keeping line structure."""

    out: List[str] = []
    in_comment = False
    for line in lines:
        kept = []
        cursor = 0
        while cursor < len(line):
            if in_comment:
                end = line.find(COMMENT_CLOSE, cursor)
                if end == -1:
                    cursor = len(line)
                else:
                    in_comment = False
                    cursor = end + len(COMMENT_CLOSE)
                continue
            start = line.find(COMMENT_OPEN, cursor)
            if start == -1:
                kept.append(line[cursor:])
                break
            kept.append(line[cursor:start])
            in_comment = True
            cursor = start + len(COMMENT_OPEN)
        out.append("".join(kept).rstrip())
    return out


def _split_row(text: str) -> List[str]:
    body = text.strip().replace("\\|", "\x00")
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.replace("\x00", "|").strip() for cell in body.split("|")]


def _is_separator(cells: Sequence[str]) -> bool:
    return bool(cells) and all(SEPARATOR_CELL_RE.match(cell) for cell in cells)


def parse_template(text: str) -> Tuple[List[str], List[TemplateSection]]:
    lines = _strip_comments(text.split("\n"))
    preamble: List[str] = []
    sections: List[TemplateSection] = []
    current: Optional[TemplateSection] = None

    index = 0
    while index < len(lines):
        line = lines[index]
        heading = SECTION_HEADING_RE.match(line)
        if heading:
            current = TemplateSection(number=int(heading.group(1)), title=heading.group(2))
            sections.append(current)
            index += 1
            continue

        if current is None:
            preamble.append(line)
            index += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            language = fence.group(2) or "text"
            body: List[str] = []
            index += 1
            while index < len(lines) and not FENCE_RE.match(lines[index]):
                body.append(lines[index])
                index += 1
            index += 1  # closing fence
            if language == "yaml":
                entries: List[Tuple[str, str]] = []
                for body_line in body:
                    m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$", body_line)
                    if m:
                        entries.append((m.group(1), m.group(2)))
                current.elements.append(YamlBlock(entries=entries))
            else:
                current.elements.append(CodeBlock(language=language, lines=body))
            continue

        if TABLE_ROW_RE.match(line) and index + 1 < len(lines) and TABLE_ROW_RE.match(lines[index + 1]):
            if _is_separator(_split_row(lines[index + 1])):
                headers = _split_row(line)
                rows: List[List[str]] = []
                index += 2
                while index < len(lines) and TABLE_ROW_RE.match(lines[index]):
                    cells = _split_row(lines[index])
                    if _is_separator(cells):
                        break
                    rows.append(cells)
                    index += 1
                current.elements.append(TableBlock(headers=headers, rows=rows))
                continue

        # plain prose: accumulate until the next structural element
        chunk: List[str] = []
        while index < len(lines):
            candidate = lines[index]
            if SECTION_HEADING_RE.match(candidate) or FENCE_RE.match(candidate):
                break
            if TABLE_ROW_RE.match(candidate) and index + 1 < len(lines) and TABLE_ROW_RE.match(lines[index + 1]):
                if _is_separator(_split_row(lines[index + 1])):
                    break
            chunk.append(candidate)
            index += 1
        current.elements.append(ProseBlock(lines=chunk))

    return preamble, sections


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def _spec_of(cell: str) -> Optional[str]:
    match = PLACEHOLDER_RE.search(cell)
    if not match:
        return None
    return match.group(1).strip()


def _first_alternative(spec: str) -> Optional[str]:
    if "|" not in spec:
        return None
    return spec.split("|")[0].strip()


def resolve_value(section: int, field_name: str, spec: str) -> str:
    table = CONTENT.get(section, {})
    if field_name in table:
        value = table[field_name]
        if isinstance(value, list):  # caller must expand lists; single value fallback
            value = value[0]
        return str(value)
    alternative = _first_alternative(spec)
    if alternative is not None:
        return alternative
    raise MissingContent(
        "section %d field '%s' (placeholder: {{REQUIRED: %s}}) has no CONTENT entry" % (section, field_name, spec)
    )


def render_yaml(section: int, block: YamlBlock, status: str) -> List[str]:
    """Resolve a fenced YAML block, keeping literal (non-placeholder) entries as written."""

    out: List[str] = ["```yaml"]
    for key, raw in block.entries:
        spec = _spec_of(raw)
        if key == "section_status":
            out.append('%s: "%s"' % (key, status))
        elif key == "status_reason":
            out.append('%s: "%s"' % (key, STATUS_REASON[section]))
        elif spec is None:
            out.append("%s: %s" % (key, raw.strip()))
        else:
            out.append('%s: "%s"' % (key, resolve_value(section, key, spec)))
    out.append("```")
    return out


def render_table(section: int, block: TableBlock) -> List[str]:
    """Resolve a Markdown table; placeholder cells live in data rows, not headers."""

    table_content = CONTENT.get(section, {})
    # A column is fillable when its template cell carries a placeholder OR when
    # CONTENT supplies a value for that column header.  The second case matters
    # because the template hardcodes the first record ID of several tables
    # (| CLM-001 |, | EXP-001 |, | RIV-001 |, ...) which must be replaced when a
    # table is expanded to several rows.
    column_specs: Dict[int, str] = {}
    template_row = block.rows[0]
    for col_index, header in enumerate(block.headers):
        spec = _spec_of(template_row[col_index]) if col_index < len(template_row) else None
        if spec is None and header in table_content:
            spec = ""
        if spec is not None:
            column_specs[col_index] = spec

    row_count: Optional[int] = None
    for idx, spec in column_specs.items():
        value = table_content.get(block.headers[idx])
        if isinstance(value, list):
            if row_count is None or len(value) > row_count:
                row_count = len(value)
    template_rows = len(block.rows)
    if row_count is None:
        row_count = template_rows
    if template_rows > 1 and row_count != template_rows:
        raise MissingContent(
            "section %d table %s has %d template rows but CONTENT supplies %d"
            % (section, block.headers[0], template_rows, row_count)
        )

    out: List[str] = [
        "| " + " | ".join(block.headers) + " |",
        "|" + "|".join(["---"] * len(block.headers)) + "|",
    ]
    for row_index in range(row_count):
        template_row = block.rows[row_index] if template_rows > 1 else block.rows[0]
        cells: List[str] = []
        for col_index, raw_cell in enumerate(template_row):
            spec = column_specs.get(col_index)
            if spec is None:
                cells.append(raw_cell)
                continue
            header = block.headers[col_index]
            value = table_content.get(header)
            if isinstance(value, list):
                resolved = str(value[row_index] if row_index < len(value) else value[-1])
            elif value is not None:
                resolved = str(value)
            else:
                resolved = resolve_value(section, header, spec)
            if "|" in resolved or "{{" in resolved:
                raise ValueError(
                    "section %d column %s value must not contain '|' or a placeholder: %r"
                    % (section, header, resolved[:80])
                )
            cells.append(resolved)
        out.append("| " + " | ".join(cells) + " |")
    return out


def render_section(section: TemplateSection) -> List[str]:
    status = LIFECYCLE[section.number]
    heading = "## %d. %s" % (section.number, section.title)
    if status in ("NOT-STARTED", "BLOCKED"):
        return [
            heading,
            "",
            "```yaml",
            'section_status: "%s"' % status,
            'status_reason: "%s"' % STATUS_REASON[section.number],
            "```",
        ]

    lines: List[str] = [heading, ""]
    lifecycle_written = False
    for element in section.elements:
        if isinstance(element, YamlBlock):
            is_lifecycle = any(key == "section_status" for key, _ in element.entries)
            if is_lifecycle and lifecycle_written:
                continue
            lines.extend(render_yaml(section.number, element, status))
            if is_lifecycle:
                lifecycle_written = True
            lines.append("")
        elif isinstance(element, CodeBlock):
            lines.append("```%s" % element.language)
            lines.extend(element.lines)
            lines.append("```")
            lines.append("")
        elif isinstance(element, TableBlock):
            lines.extend(render_table(section.number, element))
            lines.append("")
        else:  # ProseBlock
            lines.extend(element.lines)
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def render_dossier(preamble: List[str], sections: List[TemplateSection]) -> str:
    out: List[str] = list(preamble)
    while out and out[-1] == "":
        out.pop()
    for section in sections:
        out.append("")
        out.extend(render_section(section))
    return "\n".join(out).rstrip() + "\n"


GOOD_BANNER = """\
<!--
FIXTURE: good-dossier.md -- SYNTHETIC, generated by evals/fixtures/make_fixtures.py from
skills/time-series-model-ideation/assets/idea-dossier-template.md.

Every value below is invented sample prose: no real research claims, no real citations,
no real measurements. The fixture exists only to exercise the Tier-1 structural grader.
Regenerate with:  python3 evals/fixtures/make_fixtures.py
-->"""


# --------------------------------------------------------------------------
# Defect injection for the bad fixture
# --------------------------------------------------------------------------


@dataclass
class Defect:
    check_id: str
    description: str
    apply: object  # Callable[[List[List[str]]], None]


def _block_number(heading: str) -> Optional[int]:
    match = SECTION_HEADING_RE.match(heading)
    return int(match.group(1)) if match else None


class Rendered:
    """A rendered dossier split back into (heading, body) blocks for injection."""

    def __init__(self, preamble: List[str], blocks: List[Tuple[str, List[str]]]) -> None:
        self.preamble = preamble
        self.blocks = blocks

    @classmethod
    def from_text(cls, text: str) -> "Rendered":
        lines = text.split("\n")
        preamble: List[str] = []
        blocks: List[Tuple[str, List[str]]] = []
        current: Optional[List[str]] = None
        for line in lines:
            if SECTION_HEADING_RE.match(line):
                current = []
                blocks.append((line, current))
                continue
            if current is None:
                preamble.append(line)
            else:
                current.append(line)
        # trim the blank separator lines that the renderer added before each heading
        for _heading, body in blocks:
            while body and body[0] == "":
                body.pop(0)
            while body and body[-1] == "":
                body.pop()
        while preamble and preamble[-1] == "":
            preamble.pop()
        return cls(preamble, blocks)

    def block(self, number: int) -> List[str]:
        for heading, body in self.blocks:
            if _block_number(heading) == number:
                return body
        raise KeyError("no rendered block for section %d" % number)

    def heading_of(self, number: int) -> str:
        for heading, _body in self.blocks:
            if _block_number(heading) == number:
                return heading
        raise KeyError("no rendered block for section %d" % number)

    def set_yaml(self, number: int, key: str, value: str, occurrence: int = 1) -> None:
        body = self.block(number)
        seen = 0
        for index, line in enumerate(body):
            if re.match(r"^\s*%s\s*:" % re.escape(key), line):
                seen += 1
                if seen == occurrence:
                    body[index] = '%s: "%s"' % (key, value)
                    return
        raise KeyError("section %d has no yaml field %s" % (number, key))

    def append(self, number: int, lines: Sequence[str]) -> None:
        self.block(number).extend(lines)

    def row_index(self, number: int, first_cell: str) -> int:
        body = self.block(number)
        for index, line in enumerate(body):
            if TABLE_ROW_RE.match(line):
                label = _split_row(line)[0]
                if label == first_cell or label.startswith(first_cell + " "):
                    return index
        raise KeyError("section %d has no row starting with %r" % (number, first_cell))

    def drop_row(self, number: int, first_cell: str) -> None:
        del self.block(number)[self.row_index(number, first_cell)]

    def set_cell(self, number: int, first_cell: str, column: int, value: str) -> None:
        body = self.block(number)
        index = self.row_index(number, first_cell)
        cells = _split_row(body[index])
        cells[column] = value
        body[index] = "| " + " | ".join(cells) + " |"

    def to_text(self) -> str:
        out: List[str] = list(self.preamble)
        for heading, body in self.blocks:
            if not heading and not body:
                continue  # a defect removed this section entirely
            out.append("")
            out.append(heading)
            out.extend(body)
        return "\n".join(out).rstrip() + "\n"


def _defect_s01(rendered: Rendered) -> None:
    """Drop section 12 entirely: heading and lifecycle block are absent.

    Removing only the heading would orphan the lifecycle block into section 11
    and make S05 report a second, unrelated violation, so the whole section goes.
    """

    for index, (heading, _body) in enumerate(rendered.blocks):
        if _block_number(heading) == 12:
            rendered.blocks[index] = ("", [])
            return
    raise KeyError("section 12 not found")


def _defect_s02(rendered: Rendered) -> None:
    positions = {}
    for index, (heading, _body) in enumerate(rendered.blocks):
        number = _block_number(heading)
        if number is not None:
            positions[number] = index
    i, j = positions[4], positions[5]
    rendered.blocks[i], rendered.blocks[j] = rendered.blocks[j], rendered.blocks[i]


def _defect_s03(rendered: Rendered) -> None:
    rendered.append(
        2,
        [
            "",
            "- Unresolved work left in the body: {{REQUIRED: the smallest next measurement}}",
        ],
    )


def _defect_s04(rendered: Rendered) -> None:
    rendered.set_yaml(6, "section_status", "DONE")


def _defect_s05(rendered: Rendered) -> None:
    rendered.append(
        8,
        [
            "",
            "| FIND-001 | CAND-001 | FAILURE | A finding instantiated although the section is NOT-STARTED | CLM-001 | ADAPT | Adds a component before Stage 6 |",
        ],
    )
    rendered.set_yaml(9, "section_status", "ACTIVE")


def _defect_s06(rendered: Rendered) -> None:
    rendered.append(1, ["", "- Cross-reference: see REF-042 for the missing dependency."])


def _defect_s07(rendered: Rendered) -> None:
    rendered.append(
        16,
        [
            "",
            '- Reported as "novelty: 9/10" with an additional novelty score 0.8 and an aggregate gate score: 7.',
        ],
    )


def _defect_s08(rendered: Rendered) -> None:
    """A second decision field, outside the canonical enum, next to the compiled one."""

    rendered.append(16, ['decision: "MAYBE"'])


def _defect_s09(rendered: Rendered) -> None:
    rendered.set_yaml(16, "decision_consistency_check", "FAIL")


def _defect_s10(rendered: Rendered) -> None:
    # G11 stays in place so the S18 defect can put it in contradiction with the
    # section 13 coverage state.
    rendered.drop_row(15, "G10")
    rendered.set_cell(15, "G5", 2, "")  # blank state cell
    rendered.set_cell(15, "G6", 1, "DEFERRED")
    rendered.set_cell(15, "G6", 2, "SATISFIED")  # deferred gate pretending to be evaluated


def _defect_s11(rendered: Rendered) -> None:
    """One row whose evidence strength is off the E0-E5 scale; the type and status stay legal."""

    rendered.append(
        3,
        [
            "| CLM-777 | HYPOTHESIS | SUPPORTING | A claim whose evidence strength sits outside the scale | INFERENCE | N/A | E7 | N/A | N/A | UNRESOLVED | N/A |",
        ],
    )


def _defect_s12(rendered: Rendered) -> None:
    """One row with an invented Claim type and Status; the evidence level stays legal."""

    rendered.append(
        3,
        [
            "| CLM-779 | OPINION | CORE | A claim with an invented type and status | NONE | N/A | E0 | N/A | N/A | MAYBE | N/A |",
        ],
    )


def _defect_s13(rendered: Rendered) -> None:
    rendered.set_yaml(0, "current_phase", "DIAGNOSIS")


def _defect_s14(rendered: Rendered) -> None:
    rendered.append(
        3,
        [
            "| CLM-778 | EVIDENCE | CORE | The planned diagnostic already proves the mechanism | DIRECT-MEASUREMENT | PENDING - EXP-004 planned | E3 | EXP-004 | N/A | SUPPORTED | Pivot straight to repair |",
        ],
    )


def _defect_s15(rendered: Rendered) -> None:
    rendered.set_yaml(16, "decisive_ledger_ids", "CLM-001, CLM-999")
    rendered.append(16, ['smallest_next_action_detail: "run EXP-404 next"'])


def _defect_s18(rendered: Rendered) -> None:
    """Schema 1.1.0 gate semantics: incomplete coverage while G11 is satisfied and GO is decided."""

    rendered.set_yaml(13, "covered_core_claim_ids", "CLM-001")
    rendered.set_yaml(13, "uncovered_core_claim_ids", "CLM-002")
    rendered.set_yaml(13, "coverage_complete", "NO")
    rendered.set_yaml(16, "decision", "GO")  # the compiled decision field
    rendered.set_cell(15, "G11", 1, "EVALUATED")
    rendered.set_cell(15, "G11", 2, "SATISFIED")
    rendered.set_cell(15, "G11", 3, "null")


DEFECTS: Tuple[Defect, ...] = (
    Defect("S01", "section 12 (Theory Boundary) is absent: neither its heading nor its lifecycle block is emitted", _defect_s01),
    Defect("S02", "section blocks 4 and 5 emitted out of ascending order", _defect_s02),
    Defect("S03", "an unreplaced {{REQUIRED: ...}} placeholder left in section 2", _defect_s03),
    Defect("S04", "section 6 section_status set to 'DONE' instead of a canonical value", _defect_s04),
    Defect(
        "S05",
        "section 8 is NOT-STARTED but instantiates a FIND-001 row, and section 9 is ACTIVE with no body",
        _defect_s05,
    ),
    Defect("S06", "section 1 cites REF-042, a namespace the template does not permit", _defect_s06),
    Defect("S07", "section 16 reports a numeric novelty score and an aggregate gate score", _defect_s07),
    Defect("S08", "section 16 declares a second decision field 'MAYBE' outside the canonical enum", _defect_s08),
    Defect("S09", "section 16 sets decision_consistency_check to FAIL", _defect_s09),
    Defect("S10", "gate G10 removed, G5 has no state, G6 is DEFERRED yet SATISFIED", _defect_s10),
    Defect("S11", "a ledger row records evidence strength E7, outside E0-E5", _defect_s11),
    Defect(
        "S12",
        "a ledger row uses Claim type 'OPINION' and Status 'MAYBE' instead of the canonical sets",
        _defect_s12,
    ),
    Defect("S13", "current_phase says DIAGNOSIS while sections 9 and 13-16 are entered", _defect_s13),
    Defect("S14", "a SUPPORTED claim rests on a PENDING experiment, and plans are not evidence", _defect_s14),
    Defect("S15", "section 16 references CLM-999 and EXP-404, which are never defined in sections 0-13", _defect_s15),
    Defect(
        "S18",
        "section 13 reports coverage_complete: NO (CLM-002 uncovered) while G11 is SATISFIED and section 16 decides GO",
        _defect_s18,
    ),
)


def bad_banner() -> str:
    lines = [
        "<!--",
        "FIXTURE: bad-dossier.md -- SYNTHETIC, generated by evals/fixtures/make_fixtures.py.",
        "Derived from good-dossier.md by injecting the defects listed below. Every DEFECT line names",
        "the Tier-1 structural check that the injection must trigger; `python3 evals/run.py --self-test`",
        "fails when any listed check does not fire. This file is not a research artifact.",
        "",
    ]
    for defect in DEFECTS:
        lines.append("DEFECT: %s :: %s" % (defect.check_id, defect.description))
    lines.append("-->")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def build_good() -> str:
    template_text = TEMPLATE.read_text(encoding="utf-8")
    _preamble, sections = parse_template(template_text)
    numbers = [section.number for section in sections]
    if numbers != list(range(17)):
        raise SystemExit("template sections are not 0..16 in order: %s" % numbers)
    return render_dossier(GOOD_BANNER.split("\n"), sections)


def build_bad(good_text: str) -> str:
    template_text = TEMPLATE.read_text(encoding="utf-8")
    _preamble, sections = parse_template(template_text)
    rendered = Rendered.from_text(render_dossier(GOOD_BANNER.split("\n"), sections))
    for defect in DEFECTS:
        defect.apply(rendered)
    rendered.preamble = bad_banner().split("\n")
    return rendered.to_text()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the Tier-1 fixtures from the shipped dossier template.")
    parser.add_argument("--check", action="store_true", help="verify the checked-in fixtures are up to date")
    args = parser.parse_args(argv)

    good = build_good()
    bad = build_bad(good)

    if args.check:
        stale = []
        for path, expected in ((GOOD_PATH, good), (BAD_PATH, bad)):
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                stale.append(path.name)
        if stale:
            print("stale fixture(s): %s — run: python3 evals/fixtures/make_fixtures.py" % ", ".join(stale))
            return 1
        print("fixtures are up to date with %s" % TEMPLATE.relative_to(REPO_ROOT))
        return 0

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    GOOD_PATH.write_text(good, encoding="utf-8")
    BAD_PATH.write_text(bad, encoding="utf-8")
    print("wrote %s (%d lines)" % (GOOD_PATH.relative_to(REPO_ROOT), good.count("\n")))
    print("wrote %s (%d lines, %d documented defects)" % (BAD_PATH.relative_to(REPO_ROOT), bad.count("\n"), len(DEFECTS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
