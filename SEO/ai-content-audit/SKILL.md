---
name: ai-content-audit
description: Audit web pages or text content for the 7 critical AI content SEO issues that cause poor rankings. Use this skill whenever the user wants to audit a page, blog post, article, or block of text for AI-generated content problems, SEO quality issues, or ranking improvements. Trigger on phrases like "audit this page", "why isn't this ranking", "check my content", "AI content review", "SEO audit", "content audit", "debug my content", "what's wrong with my post", "improve my rankings", or any URL or text block the user wants evaluated for AI content quality. Also trigger when the user mentions poor search performance, low clicks, high bounce rate, or generic AI writing.
---

# AI Content SEO Audit Skill

Audits a web page or block of text against 7 critical AI content issues that cause poor search rankings (based on the Noel Ceta framework). Produces a detailed before/after audit report as a styled HTML file.

## Input Handling

The user will provide ONE of:
1. **A URL** — Scrape it first, then audit the content
2. **A block of text** — Audit it directly

### If the input is a URL:

1. Use `web_fetch` to retrieve the page content as markdown
2. Save the raw scraped content to a writable workspace file such as `.skill-state/ai-content-audit/scraped-content.md`
3. Proceed to the audit

### If the input is text:

1. Save the provided text to a writable workspace file such as `.skill-state/ai-content-audit/scraped-content.md`
2. Proceed to the audit

## The 7-Issue Audit Framework

Score each issue from 1 (severe problem) to 5 (no issues found). For each issue, provide:
- **Score** (1-5)
- **What was found** — specific examples pulled from the actual content
- **Before** — quote or describe the problematic pattern in the content
- **After** — write a concrete rewritten/improved version
- **Impact** — what fixing this will likely improve

### Issue #1: Generic Introductions

**What to look for:**
- Opens with "In today's [digital landscape/world/era]..."
- Uses "has become increasingly important" or similar filler
- Contains "This comprehensive/ultimate/complete guide will..."
- First paragraph could apply to any article on any topic
- No hook, no data point, no story, no contrarian angle

**Scoring:**
- 1 = Classic AI opener, completely generic
- 3 = Has some specificity but still template-feeling
- 5 = Opens with a specific hook, data point, story, or contrarian statement

**Fix pattern:** Replace with a specific data point, contrarian statement, personal anecdote, or case study result. The intro should be impossible to reuse on another article.

---

### Issue #2: Wikipedia-Style Structure

**What to look for:**
- Follows the pattern: What is X → Why X Matters → Benefits of X → How to X → Best Practices → Conclusion
- H2s read like a table of contents for a textbook
- Structure doesn't match user intent (e.g., a how-to query that starts with definitions)
- Predictable, formulaic heading progression

**Scoring:**
- 1 = Exact Wikipedia/textbook pattern
- 3 = Some structural variation but still predictable
- 5 = Structure matches user journey and intent perfectly

**Fix pattern:** Restructure based on user intent:
- How-to queries → start with the process immediately
- Problem-solving → symptoms → diagnosis → solution
- Comparison → direct comparison first, context after

---

### Issue #3: No E-E-A-T Signals

**What to look for:**
- No first-person experience markers ("In our testing...", "We found that...")
- No author credentials or bio
- No screenshots, original data, or case study references
- No mention of specific tools used, clients served, or experiments run
- Content reads as theoretical/encyclopedic rather than experiential

**Scoring:**
- 1 = Zero experience signals, reads like a Wikipedia summary
- 3 = Some experience markers but feel bolted-on
- 5 = Rich with genuine experience, credentials, and original data

**Fix pattern:** Add experience markers throughout:
- "In our analysis of [N] campaigns..."
- "When we tested this with [specific client/project]..."
- Add author bio with relevant credentials
- Reference specific screenshots, tools, or datasets

---

### Issue #4: Statistical Averages Problem (No Unique Perspective)

**What to look for:**
- Advice is middle-ground, safe, and uncontroversial
- No original frameworks, methodologies, or named approaches
- No contrarian angles or surprising takes
- Could have been written by averaging the top 10 results
- No proprietary data, unique constraints, or specific context

**Scoring:**
- 1 = Pure average advice, nothing original
- 3 = Some unique angles but mostly conventional wisdom
- 5 = Clear original framework, contrarian takes, or proprietary insights

**Fix pattern:**
- Name an original methodology (e.g., "our 3-layer framework")
- Add contrarian angles that challenge conventional wisdom
- Include proprietary data or specific constraints
- Share what worked AND what didn't

---

### Issue #5: Keyword Stuffing Patterns

