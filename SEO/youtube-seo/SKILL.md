---
name: youtube-seo
description: >
  Use for YouTube SEO planning, publishing, and audits. Trigger on video search visibility,
  titles, thumbnails, descriptions, captions, transcripts, retention, companion pages,
  VideoObject schema, distribution, or conversion measurement.
version: 1.0.0
author: Hermes Agent
license: MIT
source: "https://x.com/noelcetaseo/status/2091956237252407772"
metadata:
  hermes:
    tags: [youtube, video-seo, search, content, schema, analytics]
---

# YouTube SEO

Turn a search opportunity into a useful, discoverable YouTube video and supporting on-site content package, then measure whether it creates audience or business value.

This method is informed by Noel Ceta's public YouTube SEO thread from 24 August 2026. The thread is practitioner guidance, not an official Google or YouTube ranking specification. Treat causal claims and case studies as hypotheses until supported by current official documentation, live search results, or first-party data.

## When to use

Use this skill for:

- planning a video intended to rank in YouTube or Google Search;
- optimizing a video's title, description, thumbnail, captions, transcript, metadata, playlist placement, or retention structure;
- publishing a companion page with an embedded video and `VideoObject` structured data;
- auditing an existing video or video-led campaign; or
- turning one video into reusable website, email, product, documentation, social, and follow-on video assets.

Do not use this method as proof that video alone improves rankings. Evaluate query intent, audience fit, content quality, technical implementation, distribution, and measurement together.

## Required inputs

Collect or state assumptions for:

1. Audience and search problem.
2. Primary query and supporting query cluster.
3. Desired result after watching.
4. Video format and planned duration.
5. YouTube channel and destination page.
6. Call to action and measurable conversion event.
7. Distribution paths beyond YouTube.
8. Baseline performance, measurement window, success threshold, and stop-or-iterate threshold.
9. Available evidence: current search results, first-party analytics, audience language, and official documentation.

If only a topic is supplied, research intent and current results before recommending production.

## Evidence standard

Label evidence as one of:

- **Current platform evidence:** live Google or YouTube results and current official documentation.
- **First-party evidence:** YouTube Analytics, website analytics, conversions, support questions, interviews, or surveys.
- **Practitioner guidance:** useful hypotheses from the source thread or other experts.
- **Assumption:** anything not yet verified.

Do not present these practitioner claims as settled facts:

- Video is categorically a Google ranking factor.
- A description over a particular word count is inherently better.
- Thumbnail click-through rate directly causes Google rankings.
- One video format always ranks better than another.
- A reported case-study result is generally reproducible.

## Completion gate

Before calling a plan complete, define all of:

- **Audience:** the specific viewer segment.
- **Desired result:** what viewers can do or decide after watching.
- **Evidence:** why the topic, query, and format deserve investment.
- **Distribution:** the relevant channels beyond the upload itself.
- **Call to action:** the next step and how it will be recorded.
- **Measurement window:** when leading and business outcomes will be reviewed.
- **Success threshold:** the result that justifies continuing or scaling.
- **Stop-or-iterate threshold:** the result that triggers a title, thumbnail, hook, distribution, offer, or topic change.

Views, impressions, rankings, and subscribers are intermediate signals, not the final result.

## Workflow

### 1. Qualify the opportunity

1. Define the audience, problem, search intent, and desired result.
2. Inspect current Google and YouTube results for the target query.
3. Determine whether video is prominent in the results or genuinely useful for the intent.
4. Prefer a format that directly satisfies the query, such as:
   - how-to or tutorial;
   - case study or demonstrated result;
   - expert interview where authority matters; or
   - data visualization for a complex topic.
5. Deprioritize vague education, generic livestreams, and low-intent vlogs unless current results or first-party data support them.
6. Record a baseline: rankings, impressions, clicks, traffic, average view duration, conversions, and relevant on-page engagement.

**Decision rule:** Do not produce a video merely to satisfy a publishing cadence. The topic should support a useful video, a credible distribution path, and a measurable next action.

### 2. Design the content package

Plan a package rather than a standalone upload:

