#!/usr/bin/env python3
"""
Compute approximate function_score components for each plugin in a SERP.

Useful for: "if this plugin has better quality signals than competitors above it,
the gap is in text relevance, not function score."

Usage:
    python3 function_score.py --serp /tmp/serp.json --user-slug elementor [--top-n 10]
"""

import argparse
import json
import math
from datetime import datetime, timezone


def recency_decay(date_str, today=None):
    """Exp decay with offset=180d, scale=360d, decay=0.5 (half-life)."""
    if not date_str:
        return 0.0, None
    if today is None:
        today = datetime.now(timezone.utc)
    # Parse "2026-05-14 10:51am GMT" or similar
    date_part = date_str.split()[0]
    try:
        d = datetime.fromisoformat(date_part).replace(tzinfo=timezone.utc)
    except Exception:
        return 0.0, None
    days = (today - d).days
    offset = 180
    scale = 360
    if days <= offset:
        return 1.0, days
    return 0.5 ** ((days - offset) / scale), days


def sub1m_boost(installs):
    """Sub-1M booster: exp decay origin=1M, scale=900K, decay=0.75."""
    origin = 1_000_000
    scale = 900_000
    diff = max(0, origin - installs)
    return 0.75 ** (diff / scale)


def install_log_factor(installs):
    """log2p with factor 0.375."""
    return math.log2(installs + 2) * 0.375


def rating_factor(rating):
    """sqrt(r/100) * 0.25 (rating is 0-100)."""
    if rating <= 0:
        return 0
    return math.sqrt(rating / 100) * 0.25


def support_factor(resolved):
    """log2p with factor 0.25."""
    return math.log2(resolved + 2) * 0.25


def compute_function_score(plugin, today=None):
    inst = plugin.get("active_installs", 0)
    rating = plugin.get("rating", 0)
    last_updated = plugin.get("last_updated", "")
    sr = plugin.get("support_threads_resolved", 0) or 0

    rec, days = recency_decay(last_updated, today)
    s1m = sub1m_boost(inst)
    ilg = install_log_factor(inst)
    rat = rating_factor(rating)
    sup = support_factor(sr)

    # Approximate combination: decay functions multiply, field_value_factors add
    # (Real algorithm uses boost_mode=multiply with score_mode=sum on field factors)
    summed_factors = 1 + ilg + rat + sup
    func_score = rec * s1m * summed_factors

    return {
        "recency": rec,
        "recency_days": days,
        "sub1m": s1m,
        "install_log": ilg,
        "rating_factor": rat,
        "support_factor": sup,
        "approx_function_score": func_score,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serp", required=True)
    ap.add_argument("--user-slug", required=True)
    ap.add_argument("--top-n", type=int, default=10)
    ap.add_argument("--today", help="ISO date for reproducible calculations")
    args = ap.parse_args()

    today = None
    if args.today:
        today = datetime.fromisoformat(args.today).replace(tzinfo=timezone.utc)

    with open(args.serp) as f:
        data = json.load(f)

    plugins = data.get("plugins", [])

    # Find user
    user_rank = None
    for i, p in enumerate(plugins, 1):
        if p.get("slug") == args.user_slug:
            user_rank = i
            break

    targets = plugins[:args.top_n]
    if user_rank and user_rank > args.top_n:
        targets = list(targets) + [plugins[user_rank - 1]]

    print(f"\nFUNCTION SCORE COMPONENTS — user={args.user_slug} (rank {user_rank or 'not found'})\n")
    print(f"{'#':>3} {'slug':<32} {'days':>5} {'rec':>5} {'sub1m':>6} {'inst':>6} {'rat':>5} {'supp':>5} {'≈score':>7}")
    print("-" * 90)

    for i, p in enumerate(targets, 1):
        slug = p.get("slug", "")
        actual_rank = (i if i <= args.top_n else user_rank)
        if user_rank and slug == args.user_slug:
            actual_rank = user_rank
        fs = compute_function_score(p, today)
        marker = " ★" if slug == args.user_slug else ""
        days = fs["recency_days"]
        days_str = f"{days}" if days is not None else "?"
        print(
            f"{actual_rank:>3} {slug[:32]:<32} {days_str:>5} {fs['recency']:>5.2f} "
            f"{fs['sub1m']:>6.3f} {fs['install_log']:>6.2f} {fs['rating_factor']:>5.3f} "
            f"{fs['support_factor']:>5.2f} {fs['approx_function_score']:>7.2f}{marker}"
        )

    print()
    print("Reading the table:")
    print("  - recency=1.0 means inside the 180-day offset (full credit). Below 1.0 = decay.")
    print("  - sub1m booster: closer to 1.0 means closer to 1M installs.")
    print("  - inst (install_log), rat (rating), supp (support) are additive factors.")
    print("  - ≈score is a rough proxy — relative ordering matters more than absolute values.")
    print()
    print("Interpretation:")
    print("  If user's ≈score is HIGHER than competitors above them in the SERP,")
    print("  the gap is in text relevance (BM25), not function score.")
    print("  If LOWER, the gap is in quality signals (likely rating or recency).")


if __name__ == "__main__":
    main()
