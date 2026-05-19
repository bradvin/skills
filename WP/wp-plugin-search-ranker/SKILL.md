---
name: wp-plugin-search-ranker
description: Diagnose why a WordPress.org plugin ranks where it does for a given search term, and recommend specific, prioritized changes to improve its position. Use this skill whenever the user gives a search term and a plugin slug (or plugin name) and asks why their plugin is at position N, how to outrank a competitor, why a competitor is ahead, what to change in the title/tags/readme to rank higher, or anything similar about WP.org plugin directory search rankings. Trigger phrases include "why am I ranking #N for X", "how do I rank higher for [term]", "what's beating my plugin for [term]", "outrank [competitor]", "WP plugin SEO", "WordPress plugin directory ranking", "audit my plugin against [term]". Use proactively when the user is comparing their plugin against competitors in a SERP. Do NOT trigger for Google SEO of marketing pages (that's a different problem).
---

# WordPress.org Plugin Directory Search Ranker

This skill diagnoses why a plugin ranks where it does on the WP.org directory search and recommends specific changes based on the actual ranking algorithm.

## When this triggers vs when it doesn't

- ✅ "Why is my plugin #11 for 'lightbox'?"
- ✅ "How do I outrank Elementor for 'page builder'?"
- ✅ "Audit my plugin titled X against the term Y"
- ❌ "How do I rank my plugin's marketing site on Google?" — that's a different problem; tell the user this skill is for WP.org directory search, not Google.

## Inputs needed

You need two things from the user. Ask only for what's missing:
1. **Search term** (e.g. "gallery", "lightbox", "popup")
2. **Plugin slug or name** (e.g. `elementor`, `woocommerce`, `contact-form-7`)

If they give a plugin name but not a slug, search the API and confirm the match before proceeding.

## How the algorithm works — what to keep in mind

The full algorithm reference lives in `references/algorithm.md`. Read it before running an analysis if you haven't already this session, or if the user asks "why does X matter". Key principles that drive recommendations:

- **Text relevance × function score.** BM25 over title/slug/excerpt/description/tags multiplied by function-score factors (installs, recency, rating, support resolution).
- **BM25 saturates fast.** Going from 1× → 2× of a term gives meaningful lift; 2× → 3× is small; beyond that, near zero. Density matters more than raw count because longer docs are penalized.
- **Slug + title get a ×5 boost** — the biggest text lever. Tags get ×2. Author/contributors get ×3 (rarely relevant).
- **Title leading-position matters** for the engram analyzer — having the search term as one of the first words helps.
- **Function score multipliers compound** but each has a small individual factor (rating 0.25, support 0.25, installs 0.375). When BM25 is saturated across the field, these decide rank within the tier.
- **Sub-1M install booster** is non-trivial: plugins closer to 1M installs get a meaningful lift over plugins at 10K–100K.
- **Recency offset is 180 days** then exp decay (360d half-life). Updates within 6 months get full credit.

## The workflow

Walk through these steps in order. The user wants a diagnosis + recommendations, not a brain dump — keep the output focused on what they should actually do.

### Step 1: Pull the SERP

Fetch the top 10–15 results for the search term via the WP.org API:

```bash
curl -s -A "Mozilla/5.0" "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request%5Bsearch%5D=TERM&request%5Bper_page%5D=15&request%5Bpage%5D=1" -o /tmp/serp.json
```

URL-encode the brackets (`%5B`/`%5D`) and set a User-Agent — the API rejects plain bracket requests and empty UAs. Locate the user's plugin in the results and note its position. If the plugin isn't in the top 15, page through (page=2, page=3) to find it. If it's past page 5, say so — the gap is too large to close with the techniques in this skill alone.

### Step 2: Pull readmes for the top 3 + the user's plugin

```bash
for slug in <top3-slugs> <user-slug>; do
  curl -s -A "Mozilla/5.0" "https://plugins.svn.wordpress.org/$slug/trunk/readme.txt" -o "/tmp/readmes/$slug.txt"
  # If size < 500 bytes, try uppercase README.txt
done
```

Some plugins use uppercase `README.txt` or another nonstandard readme filename. Check the file size — if it returned a 404 HTML page (< 500 bytes), retry with `README.txt`. If that also fails, list the SVN trunk directory to find the actual filename.

### Step 3: Run the comparison

Use `scripts/analyze.py` — it parses readmes, runs BM25 saturation math, and outputs a structured comparison. Pass it the term, the user's slug, and the path to the SERP JSON.

```bash
python3 /path/to/scripts/analyze.py --term "page builder" --user-slug elementor --serp /tmp/serp.json --readmes-dir /tmp/readmes
```

This gives you the raw data you'll reason from. Don't dump the script output verbatim — use it to inform your recommendations.

### Step 4: Diagnose where the gap is

Walk through the signal hierarchy in this order, and stop at the first one that explains a meaningful share of the gap. Don't recommend every possible improvement — only the levers that matter for *this specific* SERP.

1. **Slug** — does the user's slug contain the term as a clean dash-separated token? If not, they're missing the ×5 slug boost. Slugs can't be changed, so partial recovery comes via title and engram fields.
2. **Title** — how many times does the term appear as a whole word? Compare against the top 3. Below average = clear lever. Already at parity = move on.
3. **Title leading position** — is the term in the first 2-3 words? Important for the engram analyzer.
4. **Tags** — how many of the 5 allowed tags contain the term or close variants? Compare against competitors. Adding the term to a tag is free.
5. **Short description** — BM25 saturated tf for the term. Short, focused, query-rich descriptions outperform long generic ones because BM25 normalizes for length.
6. **Description body** — only matters if egregiously low. Most plugins are saturated here.
7. **Function score factors** — installs, rating, recency, support resolution. These decide ranking *within a text-relevance tier*. If the user's text relevance is roughly tied with competitors but they're ranked below, this is the bottleneck.

### Step 5: Sanity-check via function score

Use `scripts/function_score.py` to compute approximate function-score components for each plugin in the top 10 and the user's plugin. If the math says the user *should* rank higher than they do based on installs/rating/recency/support, the gap is in text relevance (likely an effect not fully captured by your readme analysis — see "edge cases" below).

### Step 6: Decide whether to pull search volume data

This is the only optional external call. **Only pull DataForSEO volumes when the analysis suggests the user should consider pivoting their title/positioning to a different but related term.** For example:

- They're ranked #11 on a saturated term and #5 on a related smaller term — should they reposition?
- The recommended title change would weaken their position on the original term to gain on a related one.

In those cases, call `dataforseo:dataforseo_labs_google_keyword_overview` with the relevant variations to ground the recommendation in real volume data. Otherwise skip it — it adds noise.

For everything else (rating fixes, support resolution, density tweaks within the same term), don't bother with volume data.

### Step 7: Write the response

Output format: **inline conversational analysis, not a report**. Match the tone of an experienced SEO consultant explaining things to a competent operator. The structure that works:

1. **Headline finding** — one sentence on the primary cause of the gap.
2. **Comparison table** — top 3 competitors vs the user on the relevant signals (only the signals that matter for this SERP).
3. **Walkthrough** — paragraphs explaining the gap, with specific numbers from the analysis.
4. **Action list** — ranked by impact, with effort estimates. Each item should be concrete enough that the user can act on it without further questions.
5. **What not to do** — explicitly call out things that look like good ideas but aren't (e.g. "don't stuff more of the term into your description — you're already at saturation").

Use markdown sparingly: headers, one comparison table, and prose. No bullet-point soup. Match the style of the gallery/lightbox analyses in the conversation history.

## Things to watch for

**BM25 saturation is real.** Stop suggesting "add more of the term to the description" once tf is above ~10 in the body. The math says it doesn't help. Length normalization actively penalizes longer docs.

**Title length penalty exists but is small.** Going from a 30-char title to an 80-char title to fit 3× the term is usually net positive. Going to 120+ chars to fit 5× is usually net negative.

**WordPress's production algorithm has been tweaked beyond what's in the public GitHub `trunk`.** When your function score math says someone should rank higher than they do, acknowledge uncertainty — there are likely hidden quality signals (rating-recency, review velocity, etc.) that the public code doesn't fully expose.

**Reindexing takes 12–48 hours.** When users make changes, the API may show stale data. Trust the live UI ranking they're seeing. After a release, the index refreshes faster than it does for just a readme edit.

**Tag limit is 5.** WP.org uses only the first 5 even if more are listed. Always confirm with the user which 5 are being indexed before suggesting tag swaps.

**Don't recommend changing the slug.** Plugin slugs are immutable for established plugins (you'd lose all installs). Work around slug deficiencies via title and tags.

