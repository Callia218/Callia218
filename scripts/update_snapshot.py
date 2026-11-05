#!/usr/bin/env python3
"""Generate matching notebook-style cards using public GitHub data.

Stars include public repositories owned by Callia218, including forks.
Language shares count each owned public repository once by its GitHub primary
language. Repositories with no detected language are excluded from the shares.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree

USER = "Callia218"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
API_ROOT = "https://api.github.com"


def get_json(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile-snapshot", "X-GitHub-Api-Version": "2022-11-28"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(API_ROOT + path, headers=headers), timeout=20) as response:
        return json.load(response)


def get_public_repositories() -> list[dict]:
    repositories = []
    for page in range(1, 101):
        batch = get_json(f"/users/{USER}/repos?per_page=100&page={page}&type=owner")
        if not isinstance(batch, list):
            raise ValueError("Unexpected repository list")
        repositories.extend(batch)
        if len(batch) < 100:
            return repositories
    raise ValueError("Repository pagination limit exceeded")


def language_shares(repositories: list[dict]) -> list[tuple[str, int]]:
    counts = Counter(repo["language"] for repo in repositories if repo.get("language"))
    if not counts:
        return []
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    grouped = ordered[:3]
    if len(ordered) > 3:
        grouped.append(("Other", sum(count for _, count in ordered[3:])))
    total = sum(count for _, count in grouped)
    floors = [100 * count // total for _, count in grouped]
    for index in sorted(range(len(grouped)), key=lambda i: (-(100 * grouped[i][1] % total), i))[:100 - sum(floors)]:
        floors[index] += 1
    return [(name, floors[i]) for i, (name, _) in enumerate(grouped)]


def card(repos: int, stars: int, followers: int, languages: list[tuple[str, int]], mobile: bool = False) -> str:
    width, height = (428, 340) if mobile else (880, 188)
    side_rule = '<path d="M24 166 Q210 163 404 166" stroke="var(--rule)" stroke-dasharray="4 5"/>' if mobile else '<path d="M440 25 Q443 95 440 164" stroke="var(--rule)" stroke-dasharray="4 5"/>'
    lang_x, lang_y = (24, 190) if mobile else (468, 25)
    colors = ["var(--green)", "var(--blue)", "var(--gold)", "var(--lilac)"]
    bars, legends, offset = [], [], 0.0
    for index, (name, percent) in enumerate(languages):
        bar_width = 380 * percent / 100
        bars.append(f'<rect x="{offset:.1f}" y="64" width="{bar_width:.1f}" height="12" fill="{colors[index]}"/>')
        x = 0 if index % 2 == 0 else 198
        y = 101 if index < 2 else 127
        legends.append(f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{colors[index]}"/><text x="{x+16}" y="{y}" class="label">{escape(name)}</text><text x="{x+181}" y="{y}" text-anchor="end" class="label">{percent}%</text>')
        offset += bar_width
    if not languages:
        legends.append('<text x="0" y="101" class="label">No primary languages yet</text>')
    desc = f"{stars:,} stars, {followers:,} followers, {repos:,} public repositories. " + ", ".join(f"{name}: {share}%" for name, share in languages)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Callia's GitHub snapshot</title><desc id="desc">{escape(desc)}</desc>
  <defs>
    <style>
      svg {{ --paper:#faf7e9; --ink:#514a3c; --muted:#6e6a57; --edge:#cac9ae; --rule:#aaa98b; --green:#a0b77e; --blue:#8ebdb8; --gold:#dfc17e; --lilac:#b5a6b5; }}
      @media (prefers-color-scheme:dark) {{ svg {{ --paper:#2d3028; --ink:#f8eedb; --muted:#dbd4bf; --edge:#5a6650; --rule:#899078; --green:#a8c184; --blue:#86b8b2; --gold:#dfc17e; --lilac:#b5a6b5; }} }}
      text {{ font-family:"Segoe Print","Comic Sans MS","Chalkboard SE","Trebuchet MS",sans-serif; }}
      .heading {{ font-size:22px; font-weight:700; fill:var(--ink); }} .caption,.label {{ font-size:13px; fill:var(--muted); }} .value {{ font-size:30px; font-weight:700; fill:var(--ink); }}
    </style>
    <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r=".75" fill="var(--rule)" opacity=".25"/></pattern>
    <clipPath id="bar"><rect x="0" y="64" width="380" height="12" rx="6"/></clipPath>
  </defs>
  <rect x="3" y="4" width="{width-6}" height="{height-8}" rx="16" fill="var(--paper)" stroke="var(--edge)" stroke-width="1.7"/>
  <rect x="5" y="6" width="{width-10}" height="{height-12}" rx="14" fill="url(#dots)"/>
  <g fill="none" stroke-width="1.4" stroke-linecap="round">{side_rule}</g>
  <g transform="translate(28 25)">
    <text x="0" y="21" class="heading">Open source</text><path d="M0 29 Q70 33 152 28" fill="none" stroke="var(--green)" stroke-width="2.4"/>
    <text x="0" y="47" class="caption">Public GitHub activity</text>
    <text x="0" y="101" class="value">{stars:,}</text><text x="0" y="127" class="label">Stars received</text>
    <text x="151" y="101" class="value">{followers:,}</text><text x="151" y="127" class="label">Followers</text>
    <text x="280" y="101" class="value">{repos:,}</text><text x="280" y="127" class="label">Public repos</text>
  </g>
  <g transform="translate({lang_x} {lang_y})">
    <text x="0" y="21" class="heading">Primary languages</text><path d="M0 29 Q115 33 244 28" fill="none" stroke="var(--blue)" stroke-width="2.4"/>
    <text x="0" y="47" class="caption">Share of public repos with a detected language</text>
    <g clip-path="url(#bar)">{''.join(bars)}</g><rect x="0" y="64" width="380" height="12" rx="6" fill="none" stroke="var(--rule)" stroke-width="1"/>
    {''.join(legends)}
  </g>
</svg>
'''


def main() -> int:
    try:
        profile = get_json(f"/users/{USER}")
        repositories = get_public_repositories()
        stars = sum(int(repo["stargazers_count"]) for repo in repositories)
        followers = int(profile["followers"])
        languages = language_shares(repositories)
        for filename, mobile in (("github-snapshot.svg", False), ("github-snapshot-mobile.svg", True)):
            svg = card(len(repositories), stars, followers, languages, mobile)
            ElementTree.fromstring(svg)
            (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
        print(f"Updated snapshot: {len(repositories)} public repositories, {stars} stars, {followers} followers; languages: {languages}")
        return 0
    except (HTTPError, URLError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Could not update snapshot: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
