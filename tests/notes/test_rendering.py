"""Tests for markdown rendering and HTML sanitization."""

from notes.rendering import markdown_to_html, sanitize_html

# --- markdown_to_html ---


def test_headings_and_paragraphs():
    html = markdown_to_html("# Title\n\nSome **bold** and *italic* text.")
    assert "<h1>Title</h1>" in html
    assert "<p>Some <strong>bold</strong> and <em>italic</em> text.</p>" in html


def test_lists():
    html = markdown_to_html("- one\n- two\n\n1. first\n2. second")
    assert "<ul>" in html and html.count("<li>") == 4 and "<ol>" in html


def test_fenced_code_blocks_are_escaped_verbatim():
    html = markdown_to_html("```\n<script>alert('x')</script>\n**not bold**\n```")
    assert "<pre><code>" in html
    assert "&lt;script&gt;" in html
    assert "<strong>" not in html


def test_inline_code_not_emphasized():
    html = markdown_to_html("use `a * b * c` here")
    assert "<code>a * b * c</code>" in html
    assert "<em>" not in html


def test_links_only_http_https():
    html = markdown_to_html("[ok](https://example.com) [bad](javascript:alert(1))")
    assert '<a href="https://example.com">ok</a>' in html
    assert "javascript:" not in html
    assert "bad" in html  # text kept, link dropped


def test_blockquote_and_hr():
    html = markdown_to_html("> quoted wisdom\n\n---")
    assert "<blockquote><p>quoted wisdom</p></blockquote>" in html
    assert "<hr>" in html


def test_pipe_table():
    html = markdown_to_html("| a | b |\n| --- | --- |\n| 1 | 2 |")
    assert "<table>" in html
    assert "<th>a</th>" in html
    assert "<td>2</td>" in html


def test_raw_html_in_markdown_is_escaped():
    html = markdown_to_html("<img src=x onerror=alert(1)> hello")
    assert "<img" not in html
    assert "&lt;img" in html


# --- sanitize_html ---


def test_sanitize_strips_script_entirely():
    assert "alert" not in sanitize_html("<p>ok</p><script>alert(1)</script>")


def test_sanitize_removes_event_handlers():
    out = sanitize_html('<p onclick="evil()">text</p>')
    assert "onclick" not in out
    assert "<p>text</p>" in out


def test_sanitize_unwraps_unknown_tags():
    out = sanitize_html("<article><p>kept</p></article>")
    assert "<article>" not in out
    assert "<p>kept</p>" in out


def test_sanitize_drops_javascript_hrefs():
    out = sanitize_html('<a href="javascript:alert(1)">x</a>')
    assert "javascript:" not in out


def test_sanitize_keeps_https_links_with_rel():
    out = sanitize_html('<a href="https://example.com" target="_blank">x</a>')
    assert 'href="https://example.com"' in out
    assert "target" not in out
    assert 'rel="noopener noreferrer"' in out


def test_sanitize_removes_comments():
    assert "secret" not in sanitize_html("<p>a</p><!-- secret -->")


def test_end_to_end_render_and_sanitize():
    md = "# Notes\n\n- item `code`\n\n[link](https://x.dev)\n\n<script>boom()</script>"
    out = sanitize_html(markdown_to_html(md))
    assert "<h1>Notes</h1>" in out
    assert "<code>code</code>" in out
    assert "boom" not in out or "<script>" not in out
