# Theory Audit

Use this reference to execute Stage 10 on the same frozen subject assessed at Stage 9. Determine whether each theoretical claim is coherent, correctly bounded, and supported under assumptions that apply to the implemented subject. Do not use theory to establish empirical task performance, novelty, or feasibility.

## Contents

1. Entry and Theory Subjects
2. Theory-Claim Contract
3. Assumptions and Applicability
4. Theory Maturity and Formalization
5. Guarantees, Non-Guarantees, and Counterparts
6. Compile G10 and Route Repairs
7. Stage-Specific Anti-Patterns

## 1. Entry and Theory Subjects

Require a stable `CAND-*` or `SYS-*`, completed implementation contracts, every CORE mechanism and contribution claim, and the current data and operating regime. Keep G10 `DEFERRED` when unresolved upstream work may change the subject.

Use:

- `CAND-*` or `SYS-*` for system-level consistency and guarantees;
- `COMP-*` when a property belongs locally to an operator, constraint, projection, or decision head; and
- one separate overall G10 result for every final subject in `COMPARE`.

Invalidate dependent theory rows whenever the operator, composition, information access, responsibility, state transition, constraint, objective, or CORE contribution changes.

Stage 10 is mandatory even when no formal theorem is claimed. Require at least one theory-relevant CORE mechanism-consistency claim.

## 2. Theory-Claim Contract

Compile one internal contract for every theory-relevant `CLM-*`:

```text
Theory subject ID:
Theory claim ID and ledger centrality:
Theory role: CONSISTENCY | FORMAL-PROPERTY | LIMITATION
Exact statement and quantifiers:
Operating and mathematical scope:
Assumption CLM-* IDs:
Consistency conditions:
Theory maturity:
Formalization status:
Proof, derivation, or source mapping:
Guarantees:
Does not guarantee:
Weakest assumption:
Empirical or formal counterpart CLM-* IDs:
```

Use `CONSISTENCY` for the immediate mathematical or causal coherence of the implemented mechanism. Use `FORMAL-PROPERTY` for a bounded property such as stability, invertibility, legality, approximation, complexity, conservation, or identifiability. Use `LIMITATION` for a boundary, counterexample, impossibility, or non-guarantee.

Do not create a theorem row from an imprecise slogan. Define the object, metric, operator, conditions, and scope first.

## 3. Assumptions and Applicability

Represent material data, operator, representation, optimization, information-access, boundary, and sampling conditions as `ASSUMPTION` `CLM-*` rows. Distinguish assumptions needed by execution from assumptions needed only by a proof.

Keep two axes independent:

```text
theory maturity = how far the target claim is derived or proved
assumption applicability = whether its assumptions hold for this subject and regime
```

Compile applicability:

```text
any assumption CONTRADICTED -> CONTRADICTED
else any assumption UNRESOLVED -> UNRESOLVED
else all assumptions SUPPORTED -> SUPPORTED
```

For a genuinely unconditional claim, verify that the actual implemented operator lies inside the declared domain before using `SUPPORTED`.

Re-establish transferred properties explicitly:

```text
source operator and result
-> target implemented operator
-> source assumptions
-> target assumption CLM-* records
-> preserved and changed terms
-> applicable target conclusion
```

Do not inherit a source theorem after learning, approximation, changed boundary handling, altered information access, stochasticity, or composition unless an exact mapping or target proof closes the gap.

## 4. Theory Maturity and Formalization

Assign maturity per claim:

| Level | Meaning | Minimum record |
|---|---|---|
| `T0-ASSUMED` | Intuition or imported statement without a target derivation | Exact claim, assumptions, and missing argument |
| `T1-DERIVED` | Target derivation or proof sketch closes consistency but leaves a material proof obligation | Derivation, missing step, scope, and counterpart |
| `T2-PROVED` | Complete proof or exact theorem-to-implementation mapping establishes the bounded claim | Proof or source, assumption mapping, and exact guarantee |

