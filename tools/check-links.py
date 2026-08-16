#!/usr/bin/env python3
"""Check every internal link on the site before pushing.

Catches four classes of problem, two of which `mkdocs build --strict` misses:

  1. Broken relative links (strict catches these)
  2. Links to a directory with no README.md (strict catches these)
  3. Broken in-page anchors, e.g. [x](#a-heading-that-moved) (strict does NOT)
  4. Published pages linking to pages excluded from the site, which would
     produce a dead link for every visitor (strict does NOT, because the
     target file exists on disk)

Links to files that are not Markdown pages — the official PDFs, the session
.pptx decks, the .llsp3 programs, the .html slide decks — are allowed when the
file exists, because MkDocs copies those through as static assets. Every one of
them is reported if the file is missing, so a typo'd filename is still caught.

Usage:
    python3 tools/check-links.py

Exit code is 1 if anything is wrong, so it works in a pre-push hook or CI.
"""

import os
import re
import sys

# Kept in sync with exclude_docs in mkdocs.yml. These files exist in the repo
# but are not published, so a relative link to them from a published page is a
# dead link on the site.
EXCLUDED = {
    "docs/team-roster.md",
    "docs/team-fund.md",
    "docs/team-fund.csv",
    "docs/team-links.md",
    "CLAUDE.md",
    "code/2025-reference/README.md",
}

SKIP_DIRS = {".git", "site", ".venv", "venv", "__pycache__", ".github", "tools"}


def heading_slug(heading: str) -> str:
    """Approximate the anchor id MkDocs generates for a heading."""
    s = heading.strip().lower()
    s = re.sub(r"[`*_\[\]()]", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s).strip("-")


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code so link-shaped examples in
    documentation are not mistaken for real links."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def main() -> int:
    excluded_norm = {os.path.normpath(p) for p in EXCLUDED}

    pages = {}
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(".md"):
                path = os.path.normpath(os.path.join(root, name))
                with open(path, encoding="utf-8") as fh:
                    pages[path] = fh.read()

    anchors = {
        path: {heading_slug(h) for h in re.findall(r"^#{1,6}\s+(.+)$", text, re.M)}
        for path, text in pages.items()
    }

    broken, leaks, bad_anchors = [], [], []

    for path, text in pages.items():
        rel = os.path.relpath(path, ".")
        published = rel not in EXCLUDED
        scannable = strip_code(text)

        for link in re.findall(r"\]\((?!https?:|mailto:)([^)]+)\)", scannable):
            target, _, frag = link.partition("#")

            if not target:  # same-page anchor
                if frag and frag not in anchors[path]:
                    bad_anchors.append(f"{rel}: #{frag}")
                continue

            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))

            if target.endswith("/"):
                if published and not os.path.exists(os.path.join(resolved, "README.md")):
                    broken.append(f"{rel}: {link}  (directory with no README.md)")
                continue

            # Non-.md targets are static assets that MkDocs copies through
            # verbatim — the official PDFs, the session .pptx decks, the .llsp3
            # programs, the slide decks in robot-design/. They are fine as long
            # as the file is really there. A bare directory link is still caught
            # by the branch above, and a typo'd filename is still caught here.
            if published and not target.endswith(".md"):
                if not os.path.exists(resolved):
                    broken.append(f"{rel}: {link}  (no such file)")
                continue

            if published and not os.path.exists(resolved):
                broken.append(f"{rel}: {link}")
                continue

            if published and resolved in excluded_norm:
                leaks.append(f"{rel} -> {link}  (target is excluded from the site)")

            if frag and resolved in anchors and frag not in anchors[resolved]:
                bad_anchors.append(f"{rel}: {link}")

    problems = [
        ("Broken links", broken),
        ("Links to excluded pages", leaks),
        ("Broken anchors", bad_anchors),
    ]

    failed = False
    for label, items in problems:
        if items:
            failed = True
            print(f"\n{label} ({len(items)}):")
            for item in items:
                print(f"  {item}")
        else:
            print(f"{label}: ok")

    print(f"\nchecked {len(pages)} pages")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