**Rating recovery is a multi-quarter project.** When rating is the bottleneck, set expectations honestly — it's not a 1-week fix.

## Edge cases

**The user's plugin isn't on page 1 at all.** Be honest: the gap may be too large for incremental changes. Look at the top 3 anyway, but flag that closing it would require a major repositioning, not a tag tweak.

**The user is at #1 already.** Pivot to defense: what's the closest competitor, what advantages do they have, what would they need to change to overtake. Also note quality risks (e.g. low recency means they're vulnerable to a competitor shipping a release).

**Multi-word search terms.** The algorithm tokenizes and scores each term independently then combines — so for "image gallery" you're looking at how each plugin scores on "image" AND on "gallery", with phrase bonuses for adjacency in title.engram. Run the analysis for both terms separately if useful.

**The plugin slug is a compound word containing the term.** E.g. `wpforms-lite` for "forms". The Elasticsearch n-gram/edge-ngram analyzer partially recovers credit for this — it's not zero, but it's not the full clean-token ×5 boost either. Note this in your analysis.

**Different SERP for same term page 1 vs API call.** WP.org caches search results behind a CDN; the API and the user-facing UI sometimes diverge by 12–48 hours after content changes. Trust what the user sees in the live UI.

## Reference files

- `references/algorithm.md` — Full breakdown of `class-plugin-search.php` scoring components, with the actual code references and what each modifier does.
- `scripts/analyze.py` — Pulls readmes, computes BM25, generates the comparison data.
- `scripts/function_score.py` — Computes approximate function-score multipliers across the SERP so you can see which signals are doing the work.
