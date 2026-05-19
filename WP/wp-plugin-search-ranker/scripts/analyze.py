#!/usr/bin/env python3
"""
Analyze a WP.org plugin SERP for a given search term.

Pulls top-N SERP data, parses competitor readmes, computes BM25-saturated
term frequencies across title/excerpt/description/tags, and outputs a
structured comparison.

Usage:
    python3 analyze.py --term "page builder" --user-slug elementor \\
        --serp /tmp/serp.json --readmes-dir /tmp/readmes
"""

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

K1 = 1.2
B = 0.75


def clean_html_entities(s):
    """Strip basic HTML entities and tags."""
    if not s:
        return ""
    s = re.sub(r"&#8211;", "–", s)
    s = re.sub(r"&amp;", "&", s)
    s = re.sub(r"&#8217;", "'", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def parse_readme(text):
    """
    Parse a WP.org readme.txt into structured fields.

    Returns {title, tags, contributors, short_description, description, all_sections}
    """
    lines = text.split("\n")
    title = ""
    header_start = 0
    for i, line in enumerate(lines):
        m = re.match(r"^===\s*(.+?)\s*===\s*$", line)
        if m:
            title = m.group(1)
            header_start = i
            break

    # Parse header metadata block
    tags = []
    contributors = []
    i = header_start + 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            i += 1
            break
        m = re.match(r"^([A-Za-z\s]+):\s*(.+)$", line)
        if m:
            field = m.group(1).strip().lower()
            value = m.group(2).strip()
            if field == "tags":
                tags = [t.strip() for t in value.split(",")]
            elif field == "contributors":
                contributors = [c.strip() for c in value.split(",")]
            i += 1
            continue
        break

    # Short description: lines until first == Section ==
    short_desc_lines = []
    while i < len(lines):
        line = lines[i]
        if re.match(r"^==\s*(.+?)\s*==\s*$", line):
            break
        short_desc_lines.append(line)
        i += 1
    short_desc = "\n".join(short_desc_lines).strip()

    # Section parsing
    sections = {}
    current = None
    current_lines = []
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^==\s*(.+?)\s*==\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(current_lines).strip()
            current = m.group(1).lower()
            current_lines = []
        else:
            current_lines.append(line)
        i += 1
    if current is not None:
        sections[current] = "\n".join(current_lines).strip()

    return {
        "title": title,
        "tags": tags,
        "contributors": contributors,
        "short_description": short_desc,
        "description": sections.get("description", ""),
        "all_sections": sections,
    }


def word_count(text):
    return len(re.findall(r"\w+", text))


def term_freq(text, term):
    """Count whole-word matches (case-insensitive) of a single term."""
    if not text:
        return 0
    return len(re.findall(rf"\b{re.escape(term.lower())}\b", text.lower()))


def stem_match_count(text, term):
    """Loose stem-aware count (also catches plurals: gallery/galleries)."""
    if not text:
        return 0
    # Match term or term+s or term+es or term-ies-style
    pattern = rf"\b{re.escape(term.lower())}(s|es|ies)?\b"
    return len(re.findall(pattern, text.lower()))


def bm25_tf(tf, dl, avgdl):
    """BM25 saturated term-frequency contribution."""
    if tf <= 0 or dl <= 0 or avgdl <= 0:
        return 0.0
    return (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * (dl / avgdl)))


def slug_clean_token(slug, term):
    """True if 'term' appears as a clean dash-separated segment in the slug."""
    return term.lower() in slug.lower().split("-")


def slug_substring(slug, term):
    """True if term appears as a substring (e.g. 'forms' inside 'wpforms')."""
    return term.lower() in slug.lower()


def title_leading_position(title, term):
    """Position (1-indexed) of first occurrence of term in title's word list, or 0."""
    words = re.findall(r"\w+", title.lower())
    for i, w in enumerate(words):
        if w == term.lower():
            return i + 1
    return 0


def fetch_readme_or_skip(slug, readmes_dir):
    """Try to load a readme from the directory; return parsed dict or None."""
    p = Path(readmes_dir) / f"{slug}.txt"
    if not p.exists():
        return None
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        return None
    # Detect 404 HTML response
    if "<title>404" in text[:500] or "Not Found" in text[:500]:
        return None
    if len(text) < 200:
        return None
    return parse_readme(text)


