---
name: content-gap-finder
description: >
  Analyze a website page's GSC query data to find content gaps and new page opportunities.
  Use this skill whenever the user says things like "find content gaps", "what should I add to this page",
  "content gap analysis", "what new pages should I create", "analyze queries for [url]", "daily content task",
  "run the content gap finder", "content opportunities", "what are people searching for on this page",
  "what queries am I missing", "gap analysis", or "expand this page". Also trigger when the user pastes
  a URL for a verified site and asks what content to add, or asks "what should I write about next" or
  "pick a page to improve". If no URL is given, the skill auto-picks the best candidate page.
  This skill combines GSC query data, live page scraping, and DataForSEO keyword enrichment to produce
  an HTML report with concrete content section suggestions and new page ideas.
---

# Content Gap Finder

Analyzes a website page by comparing its actual content against the GSC queries driving impressions to it. Identifies content sections to add and new standalone pages to create. Outputs a styled HTML report.

## Defaults

- **GSC site URL**: The verified property for the submitted site, inferred from the URL when possible or supplied by the user.
- **Audit history file**: `/home/claude/content-gap-audits.json`
- **Report output**: `/mnt/user-data/outputs/content-gap-report.html`

## Workflow

### Step 1: Select the target page

**If the user provides a URL**, use that URL directly.

**If no URL is provided**, auto-pick the best candidate:

1. Load the audit history from `/home/claude/content-gap-audits.json` (create it as `{"audits":[]}` if it doesn't exist)
2. Query GSC for the top 50 pages by clicks over the last 90 days:
   - `gsc_query_search_analytics` with dimensions `["page"]`, row_limit 50, date range = last 90 days
3. Filter out pages that were audited in the last 30 days (check audit history)
4. Filter out non-content pages (anything matching `/cart`, `/checkout`, `/my-account`, `/wp-admin`, `/wp-login`, `/feed`, or the site's bare homepage itself unless no other candidates exist)
5. Pick the top remaining page by clicks — this is the page doing well enough to be worth investing in, but hasn't been audited recently

Tell the user which page was selected and why (e.g., "Auto-picked /blog/product-category-guide/ — 342 clicks in the last 90 days, last audited 45 days ago").

### Step 2: Pull GSC query data for the page

Query GSC for all queries driving traffic to this specific page over the last 90 days.

GSC doesn't support filtering by page and query simultaneously in a single call. Instead:
- First call: dimensions `["page"]` to confirm the page's overall metrics
- Second call: dimensions `["query", "page"]` with row_limit 500 to get query-page pairs, then filter results to only rows matching the target page URL

Sort the resulting queries by impressions descending. These are the signals people are sending — what they expect to find on this page.

### Step 3: Scrape the actual page content

Use `web_fetch` to retrieve the page content. Save it for analysis. Extract:
- The page title and H1
- All H2 and H3 headings (these define the content structure)
- Key topics and terms covered in the body text
- Existing internal links

This is what the page actually delivers. The gap between what people search for (Step 2) and what the page covers (Step 3) is where the opportunities live.

### Step 4: Enrich queries with keyword data

Take the top 30-50 queries by impressions from Step 2 and batch them into a DataForSEO keyword overview call:

```
dataforseo_labs_google_keyword_overview:
  keywords: [top queries from GSC]
  language_code: "en"
  location_name: "United States"
```

This adds search volume, CPC, competition level, and search intent data to each query. This enrichment helps prioritize which gaps matter most — a query with 5,000 monthly searches is more valuable than one with 50.

### Step 5: Analyze and categorize

Compare the GSC queries against the page content. Categorize each query into one of these buckets:

**A) Well-covered** — The page already has a section addressing this query. Skip these.

**B) Content gap (add a section)** — The query is closely related to the page's core topic but isn't adequately addressed. These become "add a section" recommendations. Indicators:
- Query contains the page's primary keyword plus additional qualifying terms
- Query asks a specific question the page doesn't answer
- Query targets a subtopic the page mentions but doesn't elaborate on
- The page ranks position 4-20 for this query (close but not nailed)

**C) New page opportunity** — The query represents a topic that deserves its own dedicated page. Indicators:
- Query has high search volume (>200/mo) but is tangential to the page's core topic
- Query represents a different search intent than the current page
- Query could be a standalone article or landing page
- Multiple related queries cluster around the same sub-topic

**D) Irrelevant / noise** — Brand terms, navigational queries, or queries that don't represent content opportunities. Skip these.

### Step 6: Build recommendations

**For each "add a section" recommendation:**
- Suggested H2 or H3 heading
- What the section should cover (2-3 sentences)
- Which GSC queries it would satisfy (list them with impressions + search volume)
- Estimated position improvement rationale
- Priority score (High / Medium / Low) based on combined impressions + search volume

**For each "new page" recommendation:**
- Suggested page title and URL slug
- Target primary keyword + search volume
- Supporting queries that would also be addressed
- Content brief (what the page should cover, 3-5 bullet points)
- Internal linking suggestion (how it connects back to the analyzed page)
- Priority score based on total opportunity (search volume × estimated CTR potential)

Sort both lists by priority score descending.

### Step 7: Generate the HTML report

Generate a single self-contained HTML file following the report specification in the next section. Save to `/home/claude/content-gap-report.html`, then copy to `/mnt/user-data/outputs/content-gap-report.html`.

### Step 8: Update the audit history

Append an entry to `/home/claude/content-gap-audits.json`:

