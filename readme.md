# Skills

A collection of agent skills for SEO analysis, topical authority and YouTube SEO planning, project knowledge bases, newsletter intelligence, marketing conversion review, health/diet meal planning, X/social post drafting, frontend/UI guidance, cofounder-style project interviews, SaaS pre-launch security review, Cloudflare site auditing, WordPress.org plugin search ranking, and WordPress support debugging work.

Each skill lives in its own directory and is defined by a `SKILL.md` file with frontmatter metadata (`name`, `description`, and optional compatibility/licensing notes) followed by the workflow instructions an agent should follow.

## Repository Contents

### SEO

| Skill | Path | Purpose |
| --- | --- | --- |
| AI Content Audit | [`SEO/ai-content-audit/SKILL.md`](./SEO/ai-content-audit/SKILL.md) | Audits a page or text block against seven AI-content SEO issues and produces a styled HTML audit report. |
| Content Gap Finder | [`SEO/content-gap-finder/SKILL.md`](./SEO/content-gap-finder/SKILL.md) | Compares a website page against Google Search Console query data, with DataForSEO enrichment and optional GA4 engagement context, to find section additions and new page opportunities. |
| SEO Title Optimizer | [`SEO/seo-title-optimizer/SKILL.md`](./SEO/seo-title-optimizer/SKILL.md) | Uses page scrape, GSC, DataForSEO, live SERP, and optional GA4 data to recommend title tags, H1s, and meta descriptions. |
| Topical Authority Map Generator | [`SEO/topical-authority-map-generator/SKILL.md`](./SEO/topical-authority-map-generator/SKILL.md) | Builds a hierarchical topical authority map with pillar pages, clusters, supporting pages, an HTML report, and a machine-readable JSON map. |
| Article E-E-A-T Pruning Audit | [`SEO/article-eeat-pruning-audit/SKILL.md`](./SEO/article-eeat-pruning-audit/SKILL.md) | Audits a single article for helpful-content quality, E-E-A-T/trust signals, freshness, factual risk, and pruning actions: keep, update, merge, redirect, noindex, or delete. |
| YouTube SEO | [`SEO/youtube-seo/SKILL.md`](./SEO/youtube-seo/SKILL.md) | Plans, publishes, optimizes, and audits search-led videos, companion pages, structured data, distribution, and conversion measurement. |

### UI

| Skill | Path | Purpose |
| --- | --- | --- |
| UI Skills | [`UI/ui-skills/SKILL.md`](./UI/ui-skills/SKILL.md) | Provides opinionated implementation constraints for accessible, consistent, high-quality agent-built interfaces. |
| Frontend Design | [`UI/frontend-design/SKILL.md`](./UI/frontend-design/SKILL.md) | Guides production-grade frontend interface design with a clear visual direction and polished implementation details. |

### Productivity

| Skill | Path | Purpose |
| --- | --- | --- |
| Project Knowledge Base | [`PRODUCTIVITY/project-knowledge-base/SKILL.md`](./PRODUCTIVITY/project-knowledge-base/SKILL.md) | Maintains an OKF-inspired, Markdown-first project documentation tree as a durable second brain for humans and agents, with operating metadata, auditing rules, and suggested cron jobs. |
| AgentMail Newsletter Intelligence | [`PRODUCTIVITY/agentmail-newsletter-intelligence/SKILL.md`](./PRODUCTIVITY/agentmail-newsletter-intelligence/SKILL.md) | Sets up and operates an AgentMail-backed newsletter intelligence inbox that summarizes only useful items, confirms expected signups, forwards attention-needed mail, creates non-duplicate research/execution tasks, and stays silent on noise. |

### Marketing

| Skill | Path | Purpose |
| --- | --- | --- |
| Buy or Bounce | [`MARKETING/buy-or-bounce/SKILL.md`](./MARKETING/buy-or-bounce/SKILL.md) | Simulates five buyer personas reviewing a conversion asset section by section, then produces an HTML report with buyer verdicts, friction clusters, prioritized fixes, and rewrite directions. Original concept by [@olelehmann1337](https://github.com/olelehmann1337). |

### Social

| Skill | Path | Purpose |
| --- | --- | --- |
| Compose Viral Skill X Post | [`SOCIAL/compose-viral-skill-x-post/SKILL.md`](./SOCIAL/compose-viral-skill-x-post/SKILL.md) | Turns an AI skill, workflow, prompt, agent setup, automation, pipeline, or tool into a high-engagement X/Twitter post or thread with hook options, breakdown structure, CTA guidance, and an optional infographic prompt. |

### Health

| Skill | Path | Purpose |
| --- | --- | --- |
| Health / Diet Trainer | [`HEALTH/health-diet-trainer/SKILL.md`](./HEALTH/health-diet-trainer/SKILL.md) | Plans easy high-protein, lower-carb/lower-fat weekly family meals, tracks suggested and selected meals, and learns preferences from weekly feedback. |

### OPS

| Skill | Path | Purpose |
| --- | --- | --- |
| Cofounder Vision Interview | [`OPS/cofounder-vision-interview/SKILL.md`](./OPS/cofounder-vision-interview/SKILL.md) | Runs a candid cofounder-style project vision interview, forces strategic clarity, makes an explicit proceed/validate/park/kill recommendation, and saves synthesized decisions into project docs. |

### SaaS

| Skill | Path | Purpose |
| --- | --- | --- |
| SaaS Pre-launch Security Checklist | [`SAAS/saas-prelaunch-security-checklist/SKILL.md`](./SAAS/saas-prelaunch-security-checklist/SKILL.md) | Runs a practical security/privacy readiness gate before launching, dogfooding, beta-testing, or onboarding real users to a SaaS app, with project-specific minimum checks. |

### DevOps

| Skill | Path | Purpose |
| --- | --- | --- |
| Cloudflare Site Audit | [`DEVOPS/cloudflare-site-audit/SKILL.md`](./DEVOPS/cloudflare-site-audit/SKILL.md) | Audits a Cloudflare-hosted site from the CLI/API for DNS proxying, crawler access, HTTPS/TLS, caching, security posture, AI bot policies, and prioritized next steps. |

### WordPress

| Skill | Path | Purpose |
| --- | --- | --- |
| WP Plugin Search Ranker | [`WP/wp-plugin-search-ranker/SKILL.md`](./WP/wp-plugin-search-ranker/SKILL.md) | Diagnoses WordPress.org plugin directory search rankings for a given plugin and search term, then recommends prioritized ranking improvements. |
| WordPress Support Debugging | [`WP/wordpress-support-debugging/SKILL.md`](./WP/wordpress-support-debugging/SKILL.md) | Guides evidence-led WordPress plugin support debugging: choose the right local/cloud repro tool, collect proof, test a fix or snippet, and draft a support reply. |

## Using These Skills

Install or reference the desired skill directory from your agent environment. The `SKILL.md` file is the source of truth for when the skill should trigger, what inputs it expects, and the workflow the agent should run.
