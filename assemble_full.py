#!/usr/bin/env python3
# 组装完整稿 — 三版输出：总完整版 / 无脚注版 / HTML 阅读器
import os, re, shutil, html as html_mod
from datetime import datetime

BASE = "E:/界限论"
OUT_HTML = f"{BASE}/docs"
KATEX = "vendor/katex"

files = [
    (f"{BASE}/界限论_导论_可读重写_v0_33.md",         "导论"),
    ("_零",                                             "第零章"),
    (f"{BASE}/界限论_第一章_可读重写_v0_21.md",         "第一章"),
    (f"{BASE}/界限论_第二章_可读重写_v0_19.md",         "第二章"),
    (f"{BASE}/界限论_第三章_可读重写_v1_4.md",          "第三章"),
    (f"{BASE}/界限论_第四章_可读重写_v0_24.md",         "第四章"),
    (f"{BASE}/界限论_第五章_可读重写_v0_13.md",          "第五章"),
    (f"{BASE}/界限论_第六章_可读重写_v0_21.md",         "第六章"),
    (f"{BASE}/界限论_第七章_可读重写_v0_26.md",         "第七章"),
    (f"{BASE}/界限论_第八章_可读重写_v0_14.md",         "第八章"),
    (f"{BASE}/界限论_第九章_可读重写_v0.14.md",         "第九章"),
    (f"{BASE}/界限论_尾声_可读重写_v0_12.md",           "尾声"),
    (f"{BASE}/界限论_附录W_v8_4.md",                    "附录"),
]

SAFE_NAME = {
    "导论": "introduction",
    "零": "start", "一": "twostreams", "二": "intentionality",
    "三": "unknowable", "四": "theother",
    "五": "worldtopos", "六": "intuition",
    "七": "assertion", "八": "classicalworld",
    "九": "boundary", "尾声": "epilogue", "附录": "appendixW",
}

PH_INLINE = "⟦MATH:{0}⟧"
PH_DISPLAY = "⟦MATHD:{0}⟧"

