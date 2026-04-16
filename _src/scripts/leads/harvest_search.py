#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from urllib.parse import quote_plus

from shared import RATE_LIMIT_DELAY, fetch_listing, fetch_post, load_tracking, normalize_url, record_found, save_post


def build_search_url(community: str, query: str) -> str:
    q = quote_plus(query)
    return f'https://www.reddit.com/r/{community}/search/?q={q}&restrict_sr=1&sort=top&type=link&t=all'


def main() -> None:
    parser = argparse.ArgumentParser(description='Fetch Reddit search results for a specific community/query pair.')
    parser.add_argument('community', help='Subreddit name without r/')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', type=int, default=None, metavar='N', help='Max posts to process')
    parser.add_argument('--top', type=int, default=5, metavar='N', help='Top comments to save per post')
    parser.add_argument('--force', action='store_true', help='Re-fetch posts already in tracking')
    args = parser.parse_args()

    tracking = load_tracking()
    search_url = normalize_url(build_search_url(args.community, args.query))
    posts = fetch_listing(search_url, limit=args.limit)
    to_fetch = [p for p in posts if args.force or p['id'] not in tracking]

    for i, post_data in enumerate(to_fetch, 1):
        post, comments = fetch_post(post_data['permalink'])
        out_file = save_post(post, comments, args.top)
        record_found(tracking, post, out_file)
        print(f'[{i}/{len(to_fetch)}] saved {out_file.name}')
        if i < len(to_fetch):
            time.sleep(RATE_LIMIT_DELAY)


if __name__ == '__main__':
    main()
