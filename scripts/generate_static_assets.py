#!/usr/bin/env python3
"""Create the self-contained animated banner from the original character art."""

import base64
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def banner() -> str:
    character = base64.b64encode((ASSETS / "callia-character.webp").read_bytes()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="880" height="248" viewBox="0 0 880 248" id="still" role="img" aria-labelledby="title desc">
  <title id="title">Callia's evergreen notebook</title>
  <desc id="desc">An animated sketchbook banner with drifting clouds and leaves, a gently swaying character, and the words Callia, little things, growing slowly.</desc>
  <defs>
    <style>
      svg {{ --paper:#faf5e8; --ink:#514b39; --muted:#706b51; --edge:#c3c5a8; --rule:#d9d4b9; --sky:#c6e0d8; --sky2:#e7eee1; --cloud:#fff9e8; --hill:#a6bb83; --hill2:#809e69; --grass:#627f58; --accent:#779260; --chip:#edf1d9; }}
      @media (prefers-color-scheme:dark) {{ svg {{ --paper:#292d28; --ink:#f6edd8; --muted:#d5d6b9; --edge:#606c53; --rule:#626c55; --sky:#354e4a; --sky2:#34413a; --cloud:#bed6ce; --hill:#607c51; --hill2:#425f3f; --grass:#b0c58b; --accent:#adc188; --chip:#48563e; }} }}
      text {{ font-family:"Segoe Print","Comic Sans MS","Chalkboard SE","Trebuchet MS",sans-serif; fill:var(--ink); }}
      .small {{ font-size:15px; font-weight:700; fill:var(--muted); }}
      .still {{ display:none; }}
      svg:target .moving {{ display:none; }}
      svg:target .still {{ display:inline; }}
      @media (prefers-reduced-motion:reduce) {{ .moving {{ display:none; }} .still {{ display:inline; }} }}
    </style>
    <path id="page" d="M21 11 Q198 7 440 10 T859 10 Q872 11 872 25 L873 220 Q872 236 856 236 Q650 240 430 236 T24 238 Q9 237 9 222 L8 28 Q8 14 21 11Z"/>
    <clipPath id="clip"><use href="#page"/></clipPath>
    <linearGradient id="sky" x1="0" y1="0" x2="1" y2=".15"><stop offset=".36" stop-color="var(--paper)"/><stop offset=".76" stop-color="var(--sky2)"/><stop offset="1" stop-color="var(--sky)"/></linearGradient>
    <pattern id="ruled" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M0 1h28" stroke="var(--rule)" stroke-opacity=".28"/></pattern>
    <path id="cloud" d="M0 29 Q7 17 23 19 Q29 4 47 6 Q63 5 68 18 Q84 14 91 25 Q104 25 107 32 Q87 37 49 36 Q15 37 0 32Z"/>
    <g id="leaf" stroke="var(--grass)" stroke-width="1.2" stroke-linejoin="round"><path d="M0 1 C-3-10 8-13 12-15 C15-6 8 1 0 1Z" fill="var(--chip)"/><path d="M0 1 Q6-6 10-11" fill="none"/></g>
    <g id="daisy"><circle cx="0" cy="-5" r="4" fill="#fff4da"/><circle cx="5" cy="0" r="4" fill="#fff4da"/><circle cx="0" cy="5" r="4" fill="#fff4da"/><circle cx="-5" cy="0" r="4" fill="#fff4da"/><circle r="3" fill="#dbbc72"/></g>
    <image id="character" x="-84" y="-157" width="168" height="178" href="data:image/webp;base64,{character}" xlink:href="data:image/webp;base64,{character}"/>
  </defs>
  <use href="#page" transform="translate(1 3)" fill="var(--edge)" opacity=".5"/>
  <g clip-path="url(#clip)">
    <rect width="880" height="248" fill="url(#sky)"/><rect width="880" height="248" fill="url(#ruled)"/>
    <path d="M32 9 Q30 121 33 240" fill="none" stroke="var(--accent)" stroke-width="1.5" opacity=".65"/>
    <g fill="var(--cloud)" opacity=".8">
      <g class="moving"><animateTransform attributeName="transform" type="translate" values="-12 0;15 0;-12 0" dur="12s" repeatCount="indefinite"/><use href="#cloud" x="550" y="28"/></g>
      <use class="still" href="#cloud" x="550" y="28"/>
      <g class="moving"><animateTransform attributeName="transform" type="translate" values="10 0;-16 0;10 0" dur="16s" repeatCount="indefinite"/><use href="#cloud" x="735" y="24" transform="scale(.82) translate(162 0)"/></g>
      <use class="still" href="#cloud" x="735" y="24" transform="scale(.82) translate(162 0)"/>
    </g>
    <path d="M441 248 Q505 219 564 177 Q624 136 687 130 Q766 112 880 110 L880 248Z" fill="var(--hill)"/>
    <path d="M531 248 Q631 203 713 189 Q804 158 880 158 L880 248Z" fill="var(--hill2)"/>
    <g fill="none" stroke="var(--grass)" stroke-width="1.8" stroke-linecap="round" opacity=".9"><path d="M550 221l-4-5m5 5 3-8m31-10-4-5m6 5 2-8m48-11-4-5m6 4 3-7m136-12-4-5m6 4 2-7m61 38-4-5m6 5 3-7"/></g>
    <use href="#daisy" x="615" y="196" transform="rotate(-9 615 196)"/><use href="#daisy" x="669" y="181" transform="scale(.8) translate(167 45)"/>
    <g class="moving"><animateMotion path="M0 0 C12 -9 24 -15 35 -6 C21 4 11 4 0 0Z" dur="7s" repeatCount="indefinite"/><use href="#leaf" x="660" y="94"/></g>
    <use class="still" href="#leaf" x="660" y="94"/>
    <g transform="translate(760 174)">
      <ellipse cx="0" cy="18" rx="61" ry="8" fill="#283b2e" opacity=".19"/>
      <use class="still" href="#character"/>
      <g class="moving"><animateTransform attributeName="transform" type="scale" values="1 1;1.012 1.022;1 1" dur="4s" repeatCount="indefinite"/><use href="#character"><animateTransform attributeName="transform" type="rotate" values="-1.2;1.2;-1.2" dur="6s" repeatCount="indefinite"/></use></g>
    </g>
    <g transform="translate(522 210)"><rect x="0" y="-14" width="69" height="23" rx="8" fill="var(--chip)" stroke="var(--accent)"/><text x="34.5" y="2" font-size="12" font-weight="700" text-anchor="middle">Python</text></g>
    <g transform="translate(598 210)"><rect x="0" y="-14" width="94" height="23" rx="8" fill="var(--chip)" stroke="var(--accent)"/><text x="47" y="2" font-size="12" font-weight="700" text-anchor="middle">JavaScript</text></g>
    <g transform="translate(699 210)"><rect x="0" y="-14" width="61" height="23" rx="8" fill="var(--chip)" stroke="var(--accent)"/><text x="30.5" y="2" font-size="12" font-weight="700" text-anchor="middle">Swift</text></g>
  </g>
  <use href="#page" fill="none" stroke="var(--edge)" stroke-width="1.7"/>
  <text x="58" y="53" class="small">@Callia218</text>
  <path d="M58 58 Q110 61 162 57" fill="none" stroke="var(--accent)" stroke-width="2.4" stroke-linecap="round"/>
  <text x="53" y="128" font-size="62" font-weight="700" letter-spacing="-2">Callia</text>
  <path d="M56 138 Q140 143 224 137" fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>
  <text x="58" y="178" font-size="23" font-weight="700">little things, growing slowly</text>
</svg>
'''


def main() -> None:
    svg = banner()
    ElementTree.fromstring(svg)
    (ASSETS / "evergreen-animated.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("Generated assets/evergreen-animated.svg")


if __name__ == "__main__":
    main()