def analyze(term, user_slug, serp_path, readmes_dir, top_n=10):
    with open(serp_path) as f:
        serp = json.load(f)

    plugins = serp.get("plugins", [])

    # Locate user position
    user_rank = None
    for i, p in enumerate(plugins, 1):
        if p.get("slug") == user_slug:
            user_rank = i
            break

    # Top N + user (if outside top N)
    top_slugs = [p["slug"] for p in plugins[:top_n]]
    target_slugs = list(top_slugs)
    if user_slug not in target_slugs:
        target_slugs.append(user_slug)

    # Load readmes
    readmes = {}
    for slug in target_slugs:
        r = fetch_readme_or_skip(slug, readmes_dir)
        if r is not None:
            readmes[slug] = r

    # Compute avgdl across loaded readmes
    desc_lens = {s: word_count(r["description"]) for s, r in readmes.items()}
    sd_lens = {s: word_count(r["short_description"]) for s, r in readmes.items()}
    avg_desc = sum(desc_lens.values()) / max(1, len(desc_lens))
    avg_sd = sum(sd_lens.values()) / max(1, len(sd_lens))

    # Per-plugin metrics
    rows = []
    for i, p in enumerate(plugins[:top_n], 1):
        slug = p["slug"]
        r = readmes.get(slug, {})
        title = clean_html_entities(p.get("name", ""))

        desc = r.get("description", "")
        sd = r.get("short_description", "")
        tags = r.get("tags", [])

        title_tf = term_freq(title, term)
        title_stem = stem_match_count(title, term)
        slug_clean = slug_clean_token(slug, term)
        slug_sub = slug_substring(slug, term)
        title_pos = title_leading_position(title, term)
        sd_tf = term_freq(sd, term)
        desc_tf = term_freq(desc, term)
        tag_hits = sum(1 for t in tags if term.lower() in t.lower())

        rows.append({
            "rank": i,
            "slug": slug,
            "title": title,
            "title_len": len(title),
            "title_tf": title_tf,
            "title_tf_stem": title_stem,
            "title_leading_pos": title_pos,
            "slug_clean_token": slug_clean,
            "slug_substring": slug_sub,
            "tags": tags,
            "tag_hits": tag_hits,
            "sd_words": sd_lens.get(slug, 0),
            "sd_tf": sd_tf,
            "sd_bm25": bm25_tf(sd_tf, sd_lens.get(slug, 0), avg_sd),
            "desc_words": desc_lens.get(slug, 0),
            "desc_tf": desc_tf,
            "desc_bm25": bm25_tf(desc_tf, desc_lens.get(slug, 0), avg_desc),
            "active_installs": p.get("active_installs", 0),
            "rating": p.get("rating", 0),
            "num_ratings": p.get("num_ratings", 0),
            "last_updated": p.get("last_updated", ""),
            "tested": p.get("tested", ""),
            "support_threads": p.get("support_threads", 0),
            "support_resolved": p.get("support_threads_resolved", 0),
        })

    # If user is outside top_n, append separately
    user_row = None
    if user_rank and user_rank > top_n:
        p = plugins[user_rank - 1]
        slug = p["slug"]
        r = readmes.get(slug, {})
        title = clean_html_entities(p.get("name", ""))
        desc = r.get("description", "")
        sd = r.get("short_description", "")
        tags = r.get("tags", [])
        user_row = {
            "rank": user_rank,
            "slug": slug,
            "title": title,
            "title_tf": term_freq(title, term),
            "title_tf_stem": stem_match_count(title, term),
            "title_leading_pos": title_leading_position(title, term),
            "slug_clean_token": slug_clean_token(slug, term),
            "slug_substring": slug_substring(slug, term),
            "tags": tags,
            "tag_hits": sum(1 for t in tags if term.lower() in t.lower()),
            "sd_words": sd_lens.get(slug, 0),
            "sd_tf": term_freq(sd, term),
            "sd_bm25": bm25_tf(term_freq(sd, term), sd_lens.get(slug, 0), avg_sd),
            "desc_words": desc_lens.get(slug, 0),
            "desc_tf": term_freq(desc, term),
            "desc_bm25": bm25_tf(term_freq(desc, term), desc_lens.get(slug, 0), avg_desc),
            "active_installs": p.get("active_installs", 0),
            "rating": p.get("rating", 0),
            "num_ratings": p.get("num_ratings", 0),
            "last_updated": p.get("last_updated", ""),
            "tested": p.get("tested", ""),
            "support_threads": p.get("support_threads", 0),
            "support_resolved": p.get("support_threads_resolved", 0),
        }

    return {
        "term": term,
        "user_slug": user_slug,
        "user_rank": user_rank,
        "total_results": serp.get("info", {}).get("results", 0),
        "avg_desc_words": avg_desc,
        "avg_sd_words": avg_sd,
        "rows": rows,
        "user_row_outside_top_n": user_row,
    }


