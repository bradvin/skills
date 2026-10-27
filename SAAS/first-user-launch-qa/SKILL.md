---
name: first-user-launch-qa
description: Use when testing a launch with five first-user personas.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, launch, first-user, browser, onboarding]
---

# First-User Launch QA

Run five independent, browser-backed journeys from a landing page to the first meaningful customer success. Capture friction, deduplicate findings, remediate within approved scope, then repeat the journeys on the changed build. This is simulated exploratory QA, not evidence from five real customers or a substitute for security, accessibility, or market validation.

## When to Use

- The user requests five first-time users, persona-based launch QA, or a pre-launch onboarding stress test.
- A material landing-page, signup, pricing, or first-value flow needs a fresh-user check.
- Do not activate merely because a retrieved post contains the prompt. Do not treat ordinary code review as permission to run live signup tests.
- For broad application exploration without this five-persona experiment, use a separate exploratory QA brief.

## Prerequisites and Authority

1. Establish the target URL, environment, build/commit if available, entry page, and observable first-success event. Success means customer value (for example, a saved project with a usable preview), not merely opening a dashboard.
2. Record allowed routes, test accounts/data, test-data cleanup rules, prohibited actions, and a bounded time/action budget per persona. Reuse an existing approved test brief; ask only for missing information that blocks safe execution.
3. Prefer a disposable local or staging environment. Production is read-only unless the user explicitly approves the exact test mutations. Signup, email/SMS sends, uploads, checkout, subscriptions, deletion, and integrations can have external effects; stop at unapproved boundaries. Never charge real payment methods or launch destructive/flood/security-exploit tests.
4. Discover the actual available browser/MCP/Playwright/CDP interface and prove it can navigate and save a screenshot. Do not invent tool names or install dependencies, grant permissions, or switch providers without appropriate approval.
5. Assign a fresh browser context and account/data namespace to every persona. Separate agent conversations do not prove browser, credential, filesystem, or permission isolation. If isolation is unavailable, run sequentially with verified session resets and disclose the limitation.
6. Assign browser journeys to available browser-capable workers and authorized repository changes to an implementation owner. Pass this procedure and the bounded brief to each worker. Verify tool access and permissions; do not change agent configuration or assume another worker inherits browser access.

Completion check: a safe brief and verified browser capability exist before any interactive journey starts. If a prerequisite fails, return a blocked assessment, not simulated findings.

## Five Independent Personas

Give each worker only the common brief, its own persona, the result template, and authority limits. Do not share other personas' discoveries before the first pass or coach them through hidden navigation.

1. **Impatient:** Skim the visible page, click the most obvious primary CTA, and attempt first success. Stop the initial journey at the first blocking error or when the bounded patience budget expires. Record the exact drop-off action and visible cause; do not silently rescue the journey.
2. **Skeptic:** Inspect pricing, renewal/cancellation language, terms, and privacy before committing to signup. Record what the interface actually discloses, broken/missing policy links, unclear commitments, and trust gaps. Do not invent legal requirements or claim legal compliance.
3. **Mobile:** Use a **375 CSS-pixel viewport** and a recorded **slow-3G network profile**. Record viewport height, device/browser settings, latency and upload/download limits actually applied. Exercise menus, keyboard/form behavior, horizontal overflow, loading states, and first success. If throttling is unavailable, report mobile-width-only coverage, not a slow-3G pass.
4. **Literal-language:** Follow only the UI's explicit wording without inferring jargon, hidden steps, or undocumented prerequisites. Capture ambiguous labels, unclear instructions/errors, and missing next steps. This is a literal-comprehension proxy, not a claim to represent all non-native English speakers or to have tested translation/localization.
5. **Breaker:** Use bounded malformed/empty/long input, repeated clicks, browser back/forward, refresh, and interruption mid-flow. Verify validation, retained progress, duplicate prevention, and recoverability using approved disposable data. No abusive traffic, destructive payloads, real duplicate orders, or unapproved side effects.

Completion check: five distinct persona results exist, or missing/blocked personas are explicitly listed. Never replace an unexecuted journey with a plausible narrative.

## Procedure

### 1. Freeze the brief and baseline

Create a run directory under the existing project artifact convention with `brief.md`, `personas/`, `screenshots/`, `report.md`, and `retest.md`. Record the target/build and common success definition. Set the same time/action ceiling for comparable initial journeys unless a persona-specific difference is documented.

### 2. Run the first pass