HTML_SHELL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{ max-width: 46rem; margin: 2rem auto; padding: 0 1.2rem;
         font-family: "Noto Serif SC", "Source Han Serif SC", Georgia, serif;
         font-size: 1.05rem; line-height: 1.75; color: #1a1a1a; }}
  h1 {{ font-size: 1.55rem; border-bottom: 1px solid #ddd; padding-bottom: .35rem; }}
  h2 {{ font-size: 1.22rem; margin-top: 1.8rem; }}
  h3 {{ font-size: 1.08rem; }}
  blockquote {{ border-left: 3px solid #bbb; margin: 1rem 0; padding: .2rem 0 .2rem 1rem; color: #333; }}
  code {{ background: #f5f5f5; padding: .08em .3em; border-radius: 3px; font-size: .9em; }}
  pre {{ background: #f5f5f5; padding: .75rem; overflow-x: auto; border-radius: 4px; }}
  .nav {{ font-size: .88rem; margin-bottom: 1.2rem; color: #666; }}
  .nav a {{ color: #0366d6; text-decoration: none; }}
  .math-block {{ text-align: center; margin: 1.2rem 0; }}
  .katex-display {{ margin: 1rem 0; overflow-x: auto; }}
  a.fn-ref {{ color: #0366d6; text-decoration: none; font-weight: 600; }}
  a.fn-ref:hover {{ text-decoration: underline; }}
  .footnotes {{ margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #ddd; font-size: .92rem; }}
  .footnotes h2 {{ font-size: 1rem; color: #666; margin-top: 0; }}
  ol.footnotes {{ padding-left: 1.4rem; }}
  li.footnote {{ margin: .65rem 0; }}
  li.footnote:target {{ background: #fff8e6; margin-left: -0.4rem; padding: .35rem .4rem; border-radius: 4px; }}
  a.fn-back {{ color: #666; text-decoration: none; margin-right: .35rem; }}
  a.fn-back:hover {{ color: #0366d6; }}
  a.ch-map {{ color: #0366d6; text-decoration: none; }}
  a.ch-map:hover {{ text-decoration: underline; }}
  .fn-back-list {{ margin-left: .25rem; font-size: .85em; color: #888; }}
  .fn-back-list a {{ color: #888; text-decoration: none; }}
  .fn-back-list a:hover {{ color: #0366d6; text-decoration: underline; }}
  .toc {{ background: #f8f9fa; padding: .6rem 1rem; border-radius: 6px; margin: 1rem 0; font-size: .9rem; }}
  .toc strong {{ display: block; margin-bottom: .3rem; color: #444; }}
  .toc ul {{ margin: 0; padding-left: 1.2rem; list-style: none; }}
  .toc li {{ margin: .2rem 0; }}
  a.toc-link {{ color: #0366d6; text-decoration: none; }}
  a.toc-link:hover {{ text-decoration: underline; }}
  .math-block {{ overflow-x: auto; overflow-y: hidden; }}
  .math-block::-webkit-scrollbar {{ height: 6px; }}
  .math-block::-webkit-scrollbar-thumb {{ background: #ccc; border-radius: 3px; }}
  .math-block::-webkit-scrollbar-thumb:hover {{ background: #999; }}
  #status {{ font-size: .85rem; color: #888; margin-top: 2rem; }}
  #status.err {{ color: #c00; }}
</style>
<link rel="stylesheet" href="{katex}/katex.min.css">
<script defer src="{katex}/katex.min.js"></script>
<script defer src="{katex}/auto-render.min.js"></script>
</head>
<body>
<p class="nav"><a href="index.html">← 目录</a></p>
{body}
<p id="status">正在渲染公式…</p>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  var st = document.getElementById('status');
  if (typeof renderMathInElement !== 'function') {{
    st.className = 'err';
    st.textContent = 'KaTeX 未加载（请确认 vendor/katex 文件夹完整）。';
    return;
  }}
  try {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '\\\\[', right: '\\\\]', display: true}},
        {{left: '\\\\(', right: '\\\\)', display: false}},
        {{left: '$', right: '$', display: false}}
      ],
      throwOnError: false
    }});
    st.textContent = '公式已由 KaTeX 渲染（本地，无需联网）。';
  }} catch (e) {{
    st.className = 'err';
    st.textContent = 'KaTeX 渲染出错: ' + e;
  }}
  if (location.hash && location.hash.indexOf('fn-') === 1) {{
    var el = document.getElementById(location.hash.slice(1));
    if (el) el.scrollIntoView({{ block: 'center' }});
  }}
}});
</script>
</body>
</html>
"""

FN_REF = re.compile(r'\[\^([\w-]+)\](?!:)')
FN_DEF = re.compile(r'^\[\^([\w-]+)\]:\s*(.*)', re.M)


# ── 章节加载与清理 ──────────────────────────────────────────

def clean_title(line):
    line = re.sub(r'\s*[（(][^）)]*[）)]', '', line)
    return line.strip()


def clean_chapter(text, ch_name):
    sep = '\n---\n'
    while True:
        last = text.rfind(sep)
        if last < 0:
            break
        after = text[last + len(sep):].strip()
        if after.startswith('*'):
            text = text[:last]
        else:
            break

    lines = text.split('\n')
    result = []
    for line in lines:
        if line.startswith('# ') and ch_name != '导论':
            line = clean_title(line)
        result.append(line)

    text = '\n'.join(result)
    text = re.sub(r'\n---\n', '\n* * *\n', text)
    return text


def strip_footnotes_and_refs(text, ch_name=""):
    text = re.sub(r'\n(?:---\n)?## 脚注\n.*?(?=\n---\n|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'\n(?:---\n)?## 参考文献\n.*?(?=\n---\n|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'\n(?:---\n)?### 参考文献\n.*?(?=\n---\n|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'\n\[\^[\w-]+\]:[^\n]*(?:\n(?!\[\^[\w-]+\]:|\n---\n)[^\n]*)*', '', text)
    text = re.sub(r'\[\^[\w-]+\]', '', text)
    if '附录' in ch_name:
        m = re.search(r'\n## W\.6\b', text)
        if m:
            text = text[:m.start()]
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def load_chapter(file_path, ch_name):
    if file_path == "_零":
        actual = f"{BASE}/界限论_第零章_可读重写_v0_35.md"
    else:
        actual = file_path
    with open(actual, encoding="utf-8") as f:
        return f.read()


def chapter_html_name(i, ch_name):
    short = ch_name.replace("章", "").replace("第", "")
    sname = SAFE_NAME.get(short, ch_name)
    return f"{i:02d}_{sname}.html"


def build_chapter_link_map():
    """第零章～第九章 → HTML 文件名（与 files 列表同步，无需另维护）。"""
    return {
        ch_name: chapter_html_name(i, ch_name)
        for i, (_, ch_name) in enumerate(files, 1)
        if ch_name != "导论"
    }


def linkify_chapter_map(html, link_map):
    """导论「章节地图」blockquote 内的 **第X章** → 跳转链接（仅 HTML 层）。"""
    marker = "章节地图"
    idx = html.find(marker)
    if idx < 0:
        return html
    bq_start = html.rfind("<blockquote>", 0, idx)
    bq_end = html.find("</blockquote>", idx)
    if bq_start < 0 or bq_end < 0:
        return html
    segment = html[bq_start:bq_end]
    for ch_label, href in link_map.items():
        segment = segment.replace(
            f"<strong>{ch_label}</strong>",
            f'<strong><a href="{href}" class="ch-map">{ch_label}</a></strong>',
        )
    return html[:bq_start] + segment + html[bq_end:]


# ── 附录目录（自动生成） ──────────────────────────────────

def heading_anchor(text):
    """从 ## 标题文本生成 HTML 锚点 ID。"""
    plain = re.sub(r'⟦MATH:?\d+⟧', '', text).strip()
    m = re.match(r'(W[\d.★]+)', re.sub(r'\s', '', plain))
    if m:
        return m.group(1).lower().replace('.', '-').replace('★', 'star')
    s = re.sub(r'[^\w\u4e00-\u9fff]+', '-', plain).strip('-').lower()
    return s


def extract_h2_headings(md_text):
    """从附录 Markdown 提取 ## 标题 + 锚点 ID。"""
    heads = []
    for line in md_text.splitlines():
        s = line.strip()
        if s.startswith('## '):
            text = s[3:].strip()
            heads.append((heading_anchor(text), text))
    return heads


def toc_html(headings):
    if not headings:
        return ''
    items = '\n'.join(
        f'    <li><a href="#{h}" class="toc-link">{html_mod.escape(t)}</a></li>'
        for h, t in headings
    )
    return f'<div class="toc"><strong>目录（可点击跳转）</strong><ul>\n{items}\n</ul></div>\n'


def title_from_md(text):
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return "章节"


def ts():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def load_all_chapters():
    chapters = []
    for i, (file_path, ch_name) in enumerate(files, 1):
        ch = clean_chapter(load_chapter(file_path, ch_name), ch_name)
        chapters.append((chapter_html_name(i, ch_name), ch_name, ch))
    return chapters


# ── Markdown → HTML ─────────────────────────────────────────

def extract_math(text):
    store = []

    def put(content, display=False):
        idx = len(store)
        store.append((display, content.strip()))
        return PH_DISPLAY.format(idx) if display else PH_INLINE.format(idx)

    text = re.sub(r'\$\$([\s\S]*?)\$\$', lambda m: put(m.group(1), True), text)
    text = re.sub(r'\$([^$\n]+?)\$', lambda m: put(m.group(1), False), text)
    return text, store


def restore_math(html, store):
    for i, (display, content) in enumerate(store):
        ph = PH_DISPLAY.format(i) if display else PH_INLINE.format(i)
        repl = f'\\[{content}\\]' if display else f'\\({content}\\)'
        html = html.replace(ph, repl)
    return html


class FootnoteIndex:
    def __init__(self, chapters):
        self.chapters = chapters  # [(html_name, md_text), ...]
        self.defs = {}
        self.backrefs = {}
        self._scan_defs()
        self._scan_backrefs()

    def _scan_defs(self):
        for html_name, md in self.chapters:
            for m in FN_DEF.finditer(md):
                fid = m.group(1)
                key = (html_name, fid)
                if key not in self.defs:
                    self.defs[key] = m.group(2)

    def _scan_backrefs(self):
        for ref_html, md in self.chapters:
            seen = set()
            for m in FN_REF.finditer(md):
                fid = m.group(1)
                def_html = self.locate_def(ref_html, fid)
                if not def_html:
                    continue
                key = (def_html, fid)
                anchor = f"fnref-{fid}" if fid not in seen else None
                if fid not in seen:
                    seen.add(fid)
                    anchor = f"fnref-{fid}"
                self.backrefs.setdefault(key, []).append((ref_html, anchor))

    def locate_def(self, ref_html, fid):
        if (ref_html, fid) in self.defs:
            return ref_html
        for html_name, _ in self.chapters:
            if (html_name, fid) in self.defs:
                return html_name
        return None

    def href(self, ref_html, fid):
        def_html = self.locate_def(ref_html, fid)
        if not def_html:
            return None
        if def_html == ref_html:
            return f"#fn-{fid}"
        return f"{def_html}#fn-{fid}"

    def back_links(self, def_html, fid):
        links = []
        for ref_html, anchor in self.backrefs.get((def_html, fid), []):
            if not anchor:
                continue
            href = f"{ref_html}#{anchor}" if ref_html != def_html else f"#{anchor}"
            label = "正文" if ref_html == def_html else ref_html.replace('.html', '')
            links.append((href, label))
        return links


class PageConverter:
    def __init__(self, html_name, fn_index):
        self.html_name = html_name
        self.fn_index = fn_index
        self.fn_ref_seen = set()
        self.footnote_items = []

    def fmt_inline(self, s):
        parts = re.split(r'(⟦MATH:?[\d]+⟧)', s)

        def footnote_link(m):
            fid = m.group(1)
            href = self.fn_index.href(self.html_name, fid)
            label = html_mod.escape(fid)
            if not href:
                return f'<sup class="fn-missing" title="未找到脚注定义">[{label}]</sup>'
            if fid not in self.fn_ref_seen:
                self.fn_ref_seen.add(fid)
                return (
                    f'<sup><a href="{html_mod.escape(href)}" id="fnref-{fid}" '
                    f'class="fn-ref">[{label}]</a></sup>'
                )
            return f'<sup><a href="{html_mod.escape(href)}" class="fn-ref">[{label}]</a></sup>'

        out = []
        for p in parts:
            if p.startswith('⟦MATH'):
                out.append(p)
            else:
                p = html_mod.escape(p)
                p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
                p = FN_REF.sub(footnote_link, p)
                out.append(p)
        return ''.join(out)

    def collect_footnote(self, fid, body):
        content = self.fmt_inline(body)
        backs = self.fn_index.back_links(self.html_name, fid)
        back_html = ''
        if backs:
            parts = [
                f'<a href="{html_mod.escape(h)}" class="fn-back" title="返回引用处">↩</a>'
                for h, _ in backs[:1]
            ]
            if len(backs) > 1:
                extra = ', '.join(
                    f'<a href="{html_mod.escape(h)}">{html_mod.escape(lbl)}</a>'
                    for h, lbl in backs[1:]
                )
                back_html = f'<span class="fn-back-list"> · 亦见 {extra}</span>'
            back_html = parts[0] + back_html if parts else ''
        self.footnote_items.append(
            (fid, f'<li id="fn-{fid}" class="footnote">{back_html}{content}</li>')
        )

    def md_to_html(self, text):
        text, math_store = extract_math(text)
        lines = text.split('\n')
        out = []
        i = 0
        in_pre = False
        quote_lines = []

        def flush_quote():
            nonlocal quote_lines
            if quote_lines:
                body = '<br>\n'.join(self.fmt_inline(l) for l in quote_lines)
                out.append(f'<blockquote><p>{body}</p></blockquote>')
                quote_lines = []

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if in_pre:
                if stripped.startswith('```'):
                    out.append('</code></pre>')
                    in_pre = False
                else:
                    out.append(html_mod.escape(line))
                i += 1
                continue

            if stripped.startswith('```'):
                flush_quote()
                out.append('<pre><code>')
                in_pre = True
                i += 1
                continue

            if stripped.startswith('>'):
                quote_lines.append(stripped.lstrip('>').strip())
                i += 1
                continue
            if quote_lines and stripped == '':
                flush_quote()
                i += 1
                continue
            if quote_lines and not stripped.startswith('>'):
                flush_quote()

            if stripped == '' or stripped == '* * *':
                i += 1
                continue

            if re.fullmatch(r'⟦MATHD:\d+⟧', stripped):
                out.append(f'<div class="math-block">{stripped}</div>')
                i += 1
                continue

            m_def = FN_DEF.match(stripped)
            if m_def:
                self.collect_footnote(m_def.group(1), m_def.group(2))
                i += 1
                continue

            if stripped.startswith('### '):
                out.append(f'<h3>{self.fmt_inline(stripped[4:])}</h3>')
            elif stripped.startswith('## '):
                h2_text = stripped[3:]
                h2_id = heading_anchor(h2_text)
                out.append(f'<h2 id="{h2_id}">{self.fmt_inline(h2_text)}</h2>')
            elif stripped.startswith('# '):
                out.append(f'<h1>{self.fmt_inline(stripped[2:])}</h1>')
            elif stripped.startswith('|') and i + 1 < len(lines) and '|' in lines[i + 1]:
                rows = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    if not re.match(r'^\|[\s\-:|]+\|$', lines[i].strip()):
                        cells = [self.fmt_inline(c.strip()) for c in lines[i].strip().strip('|').split('|')]
                        rows.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
                    i += 1
                out.append('<table border="1" cellpadding="6" cellspacing="0">' + ''.join(rows) + '</table>')
                continue
            else:
                para = [line]
                i += 1
                while i < len(lines):
                    s = lines[i].strip()
                    if s == '' or s == '* * *' or s.startswith('#') or s.startswith('>') or s.startswith('```'):
                        break
                    if re.fullmatch(r'⟦MATHD:\d+⟧', s):
                        break
                    if FN_DEF.match(s):
                        break
                    para.append(lines[i])
                    i += 1
                out.append(f'<p>{self.fmt_inline(" ".join(p.strip() for p in para))}</p>')
                continue
            i += 1

        flush_quote()
        body = restore_math('\n'.join(out), math_store)
        if self.footnote_items:
            items = '\n'.join(
                restore_math(html, math_store) for _, html in self.footnote_items
            )
            body += f'\n<section class="footnotes"><h2>脚注</h2><ol class="footnotes">\n{items}\n</ol></section>'
        return body


def write_html_page(path, title, body_html):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(HTML_SHELL.format(title=html_mod.escape(title), body=body_html, katex=KATEX))


def export_html(chapters):
    """chapters: [(html_name, ch_name, md_text), ...]"""
    os.makedirs(OUT_HTML, exist_ok=True)
    html_chapters = [(h, md) for h, _, md in chapters]
    fn_index = FootnoteIndex(html_chapters)

    index_items = []
    chapter_links = build_chapter_link_map()
    for html_name, ch_name, md in chapters:
        title = title_from_md(md)
        conv = PageConverter(html_name, fn_index)
        body = conv.md_to_html(md)
        if ch_name == "导论":
            body = linkify_chapter_map(body, chapter_links)
        if ch_name == "附录":
            heads = extract_h2_headings(md)
            toc = toc_html(heads)
            body = body.replace('</h1>', f'</h1>\n{toc}', 1)
        write_html_page(os.path.join(OUT_HTML, html_name), title, body)
        index_items.append((html_name, title))
        print(f"    {html_name}")

    links = '\n'.join(
        f'    <li><a href="{html_mod.escape(h)}">{html_mod.escape(t)}</a></li>'
        for h, t in index_items
    )
    index = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>《界限论》阅读器</title>
<style>body{{max-width:36rem;margin:2rem auto;font-family:serif;line-height:1.6}}
a{{color:#0366d6}} .note{{color:#666;font-size:.95rem}}</style></head>
<body>
<h1>《界限论》阅读器</h1>
<p class="note">用 Chrome / Edge 直接打开（本地 KaTeX，无需联网）。
脚注可点击跳转；跨章引用会自动跳到对应章节。</p>
<p class="note">生成：{datetime.now():%Y-%m-%d %H:%M}</p>
<ul>{links}</ul>
</body></html>"""
    with open(f"{OUT_HTML}/index.html", 'w', encoding='utf-8', newline='\n') as f:
        f.write(index)
    print(f"    index.html")


# ── 主流程 ──────────────────────────────────────────────────

def main():
    split_dir = f"{BASE}/分章完整稿"
    if os.path.isdir(split_dir):
        shutil.rmtree(split_dir)
        print(f"Removed: {split_dir}")

    chapters = load_all_chapters()
    stamp = ts()

    # 1. 总完整版
    output = []
    for html_name, ch_name, ch in chapters:
        ch = ch.rstrip() + '\n'
        if ch_name == "导论":
            lines = ch.split('\n')
            if lines and lines[0].startswith('# '):
                lines[0] = '# 《界限论》'
            ch = '\n'.join(lines)
        output.append(ch)
        output.append('\n\n* * *\n\n')

    result = f'<!-- Assembled: {stamp} -->\n' + ''.join(output).rstrip() + '\n'
    out_full = f"{BASE}/界限论_完整稿.md"
    with open(out_full, "w", encoding="utf-8", newline='\n') as f:
        f.write(result)
    print(f"[1/3] FULL     → {out_full}")

    # 2. 无脚注版
    output = []
    for html_name, ch_name, ch in chapters:
        ch = ch.rstrip() + '\n'
        if ch_name == "导论":
            lines = ch.split('\n')
            if lines and lines[0].startswith('# '):
                lines[0] = '# 《界限论》（精读版 · 省略了大量数学脚注与开放命题）'
            ch = '\n'.join(lines)
        ch = strip_footnotes_and_refs(ch, ch_name)
        output.append(ch)
        output.append('\n\n* * *\n\n')

    result = f'<!-- Assembled: {stamp} -->\n' + ''.join(output).rstrip() + '\n'
    out_stripped = f"{BASE}/界限论_完整稿_无脚注.md"
    with open(out_stripped, "w", encoding="utf-8", newline='\n') as f:
        f.write(result)
    print(f"[2/3] STRIPPED → {out_stripped}")

    # 3. HTML 阅读器
    print(f"[3/3] HTML     → {OUT_HTML}/")
    export_html(chapters)

    print("\nDone.")


if __name__ == '__main__':
    main()
