---
name: exec-reply
description: Use when replying directly to an executive. Be concise.
version: 1.0.0
author: bradvin
license: MIT
---

# Exec Reply

## Purpose

Give an executive the decision-ready result without making them read an implementation log. Preserve full detail for internal execution and agent-to-agent coordination.

## Apply This Skill When

Apply it when the final audience is a founder, owner, CEO, or other designated executive, including:

- direct conversational replies;
- scheduled reports and alerts;
- approval requests, executive summaries, completion reports, and blockers;
- drafts explicitly intended for that executive.

Do not apply it to:

- agent-to-agent messages;
- specialist handoffs;
- work-queue records;
- implementation briefs, code reviews, raw evidence, or internal analysis;
- detailed material the executive explicitly requested, although the conclusion should still come first.

When the audience is uncertain, preserve the detailed internal artifact and make only the human-facing wrapper concise.

## Default Response Contract

1. State the subject and bottom line in the first sentence.
2. Follow with 3–5 short, plain-English bullets containing only decision-relevant information.
3. Give one recommendation. Offer no more than two genuine alternatives unless a broader comparison was requested.
4. Target roughly 150 words or fewer for routine replies and 250 words or fewer for a decision brief. Exceed this only when shortening would hide a material risk or the executive requested detail.
5. End after the answer. Do not append a verification ledger, implementation diary, exhaustive next-step list, or generic offer to help.
6. Keep supporting evidence available for follow-up instead of preloading it into every response.

## Asking for a Decision

State, in plain business language:

- what decision or input is needed;
- the recommended default;
- why it matters now;
- the consequence of waiting, only when material.

Make the requested response obvious, such as “Approve”, “Defer”, or one short factual answer. Do not lead with commands, rollout mechanics, task counts, or internal terminology.

## Technical Detail

Omit commands, hashes, commits, task IDs, branches, worktrees, manifests, helper names, and verification mechanics unless one materially changes the executive's decision.

Translate necessary technical facts into business impact. Include only the few accessible links needed for the decision.

## Accessible Artifacts

Never cite an inaccessible file location as the deliverable or tell the executive to inspect a file they cannot access.

Instead:

- quote or summarize the relevant excerpt in the message;
- attach the artifact through the active platform when the full file matters; or
- provide an accessible external link when one already exists and is safe to share.

Internal file locations may remain in agent-to-agent handoffs and durable operational records.

## Scheduled Reports

An executive-facing scheduled report should contain only:

- decisions or approvals required;
- urgent commercial, customer, trust, or operational risks;
- material progress that changes priorities;
- one recommended next action.

Remain silent when there is no meaningful update. Do not report healthy routine checks, raw verification evidence, implementation metadata, or internal bookkeeping.

## Accuracy and Exceptions

Conciseness must not hide uncertainty, failed verification, customer risk, production risk, legal or compliance risk, or an irreversible action. State the material caveat briefly and clearly.

If the executive asks for detailed evidence, provide it in a separate response or accessible artifact without weakening the internal handoff record.

## Quick Test Before Sending

- Can the executive understand the subject and conclusion from the first sentence?
- Is there one clear recommendation or answer?
- Are there no more than 3–5 main bullets and two choices?
- Have inaccessible locations and low-value technical identifiers been removed?
- Is every remaining detail necessary for the decision?
- If this is agent-to-agent communication, has this skill been deliberately left unapplied?
