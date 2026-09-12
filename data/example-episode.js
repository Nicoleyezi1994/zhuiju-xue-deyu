// EXAMPLE / TEMPLATE DATA FILE
// ----------------------------
// This is entirely invented placeholder content (two friends meeting at a
// café) — NOT transcribed from any real film, show, or copyrighted source.
// It exists purely to document the schema every episode data file must
// follow. Copy this file, replace every field with your own material
// (derived from subtitles you have the rights to use), and add an entry
// for it in manifest.js.
//
// Required top-level shape: window.APP_DATA = { cues, vocab, grammar,
// summary, keyScenes, quiz }.

window.APP_DATA = {

  // One entry per subtitle line that should be shown/synced against the
  // video's currentTime. `idx` just needs to be unique and increasing;
  // it doesn't have to be contiguous. `start`/`end` are in MILLISECONDS.
  // Pure sound-effect / music cues (no spoken line) should be marked
  // sfx:true with an empty "text" and "zh" — the player skips them when
  // finding "what's the current subtitle line" and when highlighting text.
  "cues": [
    { "idx": 1, "start": 0,     "end": 2000,  "speaker": null, "text": "[Café-Geräusche]", "sfx": true, "zh": "" },
    { "idx": 2, "start": 2000,  "end": 4500,  "speaker": "Anna", "text": "Entschuldigung, ist hier noch frei?", "sfx": false,
      "zh": "打扰一下，这里还有空位吗？" },
    { "idx": 3, "start": 4500,  "end": 6800,  "speaker": "Tom", "text": "Ja, klar, setz dich!", "sfx": false,
      "zh": "当然，坐吧！" },
    { "idx": 4, "start": 6800,  "end": 10200, "speaker": "Anna", "text": "Ich habe dich schon ewig nicht mehr gesehen.", "sfx": false,
      "zh": "我好久没见到你了。" },
    { "idx": 5, "start": 10200, "end": 13000, "speaker": "Tom", "text": "Stimmt, ich war die letzten Monate total im Stress.", "sfx": false,
      "zh": "没错，我这几个月一直压力很大。" }
  ],

  // Vocabulary annotations. `match` lists the surface forms the highlighter
  // should look for inside cue text (case-insensitive substring match).
  // A phrase containing a space is matched as a whole phrase across the
  // sentence; single words are matched token-by-token.
  "vocab": [
    {
      "id": "ewig",
      "term": "ewig",
      "pos": "Adv./Adj.",
      "level": "B1",
      "meaning_zh": "（口语）很久、好久（字面：永恒的）",
      "example_de": "Ich habe dich schon ewig nicht mehr gesehen.",
      "example_zh": "我好久没见到你了。",
      "note": "字面意思是“永恒的”，口语中常用来夸张地表示“很久”，类似中文的“好久好久”。",
      "match": ["ewig"]
    },
    {
      "id": "im_stress_sein",
      "term": "im Stress sein",
      "pos": "Redewendung",
      "level": "B1",
      "meaning_zh": "压力很大、很忙碌",
      "example_de": "Ich war die letzten Monate total im Stress.",
      "example_zh": "我这几个月一直压力很大。",
      "note": "固定搭配：im Stress sein，比 gestresst sein 更口语化。",
      "match": ["im stress"]
    }
  ],

  // Grammar points. `cue_idx` should match the `idx` of the cue whose
  // moment (± a few cues) is the best place to surface this explanation
  // when the learner pauses there.
  "grammar": [
    {
      "id": "g1",
      "title": "现在完成时（Perfekt）在口语中的使用",
      "tag": "Perfekt",
      "cue_idx": 4,
      "explain_zh": "德语口语中，过去发生的事情几乎总是用现在完成时（haben/sein + Partizip II），而不是简单过去时（Präteritum），后者主要用于书面语和讲故事。",
      "example_de": "Ich habe dich schon ewig nicht mehr gesehen.",
      "example_zh": "我好久没见到你了。"
    }
  ],

  // Free-text episode synopsis + a short list of key phrases worth
  // remembering, shown on the "Summary" tab.
  "summary": {
    "synopsis_zh": "安娜在咖啡馆里偶遇老朋友汤姆，两人聊起最近的近况——这是一段示例对话，用来演示数据格式，并不代表任何真实剧集内容。",
    "key_phrases": [
      { "de": "im Stress sein", "zh": "压力很大、很忙碌" },
      { "de": "schon ewig nicht mehr", "zh": "已经好久没有…了" }
    ]
  },

  // Timestamps (in milliseconds, matching cue start/end) for a "jump to
  // this moment" button on the Scenes tab.
  "keyScenes": [
    { "title": "示例片段：咖啡馆重逢", "start": 2000, "end": 13000,
      "note_zh": "演示如何标注一个值得反复回放的片段。" }
  ],

  // Two question types are supported: "mc" (multiple choice, `answer` is
  // the correct option's index) and "fill" (free-text, `answer_text` may
  // list multiple acceptable substrings separated by " / ").
  "quiz": [
    {
      "type": "mc",
      "q": "Was bedeutet 'im Stress sein'?",
      "options": ["Sehr beschäftigt/gestresst sein", "Im Urlaub sein", "Sich freuen", "Schlafen"],
      "answer": 0,
      "expl": "'im Stress sein' ist eine umgangssprachliche Redewendung für 'gestresst/sehr beschäftigt sein'."
    },
    {
      "type": "fill",
      "q": "Ergänzen Sie: 'Ich habe dich schon ewig nicht mehr ___.'",
      "answer_text": "gesehen",
      "expl": "Perfekt von 'sehen': habe...gesehen."
    }
  ]
};
