#!/usr/bin/env python3
"""Refresh stars / pushed_at in data/repos.json via GitHub REST API. GITHUB_TOKEN optional (60 req/h without)."""
import json, os, urllib.request, datetime
from pathlib import Path
P = Path(__file__).resolve().parent.parent/'data/repos.json'
R = json.load(open(P)); tok = os.environ.get('GITHUB_TOKEN')
for r in R:
    if not r.get('repo'): continue
    req = urllib.request.Request(f"https://api.github.com/repos/{r['repo']}", headers={'Accept':'application/vnd.github+json','User-Agent':'recipebench'})
    if tok: req.add_header('Authorization', f'Bearer {tok}')
    try:
        d = json.load(urllib.request.urlopen(req, timeout=20))
        r.update(stars=d['stargazers_count'], pushed_at=d['pushed_at'], url=d['html_url'], archived=d['archived'])
        print(f"{r['repo']:40} {d['stargazers_count']:>8} {d['pushed_at']}")
    except Exception as e:
        print(f"{r['repo']:40} FAILED ({e}); keeping previous values")
meta = {'updated_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}
json.dump(R, open(P,'w'), ensure_ascii=False, indent=1)
json.dump(meta, open(P.with_name('repos.meta.json'),'w'))
