---
name: public-skill-extractor
description: >
  Extract an installed Hermes skill into a privacy-safe, public-ready skill for a GitHub skills repository.
  Use whenever the user says things like "extract skill xyz to my repo", "publish this skill to my skills repo",
  "package skill xyz for public consumption", "make skill xyz public", "update the public copy of skill xyz",
  or asks to sync a local/private skill into a public skills repository. The workflow preserves the skill's reusable
  essence while removing company IP, private operational details, credentials, local paths, personal data, and one-off nuance.
metadata:
  author: bradvin
  version: "1.0"
---

# Public Skill Extractor

Turn an installed/private Hermes skill into a clean public skill and submit it as a GitHub PR for human approval.

Primary trigger: **"extract skill xyz to my repo"**.

## Core principle

Do **not** copy local skills verbatim. Local skills often contain private operating context, company-specific strategy, credentials, host paths, profile names, customer details, private repository names, or brittle personal conventions. Your job is to extract the **portable essence**: when to use the skill, inputs, workflow, decision rules, verification, pitfalls, and reusable templates.

## Inputs

Infer what you can, ask only when required:

- **Skill name**: from the user's phrase, e.g. `xyz` in "extract skill xyz to my repo".
- **Target repo**: use the repository named by the user; if they say "my skills repo", infer the configured/default skills repo for that user.
- **Mode**: create if no public copy exists; update if a public copy already exists or the user says "update"/"sync".
- **Category/path**: infer from repo conventions. If unclear, choose the most general category and explain it in the PR.

## Workflow

### 1. Load the source skill safely

1. Use the agent's skill-loading capability to load the installed source skill.
2. If the skill has linked `references/`, `templates/`, `scripts/`, or `assets/`, inspect only files that appear reusable. Do not bulk-copy private support files.
3. Identify source metadata:
   - skill name and description
   - trigger phrases
   - required tools/commands/env vars
   - workflow steps
   - reusable templates/checklists
   - pitfalls and verification steps

If the source skill cannot be found, search installed skills by name and ask only if multiple plausible matches remain.

### 2. Extract the essence

Create a short internal extraction map before writing files:

- **Job-to-be-done**: one sentence describing the skill's reusable outcome.
- **Trigger class**: user phrases and situations where it should load.
- **Public workflow**: generalized steps that work for any user or organization.
- **Decision rules**: criteria, scoring, or branching logic worth preserving.
- **Tool requirements**: generic tools only; no private endpoint names unless they are public services.
- **Reusable artifacts**: templates, scripts, references that can be safely included.
- **Verification**: how an agent proves the skill worked.
- **Private material to remove**: list every removed item category.

Keep mechanisms; remove private nouns.

### 3. Privacy and IP scrub

Rewrite before committing. Remove or generalize:

- Company/product/customer names unless the skill is explicitly about a public product.
- Non-public strategy, revenue numbers, roadmap items, support cases, customer quotes, and internal priorities.
- Personal email addresses, phone numbers, home/family details, Slack/Discord IDs, internal channel IDs, and profile routing details.
- Local filesystem paths, profile paths, repo paths, machine names, service names, and ports unless generic.
- Credentials, token env var names tied to private services, API keys, cookies, auth snippets, and secret-loading commands.
- Private repository names, issue/PR numbers, branch names, commit SHAs, cron IDs, MCP server names, and internal databases.
- One-off task progress, session history, implementation logs, and conclusions that will stale quickly.
- Any language that tells future agents to act as a specific private company/operator unless that is the public purpose of the skill.

Replace with placeholders only when useful, e.g. `<owner>/<repo>`, `<api-key-env-var>`, `<project-root>`.

Run a local private-marker scan before committing. At minimum search the new/changed files for patterns like email addresses, local paths, credential words, private company/product names, internal chat platform names, customer data, revenue metrics, and secret env var names. A match is not automatically forbidden, but every match must be intentional and safe.

### 4. Recreate the public skill

Follow the target repo's layout and style:

1. Clone or update the target repository under the user's normal repositories directory.
2. Create a feature branch, e.g. `add-<skill-name>-skill` or `update-<skill-name>-skill`.
3. Place the skill under the best category directory.
4. Write a public `SKILL.md` with:
   - valid YAML frontmatter starting at byte 0
   - `name` and a trigger-rich `description`
   - concise overview
   - required inputs/tools
   - step-by-step workflow
   - privacy-safe examples/templates if helpful
   - verification checklist
   - pitfalls/anti-patterns
5. Add supporting files only when they materially improve reuse.
6. Update repository index/readme tables if the repo uses them.

Do not include task-specific exports, generated reports, source private files, or raw logs.

### 5. Update an existing public skill

When the target repo already contains a public version:

1. Read the public `SKILL.md` and any support files.
2. Compare it against the current installed source skill.
3. Preserve the public skill's structure and public-safe wording where possible.
4. Port only durable improvements from the source:
   - new trigger classes
   - clearer workflow steps
   - better verification
   - reusable pitfalls
   - generic templates/scripts
5. Do **not** reintroduce private details that were scrubbed previously.
6. Add a short "what changed" section in the PR body explaining the sync.

If the installed source has drifted in a private direction, keep the public version generic and state that only reusable workflow improvements were extracted.

### 6. Validate

Before committing:

- Run a whitespace/diff check such as `git diff --check`.
- Verify every changed `SKILL.md` starts with valid YAML frontmatter.
- Run the privacy-marker scan against only the changed skill path.
- Read the final public skill once more as if you were an outside user with no private context.

### 7. Commit, push, and open a PR

Use GitHub CLI when available. If the upstream repo is read-only, push to the authenticated user's fork and open the PR against upstream.

Verify the opened PR before reporting success by re-reading its number, URL, state, head/base branches, changed files, commits, and status checks.

## PR body checklist

Include:

- Summary of the skill added/updated.
- Source installed skill name.
- Sanitization notes: categories of private data removed/generalized.
- Validation run: diff check, frontmatter check, privacy-marker scan.
- Review notes: any intentional public mentions that matched the privacy scan.

## Quality bar

A public extraction is good only if:

- A stranger can use it without knowing the original user's company or machine.
- It has enough trigger phrases to load reliably.
- It preserves the workflow's decision logic, not just a vague summary.
- It contains verification steps so an agent can prove completion.
- It has no credentials, private names, internal paths, or stale session artifacts.
- The PR is opened and verified; do not stop at local files.
