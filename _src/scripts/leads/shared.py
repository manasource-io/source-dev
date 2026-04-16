from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import requests

ROOT = Path(__file__).resolve().parents[3]
LEADS_ROOT = ROOT / '_src' / 'leads'
REDDIT_ROOT = LEADS_ROOT / 'reddit'
CONFIG_ROOT = LEADS_ROOT / 'config'
FOUND_FILE = REDDIT_ROOT / 'found.json'
RESULTS_DIR = REDDIT_ROOT / 'results'
COMMUNITIES_FILE = CONFIG_ROOT / 'communities.json'
QUERIES_FILE = CONFIG_ROOT / 'queries.json'

HEADERS = {
    'User-Agent': 'manasource-source-leads/1.0 (research tool; contact: hermes.myth.agent@gmail.com)'
}
RATE_LIMIT_DELAY = 1.2


def ensure_dirs() -> None:
    REDDIT_ROOT.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def load_tracking() -> dict:
    return load_json(FOUND_FILE, {})


def save_tracking(data: dict) -> None:
    save_json(FOUND_FILE, data)


def load_communities() -> list[dict]:
    data = load_json(COMMUNITIES_FILE, {'communities': []})
    return [c for c in data.get('communities', []) if c.get('enabled', True)]


def load_queries() -> list[str]:
    data = load_json(QUERIES_FILE, {'queries': []})
    return data.get('queries', [])


def normalize_url(url: str) -> str:
    url = url.strip()
    url = re.sub(r'^https?://(old\.|new\.)?reddit\.com', 'https://www.reddit.com', url)
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    if not path.endswith('.json'):
        path += '.json'
    return urlunparse(parsed._replace(path=path))


def fetch_json(url: str, params: dict | None = None):
    resp = requests.get(url, headers=HEADERS, params=params or {}, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_listing(listing_url: str, limit: int | None = None) -> list[dict]:
    posts: list[dict] = []
    after = None
    while True:
        params = {'limit': 100}
        if after:
            params['after'] = after
        data = fetch_json(listing_url, params)
        children = data['data']['children']
        if not children:
            break
        for child in children:
            if child['kind'] == 't3':
                posts.append(child['data'])
        after = data['data'].get('after')
        if not after or (limit and len(posts) >= limit):
            break
        time.sleep(RATE_LIMIT_DELAY)
    return posts[:limit] if limit else posts


def parse_post(data: list) -> dict:
    d = data[0]['data']['children'][0]['data']
    return {
        'id': d.get('id', ''),
        'title': d.get('title', ''),
        'subreddit': d.get('subreddit_name_prefixed', ''),
        'author': d.get('author', '[deleted]'),
        'score': d.get('score', 0),
        'upvote_ratio': d.get('upvote_ratio', 0),
        'url': f"https://www.reddit.com{d.get('permalink', '')}",
        'created': datetime.fromtimestamp(d.get('created_utc', 0), tz=timezone.utc).strftime('%Y-%m-%d'),
        'selftext': d.get('selftext', '').strip(),
        'num_comments': d.get('num_comments', 0),
        'flair': d.get('link_flair_text') or '',
    }


def parse_comments(children: list, depth: int = 0, results: list | None = None) -> list:
    if results is None:
        results = []
    for child in children:
        if child.get('kind') != 't1':
            continue
        d = child['data']
        body = d.get('body', '').strip()
        if not body or body in ('[deleted]', '[removed]'):
            continue
        results.append({
            'depth': depth,
            'author': d.get('author', '[deleted]'),
            'score': d.get('score', 0),
            'body': body,
        })
        replies = d.get('replies')
        if isinstance(replies, dict):
            parse_comments(replies['data']['children'], depth + 1, results)
    return results


def fetch_post(permalink: str) -> tuple[dict, list]:
    url = normalize_url(f'https://www.reddit.com{permalink}')
    data = fetch_json(url, {'limit': 500})
    return parse_post(data), parse_comments(data[1]['data']['children'])


def top_comments(comments: list, n: int = 25) -> list:
    root = [c for c in comments if c['depth'] == 0]
    return sorted(root, key=lambda c: c['score'], reverse=True)[:n]


def render_post(post: dict, comments: list, top_n: int = 25) -> str:
    lines = [
        '=' * 72,
        f"TITLE:      {post['title']}",
        f"SUBREDDIT:  {post['subreddit']}",
        f"AUTHOR:     u/{post['author']}",
        f"SCORE:      {post['score']} ({int(post['upvote_ratio'] * 100)}% upvoted)",
        f"DATE:       {post['created']}",
        f"COMMENTS:   {post['num_comments']}",
        f"URL:        {post['url']}",
    ]
    if post['flair']:
        lines.append(f"FLAIR:      {post['flair']}")
    lines.append('=' * 72)
    if post['selftext']:
        lines += ['', 'POST BODY', '-' * 40, post['selftext']]
    shown = top_comments(comments, top_n)
    all_root = [c for c in comments if c['depth'] == 0]
    lines += ['', f"TOP {len(shown)} COMMENTS (of {len(all_root)} top-level, {len(comments)} total)", '-' * 40]
    for i, c in enumerate(shown, 1):
        lines.append('')
        lines.append(f"[{i}] u/{c['author']}  |  score: {c['score']}")
        for line in c['body'].splitlines():
            lines.append(f'    {line}')
    lines += ['', '=' * 72]
    return '\n'.join(lines)


def post_filename(post: dict) -> str:
    slug = post['title'][:50].lower()
    slug = ''.join(c if c.isalnum() or c in ' -' else ' ' for c in slug)
    slug = '-'.join(slug.split())
    return f"{post['created']}_{post['id']}_{slug}.txt"


def save_post(post: dict, comments: list, top_n: int) -> Path:
    ensure_dirs()
    out_file = RESULTS_DIR / post_filename(post)
    out_file.write_text(render_post(post, comments, top_n), encoding='utf-8')
    return out_file


def record_found(tracking: dict, post: dict, out_file: Path) -> None:
    tracking[post['id']] = {
        'title': post['title'],
        'subreddit': post['subreddit'],
        'url': post['url'],
        'score': post['score'],
        'found_at': datetime.now(tz=timezone.utc).isoformat(),
        'file': str(out_file.relative_to(ROOT)),
    }
    save_tracking(tracking)
