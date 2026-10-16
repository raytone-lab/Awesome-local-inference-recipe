#!/usr/bin/env python3
"""Render docs/watchlist.md from data/sources.json (every source, sorted by tier).
Run: python3 scripts/gen_watchlist.py"""
import json
from pathlib import Path
R = Path(__file__).resolve().parent.parent
SOURCES, WATCH = R/'data/sources.json', R/'docs/watchlist.md'
TIER_ORDER = {'A': 0, 'B': 1, 'C': 2}
HEADER = ('# Recipe sources to watch / 重点跟踪来源\n\n'
          'Generated from `data/sources.json` ({updated}) by `scripts/gen_watchlist.py`. '
          'Tier A = 参数具体且可复现；B = 有具体数字但条件不全；C = 多为转述或覆盖面窄。\n\n'
          '| Tier | Name | Platform | Followers | Focus | Why | Sample |\n'
          '|---|---|---|---|---|---|---|\n')

def cell(v):
    return str(v).replace('|', '\\|').replace('\n', ' ')

def row(s):
    followers = '—' if s.get('followers') is None else s['followers']
    return (f"| {s['tier']} | [{cell(s['name'])}]({s['url']}) | {s['platform']} | {followers} | "
            f"{cell(s['focus'])} | {cell(s['why'])} | [link]({s['sample_post']}) |")

def render(sources):
    ordered = sorted(sources['sources'], key=lambda s: TIER_ORDER[s['tier']])
    return HEADER.format(updated=sources['updated']) + '\n'.join(row(s) for s in ordered) + '\n'

if __name__ == '__main__':
    WATCH.write_text(render(json.loads(SOURCES.read_text(encoding='utf-8'))), encoding='utf-8')
    print(f'written {WATCH.relative_to(R)}')
