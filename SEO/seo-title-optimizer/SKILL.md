---
name: seo-title-optimizer
description: >
  Use this skill whenever the user wants to optimize, rewrite, or improve the title tag,
  H1, or meta description for a webpage. Triggers include any request like "rewrite the
  title for [url]", "optimize the meta description for [page]", "why is [url] getting low
  CTR?", "improve the SERP snippet for [page]", "write better titles for [url]", or any
  time a URL is provided alongside a CTR, impressions, or ranking problem. Also use when
  the user asks to audit SERP copy across multiple pages. This skill runs a full
  multi-source data pipeline — GSC, DataForSEO ranked keywords, live SERP, page scrape —
  before generating scored, reasoned copy recommendations. Always use it rather than
  guessing from the URL alone.
compatibility: >
  Requires: GSC MCP (gsc_query_search_analytics), DataForSEO MCP
  (dataforseo_labs_google_ranked_keywords, serp_organic_live_advanced,
  kw_data_google_ads_search_volume), web_fetch tool.
---

# SEO Title / H1 / Meta Description Optimizer

This skill runs a 4-phase pipeline to generate the best possible title tag, H1, and meta
description for any given URL. Never skip phases or guess — the quality of recommendations
depends entirely on the data collected.

---

## Phase 1: Parallel Data Collection