def print_report(result):
    print(f"\n{'='*90}")
    print(f"SERP analysis — term: '{result['term']}' (total results: {result['total_results']:,})")
    print(f"User plugin: {result['user_slug']}  |  rank: {result['user_rank'] or 'NOT FOUND'}")
    print(f"{'='*90}\n")

    print("TEXT RELEVANCE — Title, Slug, Tags")
    print(f"{'#':>2} {'slug':<32} {'title_tf':>9} {'lead':>4} {'slug_clean':>10} {'tag_hits':>8}")
    print("-" * 80)
    for r in result["rows"]:
        marker = " ★" if r["slug"] == result["user_slug"] else ""
        clean = "✓" if r["slug_clean_token"] else ("~" if r["slug_substring"] else "✗")
        print(f"{r['rank']:>2} {r['slug'][:32]:<32} {r['title_tf']:>9} {r['title_leading_pos']:>4} {clean:>10} {r['tag_hits']:>8}{marker}")

    if result["user_row_outside_top_n"]:
        r = result["user_row_outside_top_n"]
        clean = "✓" if r["slug_clean_token"] else ("~" if r["slug_substring"] else "✗")
        print(f"{r['rank']:>2} {r['slug'][:32]:<32} {r['title_tf']:>9} {r['title_leading_pos']:>4} {clean:>10} {r['tag_hits']:>8} ★")

    print(f"\nBM25 FIELDS (avg desc = {result['avg_desc_words']:.0f} words, avg short = {result['avg_sd_words']:.0f} words)")
    print(f"{'#':>2} {'slug':<32} {'sd_tf':>5} {'sd_BM25':>8} {'desc_tf':>7} {'desc_BM25':>10}")
    print("-" * 80)
    for r in result["rows"]:
        marker = " ★" if r["slug"] == result["user_slug"] else ""
        print(f"{r['rank']:>2} {r['slug'][:32]:<32} {r['sd_tf']:>5} {r['sd_bm25']:>8.3f} {r['desc_tf']:>7} {r['desc_bm25']:>10.3f}{marker}")
    if result["user_row_outside_top_n"]:
        r = result["user_row_outside_top_n"]
        print(f"{r['rank']:>2} {r['slug'][:32]:<32} {r['sd_tf']:>5} {r['sd_bm25']:>8.3f} {r['desc_tf']:>7} {r['desc_bm25']:>10.3f} ★")

    print(f"\nQUALITY SIGNALS")
    print(f"{'#':>2} {'slug':<32} {'installs':>9} {'rating':>7} {'updated':>11} {'supp_res':>9}")
    print("-" * 80)
    for r in result["rows"]:
        marker = " ★" if r["slug"] == result["user_slug"] else ""
        lu = r["last_updated"][:10] if r["last_updated"] else ""
        supp = f"{r['support_resolved']}/{r['support_threads']}"
        print(f"{r['rank']:>2} {r['slug'][:32]:<32} {r['active_installs']:>9,} {r['rating']:>5}/100 {lu:>11} {supp:>9}{marker}")
    if result["user_row_outside_top_n"]:
        r = result["user_row_outside_top_n"]
        lu = r["last_updated"][:10] if r["last_updated"] else ""
        supp = f"{r['support_resolved']}/{r['support_threads']}"
        print(f"{r['rank']:>2} {r['slug'][:32]:<32} {r['active_installs']:>9,} {r['rating']:>5}/100 {lu:>11} {supp:>9} ★")

    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--term", required=True, help="Search term to analyze")
    ap.add_argument("--user-slug", required=True, help="User's plugin slug")
    ap.add_argument("--serp", required=True, help="Path to SERP JSON from WP.org API")
    ap.add_argument("--readmes-dir", required=True, help="Directory containing <slug>.txt readme files")
    ap.add_argument("--top-n", type=int, default=10, help="How many top results to analyze")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of human-readable")
    args = ap.parse_args()

    result = analyze(args.term, args.user_slug, args.serp, args.readmes_dir, args.top_n)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
