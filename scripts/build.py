#!/usr/bin/env python3
"""Generate a minimal static HTML site from Markdown content."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_DIR = ROOT / "docs"


@dataclass(order=True)
class Page:
    order: float
    title: str
    category: str
    description: str
    slug: str
    html_content: str
    source_path: Path

    @property
    def output_path(self) -> Path:
        return OUTPUT_DIR / f"{self.slug}.html"

    @property
    def url(self) -> str:
        return f"{self.slug}.html"


def main() -> None:
    pages = [build_page(path) for path in sorted(CONTENT_DIR.rglob("*.md"))]

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    grouped: Dict[str, List[Page]] = {}
    for page in pages:
        grouped.setdefault(page.category, []).append(page)

    for category_pages in grouped.values():
        category_pages.sort()

    pages.sort()

    for page in pages:
        html = render_page(
            title=page.title,
            description=page.description,
            body=page.html_content,
        )
        page.output_path.write_text(html, encoding="utf-8")

    index_html = render_index(grouped)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Generated {len(pages)} pages into {OUTPUT_DIR.relative_to(ROOT)}")


def build_page(path: Path) -> Page:
    raw_text = path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(raw_text)

    title = metadata.get("title") or path.stem.replace("-", " ").title()
    category = metadata.get("category", "Uncategorised")
    description = metadata.get("description", "")
    order = float(metadata.get("order", 0))
    slug = slugify(path.relative_to(CONTENT_DIR))
    html_content = markdown_to_html(body)

    return Page(
        order=order,
        title=title,
        category=category,
        description=description,
        slug=slug,
        html_content=html_content,
        source_path=path,
    )


def parse_front_matter(text: str) -> tuple[Dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    metadata: Dict[str, str] = {}
    body_lines: List[str] = []
    fm_lines: List[str] = []
    closing_index = None

    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            closing_index = index
            break
        fm_lines.append(line)

    if closing_index is None:
        return {}, text

    for line in fm_lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')

    body_lines = lines[closing_index + 1 :]
    body = "\n".join(body_lines).strip("\n")
    return metadata, body


def slugify(relative_path: Path) -> str:
    parts = []
    for part in relative_path.parts:
        if part.endswith(".md"):
            part = part[:-3]
        parts.append(part)
    raw = "-".join(parts)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", raw).strip("-").lower()
    return slug or "page"


def markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    html_parts: List[str] = []
    paragraph: List[str] = []
    in_ul = False
    in_ol = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            combined = " ".join(paragraph)
            html_parts.append(f"<p>{process_inline(combined)}</p>")
            paragraph = []

    for line in lines:
        stripped = line.rstrip()
        if not stripped.strip():
            flush_paragraph()
            close_lists()
            continue

        heading_match = re.match(r"^(#{1,6})\\s+(.*)", stripped)
        if heading_match:
            flush_paragraph()
            close_lists()
            level = min(len(heading_match.group(1)), 6)
            content = heading_match.group(2).strip()
            html_parts.append(f"<h{level}>{process_inline(content)}</h{level}>")
            continue

        ul_match = re.match(r"^[-*]\\s+(.*)", stripped)
        if ul_match:
            flush_paragraph()
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{process_inline(ul_match.group(1).strip())}</li>")
            continue

        ol_match = re.match(r"^\d+\\.\\s+(.*)", stripped)
        if ol_match:
            flush_paragraph()
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            html_parts.append(f"<li>{process_inline(ol_match.group(1).strip())}</li>")
            continue

        paragraph.append(stripped.strip())

    flush_paragraph()
    close_lists()

    return "\n".join(html_parts)


def process_inline(text: str) -> str:
    result: List[str] = []
    i = 0
    length = len(text)
    while i < length:
        if text.startswith("**", i):
            end = text.find("**", i + 2)
            if end != -1:
                inner = process_inline(text[i + 2 : end])
                result.append(f"<strong>{inner}</strong>")
                i = end + 2
                continue
        if text.startswith("*", i):
            end = text.find("*", i + 1)
            if end != -1:
                inner = process_inline(text[i + 1 : end])
                result.append(f"<em>{inner}</em>")
                i = end + 1
                continue
        if text.startswith("`", i):
            end = text.find("`", i + 1)
            if end != -1:
                inner = text[i + 1 : end]
                result.append(f"<code>{escape(inner)}</code>")
                i = end + 1
                continue
        if text.startswith("[", i):
            end_label = text.find("]", i + 1)
            if (
                end_label != -1
                and end_label + 1 < length
                and text[end_label + 1] == "("
            ):
                end_url = text.find(")", end_label + 2)
                if end_url != -1:
                    label = process_inline(text[i + 1 : end_label])
                    url = escape(text[end_label + 2 : end_url].strip())
                    result.append(f'<a href="{url}">{label}</a>')
                    i = end_url + 1
                    continue
        result.append(escape(text[i]))
        i += 1
    return "".join(result)


def render_page(*, title: str, description: str, body: str) -> str:
    nav = '<nav><a href="index.html">Home</a></nav>'
    meta_description = (
        escape(description) if description else "The Empowerment Economy manifesto."
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)} · The Empowerment Economy</title>
  <meta name=\"description\" content=\"{meta_description}\">
  <style>
    body {{
      background: #fff;
      color: #000;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 3rem auto;
      padding: 0 1.5rem;
      max-width: 70ch;
      line-height: 1.6;
    }}
    nav {{
      margin-bottom: 2rem;
    }}
    nav a {{
      color: inherit;
      text-decoration: none;
      font-weight: bold;
    }}
    nav a:hover {{
      text-decoration: underline;
    }}
    pre {{
      background: #f7f7f7;
      padding: 1rem;
      overflow-x: auto;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, SFMono, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }}
  </style>
</head>
<body>
  {nav}
  <main>
    {body}
  </main>
  <footer>
    <p>This site is part of <a href=\"https://github.com/demostheneslld/ai-philosophy-empowerment\">The Empowerment Economy project</a>, shared under an open licence.</p>
  </footer>
</body>
</html>"""


def render_index(grouped: Dict[str, List[Page]]) -> str:
    sections: List[str] = [
        "<h1>The Empowerment Economy</h1>",
        "<p>A community-managed manifesto, philosophy, and policy playbook for the AI age.</p>",
    ]

    for category, pages in sorted(
        grouped.items(),
        key=lambda item: (item[1][0].order if item[1] else 0, item[0].lower()),
    ):
        anchor = slugify(Path(category))
        sections.append(f'<section id="{anchor}">')
        sections.append(f"  <h2>{escape(category)}</h2>")
        sections.append("  <ul>")
        for page in pages:
            description = f" — {escape(page.description)}" if page.description else ""
            sections.append(
                f'    <li><a href="{page.url}">{escape(page.title)}</a>{description}</li>'
            )
        sections.append("  </ul>")
        sections.append("</section>")

    body = "\n".join(sections)
    return render_page(
        title="The Empowerment Economy",
        description="A manifesto and policy guide for AI-enabled empowerment.",
        body=body,
    )


if __name__ == "__main__":
    main()