- YouTube video.
- Corrected captions.
- Full transcript.
- Companion article or landing page with a native embed.
- Useful links between YouTube and the companion page.
- `VideoObject` structured data on the canonical embed page.
- Thumbnail variants.
- Playlist placement and next-video path.
- Reuse plan for email, product pages, documentation, social clips, or sales material where appropriate.

A single video may serve search, a product page, and lifecycle email when those placements support the same audience journey. Adapt the message and call to action for each placement rather than duplicating it blindly.

### 3. Write the title

Use this as a starting pattern, not a mandatory format:

```text
[Primary topic] | [Benefit or outcome] | [Brand]
```

Examples:

- `Email Automation Tutorial | Save Time on Follow-ups | [Brand]`
- `Technical SEO Basics | A Practical Beginner Guide | [Brand]`
- `Reduce Acquisition Cost | Step-by-Step Case Study | [Brand]`

Check that the title:

- accurately reflects the video;
- places the primary topic early when natural;
- gives a concrete reason to click;
- avoids stuffing, unsupported claims, and empty superlatives; and
- fits the channel's voice without sacrificing clarity.

### 4. Script for satisfaction and retention

- State the topic and payoff immediately; test a first-three-seconds hook when appropriate.
- Deliver useful evidence early instead of withholding it.
- Use chapters or clear segments for longer videos.
- Add purposeful visual changes or demonstrations, not arbitrary distraction.
- Remove slow intros and irrelevant biography.
- End with one next action: a companion resource, product action, conversion, or next video.
- Make the call to action a natural continuation of the result viewers achieved.

### 5. Create and test the thumbnail

Start with these principles:

- high contrast at small size;
- a face or emotion only when authentic and suitable for the channel;
- short, legible text conveying the topic or outcome;
- consistent visual identity; and
- controlled variant testing.

Validate at mobile thumbnail size. Avoid repeating the full title, clutter, deceptive imagery, and tiny text.

### 6. Publish complete YouTube metadata

For the video:

- Set visibility to **Public** when open organic discovery is the goal.
- Use an accurate title and useful description.
- Select the most relevant category.
- Add the video to relevant playlists with clear titles.
- Use a small set of relevant tags if useful; do not expect tags to compensate for weak content.
- Configure chapters, end screens, cards, and the next intentional asset where appropriate.
- Moderate and answer substantive comments.

For the channel:

- Keep its name, description, branding, and topical focus clear.
- Organize related videos into useful playlists.
- Do not rely on channel-level keyword stuffing.

### 7. Write the description

Use this structure:

1. **Hook:** what viewers will learn and why it matters.
2. **Outline:** chapters or timestamps.
3. **Call to action:** one primary next step.
4. **Context:** natural terminology and relevant links.
5. **Transcript path:** link to the full transcript or companion page when useful.

The source suggests a long description. Treat length as a drafting prompt, not a ranking requirement. Prefer complete, useful copy over padding.

### 8. Correct captions and publish the transcript

Use this quality order:

```text
auto-generated captions < corrected captions < corrected captions plus a useful transcript
```

- Correct names, product terms, technical vocabulary, punctuation, and timing.
- Make the transcript accessible and indexable on the companion page when useful.
- Structure the page with headings, examples, links, and the embedded video; do not publish an unreadable text dump.
- Keep video, captions, transcript, and page claims aligned.

### 9. Publish the companion page and links

- Create a page that satisfies the same intent in text and video.
- Embed the video instead of providing only a link.
- Place the embed where visitors can encounter it without unnecessary friction.
- Link to the companion page from the YouTube description when useful.
- Link to the video or channel from the companion page when it helps visitors.
- Do not claim that reciprocal links automatically transfer meaningful cross-domain authority; measure discovery and conversions.

### 10. Add `VideoObject` structured data

