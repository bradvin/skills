# WordPress.org Plugin Directory Search Algorithm

Source: `wordpress.org/public_html/wp-content/plugins/plugin-directory/class-plugin-search.php` in the WordPress meta SVN repo.

This file is the public version. The production algorithm may have undocumented tweaks — when the math says someone should rank higher than they do, acknowledge that hidden signals likely exist.

## Architecture

The search uses Elasticsearch with a `function_score` query. The final score is:

```
score = BM25_text_score × function_score_multiplier
```

`function_score` factors combine via `boost_mode=multiply` for the decay functions and `score_mode=sum` for the field_value_factors within the inner block.

## Text scoring (BM25)

The query is a `bool` with `should` clauses across multiple fields, each with its own boost:

| Field | Boost | Notes |
|---|---|---|
| `slug` | ×5 | `most_fields` match. Whole-token match strongest. Compound slugs (e.g. `wpforms-lite` for "forms") get partial credit via engram. |
| `title` | ×5 | `most_fields`, shared with slug |
| `title.engram` | ×2 | Edge n-gram analyzer. Title-leading position helps. |
| `excerpt` (short description) | ×2 | `best_fields` |
| `description` | ×1 | `best_fields`. Length normalized — long docs penalized. |
| `taxonomy.plugin_tags.name` | ×2 | `best_fields`. Tags = first 5 listed in readme. |
| `taxonomy.plugin_category.name` | ×2 | Plugin categories (rarely useful) |
| `author` | ×3 | If author name contains the term — rare |
| `contributors` | ×3 | Same, for contributor profiles |

BM25 parameters: `k1=1.2`, `b=0.75` (ES defaults).

**BM25 saturation curve:**
```
tf*  = (tf × (k1 + 1)) / (tf + k1 × (1 - b + b × dl/avgdl))
```

Going from tf=1 to tf=2: ~+50% on this field's contribution.
Going from tf=2 to tf=3: ~+15%.
Going from tf=3 to tf=5: ~+10%.
Beyond tf=10: near zero marginal gain.

Length normalization (`b=0.75`) means longer docs need *more* occurrences to score the same density.

## Function score components

All multiplied/added to the BM25 score.

### 1. Recency (`plugin_modified` field)

```
exp_decay(offset=180d, scale=360d, decay=0.5)
```

- Updates within 180 days: full 1.0 multiplier
- Half-credit at 540 days (180 + 360) since last update
- This is the main "is the plugin maintained" signal

### 2. WP version compatibility (`tested` field)

```
exp_decay vs WP_CORE_STABLE_BRANCH
```

Penalizes plugins not tested against recent WP versions. Currently the live stable branch is ~7.0, so anything tested against 6.8 or earlier starts incurring decay.

### 3. Active installs (log)

```
field_value_factor(field=active_installs, modifier=log2p, factor=0.375)
= log2(installs + 2) × 0.375
```

A 10× install jump (10K → 100K) adds ~1.25 to this factor. Diminishing returns built in.

### 4. Sub-1M install booster

```
exp_decay(origin=1_000_000, scale=900_000, decay=0.75)
```

Plugins below 1M installs get an *additional* multiplicative boost that scales with how close they are to 1M:
- 1M installs: 1.0
- 500K installs: 0.85
- 100K installs: 0.75
- 10K installs: 0.71
- 1K installs: 0.69

This is why a 500K-install plugin can dramatically outrank a 50K-install plugin if other signals are equal.

### 5. Support resolution (log)

```
field_value_factor(field=support_threads_resolved, modifier=log2p, factor=0.25)
= log2(resolved + 2) × 0.25
```

Note: this is the **resolved count**, not the resolution rate. A plugin with 50 resolved threads scores higher than one with 5 resolved threads, even if the second has 100% resolution. But the field is also moderated by the function score combination — when raw counts are tied or close, resolution rate matters via implicit signal.

In practice, support_threads_resolved=0 is a noticeable penalty. Going from 0 to 2 resolved is a real lift.

### 6. Rating (sqrt)

```
field_value_factor(field=rating, modifier=sqrt, factor=0.25)
= sqrt(rating / 100) × 0.25  (when rating is 0-100)
```

- 100/100 rating: 0.25
- 90/100 rating: 0.237
- 80/100 rating: 0.224
- 70/100 rating: 0.209
- 50/100 rating: 0.177

Small absolute differences, but compounding multiplier across other factors makes this real when BM25 scores are tied. Also: ratings are a leading indicator of other quality signals not in the public algorithm.

## What's NOT in the public algorithm (but probably is in production)

These are observed effects that the public code doesn't fully explain:

1. **Recent ratings velocity** — plugins getting fresh positive reviews seem to climb faster than the static rating factor predicts.
2. **Active install growth rate** — gaining installs fast may signal momentum.
3. **Block-editor compatibility flags** — newer "block-ready" plugins seem to get a nudge.
4. **Featured/beta program lift** — plugins in featured collections, partner programs, or beta programs may get boosts.
5. **Spam / quality penalties** — plugins with policy violations get demoted.

When your math doesn't explain the ranking, the gap is likely in one of these hidden signals — most often rating or rating-recency.

## Practical leverage hierarchy

In rough order of "biggest impact per minute spent":

1. **Title** — clean tokens of the search term, leading position. ×5 boost.
2. **Tags (5 max)** — direct term inclusion. ×2 boost. Free to change.
3. **Short description** — high-density query-matching prose. ×2 boost.
4. **Rating recovery** — multi-quarter project, but the only way past a saturated text-relevance field.
5. **Resolved support threads** — close open ones. Free and fast.
6. **Release cadence** — keep updates under 180 days for full recency credit.
7. **Description body** — only matters if egregiously low on the term. Saturated for most plugins in the top 20.
8. **Slug** — immutable for shipped plugins. Don't recommend changing.

## Useful URL patterns

- SERP API: `https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request%5Bsearch%5D=TERM&request%5Bper_page%5D=15&request%5Bpage%5D=1`
- Single plugin info: `https://api.wordpress.org/plugins/info/1.0/SLUG.json`
- Readme SVN: `https://plugins.svn.wordpress.org/SLUG/trunk/readme.txt` (try `README.txt` if 404)
- Live SERP (blocked by robots.txt for scraping, but visible to user): `https://wordpress.org/plugins/search/TERM/`

## References

- Source code: `https://raw.githubusercontent.com/WordPress/wordpress.org/refs/heads/trunk/wordpress.org/public_html/wp-content/plugins/plugin-directory/class-plugin-search.php`
- Elasticsearch BM25 docs: standard `k1=1.2, b=0.75` apply.