Fire ALL of the following simultaneously (don't wait for one before starting another):

### 1a. Page scrape (web_fetch)
Fetch the URL the user provided. Extract:
- Current `<title>` tag
- Current H1 (first `<h1>`)
- Current meta description (`<meta name="description">`)
- All H2 headings (to understand content scope)
- First 400–500 words of body copy
- Word count / content depth signal if visible

### 1b. GSC: query performance for this URL
Use `gsc_query_search_analytics` with:
- `site_url`: `https://fooplugins.com/`
- `dimensions`: `["query"]`
- `dimension_filter_groups`: filter to the exact URL
- `start_date`: 30 days ago, `end_date`: yesterday
- `row_limit`: 50

Collect: query, clicks, impressions, CTR, position for each query.

### 1c. DataForSEO: ranked keywords for the page
Use `dataforseo_labs_google_ranked_keywords` with:
- `target`: the full URL (e.g. `https://fooplugins.com/how-to-sell-photos-online/`)
- `location_name`: `United States`
- `language_code`: `en`
- `limit`: 50
- `order_by`: `["keyword_data.keyword_info.search_volume,desc"]`

Collect: keyword, search_volume, rank_group (position), type.

### 1d. DataForSEO: live SERP for primary keyword
Determine the primary keyword first (see Phase 2 — use the highest-volume keyword at
position ≤ 20). Then run `serp_organic_live_advanced` with:
- `keyword`: primary keyword
- `language_code`: `en`
- `depth`: 10

Collect: title, description, domain, rank_group for organic results 1–10. Also capture
any PAA (people_also_ask) questions and any AI Overview references.

> **If you can't determine the primary keyword until Phase 2:** Run 1a, 1b, 1c first,
> do Phase 2 signal processing, then fire 1d before Phase 3.

### 1e. DataForSEO: search volume for candidate terms
Once you have the keyword list from 1c, pick the 8–10 most promising keyword variants
and validate/enrich volumes via `kw_data_google_ads_search_volume`:
- `keywords`: array of candidate keywords
- `language_code`: `en`
- `location_name`: `United States`

---

## Phase 2: Signal Processing

Before writing a single word of copy, derive these signals from the raw data:

### Primary keyword
The single highest-volume keyword where position is ≤ 20. If there are ties, prefer
the keyword whose phrasing most naturally fits a title tag. This is the non-negotiable
must-include in the title tag.

### Striking distance keywords (positions 11–20)
List all keywords in this range with volume ≥ 500. These can realistically move to
page 1 with an improved title — include their phrasing where it fits naturally.

### CTR gap analysis
Calculate expected CTR by position using these benchmarks:
| Position | Expected CTR |
|----------|-------------|
| 1        | ~28%        |
| 2        | ~15%        |
| 3        | ~11%        |
| 4–5      | ~6–8%       |
| 6–10     | ~2–4%       |
| 11–20    | ~1–2%       |

Compare actual CTR (from GSC) to expected CTR. A page at position 10 with 0.11% CTR
vs ~3% expected is 96% below expectation — that's the severity signal. Report this
clearly so the user understands the opportunity size.

### Keyword language patterns
Look at the top 10 keywords by volume. What's the dominant phrasing?
- "how to sell photos online" → instructional "how to" intent
- "sell photos online" → transactional / direct intent  
- "selling photos" → exploratory intent
The dominant pattern should shape title structure. If both instructional and transactional
appear at high volume, the title should serve both (e.g. "How to Sell Photos Online — 10
Platforms That Pay").

### Competitor title patterns
From the SERP data (1d), analyze the top 5 organic results:
- Which title structures are common? (How-to, numbered list, year tag, question format,
  outcome-first)
- What's table stakes (done by 3+ competitors — must match)?
- What's absent (done by 0–1 competitors — differentiation opportunity)?
- What specific words appear in multiple titles?

### PAA emotional signals
People Also Ask questions reveal the anxiety or intent behind the search. Extract the
PAA questions and identify the core concern (e.g. "How much money can you make?" →
anxiety: "will this actually work for me?"). The best meta descriptions answer that
emotional question, not just describe the article.

### Current copy diagnosis
Compare current title/H1/meta against the signals above. Identify specifically what's
wrong — keyword mismatch, no differentiation, brand suffix confusion, benefit absent,
wrong intent match, etc.

---

## Phase 3: LLM Synthesis

Assemble this structured brief and use it to generate candidates. The brief forces
reasoning rather than just generating copy.

```
=== SEO COPY BRIEF ===

URL: [url]
Page topic: [1-sentence summary from body copy]
Content depth: [word count / key H2s]

--- CURRENT STATE ---
Title tag:    [current title]
H1:           [current H1]
Meta desc:    [current meta]

--- PERFORMANCE ---
CTR:          [actual]% vs [expected]% expected at avg position [X] → [Y]% below benchmark
Top queries by impressions (GSC):
  [query] — [impressions] impr, pos [X], [CTR]% CTR
  ...

--- KEYWORD TARGETS ---
Primary (must-include): "[keyword]" — vol [X], pos [Y]
Striking distance:
  "[keyword]" — vol [X], pos [Y]
  ...
Dominant intent: [instructional / transactional / exploratory]
Dominant phrasing: [e.g. "how to sell photos online"]

--- SERP LANDSCAPE ---
Top 5 competitor titles:
  [pos 1]: "[title]" — [domain]
  [pos 2]: "[title]" — [domain]
  ...
Table stakes (in 3+ titles): [e.g. year tag, numbered list]
Differentiation gaps: [e.g. no outcome-first titles, no specificity about earnings]
PAA questions: [list]
Emotional subtext: [what anxiety or hope is behind the search]

--- TASK ---
Generate:
  • 3 title tag candidates (50–60 chars ideal, 70 max)
  • 3 H1 candidates (can be slightly longer / more descriptive than title tag)
  • 3 meta description candidates (140–155 chars)

For EACH candidate:
  1. State which keyword(s) it targets
  2. Name the CTR mechanism used: [specificity / number hook / outcome / urgency /
     curiosity / social proof / emotional resonance]
  3. Explain how it differentiates from the top 3 competitors
  4. Score 1–10 on: keyword match, differentiation, CTR appeal
  5. Flag any risk (e.g. over-promises, too generic, wrong intent)

Finally: recommend ONE title, ONE H1, ONE meta as the primary recommendation,
with a brief justification.
=== END BRIEF ===
```

---

## Phase 4: Output Format

Present results in this order:

### 1. Situation summary (3–4 sentences)
State the opportunity clearly: impressions, actual CTR, expected CTR, gap, and which
keywords have the most potential. This is the "why this matters" framing.

### 2. Current copy diagnosis
One short paragraph on what's specifically wrong with the current title/H1/meta.

### 3. Recommended copy (primary)
The single best title, H1, and meta description. Present these prominently — they
should be immediately copy-pasteable. Label each clearly.

### 4. Alternative candidates
A table or card layout showing the remaining 2 candidates per element, with their
scores and the key tradeoff for each.

### 5. Implementation notes
Any important caveats: character counts, brand suffix handling (WordPress SEO plugin
settings), whether the H1 and title should differ, expected timeline to see GSC
changes (typically 2–4 weeks), and the follow-up metric to watch.

---

## Key Principles

**Title ≠ H1**: The title tag is for the SERP click — optimized for keyword match and
CTR. The H1 is for the reader who already clicked — it can be more descriptive,
benefit-oriented, or even slightly different phrasing. Don't make them identical.

**Never optimize for a keyword at position > 20**: A title change can boost CTR and
marginally improve ranking signals, but it cannot fix a page stuck at position 35.
If the primary opportunity keywords are all beyond position 20, flag this and recommend
content work first.

**CTR mechanism > keyword stuffing**: A title that hits the primary keyword once with
a compelling benefit will outperform one that hits three keyword variants. Google
bolds keyword matches — use that to your advantage, but don't sacrifice readability.

**Meta descriptions don't directly affect rankings**: They affect CTR only. So meta
descriptions should be written like ad copy — answer the emotional question behind
the search, create a specific expectation, and give a reason to click over the 9
other results on the page.

**Year tags are table stakes in fast-moving niches**: If 4/5 competitors include the
year, not including it signals your content may be outdated — even if it isn't.

---

## Reference Files

- `references/ctr-benchmarks.md` — Position-by-CTR benchmarks with device breakdowns
- `references/title-patterns.md` — Library of high-CTR title structures with examples
- `references/meta-patterns.md` — Library of high-CTR meta description formulas
