#!/usr/bin/env python3
"""
Build the ZeroHype anti-slop manifesto lead magnet PDF.

Source of truth:  manifesto.md  (single Markdown file, no template engine)
Output:           assets/anti-slop-manifesto.pdf

Why this exists: the PDF is the free entry point of the M2M funnel. The
catalog points at it, so if manifesto.md changes and the PDF is not rebuilt,
the download link serves stale content.

The output is committed on purpose: GitHub Pages deploys the repo, so the
asset must live in the tree. The build stays reproducible via this script.

Dependencies: pandoc, weasyprint. Checked up front with a clear error.

Usage:
    python3 scripts/build_manifesto_pdf.py
    python3 scripts/build_manifesto_pdf.py --check
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "manifesto.md"
OUTPUT = REPO / "assets" / "anti-slop-manifesto.pdf"

TITLE = "ZeroHype Anti-Slop Manifesto"
FOOTER = ('<div id="footer">zerohypelab.com/manifesto/ &nbsp;|&nbsp; '
          "Free download. No fluff, no hype.</div>")

# Minimalist, brand-matched, zero external font requests. System-only font
# stack on purpose so the build has no network dependency.
CSS = """
@page { size: A4; margin: 22mm 20mm 20mm 20mm; }
html { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }
body { font-size: 10.5pt; line-height: 1.55; color: #14161a; margin: 0; }
h1 { font-size: 19pt; line-height: 1.2; margin: 0 0 4mm 0; letter-spacing: -0.3pt; }
h2 { font-size: 12pt; margin: 9mm 0 2mm 0; padding-bottom: 1.5mm;
     border-bottom: 1.5pt solid #e8fd27; }
p { margin: 0 0 3.5mm 0; }
blockquote { margin: 5mm 0; padding: 3mm 4mm; background: #f6f7f2;
             border-left: 3pt solid #14161a; font-style: italic; }
blockquote p { margin: 0; }
code { font-family: "SF Mono", Menlo, monospace; font-size: 9pt;
       background: #f2f3ef; padding: 0 1pt; }
hr { border: 0; border-top: 0.5pt solid #d8dad2; margin: 7mm 0; }
a { color: #14161a; text-decoration: none; font-weight: 600; }
em { color: #5a5f66; }
strong { font-weight: 700; }
#footer { position: fixed; bottom: 0; left: 0; right: 0; font-size: 7.5pt;
          color: #9aa0a6; border-top: 0.5pt solid #e3e5de; padding-top: 2mm; }
"""


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_deps() -> None:
    missing = [t for t in ("pandoc", "weasyprint") if not shutil.which(t)]
    if missing:
        fail("missing dependency: " + ", ".join(missing) +
             "\n  macOS: brew install pandoc weasyprint")


def prepare_source(text: str) -> str:
    """Strip the leading H1 and normalise dashes.

    The H1 is dropped because pandoc already renders the document title from
    metadata, and keeping both produced a duplicated heading in the PDF.
    Dashes become plain full stops so the house voice rule (no em dash)
    holds in anything shipped to a human.
    """
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    out = "\n".join(lines)
    out = re.sub(r"\s*[\u2014\u2013\u2015]\s*", ". ", out)
    out = re.sub(r"\.{2,}", ".", out)
    return out + "\n"


def build(check_only: bool) -> int:
    check_deps()
    if not SOURCE.exists():
        fail(f"source not found: {SOURCE}")

    if check_only:
        if not OUTPUT.exists():
            fail(f"output missing: {OUTPUT}, run without --check to build it")
        data = OUTPUT.read_bytes()
        if not data.startswith(b"%PDF") or b"%%EOF" not in data[-2048:]:
            fail("output is not a valid PDF")
        print(f"source : {SOURCE}")
        print(f"output : {OUTPUT} ({len(data)} bytes)")
        print("OK: output present and valid")
        return 0

    html = prepare_source(SOURCE.read_text(encoding="utf-8"))
    if "\u2014" in html:
        fail("em dash survived preprocessing, refusing to ship it")

    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        src, css, out_html = t / "src.md", t / "style.css", t / "doc.html"
        src.write_text(html, encoding="utf-8")
        css.write_text(CSS, encoding="utf-8")

        subprocess.run(
            ["pandoc", str(src), "-f", "gfm", "-t", "html5", "--standalone",
             "--metadata", f"title={TITLE}", "--css", str(css),
             "-o", str(out_html)],
            check=True,
        )
        with out_html.open("a", encoding="utf-8") as fh:
            fh.write("\n" + FOOTER + "\n")

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["weasyprint", str(out_html), str(OUTPUT)], check=True)

    data = OUTPUT.read_bytes()
    if not data.startswith(b"%PDF") or b"%%EOF" not in data[-2048:]:
        fail("generated file is not a valid PDF")
    print(f"built {OUTPUT} ({len(data)} bytes)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="validate existing output without rebuilding")
    build(ap.parse_args().check)
