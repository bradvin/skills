# Skills

A collection of agent skills for SEO analysis, frontend/UI guidance, and WordPress.org plugin search ranking work.

Each skill lives in its own directory and is defined by a `SKILL.md` file with frontmatter metadata (`name`, `description`, and optional compatibility/licensing notes) followed by the workflow instructions an agent should follow.

## Repository Contents

### SEO

| Skill | Path | Purpose |
| --- | --- | --- |
| AI Content Audit | [`SEO/ai-content-audit/SKILL.md`](./SEO/ai-content-audit/SKILL.md) | Audits a page or text block against seven AI-content SEO issues and produces a styled HTML audit report. |
| Content Gap Finder | [`SEO/content-gap-finder/SKILL.md`](./SEO/content-gap-finder/SKILL.md) | Compares a website page against Google Search Console query data to find section additions and new page opportunities. |
| SEO Title Optimizer | [`SEO/seo-title-optimizer/SKILL.md`](./SEO/seo-title-optimizer/SKILL.md) | Uses page, GSC, DataForSEO, and SERP data to recommend title tags, H1s, and meta descriptions. |

### UI

| Skill | Path | Purpose |
| --- | --- | --- |
| UI Skills | [`UI/ui-skills/SKILL.md`](./UI/ui-skills/SKILL.md) | Provides opinionated implementation constraints for accessible, consistent, high-quality agent-built interfaces. |
| Frontend Design | [`UI/frontend-design/SKILL.md`](./UI/frontend-design/SKILL.md) | Guides production-grade frontend interface design with a clear visual direction and polished implementation details. |

### WordPress

| Skill | Path | Purpose |
| --- | --- | --- |
| WP Plugin Search Ranker | [`WP/wp-plugin-search-ranker/SKILL.md`](./WP/wp-plugin-search-ranker/SKILL.md) | Diagnoses WordPress.org plugin directory search rankings for a given plugin and search term, then recommends prioritized ranking improvements. |

## Using These Skills

Install or reference the desired skill directory from your agent environment. The `SKILL.md` file is the source of truth for when the skill should trigger, what inputs it expects, and the workflow the agent should run.