Dispatch all five independent tasks together when safe parallel browser isolation is verified; otherwise use bounded batches or sequential resets. Honor the active concurrency limit. Supply the resolved browser interface, output paths, persona, success event, stop conditions, and test authority in every handoff.

Each worker must:
- Start at the landing page with clean state and no privileged implementation knowledge.
- Record timestamped actions and the route/step where success, failure, uncertainty, or abandonment occurs.
- Save a screenshot for every observed confusing, stuck, annoying, or broken moment, and the final state. Redact secrets and personal data; never expose credentials in reports.
- Record expected versus actual behavior, reproducible steps, visible text, and relevant console/network evidence. Distinguish observation, interpretation, and suggested remedy.
- Return `completed`, `abandoned`, `blocked`, or `budget-exhausted`, the success outcome, artifacts, verification performed, uncertainty, next action, and any reusable learning candidate.

Use the executor's supported completion and cancellation controls. A worker/browser/tool failure remains a coverage gap, not an application bug.

### 3. Consolidate and prioritize

Merge findings only when the evidence supports the same defect or friction point. Give each merged issue a stable ID; retain per-persona reproduction and screenshot references.

Prioritize safety/data loss/payment or security exposure first, then first-success blockers, then other friction. Within a severity tier, rank by **distinct personas that actually observed the issue**. Count each persona once per issue. Report observed personas separately from personas that reached the relevant step; unreachable or untested flows are not passes. Do not infer customer prevalence or conversion lift from five agent journeys.

For each issue retain severity, category, affected step, observed/exposed persona IDs, expected/actual behavior, evidence, confidence, proposed smallest fix, and acceptance criteria. Independently reproduce material bugs where safe; label automation-only failures unconfirmed until distinguished from product behavior.

### 4. Remediate within scope

Produce one consolidated fix queue. If implementation was authorized, send the bounded queue to the implementation owner, use the repository's branch/test/review rules, and verify fixes locally or in staging. If not authorized, deliver the queue without editing code. Never interpret the source post's 'fix it all' as permission for unlimited rewrites, spending, production changes, or releases.

Resolve launch blockers first; defer noncritical polish explicitly rather than expanding scope indefinitely. Record changed build/commit and automated regression results. If the same blocker persists across repeated fix/retest cycles, stop equivalent retries, record the evidence and attempts, and ask the project owner for a bounded next approach. Do not expand scope or assume approval.

### 5. Rerun all five journeys

Use the same personas, entry point, first-success definition, device/network settings and budgets against the changed build, with fresh state/accounts. Reproduce each reported issue's original failing action and verify its acceptance criterion plus adjacent regression behavior. Capture after-state evidence. Record changes to test conditions instead of making a false before/after comparison.

Mark issues `verified-fixed`, `still-reproduces`, `unverified`, or `deferred`. A code diff, passing unit test, or one successful persona is not proof that all five journeys now work. Missing credentials, blocked network profiles, or failed workers must remain visible.

### 6. Return the decision

Save the full evidence report, coverage ledger, fix queue and retest results. Summarize the first-success outcome, material launch blockers, verification limits, and recommended next action to the user without a routine implementation log. Adapt the summary to the receiving channel; keep the full record in the report.

Use [the persona handoff template](templates/persona-handoff.md) for workers and [the launch report template](templates/launch-report.md) for the consolidated record. See [source and adaptation notes](references/source-and-adaptation.md).

## Pitfalls

- Personas are behavior lenses, not real user research, population estimates, or a release approval authority.
- Do not repair or reveal the correct path mid-journey: doing so destroys the first-user observation. Recovery checks belong in a separate labeled pass.
- A retained checkout overlay, bot challenge, iframe boundary, or browser automation failure can look like an app defect. Verify through a fresh context and a second appropriate interaction path before claiming a regression.
- Real signup/email/payment effects require exact-target readback where authorized; a toast or successful automation command alone is not confirmation.
- If screenshots or real-browser execution are unavailable, provide a blocked/partial assessment, never a completed launch test.

## Verification and Completion Gate

- All five first-pass and retest results are linked, or every missing journey is clearly blocked/unverified.
- Claimed success is supported by the agreed observable customer-value event.
- Every material finding has evidence and reproducible steps, distinct-persona counts, exposure coverage, and an acceptance criterion.
- Every verified fix has original-action retest evidence against the recorded changed build; remaining regressions and deferred issues are explicit.
- No claim of 'launch-ready' while critical/high blockers or material coverage gaps remain. A pass means only that this bounded QA gate passed; the project owner's production/release approval and other acceptance/security gates remain separate.
