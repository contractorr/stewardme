"""Markdown → HTML rendering and allowlist sanitization for polished notes.

The renderer intentionally covers only the constructs the polisher is prompted
to emit (headings, paragraphs, emphasis, code, lists, blockquotes, links,
pipe tables, horizontal rules). All text is HTML-escaped before markup is
generated, and the final document is passed through an allowlist sanitizer as
defense-in-depth.
"""

import re
from html import escape

from bs4 import BeautifulSoup, Comment

ALLOWED_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "br",
    "hr",
    "strong",
    "em",
    "code",
    "pre",
    "ul",
    "ol",
    "li",
    "blockquote",
    "a",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed"}

_CODE_SPAN_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_HR_RE = re.compile(r"^(\s{0,3})(-{3,}|\*{3,}|_{3,})\s*$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_ULIST_RE = re.compile(r"^\s{0,3}[-*+]\s+(.*)$")
_OLIST_RE = re.compile(r"^\s{0,3}\d+[.)]\s+(.*)$")
_TABLE_DIVIDER_RE = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")


def _safe_href(url: str) -> str | None:
    url = url.strip()
    lowered = url.lower()
    if lowered.startswith(("http://", "https://")):
        return url
    return None


def _inline(text: str) -> str:
    """Render inline markdown on already-raw text; escapes everything first."""
    escaped = escape(text, quote=False)

    code_spans: list[str] = []

    def _stash_code(match: re.Match) -> str:
        code_spans.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(code_spans) - 1}\x00"

    escaped = _CODE_SPAN_RE.sub(_stash_code, escaped)

    def _link(match: re.Match) -> str:
        href = _safe_href(match.group(2))
        if href is None:
            return match.group(1)
        return f'<a href="{escape(href)}">{match.group(1)}</a>'

    escaped = _LINK_RE.sub(_link, escaped)
    escaped = _BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = _ITALIC_RE.sub(r"<em>\1</em>", escaped)

    for index, span in enumerate(code_spans):
        escaped = escaped.replace(f"\x00{index}\x00", span)
    return escaped


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    html: list[str] = []
    paragraph: list[str] = []
    list_tag: str | None = None
    blockquote: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            html.append(f"<p>{_inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_tag
        if list_tag:
            html.append(f"</{list_tag}>")
            list_tag = None

    def flush_blockquote() -> None:
        if blockquote:
            html.append(f"<blockquote><p>{_inline(' '.join(blockquote))}</p></blockquote>")
            blockquote.clear()

    def flush_all() -> None:
        flush_paragraph()
        flush_list()
        flush_blockquote()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_all()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
            index += 1
            continue

        if not stripped:
            flush_all()
            index += 1
            continue

        heading = _HEADING_RE.match(stripped)
        if heading:
            flush_all()
            level = len(heading.group(1))
            html.append(f"<h{level}>{_inline(heading.group(2).strip())}</h{level}>")
            index += 1
            continue

        if _HR_RE.match(line):
            flush_all()
            html.append("<hr>")
            index += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            blockquote.append(stripped.lstrip("> "))
            index += 1
            continue
        flush_blockquote()

        # Pipe table: header row followed by a divider row.
        if "|" in stripped and index + 1 < len(lines) and _TABLE_DIVIDER_RE.match(lines[index + 1]):
            flush_all()
            header = _table_cells(stripped)
            html.append("<table><thead><tr>")
            html.append("".join(f"<th>{_inline(cell)}</th>" for cell in header))
            html.append("</tr></thead><tbody>")
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                cells = _table_cells(lines[index])
                cells += [""] * (len(header) - len(cells))
                html.append(
                    "<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in cells) + "</tr>"
                )
                index += 1
            html.append("</tbody></table>")
            continue

        ulist = _ULIST_RE.match(line)
        olist = _OLIST_RE.match(line)
        if ulist or olist:
            flush_paragraph()
            tag = "ul" if ulist else "ol"
            if list_tag and list_tag != tag:
                flush_list()
            if not list_tag:
                html.append(f"<{tag}>")
                list_tag = tag
            html.append(f"<li>{_inline((ulist or olist).group(1))}</li>")
            index += 1
            continue
        flush_list()

        paragraph.append(stripped)
        index += 1

    flush_all()
    return "\n".join(html)


def sanitize_html(html: str) -> str:
    """Allowlist-filter an HTML fragment (defense-in-depth after rendering)."""
    soup = BeautifulSoup(html, "html.parser")

    for comment in soup.find_all(string=lambda node: isinstance(node, Comment)):
        comment.extract()

    for tag in list(soup.find_all(True)):
        if tag.name in DROP_WITH_CONTENT:
            tag.decompose()
            continue
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
            continue
        if tag.name == "a":
            href = _safe_href(tag.get("href", "") or "")
            tag.attrs = {}
            if href is None:
                tag.unwrap()
                continue
            tag.attrs = {"href": href, "rel": "noopener noreferrer"}
        else:
            tag.attrs = {}

    # Unwrapped tags may have left stray strings; re-serialize the tree.
    return str(soup)