```json
{
  "url": "https://example.com/the-page/",
  "date": "2026-03-15",
  "sections_suggested": 5,
  "new_pages_suggested": 3,
  "top_opportunity": "best wordpress gallery plugin comparison"
}
```

Create the file if it doesn't exist yet.

### Step 9: Present the report

Use `present_files` to deliver the HTML report. Give a brief summary in chat:
- Which page was analyzed
- How many queries were examined
- Top 3 "add a section" recommendations (one-liner each)
- Top 2 "new page" opportunities (one-liner each)
- Prompt: "Want me to draft any of these sections, or should I run this on another page?"

---

## HTML Report Specification

Generate a single, self-contained HTML file. No external dependencies — inline all CSS and JS. Use system fonts.

### Report structure

```
Content Gap Analysis Report
├── Header
│   ├── Page URL (linked)
│   ├── Audit date
│   ├── Total queries analyzed
│   └── Overall opportunity score (sum of all search volume in gaps)
├── Page Snapshot
│   ├── Current title & H1
│   ├── Current content structure (H2/H3 outline)
│   ├── Total clicks / impressions / avg position (last 90 days)
│   └── Number of unique queries driving impressions
├── Content Sections to Add (sorted by priority)
│   ├── For each recommendation:
│   │   ├── Suggested heading (H2/H3)
│   │   ├── What to cover (brief description)
│   │   ├── Queries this satisfies (table: query, impressions, clicks, position, search volume, intent)
│   │   ├── Priority badge (High / Medium / Low)
│   │   └── Rationale (why this matters)
├── New Page Opportunities (sorted by priority)
│   ├── For each recommendation:
│   │   ├── Suggested title + URL slug
│   │   ├── Primary keyword + search volume
│   │   ├── Supporting queries (table: query, search volume, intent)
│   │   ├── Content brief (3-5 bullet points)
│   │   ├── Internal linking suggestion
│   │   └── Priority badge
├── Query Data Table (full reference)
│   ├── All queries with: query, impressions, clicks, CTR, position, search volume, intent, bucket
│   ├── Sortable by column (via simple JS)
│   └── Color-coded by bucket (gap = amber, new page = blue, covered = green, noise = gray)
└── Footer
    ├── Methodology note
    └── Timestamp
```

### Color palette

- Primary: `#1a1a2e` (dark navy — headers and body text)
- Accent: `#e94560` (coral red — highlights and high-priority badges)
- Secondary accent: `#0f3460` (deep blue — links and section headers)
- Background: `#ffffff`
- Surface: `#f8f9fa` (light gray — cards and table alt-rows)
- Border: `#e2e8f0`

### Priority badges

- **High**: background `#e94560`, text white, bold
- **Medium**: background `#f59e0b`, text white
- **Low**: background `#6b7280`, text white

### Bucket colors (query table row backgrounds)

- Content gap (add section): `#fef3c7` (warm amber)
- New page opportunity: `#dbeafe` (light blue)
- Well-covered: `#d1fae5` (light green)
- Noise / irrelevant: `#f3f4f6` (light gray)

### Typography

- Headings: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` — bold, generous spacing
- Body: same font stack, normal weight, 15px base size
- Tables: 13px, compact, alternating row shading
- Monospace for URLs and slugs: `'SF Mono', 'Fira Code', 'Consolas', monospace`

### Layout

- Max width 1100px, centered
- Cards with subtle `box-shadow` for each recommendation
- Collapsible query tables within each recommendation (use `<details>/<summary>`, collapsed by default)
- Sticky header showing page URL and date while scrolling
- Print-friendly: `@media print` expands all collapsed sections and hides toggle controls

### Table styling

- Right-align numeric columns (impressions, clicks, position, search volume)
- Position cell colors: < 4 = green, 4–10 = amber, > 10 = light red
- CTR cell colors: < 2% = red, 2–5% = amber, > 5% = green
- Sortable via inline JS — click column headers to toggle ascending/descending

### Recommendation cards

Each card includes:
- Left color bar indicating priority (red = high, amber = medium, gray = low)
- Heading with the suggested section title or page title
- Compact description paragraph
- Key stats inline: total impressions from supporting queries, estimated monthly search volume
- Expandable query data table (collapsed by default to keep report scannable)

### Search intent pills

When DataForSEO provides search intent, display as small inline pills:
- Informational: `#dbeafe` background, `#1e40af` text
- Commercial: `#d1fae5` background, `#065f46` text
- Transactional: `#fed7aa` background, `#9a3412` text
- Navigational: `#f3f4f6` background, `#374151` text

### JavaScript (inline, minimal)

Two features only:

1. **Table sorting** — Click any column header to sort `<tbody>` rows ascending/descending. Simple compare function, no libraries.
2. **Bucket filter buttons** — At the top of the full query data table, render filter buttons for each bucket type. Clicking one shows only rows of that bucket; clicking again shows all.

---

## Important notes

- The audit history file persists between sessions. Always check for it and create it if missing.
- When auto-picking, prefer pages with more impressions over more clicks — high impressions with lower clicks means more room to grow.
- Don't recommend sections that would make the page unfocused. If a query is popular but off-topic, it belongs in the "new page" bucket, not the "add a section" bucket.
- The DataForSEO keyword overview call can handle up to 700 keywords at once, but keep it to 30-50 to stay focused on the most meaningful queries.
- If DataForSEO is unavailable or errors, proceed without enrichment — the GSC data alone (impressions, clicks, position) is still valuable enough to generate useful recommendations.
- Always batch tool calls where possible to minimize round-trips.
