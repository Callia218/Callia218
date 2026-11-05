#!/usr/bin/env python3
"""Generate the profile snapshot from GitHub's public REST API.

Only stars on public repositories owned by this account are counted. Forks
are included in both the public repository and star counts, just as they are
on the account's public repository page.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree


USER = "Callia218"
API_ROOT = "https://api.github.com"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "github-snapshot.svg"
MOBILE_OUTPUT = OUTPUT.with_name("github-snapshot-mobile.svg")


def get_json(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-snapshot",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(API_ROOT + path, headers=headers), timeout=20) as response:
        return json.load(response)


def get_public_repositories():
    repositories = []
    for page in range(1, 101):
        batch = get_json(f"/users/{USER}/repos?per_page=100&page={page}&type=owner")
        if not isinstance(batch, list):
            raise ValueError("Unexpected response while listing public repositories")
        repositories.extend(batch)
        if len(batch) < 100:
            return repositories
    raise ValueError("Repository list exceeded the supported pagination limit")


def make_svg(repos: int, stars: int, followers: int) -> str:
    # Values are integers, so the only dynamic content is safe to place in XML.
    repos, stars, followers = (f"{int(value):,}" for value in (repos, stars, followers))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="220" viewBox="0 0 880 220" role="img" aria-labelledby="title desc">
  <title id="title">Callia's GitHub snapshot</title>
  <desc id="desc">{repos} public repositories, {stars} stars across public repositories, and {followers} followers.</desc>
  <rect x="2" y="2" width="876" height="216" rx="20" fill="#f5f7ec" stroke="#cad8be" stroke-width="2"/>
  <path d="M36 76 H844" stroke="#d7e2cb" stroke-width="1.5"/>
  <path d="M292 100 V190 M586 100 V190" stroke="#d7e2cb" stroke-width="1.5"/>
  <g font-family="Segoe UI, -apple-system, BlinkMacSystemFont, sans-serif" fill="#375b42">
    <text x="40" y="51" font-size="22" font-weight="700">A little snapshot</text>
    <text x="840" y="50" text-anchor="end" font-size="13" fill="#617a63">GROWING AT ITS OWN PACE</text>
    <g text-anchor="middle">
      <text x="147" y="150" font-size="38" font-weight="700">{repos}</text>
      <text x="147" y="179" font-size="14" fill="#617a63">public repositories</text>
      <text x="439" y="150" font-size="38" font-weight="700">{stars}</text>
      <text x="439" y="179" font-size="14" fill="#617a63">stars received</text>
      <text x="733" y="150" font-size="38" font-weight="700">{followers}</text>
      <text x="733" y="179" font-size="14" fill="#617a63">followers</text>
    </g>
  </g>
</svg>
'''


def make_mobile_svg(repos: int, stars: int, followers: int) -> str:
    repos, stars, followers = (f"{int(value):,}" for value in (repos, stars, followers))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="190" viewBox="0 0 380 190" role="img" aria-labelledby="title desc">
  <title id="title">Callia's GitHub snapshot</title>
  <desc id="desc">{repos} public repositories, {stars} stars across public repositories, and {followers} followers.</desc>
  <rect x="1" y="1" width="378" height="188" rx="16" fill="#f5f7ec" stroke="#cad8be" stroke-width="2"/>
  <path d="M24 65 H356 M127 84 V160 M253 84 V160" stroke="#d7e2cb" stroke-width="1.5"/>
  <g font-family="Segoe UI, -apple-system, BlinkMacSystemFont, sans-serif" fill="#375b42">
    <text x="24" y="43" font-size="19" font-weight="700">A little snapshot</text>
    <g text-anchor="middle">
      <text x="64" y="126" font-size="30" font-weight="700">{repos}</text>
      <text x="64" y="151" font-size="12" fill="#617a63">public repos</text>
      <text x="190" y="126" font-size="30" font-weight="700">{stars}</text>
      <text x="190" y="151" font-size="12" fill="#617a63">stars received</text>
      <text x="316" y="126" font-size="30" font-weight="700">{followers}</text>
      <text x="316" y="151" font-size="12" fill="#617a63">followers</text>
    </g>
  </g>
</svg>
'''


def main() -> int:
    try:
        profile = get_json(f"/users/{USER}")
        repositories = get_public_repositories()
        stars = sum(int(repo["stargazers_count"]) for repo in repositories)
        values = (len(repositories), stars, int(profile["followers"]))
        cards = ((OUTPUT, make_svg(*values)), (MOBILE_OUTPUT, make_mobile_svg(*values)))
        for path, svg in cards:
            ElementTree.fromstring(svg)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg, encoding="utf-8", newline="\n")
        print(f"Updated {OUTPUT}: {len(repositories)} public repositories, {stars} stars, {profile['followers']} followers")
        return 0
    except (HTTPError, URLError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Could not update the snapshot: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