**What to look for:**
- Target keyword appears unnaturally frequently (more than ~5 times per 1000 words)
- Keyword placed in ways that feel forced or robotic
- Same exact phrase repeated instead of using synonyms/variations
- Obvious optimization patterns that break reading flow
- Lack of semantic variety (related terms, synonyms, natural language variations)

**Scoring:**
- 1 = Blatant keyword stuffing (10+ unnatural uses)
- 3 = Moderate overuse, some variety
- 5 = Natural keyword usage with rich semantic variation

**Fix pattern:**
- Use target keyword 3-5 times naturally
- Replace excess occurrences with synonyms and related terms
- Focus on semantic relevance over exact-match density
- Read paragraphs aloud — if they sound forced, rewrite

---

### Issue #6: Missing Internal Linking Strategy

**What to look for:**
- No internal links at all
- Only generic "learn more" or "click here" links
- No contextual links woven into the narrative
- No evidence of hub-spoke or topic cluster architecture
- Links don't use descriptive anchor text

**Scoring:**
- 1 = Zero internal links or only generic ones
- 3 = Some links but no strategic structure
- 5 = 3-5+ contextual internal links with clear topic cluster strategy

**Fix pattern:**
- Add 3-5 contextual internal links per post
- Use hub-spoke model: main pillar page links to subtopic pages
- Use descriptive anchor text (not "click here")
- Create interlinked topic clusters

---

### Issue #7: No User Engagement Signals

**What to look for:**
- Wall of text with no visual breaks
- No images, diagrams, or media
- No interactive elements (calculators, tools, quizzes)
- Paragraphs longer than 3-4 sentences
- No bold/highlighted key takeaways
- No discussion prompts or CTAs throughout the content
- No bullet points or numbered lists for scannable sections

**Scoring:**
- 1 = Pure text wall, zero engagement elements
- 3 = Some formatting but still text-heavy
- 5 = Rich with visuals, formatting, scannable sections, and interactive elements

**Fix pattern:**
- Add images/diagrams every 300-400 words
- Keep paragraphs to 2-3 sentences max
- Bold key takeaways
- Add discussion prompts or questions throughout
- Include calculators, tools, or interactive elements where relevant

---

## Output: HTML Audit Report

Generate a single, self-contained HTML file styled as a professional audit report. Save it to a user-visible workspace path such as `outputs/ai-content-audit-report.html`.

### Report Structure

```
AI Content SEO Audit Report
├── Header: page title/URL, audit date, overall score
├── Executive Summary: overall health, top 3 priorities
├── Score Dashboard: visual overview of all 7 scores
├── Issue-by-Issue Breakdown (×7):
│   ├── Issue title + score badge (color-coded)
│   ├── What We Found (specific examples from the content)
│   ├── Before (actual content or pattern found)
│   ├── After (concrete rewrite suggestion)
│   └── Expected Impact
├── Priority Action Plan: ordered list of fixes by impact
└── Footer: methodology credit, timestamp
```

### Styling Guidelines

- Use a clean, professional design with good typography
- Color-code scores: 1-2 = red (#e74c3c), 3 = amber (#f39c12), 4-5 = green (#27ae60)
- Use before/after blocks with distinct visual treatment (red-tinted before, green-tinted after)
- Make it print-friendly
- Single file, no external dependencies (inline all CSS)
- Use system fonts for maximum compatibility
- Overall score is the average of all 7 issue scores, displayed prominently

### Before/After Block Format

Each issue's before/after should be formatted as:

```
┌─ BEFORE ──────────────────────────────────┐
│ [Quoted or described problematic content]  │
└───────────────────────────────────────────┘

┌─ AFTER ───────────────────────────────────┐
│ [Concrete rewritten/improved version]     │
└───────────────────────────────────────────┘
```

Use actual CSS-styled boxes, not ASCII art. The "Before" box should have a light red background, the "After" box a light green background.

## Workflow Summary

1. Receive URL or text from user
2. If URL → scrape with `web_fetch`, save to local file
3. If text → save to local file
4. Read saved content
5. Analyze content against all 7 issues
6. Score each issue 1-5
7. Write specific before/after examples for each issue using ACTUAL content from the page
8. Generate priority action plan (quick wins first)
9. Build HTML audit report
10. Save and present to user via `present_files`

## Critical Rules

- **Always use real content from the page** in the "Before" examples. Never invent generic examples.
- **Always write concrete rewrites** in the "After" examples. Never give vague advice.
- **Be honest with scores.** Don't inflate them to be nice.
- **Prioritize the action plan** by effort-to-impact ratio: intro rewrites (5 min) → keyword cleanup (15 min) → structural changes (30 min) → E-E-A-T additions (45 min).
- **The report must be immediately actionable.** Someone should be able to hand it to a content editor and have them implement every fix.
