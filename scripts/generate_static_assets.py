#!/usr/bin/env python3
"""Create the self-contained animated watercolor profile banner."""

import base64
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def data_url(filename: str) -> str:
    content = base64.b64encode((ASSETS / filename).read_bytes()).decode("ascii")
    return f"data:image/webp;base64,{content}"


def banner() -> str:
    background = data_url("evergreen-watercolor.webp")
    character = data_url("callia-character.webp")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="293" viewBox="0 0 880 293" id="still" role="img" aria-labelledby="title desc">
  <title id="title">Callia's evergreen garden</title>
  <desc id="desc">A watercolor meadow with ivy, a little evergreen tree and Callia sitting beneath a tree. Leaves and the character gently move beside the words Callia, little things, growing slowly.</desc>
  <defs>
    <style>
      text {{ font-family:"Segoe Print","Comic Sans MS","Chalkboard SE","Trebuchet MS",sans-serif; fill:#40583a; }}
      .still {{ display:none; }}
      svg:target .moving {{ display:none; }}
      svg:target .still {{ display:inline; }}
      @media (prefers-reduced-motion:reduce) {{ .moving {{ display:none; }} .still {{ display:inline; }} }}
    </style>
    <clipPath id="paper"><rect x="2" y="2" width="876" height="289" rx="15"/></clipPath>
    <image id="character" x="-85" y="-168" width="170" height="180" href="{character}"/>
    <g id="leaf" stroke="#7b8f61" stroke-width=".8" stroke-linejoin="round"><path d="M0 0 C-2-8 6-11 11-13 C12-6 7 0 0 0Z" fill="#adbf8a"/><path d="M0 0 Q5-5 9-10" fill="none"/></g>
  </defs>
  <g clip-path="url(#paper)">
    <image x="0" y="0" width="880" height="293" preserveAspectRatio="xMidYMid slice" href="{background}"/>
    <g transform="translate(738 224)">
      <ellipse cx="0" cy="8" rx="59" ry="7" fill="#526a3e" opacity=".2"/>
      <use class="still" href="#character"/>
      <g class="moving"><animateTransform attributeName="transform" type="scale" values="1 1;1.008 1.018;1 1" dur="4s" repeatCount="indefinite"/><use href="#character"><animateTransform attributeName="transform" type="rotate" values="-1;1;-1" dur="6s" repeatCount="indefinite"/></use></g>
    </g>
    <g class="moving"><animateMotion path="M0 0 C14 -5 23 -14 32 -8 C24 2 12 4 0 0Z" dur="7s" repeatCount="indefinite"/><use href="#leaf" x="638" y="108"/></g>
    <use class="still" href="#leaf" x="638" y="108"/>
    <g class="moving"><animateMotion path="M0 0 C-14 9 -24 0 -33 7 C-20 15 -8 13 0 0Z" dur="9s" repeatCount="indefinite"/><use href="#leaf" x="842" y="76" transform="rotate(33 842 76)"/></g>
    <use class="still" href="#leaf" x="842" y="76" transform="rotate(33 842 76)"/>
    <g font-weight="700" text-anchor="middle">
      <g transform="translate(352 249)"><rect x="-35" y="-16" width="70" height="23" rx="9" fill="#f8f5df" fill-opacity=".9" stroke="#91a275"/><text y="1" font-size="11.5">Python</text></g>
      <g transform="translate(440 249)"><rect x="-45" y="-16" width="90" height="23" rx="9" fill="#f8f5df" fill-opacity=".9" stroke="#91a275"/><text y="1" font-size="11.5">JavaScript</text></g>
      <g transform="translate(520 249)"><rect x="-30" y="-16" width="60" height="23" rx="9" fill="#f8f5df" fill-opacity=".9" stroke="#91a275"/><text y="1" font-size="11.5">Swift</text></g>
    </g>
    <text x="58" y="73" font-size="15" font-weight="700">@Callia218</text>
    <path d="M58 80 Q109 83 161 79" fill="none" stroke="#80975f" stroke-width="2.3" stroke-linecap="round"/>
    <text x="53" y="153" font-size="66" font-weight="700" letter-spacing="-1.5">Callia</text>
    <path d="M57 163 Q141 168 225 162" fill="none" stroke="#80975f" stroke-width="2.8" stroke-linecap="round"/>
    <text x="58" y="203" font-size="22" font-weight="700">little things, growing slowly</text>
  </g>
  <rect x="2" y="2" width="876" height="289" rx="15" fill="none" stroke="#b4bc91" stroke-opacity=".8" stroke-width="1.5"/>
</svg>
'''


def main() -> None:
    svg = banner()
    ElementTree.fromstring(svg)
    (ASSETS / "evergreen-animated.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("Generated watercolor assets/evergreen-animated.svg")


if __name__ == "__main__":
    main()
