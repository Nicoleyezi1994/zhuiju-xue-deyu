# -*- coding: utf-8 -*-
"""
做新一集之前，用这个脚本查一个候选生词是否已经在前面的集数里精讲过。

用法：
  python3 tools/check_dup.py Wort1 wort2 "mehrwortausdruck"

会在 tools/used_vocab_grammar.json 里查 match 形式（大小写不敏感），
命中就打印是哪一集、哪个 term，避免同一个词根被重复选为新生词。

语法点请直接打开 tools/used_vocab_grammar.json 里的 grammar_topics 列表人工比对
（语法主题靠"tag"是否属于同一结构判断，不是简单的字符串匹配，脚本不做自动判断）。
"""
import json, sys, os

TRACKER_PATH = os.path.join(os.path.dirname(__file__), "used_vocab_grammar.json")

def load_tracker():
    with open(TRACKER_PATH, encoding="utf-8") as f:
        return json.load(f)

def check_vocab(word, tracker):
    word_low = word.lower()
    hits = []
    for v in tracker["vocab"]:
        forms = [m.lower() for m in v.get("match", [])] + [v["term"].lower()]
        if word_low in forms:
            hits.append(v)
    return hits

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 tools/check_dup.py <候选词1> <候选词2> ...")
        sys.exit(1)
    tracker = load_tracker()
    any_hit = False
    for w in sys.argv[1:]:
        hits = check_vocab(w, tracker)
        if hits:
            any_hit = True
            print(f"⚠️  \"{w}\" 已经在以下集数精讲过：")
            for h in hits:
                print(f"    {h['episode']}: {h['term']} — {h['meaning_zh']}")
        else:
            print(f"✓ \"{w}\" 未出现在已完成集数的生词表中，可以作为新生词")
    if any_hit:
        print("\n提醒：命中的词不要再列为本集新生词精讲（除非有全新的、值得单独讲的搭配/语法用法）。")
