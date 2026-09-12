"""
Parse a .srt subtitle file into a list of "cues" (timestamped lines) as JSON.

This is the first step toward building a data/<episode-id>.js file for the
player: it gives you a clean, structured starting point (timestamps in
milliseconds, speaker tag extracted where the subtitle format includes one
like "[Björn] ...", sound-effect-only lines flagged) — from there, add
translations (cue["zh"]) and vocab/grammar/summary/keyScenes/quiz annotations
by hand or with an AI assistant's help, matching the schema documented in
data/example-episode.js.

Usage:
    python parse_srt.py input.srt output_cues.json
"""
import re
import json
import sys


def ts_to_ms(ts):
    h, m, s_ms = ts.split(':')
    s, ms = s_ms.split(',')
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)


def parse_srt(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\s*\n', content.strip())
    cues = []
    for b in blocks:
        lines = [l for l in b.split('\n') if l.strip() != '']
        if len(lines) < 2:
            continue
        idx_line = lines[0].strip()
        if not idx_line.isdigit():
            continue
        ts_line = lines[1]
        m = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', ts_line)
        if not m:
            continue
        start = ts_to_ms(m.group(1))
        end = ts_to_ms(m.group(2))
        text_lines = lines[2:]
        raw_text = ' '.join(text_lines)
        cues.append({'idx': int(idx_line), 'start': start, 'end': end, 'raw': raw_text})
    return cues


# Words/phrases that, when found inside a "[...]" bracket at the start of a
# line, indicate it's a sound description rather than a speaker name —
# extend this list for the language/show you're working with.
_SFX_HINTS = (
    r'(musik|Musik|Geräusch|geräusch|klingelt|Klopfen|zwitschern|seufzt|'
    r'stöhnt|lacht|brüllt|schreit|atmet|Ton|springt|Tür|Aufzug|Handy|'
    r'Wasser|Rauschen|Schritte|Applaus)'
)


def clean_text(raw):
    """Split a raw cue line into (speaker_or_None, text, is_pure_sfx)."""
    speaker = None
    m = re.match(r'^\[([^\]]+)\]\s*(.*)$', raw)
    text = raw
    if m and not re.search(_SFX_HINTS, m.group(1)):
        # looks like a speaker name, e.g. "[Anna] Hallo!" -> speaker="Anna"
        speaker = m.group(1)
        text = m.group(2)
    text = text.replace('<i>', '').replace('</i>', '')
    stripped = text.strip()
    is_sfx = stripped.startswith('[') and stripped.endswith(']')
    return speaker, text.strip(), is_sfx


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    in_path, out_path = sys.argv[1], sys.argv[2]

    cues = parse_srt(in_path)
    out = []
    for c in cues:
        speaker, text, is_sfx = clean_text(c['raw'])
        out.append({
            'idx': c['idx'],
            'start': c['start'],
            'end': c['end'],
            'speaker': speaker,
            'text': text,
            'sfx': is_sfx,
            'zh': '',  # fill in translations here (or with an AI assistant's help)
        })

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    dialogue = [o for o in out if not o['sfx'] and o['text'].strip()]
    print(f"total cues: {len(out)}")
    print(f"sfx-only cues: {sum(1 for o in out if o['sfx'])}")
    print(f"dialogue cues: {len(dialogue)}")
    print(f"wrote: {out_path}")


if __name__ == '__main__':
    main()
