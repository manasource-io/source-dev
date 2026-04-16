#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from shared import fetch_json, normalize_url, parse_post, parse_comments, render_post


def main() -> None:
    parser = argparse.ArgumentParser(description='Fetch a single Reddit post and its top comments.')
    parser.add_argument('url', help='Reddit post URL')
    parser.add_argument('--top', type=int, default=25, metavar='N', help='Number of top comments to show')
    parser.add_argument('--out', metavar='FILE', help='Write output to file')
    parser.add_argument('--json', dest='as_json', action='store_true', help='Output raw JSON')
    args = parser.parse_args()

    try:
        data = fetch_json(normalize_url(args.url), {'limit': 500})
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    post = parse_post(data)
    comments = parse_comments(data[1]['data']['children'])
    output = json.dumps({'post': post, 'comments': comments}, indent=2) if args.as_json else render_post(post, comments, args.top)

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Saved to {args.out}')
    else:
        print(output)


if __name__ == '__main__':
    main()