Keep E0–E5 evidence strength in the claim ledger and T0–T2 maturity in Section 12.

Use `FORMAL-CLAIM` when the research argument asserts a theorem, proposition, lemma, bound, or guaranteed property. Use `NO-FORMAL-THEOREM-CLAIMED` for consistency or limitation rows that assert no new formal result.

A CORE `FORMAL-CLAIM` below T2 cannot support a positive G10. Complete, narrow, or downgrade it. A CORE mechanism with no formal theorem still requires T1-or-better consistency under supported assumptions.

## 5. Guarantees, Non-Guarantees, and Counterparts

State the narrowest relevant guarantee and its non-guarantee together. Include quantifiers, norms, constants, probability, and boundary conditions when applicable.

| Property | May establish under conditions | Does not establish by itself |
|---|---|---|
| Invertibility | Recovery of the operator input | Recovery of latent task information or forecast gain |
| Stability | Bounded response to a stated perturbation | Convergence, calibration, or robustness to every shift |
| Output legality | Membership in the encoded valid set | Useful decisions, exploration, or optimality |
| Expressivity | Representation of a function class | Learnability, identifiability, generalization, or sample efficiency |
| Complexity bound | Growth under declared dimensions | Realized hardware efficiency outside the measurement regime |

Require a counterpart for every CORE consistency claim and every design-relevant formal property. The counterpart checks whether assumptions or consequences matter in the target; it does not prove the theorem. Permit `N/A` only for a non-core, purely formal limitation or counterexample.

Treat an in-scope counterexample as contradiction. Treat an out-of-scope counterexample as a boundary. Do not silently narrow a claim after observing an in-scope failure.

## 6. Compile G10 and Route Repairs

For each decisive row:

```text
assumptions CONTRADICTED -> cannot support the current subject
assumptions UNRESOLVED -> theory row remains unresolved regardless of maturity
CORE FORMAL-CLAIM below T2 -> unresolved proof obligation
CORE CONSISTENCY + T1-or-better + supported assumptions
  + explicit non-guarantees and counterpart -> may satisfy its obligation
CORE FORMAL-CLAIM + T2 + supported assumptions
  + exact subject mapping and bounded result -> may satisfy its obligation
```

Compile overall G10:

```text
any decisive claim contradicted or internally inconsistent -> G10 UNSATISFIED
else any decisive claim has unresolved assumptions, consistency, proof, scope, or counterpart -> G10 UNRESOLVED
else every CORE mechanism and claimed formal result closes its obligation -> G10 SATISFIED
```

Do not average rows or let a non-core proof compensate for an unresolved CORE mechanism.

Route repairs:

| Finding | Return |
|---|---|
| Wording is too broad but the contribution is unchanged | Narrow in Stage 10 |
| Narrowing changes a CORE contribution | Re-freeze and return to Stage 8 |
| Operator or component must change | Stage 7, or Stage 5 for a core change |
| In-scope counterexample defeats the causal mechanism | Stage 3 or 5 |
| Invariant is unnecessary or unrelated | Stage 4 |
| Task-gain claim lacks evidence | Keep unresolved and test at Stage 11 |
| Source result does not map exactly | Downgrade to T0/T1 or prove the target result |

Use `NEED-EVIDENCE` for a testable unresolved assumption or proof obligation, `PIVOT` for a repairable contradiction, and `KILL` only when no substantive research direction remains.

## 7. Stage-Specific Anti-Patterns

- Do not assign one T-level to a candidate or system.
- Do not use T-level as assumption applicability or empirical evidence.
- Do not copy a theorem across an adapted operator by name or resemblance.
- Do not hide a required proof with `NO-FORMAL-THEOREM-CLAIMED`.
- Do not omit the observable counterpart of a CORE design-linked claim.
- Do not let an irrelevant counterexample kill a scoped claim or silently scope away an in-scope contradiction.

