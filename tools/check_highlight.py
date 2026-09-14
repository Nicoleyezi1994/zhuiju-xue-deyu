# -*- coding: utf-8 -*-
"""
校验一集的生词表里，每个词的 example_de 是否真的会被播放器的高亮逻辑命中。

背景：早先只检查"example_de 的文本是否出现在某条 cue 里"，但这个检查不够——
播放器的实际高亮逻辑是"把 cue 文本按 [A-Za-zÀ-ÖØ-öø-ÿß'] 切成单词 token，
逐个查 wordMap"，加上多词短语按子串匹配。这意味着下面几种情况即使
"文本包含"检查能通过，实际也不会真正高亮：
  - 连字符复合词：Beifahrer-Airbag 会被切成 "Beifahrer"+"Airbag" 两个 token，
    整词 "beifahrer-airbag" 或 "beifahrer airbag" 都不会命中任何一个 token。
  - 可分动词被拆开使用：Schränkt...ein 中，出现的 token 是 "Schränkt"，
    不是 match 列表里常见的 "einschränkt"。
  - 短语中间插了别的词：lässt wirklich nichts aus 里，"nichts aus" 中间
    多了个 "wirklich"，如果 match 列表写的是 "lässt nichts aus"（认为两者相邻）
    就不会命中。
  - 无分隔符的复合词：Gleichberechtigungsblödsinn 整个是一个 token，
    match 列表如果只写了 "blödsinn"，因为是"整词相等"比较，不会命中子串。

用法：
  python3 tools/check_highlight.py s01e06

会打印这一集里，vocab 数组中"高亮不会触发"的条目（连同它们的 id 和 example_de），
方便逐条修 match 数组或者换成真正命中的 cue。
"""
import json, re, sys

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿß']+")
LINE_COMMENT_RE = re.compile(r"^\s*//.*$", re.MULTILINE)

def load_app_data(path):
    raw = open(path, encoding='utf-8').read()
    # Strip full-line "//" comments (e.g. the heavily-annotated example data
    # file) — data files you generate yourself are typically plain JSON with
    # no comments, but this keeps the script working against both.
    raw = LINE_COMMENT_RE.sub("", raw)
    raw = raw.strip()
    marker = "window.APP_DATA = "
    idx = raw.index(marker) + len(marker)
    return json.loads(raw[idx:].rstrip().rstrip(';').rstrip())

def check(ep):
    data = load_app_data(f"../data/{ep}.js")
    word_map = {}
    phrase_matches = []
    for v in data['vocab']:
        for m in v.get('match', []):
            if ' ' in m or '-' in m:
                phrase_matches.append((m.lower(), v['id']))
            else:
                word_map[m.lower()] = v['id']

    def would_highlight(text, vid):
        lower = text.lower()
        for phrase, pid in phrase_matches:
            if pid == vid and phrase in lower:
                return True
        for m in TOKEN_RE.finditer(text):
            tok = m.group(0).lower()
            stripped = tok.strip("'")
            if word_map.get(tok) == vid or word_map.get(stripped) == vid:
                return True
        return False

    issues = [(v['id'], v['term'], v['example_de']) for v in data['vocab'] if not would_highlight(v['example_de'], v['id'])]
    print(f"{ep}: {len(data['vocab'])} 个生词，{len(issues)} 处高亮不会触发")
    for vid, term, ex in issues:
        print(f"  - {vid} ({term}): {ex!r}")
    return len(issues)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 check_highlight.py <ep1> [ep2 ...]，例如 python3 check_highlight.py s01e06")
        sys.exit(1)
    total = sum(check(ep) for ep in sys.argv[1:])
    if total:
        print(f"\n共 {total} 处需要修复：要么在 match 数组里加上实际会出现的 token/短语，要么换成真正包含该词的 cue。")
