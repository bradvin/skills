# Skills

A collection of agent skills for SEO analysis, topical authority planning, marketing conversion review, X/social post drafting, frontend/UI guidance, Hermes skill packaging, and WordPress.org plugin search ranking work.

Each skill lives in its own directory and is defined by a `SKILL.md` file with frontmatter metadata (`name`, `description`, and optional compatibility/licensing notes) followed by the workflow instructions an agent should follow.

## Repository Contents

### SEO

| Skill | Path | Purpose |
| --- | --- | --- |
| AI Content Audit | [`SEO/ai-content-audit/SKILL.md`](./SEO/ai-content-audit/SKILL.md) | Audits a page or text block against seven AI-content SEO issues and produces a styled HTML audit report. |
| Content Gap Finder | [`SEO/content-gap-finder/SKILL.md`](./SEO/content-gap-finder/SKILL.md) | Compares a website page against Google Search Console query data, with DataForSEO enrichment and optional GA4 engagement context, to find section additions and new page opportunities. |
| SEO Title Optimizer | [`SEO/seo-title-optimizer/SKILL.md`](./SEO/seo-title-optimizer/SKILL.md) | Uses page scrape, GSC, DataForSEO, live SERP, and optional GA4 data to recommend title tags, H1s, and meta descriptions. |
| Topical Authority Map Generator | [`SEO/topical-authority-map-generator/SKILL.md`](./SEO/topical-authority-map-generator/SKILL.md) | Builds a hierarchical topical authority map with pillar pages, clusters, supporting pages, an HTML report, and a machine-readable JSON map. |

### UI

| Skill | Path | Purpose |
| --- | --- | --- |
| UI Skills | [`UI/ui-skills/SKILL.md`](./UI/ui-skills/SKILL.md) | Provides opinionated implementation constraints for accessible, consistent, high-quality agent-built interfaces. |
| Frontend Design | [`UI/frontend-design/SKILL.md`](./UI/frontend-design/SKILL.md) | Guides production-grade frontend interface design with a clear visual direction and polished implementation details. |

### Marketing

| Skill | Path | Purpose |
| --- | --- | --- |
| Buy or Bounce | [`MARKETING/buy-or-bounce/SKILL.md`](./MARKETING/buy-or-bounce/SKILL.md) | Simulates five buyer personas reviewing a conversion asset section by section, then produces an HTML report with buyer verdicts, friction clusters, prioritized fixes, and rewrite directions. Original concept by [@olelehmann1337](https://github.com/olelehmann1337). |

### Social

| Skill | Path | Purpose |
| --- | --- | --- |
| Compose Viral Skill X Post | [`SOCIAL/compose-viral-skill-x-post/SKILL.md`](./SOCIAL/compose-viral-skill-x-post/SKILL.md) | Turns an AI skill, workflow, prompt, agent setup, automation, pipeline, or tool into a high-engagement X/Twitter post or thread with hook options, breakdown structure, CTA guidance, and an optional infographic prompt. |

### Hermes

| Skill | Path | Purpose |
| --- | --- | --- |
| Public Skill Extractor | [`HERMES/public-skill-extractor/SKILL.md`](./HERMES/public-skill-extractor/SKILL.md) | Extracts an installed/private Hermes skill into a privacy-safe public skill, updates existing public copies when the source changes, and guides PR submission for approval. |

### WordPress

| Skill | Path | Purpose |
| --- | --- | --- |
| WP Plugin Search Ranker | [`WP/wp-plugin-search-ranker/SKILL.md`](./WP/wp-plugin-search-ranker/SKILL.md) | Diagnoses WordPress.org plugin directory search rankings for a given plugin and search term, then recommends prioritized ranking improvements. |

## Using These Skills

Install or reference the desired skill directory from your agent environment. The `SKILL.md` file is the source of truth for when the skill should trigger, what inputs it expects, and the workflow the agent should run.
