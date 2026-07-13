#!/usr/bin/env python3
# 组装完整稿 — 三版输出：总完整版 / 无脚注版 / HTML 阅读器
import os, re, shutil, html as html_mod, json
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
    (f"{BASE}/界限论_附录W_v8_5.md",                    "附录"),
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
         font-size: 1.05rem; line-height: 1.75;
         background: #1b1b18; color: #c8c4bc; }}
  h1 {{ font-size: 1.55rem; border-bottom: 1px solid #3a3a35; padding-bottom: .35rem; color: #e0dcd4; }}
  h2 {{ font-size: 1.22rem; margin-top: 2.4rem; padding-top: 2rem; border-top: 1px solid #3a3a35; color: #d8d4cc; }}
  h2:first-of-type {{ border-top: none; margin-top: 0; padding-top: 0; }}
  h3 {{ font-size: 1.08rem; color: #d0ccc4; }}
  blockquote {{ border-left: 3px solid #4a4a44; margin: 1rem 0; padding: .2rem 0 .2rem 1rem; color: #a8a49c; }}
  code {{ background: #2a2a26; padding: .08em .3em; border-radius: 3px; font-size: .9em; color: #c0bca0; }}
  pre {{ background: #242420; padding: .75rem; overflow-x: auto; border-radius: 4px; color: #c8c4bc; }}
  .nav {{ font-size: .88rem; margin-bottom: 1.2rem; color: #7a766e; }}
  .nav a {{ color: #7eb8da; text-decoration: none; }}
  .math-block {{ text-align: center; margin: 1.2rem 0; overflow-x: auto; overflow-y: hidden; scrollbar-width: none; }}
  .math-block::-webkit-scrollbar {{ display: none; }}
  .katex-display {{ margin: 1rem 0; overflow-x: auto; scrollbar-width: none; }}
  .katex-display::-webkit-scrollbar {{ display: none; }}
  a.fn-ref {{ color: #7eb8da; text-decoration: none; font-weight: 600; }}
  a.fn-ref:hover {{ text-decoration: underline; }}
  .footnotes {{ margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #3a3a35; font-size: .92rem; }}
  ol.footnotes {{ padding: 0 0 0 1.4rem; margin: 0; }}
  li.footnote {{ padding: .35rem 0; margin: 0; }}
  li.footnote:target {{ background: #2a2818; margin-left: -0.4rem; padding: .35rem .4rem; border-radius: 4px; }}
  a.fn-back {{ color: #8a867e; text-decoration: none; margin-right: .35rem; }}
  a.fn-back:hover {{ color: #7eb8da; }}
  a.ch-map {{ color: #7eb8da; text-decoration: none; }}
  a.ch-map:hover {{ text-decoration: underline; }}
  .fn-back-list {{ margin-left: .25rem; font-size: .85em; color: #7a766e; }}
  .fn-back-list a {{ color: #7a766e; text-decoration: none; }}
  .fn-back-list a:hover {{ color: #7eb8da; text-decoration: underline; }}
  .toc {{ background: #242420; padding: .6rem 1rem; border-radius: 6px; margin: 1rem 0; font-size: .9rem; }}
  .toc strong {{ display: block; margin-bottom: .3rem; color: #a8a49c; }}
  .toc ul {{ margin: 0; padding-left: 1.2rem; list-style: none; }}
  .toc li {{ margin: .2rem 0; }}
  a.toc-link {{ color: #7eb8da; text-decoration: none; }}
  a.toc-link:hover {{ text-decoration: underline; }}
  .diagram {{ background: #242420; padding: .75rem; overflow-x: auto; border-radius: 4px;
             font-size: .88rem; line-height: 1.35; }}
  .diagram code {{ background: none; padding: 0; }}
  a.d-link {{ color: #7eb8da; text-decoration: none; }}
  a.d-link:hover {{ text-decoration: underline; }}
  a.w-ref {{ color: #7eb8da; text-decoration: none; }}
  a.w-ref:hover {{ text-decoration: underline; }}
  .map-btn {{ position: fixed; top: .8rem; right: 1rem; z-index: 9999;
              font-size: .92rem; color: #c8c4bc; background: rgba(20,20,18,.88);
              padding: .35rem .7rem; border-radius: 6px; cursor: pointer;
              border: 1px solid #4a4a44; text-decoration: none; }}
  .map-btn:hover {{ color: #fff; background: rgba(40,40,35,.92); }}
  #map-overlay {{ display: none; position: fixed; top: 0; right: 0; z-index: 10000;
                  width: auto; max-width: 80vw; min-width: 480px;
                  background: rgba(14,14,12,.93);
                  border-radius: 0 0 0 18px; padding: 1.2rem 1.6rem 1rem 1.6rem;
                  box-shadow: -6px 6px 36px rgba(0,0,0,.6); overflow: hidden; }}
  #map-overlay.active {{ display: block; }}
  .map-container {{ position: relative; background: #f5f3eb; border-radius: 12px;
                    padding: 0 0 .6rem 0; }}
  .map-titlebar {{ display: flex; justify-content: space-between; align-items: center;
                    padding: .5rem 1rem .35rem 1rem; border-bottom: 1px solid #e0dcd4; }}
  .map-titlebar a {{ color: #7eb8da; text-decoration: none; font-size: .9rem; }}
  .map-titlebar a:hover {{ text-decoration: underline; }}
  .map-close {{ font-size: 1.5rem; color: #5f5e5a; cursor: pointer; background: none;
               border: none; line-height: 1; padding: 0 .15rem; }}
  .map-close:hover {{ color: #1b1b18; }}
  .map-svg-wrap {{ padding: 1.4rem 1.6rem 0 1.6rem; }}
  .map-svg-wrap object {{ width: 100%; display: block; }}
  /* --- footnote bubble --- */
  a.fn-a {{ color: #7eb8da; text-decoration: none; font-weight: 600; cursor: pointer; }}
  a.fn-a:hover {{ text-decoration: underline; }}
  .fn-bubble {{ position: fixed; max-width: 360px; background: #2a2a24; border: 1px solid #4a4a44;
                border-radius: 8px; padding: .7rem .9rem; font-size: .9rem; z-index: 9999;
                box-shadow: 0 6px 24px rgba(0,0,0,.7); line-height: 1.55; color: #c8c4bc; }}
  .fn-bubble-close {{ position: absolute; top: .15rem; right: .4rem; font-size: 1.1rem;
                     color: #8a867e; cursor: pointer; background: none; border: none; line-height:1; padding:0 .1rem; }}
  .fn-bubble-close:hover {{ color: #e0dcd4; }}
  .fn-bubble-arrow {{ position: absolute; bottom: 100%; left: 1rem; width: 0; height: 0;
                      border-left: 7px solid transparent; border-right: 7px solid transparent;
                      border-bottom: 7px solid #4a4a44; }}
  .fn-bubble-arrow::after {{ content: ''; position: absolute; bottom: -6px; left: -6px;
                              border-left: 6px solid transparent; border-right: 6px solid transparent;
                              border-bottom: 6px solid #2a2a24; }}
  .fn-section {{ font-size: .96rem; color: #8a867e; margin: 1.5rem 0 0 0; font-weight: 600; letter-spacing: .05em; }}
  .fn-section:first-child {{ margin-top: 0; }}
  #status {{ font-size: .85rem; color: #7a766e; margin-top: 2rem; }}
  #status.err {{ color: #d86; }}
  table {{ border-collapse: collapse; }}
  td, th {{ border: 1px solid #3a3a35; padding: .35rem .6rem; }}
  @media (max-width: 600px) {{
    body {{ font-size: .98rem; padding: 0 .8rem; margin: 1rem auto; }}
    h1 {{ font-size: 1.35rem; }}
    h2 {{ font-size: 1.1rem; }}
    pre, .diagram {{ font-size: .8rem; padding: .5rem; }}
    blockquote {{ margin: .6rem 0; padding: .15rem 0 .15rem .7rem; }}
  }}
</style>
<link rel="stylesheet" href="{katex}/katex.min.css">
<script defer src="{katex}/katex.min.js"></script>
<script defer src="{katex}/auto-render.min.js"></script>
</head>
<body>
<span class="map-btn" onclick="showMap()" title="主线图景">🗺 主线图景</span>
<p class="nav"><a href="index.html">← 目录</a></p>
{body}
<div id="map-overlay">
 <div class="map-container">
  <div class="map-titlebar">
   <a href="index.html">← 目录</a>
   <button class="map-close" onclick="hideMap()" aria-label="关闭">✕</button>
  </div>
  <div class="map-svg-wrap"><object id="map-svg" data="reality-map.svg" type="image/svg+xml"></object></div>
 </div>
</div>
<p id="status">正在渲染公式…</p>
<script>
function showMap() {{
  document.getElementById('map-overlay').classList.add('active');
}}
function hideMap() {{
  document.getElementById('map-overlay').classList.remove('active');
}}
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') {{ hideMap(); closeAllBubbles(); }}
}});
document.addEventListener('click', function(e) {{
  var ov = document.getElementById('map-overlay');
  var btn = document.querySelector('.map-btn');
  if (ov.classList.contains('active') && !ov.contains(e.target) && e.target !== btn) {{
    hideMap();
  }}
  if (!e.target.closest('.fn-bubble')) {{
    closeAllBubbles();
  }}
  var fnA = e.target.closest('a.fn-a');
  if (fnA && fnA.dataset.fn) {{
    e.preventDefault();
    showFnBubble(fnA, fnA.dataset.fn);
  }}
}});
function closeAllBubbles() {{
  document.querySelectorAll('.fn-bubble').forEach(function(b){{b.remove();}});
}}
function showFnBubble(a, fid) {{
  closeAllBubbles();
  var content = FN_CONTENT[fid];
  if (!content) return;
  var b = document.createElement('div');
  b.className = 'fn-bubble';
  b.innerHTML = '<button class="fn-bubble-close" onclick="this.parentNode.remove()">✕</button>'
              + '<div class="fn-bubble-arrow"></div>' + content;
  document.body.appendChild(b);
  var rect = a.getBoundingClientRect();
  var bRect = b.getBoundingClientRect();
  var top = rect.bottom + 8;
  var left = rect.left + rect.width / 2 - 20;
  if (left + bRect.width > window.innerWidth - 12) left = window.innerWidth - bRect.width - 12;
  if (left < 8) left = 8;
  if (top + bRect.height > window.innerHeight - 12) {{
    top = rect.top - bRect.height - 8;
    b.querySelector('.fn-bubble-arrow').style.cssText = 'top:100%;bottom:auto;border-top:7px solid #4a4a44;border-bottom:none';
  }}
  b.style.left = left + 'px';
  b.style.top = top + 'px';
  b.style.opacity = 0;
  b.addEventListener('transitionend', function(){{b.style.transition='';}});
  setTimeout(function(){{b.style.opacity=1;b.style.transition='opacity .12s';}},20);
}}
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
        if after.startswith('*') or after.startswith('>'):
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
    if ch_name == "导论":
        text = re.sub(r'\n>\s*副标题[：:]\s*.+', '', text, count=1)
        text = re.sub(r'\n---\n(?=\s*\n## )', '\n', text, count=1)
        text = re.sub(r'\n{3,}', '\n\n', text)
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


def w_ref_anchor(ref, *, use_lemma_alias=True):
    """W.x.y 标签 → HTML 锚点 id（与 heading_anchor 同规则）。"""
    ref = ref.strip()
    if use_lemma_alias and ref == 'W.2.1':
        return 'w-1-star'  # 无凸显态引理：正文称 W.2.1，节号 W.1.★
    m = re.match(r'(W[\d.★]+)', ref)
    if not m:
        return None
    return m.group(1).lower().replace('.', '-').replace('★', 'star').rstrip('-')


def linkify_w_refs(html):
    """附录内 W.x / [第 W.x 节] → 锚点链接（跳过已有链接与 pre/code）。"""
    chunks = re.split(r'(<a\b[^>]*>.*?</a>|<pre\b[^>]*>.*?</pre>)', html, flags=re.S)
    ph = '⟦WREF:{}⟧'

    def link_chunk(text):
        slots = {}

        def put(label, href, display=None):
            key = len(slots)
            slots[key] = (
                f'<a href="#{href}" class="w-ref">{display or label}</a>'
            )
            return ph.format(key)

        text = re.sub(
            r'\[第 (W\.\d+(?:\.\d+)*) 节\]',
            lambda m: put(m.group(1), w_ref_anchor(m.group(1)), f'第 {m.group(1)} 节'),
            text,
        )
        text = re.sub(
            r'(?<![">=\w])(W\.\d+\.\d+(?:\.\d+)?–(?:W\.)?\d+(?:\.\d+)*)',
            lambda m: put(
                m.group(1),
                w_ref_anchor(re.match(r'(W\.\d+)', m.group(1)).group(1), use_lemma_alias=False),
            ),
            text,
        )
        text = re.sub(
            r'(?<![">=\w])(W\.\d+(?:\.\d+){0,2})(?![\w.])',
            lambda m: (
                put(m.group(1), w_ref_anchor(m.group(1)))
                if w_ref_anchor(m.group(1)) else m.group(1)
            ),
            text,
        )
        for key, link in slots.items():
            text = text.replace(ph.format(key), link)
        return text

    for i in range(0, len(chunks), 2):
        chunks[i] = link_chunk(chunks[i])
    return ''.join(chunks)


DPIAGRAM_REPLACE = [
    ('                    公理 Σ  (W.1:M 为 III₁ 因子 · 可分)',
     '                    公理 Σ  (<a href="#w-1" class="d-link">W.1</a>:M 为 III₁ 因子 · 可分)'),
    ('        ┌──────── 引理 W.2.1  无凸显态 ────────┐   ← 全篇总源头(枢纽)',
     '        ┌──────── <a href="#w-1-star" class="d-link">引理 W.2.1  无凸显态</a> ────────┐   ← 全篇总源头(枢纽)'),
    ('   中心定理             + Cartan/FM 框架       (下游各处引用,',
     '   <a href="#w-2" class="d-link">中心定理</a>             + <a href="#w-1" class="d-link">Cartan/FM 框架</a>       (下游各处引用,'),
    (' (视角不可内生)            (W.1)                 不重复证明)',
     ' (<a href="#w-2" class="d-link">视角不可内生</a>)            (<a href="#w-1" class="d-link">W.1</a>)                 不重复证明)'),
    ('   主定理 A             主定理 B',
     '   <a href="#w-2" class="d-link">主定理 A</a>             <a href="#w-3" class="d-link">主定理 B</a>'),
    (' (不可能性:统一          (刻画:缝 = [σ] ∈',
     ' (<a href="#w-2" class="d-link">不可能性:统一</a>          (<a href="#w-3" class="d-link">刻画:缝 = [σ] ∈</a>'),
    ('  动力学不可自给)         H²(R,𝕋),他者身份)',
     '  <a href="#w-2" class="d-link">动力学不可自给</a>)         <a href="#w-3" class="d-link">H²(R,𝕋),他者身份</a>)'),
    ('        │              主定理 C',
     '        │              <a href="#w-4" class="d-link">主定理 C</a>'),
    ('        │            ([σ] 独立于全部公理;',
     '        │            (<a href="#w-4" class="d-link">[σ] 独立于全部公理;</a>'),
    ('        │             非平凡性押 (★))',
     '        │             <a href="#w-4" class="d-link">非平凡性押 (★)</a>)'),
    ('  W.2 同族配套(第一人称&quot;够不到&quot;的三面):',
     '  <a href="#w-2" class="d-link">W.2 同族配套</a>(第一人称&quot;够不到&quot;的三面):'),
    ('   态半  W.2.1–2.4(视角不可内生)',
     '   态半  <a href="#w-2" class="d-link">W.2.1–2.4</a>(视角不可内生)'),
    ('   窗口半 W.2.6(唯我论不可内生)',
     '   窗口半 <a href="#w-2" class="d-link">W.2.6</a>(唯我论不可内生)'),
    ('   舞台半 W.2.7(环境欠定,命题 R★)',
     '   舞台半 <a href="#w-2" class="d-link">W.2.7</a>(环境欠定,命题 R★)'),
    ('  推论层 W.5(非顺从/荷对偶/三刻画等价/有限性)由主定理导出',
     '  <a href="#w-5" class="d-link">推论层 W.5</a>(非顺从/荷对偶/三刻画等价/有限性)由主定理导出'),
    ('  图景层 W.6(判定机·三缺/对易性=语法/物理对照)= 讨论,非定理',
     '  <a href="#w-6" class="d-link">图景层 W.6</a>(判定机·三缺/对易性=语法/物理对照)= 讨论,非定理'),
    ('  开放    W.7((★) 等)',
     '  开放    <a href="#w-7" class="d-link">W.7</a>((★) 等)'),
]


def linkify_ascii_diagram(body):
    """将 W.0 ASCII 逻辑链图中的关键词转换为可点击跳转链接。"""
    needle = '<pre><code>\n                    公理 Σ'
    start = body.find(needle)
    if start < 0:
        return body
    end = body.find('</code></pre>', start)
    if end < 0:
        return body
    content = body[start + len('<pre><code>\n'):end]
    for old, new in DPIAGRAM_REPLACE:
        content = content.replace(old, new)
    new_block = f'<pre class="diagram"><code>{content}</code></pre>'
    return body[:start] + new_block + body[end + len('</code></pre>'):]


def extract_intro_subtitle(text):
    """导论 blockquote 副标题 → 纯文本（供目录用）。"""
    m = re.search(r'^>\s*副标题[：:]\s*(.+?)\s*$', text, re.M)
    if not m:
        return ''
    return m.group(1).rstrip('。.')


def page_title(ch_name, md):
    """页面 h1 / 窗口标题用的短名。"""
    if ch_name == "导论":
        return "导论"
    if ch_name == "附录":
        return "附录"
    return title_from_md(md)


def title_from_md(text):
    """短标题：仅章节编号/名称，无副标题（用于页面 h1 和窗口标题）。"""
    for line in text.splitlines():
        if line.startswith('# '):
            raw = line[2:].strip()
            short = raw.split('·')[0].strip()
            if short.startswith('附录'):
                return '附录'
            return short
    return "章节"


def index_title(ch_name, md):
    """目录页章节条目：导论/附录仅短名，其余带章节副标题。"""
    if ch_name in ("附录", "导论"):
        return ch_name
    return clean_title(full_title(md))


def full_title(text):
    """完整标题：包含副标题和版本号括号（用于索引页条目文本）。"""
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return "章节"


def strip_h1_subtitle(body, short):
    """将页面 h1 从完整标题替换为短标题（仅在非附录页面）。"""
    m = re.search(r'<h1>[^<]+</h1>', body)
    if m:
        return body[:m.start()] + f'<h1>{html_mod.escape(short)}</h1>' + body[m.end():]
    return body


def ts():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def load_all_chapters():
    chapters = []
    meta = {}
    for i, (file_path, ch_name) in enumerate(files, 1):
        raw = load_chapter(file_path, ch_name)
        if ch_name == "导论":
            meta["intro_subtitle"] = extract_intro_subtitle(raw)
        ch = clean_chapter(raw, ch_name)
        chapters.append((chapter_html_name(i, ch_name), ch_name, ch))
    return chapters, meta


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


# ── 脚注分类（旁注 A / 文献 B）──────────────────────────────

_BIB_JOURNALS = [
    'Springer', 'Comm. Math. Phys.', 'J. Funct. Anal.', 'Publ. RIMS',
    'Ann. Sci.', 'Trans. AMS', 'Invent. Math.', 'Nature', 'Phys. Rev.',
    'arXiv', 'Proc.', 'Univ. Press', 'LNM', 'Zbl', 'Rev. Math. Phys.',
    'Proc. Japan Acad.', 'J. Reine Angew. Math.', 'Ann. of Math.',
    'Duke Math. J.', 'Pacific J. Math.', 'Mem. AMS', 'Lecture Notes',
    'Cambridge', 'Oxford', 'Princeton', 'Harvard', 'MIT Press',
    'World Scientific', 'Birkhäuser', 'Academic Press', 'North-Holland',
    'Ergebnisse', 'Grundlehren', 'Studies in', 'J. Math. Phys.',
    'Lett. Math. Phys.', 'J. Operator Theory', 'Math. Ann.',
    'Math. Z.', 'C. R. Acad. Sci.', 'Acta Math.',
    'Int. J. Theor. Phys.', 'J. Math. Phys.', 'Rev. Mod. Phys.',
    'Math. Scand.', 'J. London Math.', 'Bull. AMS', 'Notices AMS',
    'Phil. Trans.', 'Nature Phys.',
]

_BIB_AUTHOR_RE = re.compile(
    r'[A-Z][a-zà-ü]+(?:-[A-Z][a-zà-ü]+)?,\s+[A-Z]\.'
)

_BIB_YEAR_RE = re.compile(r'\b(1[89]\d{2}|20[0-2]\d)\b')

_BIB_PAGES_RE = re.compile(r'\d{2,5}[–-]\d{2,5}')

_BIB_DOI_ARXIV_RE = re.compile(r'\b(?:[Dd][Oo][Ii]|arXiv|arxiv)\b')


def _has_bibliographic_body(text):
    """Check if footnote body is predominantly bibliographic.
    Key signal: a known journal keyword near a 4-digit year."""
    clean = re.sub(r'⟦MATH:?\d+⟧', '', text)
    if not _BIB_YEAR_RE.search(clean):
        return False
    return any(kw in clean for kw in _BIB_JOURNALS)


def _has_substantial_explanation(text):
    """Check if footnote has substantive Chinese explanation."""
    clean = re.sub(r'⟦MATH:?\d+⟧', '', text)
    # Bold markers with Chinese content (lowered to catch **无迹**, **要点** etc)
    if re.search(r'\*\*[\u4e00-\u9fff]{2,}', clean):
        return True
    # Substantial Chinese text segments
    segments = re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]{20,}', clean)
    if sum(len(s) for s in segments) > 140:
        return True
    # Explicit philosophical/explanatory markers
    if re.search(r'(要点|注意|诚实|分寸|红线|边界|前提|必须|不能|不要|切勿|须知|界限|不宣称|不承担|不证明|不保证)', clean):
        return True
    return False


def classify_footnote(body_text):
    """Classify footnote as 'A' (旁注) or 'B' (文献)."""
    if not _has_bibliographic_body(body_text):
        return 'A'
    if _has_substantial_explanation(body_text):
        return 'A'
    return 'B'


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
            (fid, f'<li id="fn-{fid}" class="footnote">{back_html}{content}</li>', body)
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

            if stripped.startswith('#### '):
                h4_text = stripped[5:]
                h4_id = heading_anchor(h4_text)
                out.append(f'<h4 id="{h4_id}">{self.fmt_inline(h4_text)}</h4>')
            elif stripped.startswith('### '):
                h3_text = stripped[4:]
                h3_id = heading_anchor(h3_text)
                out.append(f'<h3 id="{h3_id}">{self.fmt_inline(h3_text)}</h3>')
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

        # ── footnote classification + bubble injection ──
        if self.footnote_items:
            a_fids = set()
            a_htmls = []
            b_htmls = []
            fn_content_map = {}
            for fid, html, raw_body in self.footnote_items:
                html = restore_math(html, math_store)
                if classify_footnote(raw_body) == 'A':
                    a_fids.add(fid)
                    a_htmls.append(html)
                    inner = re.sub(r'^<li[^>]*>|</li>$', '', html).strip()
                    fn_content_map[f'fn-{fid}'] = inner
                else:
                    b_htmls.append(html)

            # Rewrite fn-ref links: A-type → bubble popup, B-type stays jump
            def _rewrite_fn_ref(m):
                fid = m.group(2)
                if fid in a_fids:
                    return m.group(0).replace('class="fn-ref"',
                        'class="fn-a" data-fn="fn-' + fid + '"')
                return m.group(0)

            body = re.sub(
                r'(<a\s[^>]*href="[^"]*#fn-(\w+)"[^>]*class="fn-ref"[^>]*>[^<]*</a>)',
                _rewrite_fn_ref, body)

            parts = []
            if a_htmls:
                parts.append('<h3 class="fn-section">〔旁注〕</h3>\n<ol class="footnotes">\n' +
                             '\n'.join(a_htmls) + '\n</ol>')
            if b_htmls:
                parts.append('<h3 class="fn-section">〔文献〕</h3>\n<ol class="footnotes">\n' +
                             '\n'.join(b_htmls) + '\n</ol>')
            body += '\n<section class="footnotes">\n' + '\n'.join(parts) + '\n</section>'

            # Inject FN_CONTENT map
            body += '\n<script>var FN_CONTENT=' + json.dumps(fn_content_map, ensure_ascii=False) + ';</script>'
        return body


def write_html_page(path, title, body_html):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(HTML_SHELL.format(title=html_mod.escape(title), body=body_html, katex=KATEX))


# ── 主线图景场景锚点注入 ──────────────────────────────────

SCENE_ID_MAP = {
    '02_start.html':           {'scene-wuji':     '导论把你带到了&quot;没有尺子&quot;的门口。'},
    '07_worldtopos.html':      {'scene-lishi':    '现在来看看&quot;历史&quot;到底是怎么成立的。'},
    '05_unknowable.html':      {'scene-sanzhong': '把认知够不到的边界数一数'},
    '04_intentionality.html':  {'scene-heng':     '有了两股、有了两读，&quot;物理世界&quot;可以精确地安放了'},
    '03_twostreams.html':      {'scene-zong':     '<strong>为什么理解流只能倒着写。</strong>'},
    '09_assertion.html':       {'scene-dui':      '搭板就是干两件事：<strong>打桩</strong>'},
    '06_theother.html':        {'scene-taren':    '先问一个人人都问过的问题：为什么我永远不能真正知道你在想什'},
    '10_classicalworld.html':  {'scene-xianshi':  '这是一个方向的彻底反转。'},
    '12_epilogue.html':        {'scene-songshou': '所以松开那个锚，不是失去你。'},
}


def inject_scene_ids(body, html_name):
    targets = SCENE_ID_MAP.get(html_name, {})
    for sid, marker in targets.items():
        idx = body.find(marker)
        if idx < 0:
            continue
        p_start = body.rfind('<p', 0, idx)
        if p_start < 0:
            continue
        tag_end = body.find('>', p_start)
        tag = body[p_start:tag_end + 1]
        if 'id=' in tag:
            continue
        body = body[:p_start + 2] + f' id="{sid}"' + body[p_start + 2:]
    return body


def export_html(chapters, meta=None):
    """chapters: [(html_name, ch_name, md_text), ...]"""
    os.makedirs(OUT_HTML, exist_ok=True)
    html_chapters = [(h, md) for h, _, md in chapters]
    fn_index = FootnoteIndex(html_chapters)

    index_items = []
    chapter_links = build_chapter_link_map()
    for html_name, ch_name, md in chapters:
        short = page_title(ch_name, md)
        idx_text = index_title(ch_name, md)
        conv = PageConverter(html_name, fn_index)
        body = conv.md_to_html(md)
        body = strip_h1_subtitle(body, short)
        if ch_name == "导论":
            body = re.sub(
                r'<blockquote><p>\s*副标题[：:][^<]*</p></blockquote>\s*',
                '', body, count=1)
            body = linkify_chapter_map(body, chapter_links)
        if ch_name == "附录":
            body = linkify_ascii_diagram(body)
            body = linkify_w_refs(body)
        body = inject_scene_ids(body, html_name)
        write_html_page(os.path.join(OUT_HTML, html_name), short, body)
        index_items.append((html_name, idx_text))
        print(f"    {html_name}")

    links = '\n'.join(
        f'    <li><a href="{html_mod.escape(h)}">{html_mod.escape(t)}</a></li>'
        for h, t in index_items
    )
    book_sub = html_mod.escape((meta or {}).get("intro_subtitle", ""))
    subtitle_block = (
        f'<p class="subtitle">{book_sub}</p>\n' if book_sub else ''
    )
    index = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>《界限论》阅读器</title>
<style>
  body {{ max-width: 36rem; margin: 2rem auto; padding: 0 1.2rem;
         font-family: "Noto Serif SC", "Source Han Serif SC", Georgia, serif;
         line-height: 1.8; background: #1b1b18; color: #c8c4bc; }}
  h1 {{ font-size: 1.45rem; border-bottom: 1px solid #3a3a35;
       padding-bottom: .35rem; color: #e0dcd4; margin-bottom: .4rem; }}
  .subtitle {{ color: #a8a49c; font-size: 1rem; margin: 0 0 1.4rem; }}
  a {{ color: #7eb8da; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  ul {{ padding-left: 0; list-style: none; }}
  li {{ padding: .25rem 0; border-bottom: 1px solid #2a2a26; }}
  li:last-child {{ border-bottom: none; }}
  .note {{ color: #7a766e; font-size: .88rem; margin-top: 1.8rem; }}
  @media (max-width: 600px) {{
    body {{ font-size: .95rem; padding: 0 .8rem; margin: 1rem auto; }}
    h1 {{ font-size: 1.25rem; }}
    .subtitle {{ font-size: .92rem; }}
    li {{ font-size: .93rem; padding: .35rem 0; }}
  }}
</style></head>
<body>
<h1>《界限论》阅读器</h1>
{subtitle_block}<ul>{links}</ul>
<p class="note">用 Chrome / Edge 打开即可阅读（本地 KaTeX，无需联网）。<br>
脚注可点击跳转；跨章引用会自动跳到对应章节。<br>
生成：{datetime.now():%Y-%m-%d %H:%M}</p>
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

    chapters, meta = load_all_chapters()
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
    export_html(chapters, meta)

    print("\nDone.")


if __name__ == '__main__':
    main()
