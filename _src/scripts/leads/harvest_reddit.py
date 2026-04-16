#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from urllib.parse import quote_plus

from shared import RATE_LIMIT_DELAY, fetch_listing, fetch_post, load_communities, load_queries, load_tracking, normalize_url, record_found, save_post


def listing_urls(community: str) -> list[str]:
    base = f'https://www.reddit.com/r/{community}'
    return [
        f'{base}/top/?t=all',
        f'{base}/top/?t=year',
        f'{base}/hot/',
    ]


def search_url(community: str, query: str) -> str:
    return f'https://www.reddit.com/r/{community}/search/?q={quote_plus(query)}&restrict_sr=1&sort=top&type=link&t=all'


def collect_unique_posts(urls: list[str], limit_per_url: int = 100) -> list[dict]:
    seen = set()
    posts = []
    for url in urls:
        batch = fetch_listing(normalize_url(url), limit=limit_per_url)
        for post in batch:
            if post['id'] not in seen:
                seen.add(post['id'])
                posts.append(post)
        time.sleep(RATE_LIMIT_DELAY)
    return posts


def main() -> None:
    parser = argparse.ArgumentParser(description='Harvest Reddit leads from configured communities and queries.')
    parser.add_argument('--limit', type=int, default=None, metavar='N', help='Max total posts to fetch after dedupe')
    parser.add_argument('--top', type=int, default=5, metavar='N', help='Top comments per post to save')
    parser.add_argument('--force', action='store_true', help='Re-fetch posts already tracked')
    args = parser.parse_args()

    tracking = load_tracking()
    communities = load_communities()
    queries = load_queries()

    urls: list[str] = []
    for community in communities:
        name = community['name']
        urls.extend(listing_urls(name))
        urls.extend(search_url(name, query) for query in queries)

    all_posts = collect_unique_posts(urls)
    to_fetch = [p for p in all_posts if args.force or p['id'] not in tracking]
    if args.limit:
        to_fetch = to_fetch[: args.limit]

    for i, post_data in enumerate(to_fetch, 1):
        post, comments = fetch_post(post_data['permalink'])
        out_file = save_post(post, comments, args.top)
        record_found(tracking, post, out_file)
        print(f'[{i}/{len(to_fetch)}] saved {out_file.name}')
        if i < len(to_fetch):
            time.sleep(RATE_LIMIT_DELAY)


if __name__ == '__main__':
    main()