Start with this template, then validate it against current Schema.org and Google documentation before publishing:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "<video title>",
  "description": "<video description>",
  "duration": "PT5M30S",
  "uploadDate": "<YYYY-MM-DD>",
  "thumbnailUrl": "<absolute thumbnail URL>",
  "url": "<canonical video URL>"
}
</script>
```

Check that:

- values describe the visible embedded video;
- URLs are absolute and crawlable;
- duration uses ISO 8601;
- dates are valid and accurate;
- required and recommended properties match current official guidance; and
- markup validates before release.

### 11. Distribute and reuse

Choose channels based on audience evidence, not convenience:

- companion article or product page;
- subscriber or lifecycle email;
- onboarding sequence;
- support or documentation;
- social clips pointing to the full resource;
- relevant communities or partners; and
- internal sales or support use.

For each channel, define the audience, message, call to action, tracking method, and timing.

### 12. Measure and iterate

Track three levels:

**Discovery**

- impressions;
- Google and YouTube query visibility;
- title and thumbnail click-through rate; and
- traffic sources.

**Consumption**

- average view duration and percentage viewed;
- retention curve and early drop-offs;
- chapter usage; and
- meaningful comments or repeat viewing.

**Audience or business result**

- companion-page visits;
- call-to-action clicks;
- qualified leads, trials, installs, purchases, or support deflection; and
- attributable or assisted conversions where measurement allows.

Use a predeclared review window. Review creative and distribution after enough impressions to avoid reacting to noise, then review downstream outcomes after the normal conversion cycle. Do not invent universal numeric benchmarks.

Iterate in this order:

1. Verify distribution and indexing.
2. If impressions exist but click-through rate is weak, test title and thumbnail alignment.
3. If click-through rate is healthy but early retention collapses, revise the opening and expectation match.
4. If viewing is healthy but conversions are weak, improve the offer, call to action, destination, or topic-to-offer fit.
5. If qualified reach remains negligible, reassess demand, intent, competition, and channel fit before making a full remake.

## Audit output template

```markdown
# YouTube SEO audit: <video>

## Bottom line
- Result:
- Highest-leverage change:
- Main uncertainty:

## Strategy
- Audience:
- Search problem and query:
- Desired result:
- Evidence and current search-result pattern:
- Format fit:

## Asset audit
- Title:
- Thumbnail:
- Hook and retention structure:
- Description:
- Captions and transcript:
- Channel, category, tags, and playlists:
- Companion page, embed, and links:
- VideoObject validation:

## Distribution and conversion
- Distribution paths:
- Call to action and conversion event:
- Tracking:

## Measurement
- Baseline:
- Window:
- Success threshold:
- Stop-or-iterate threshold:

## Prioritized actions
1. ...
2. ...
3. ...

## Evidence and caveats
- Official and current sources:
- First-party sources:
- Practitioner guidance:
- Missing or unverified:
```

## Acceptance checklist

- [ ] Audience, query, intent, and desired result are explicit.
- [ ] Live results or first-party evidence justify video as the format.
- [ ] Title is accurate, specific, and compelling without overpromising.
- [ ] Thumbnail is legible at small size and not deceptive.
- [ ] Opening quickly confirms the topic and payoff.
- [ ] Chapters or segments and a purposeful next action are present where useful.
- [ ] Description has a hook, timestamps, natural context, a call to action, and transcript path without padding.
- [ ] Captions are corrected and a useful transcript is available where appropriate.
- [ ] Visibility, category, playlists, and relevant metadata are complete.
- [ ] Companion page has a native embed and coherent linking.
- [ ] `VideoObject` matches the page and video and validates against current guidance.
- [ ] Distribution paths, conversion tracking, and owners are defined.
- [ ] Baseline, measurement window, success threshold, and stop-or-iterate threshold are recorded.
- [ ] Practitioner claims remain labelled and are not reported as verified platform facts.

## Anti-patterns

- Producing video because it is supposedly mandatory for SEO.
- Keyword-heavy titles with no credible viewer benefit.
- Padding descriptions to reach an arbitrary word count.
- Relying on uncorrected auto-captions for important or technical material.
- Publishing only on YouTube when a companion page would improve the audience journey.
- Embedding video without useful supporting text, accessibility, schema validation, or a call to action.
- Expecting generic livestreams or vlogs to rank for focused informational intent.
- Treating views, rankings, or watch time as the final result.
- Citing a practitioner case study as universal proof.
- Rewriting the whole video before checking title, thumbnail, indexing, distribution, and conversion fit.

## Source provenance

Primary public source:

- Noel Ceta, X thread root: https://x.com/noelcetaseo/status/2091956237252407772

The source's examples, causal claims, and reported outcomes are retained only as practitioner provenance. Verify current platform requirements and measure results independently before treating any claim as established or transferable.
