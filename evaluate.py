"""Run the summarizer on all sample articles and write test_results.md
(use this table + screenshots in your report).   Run: python evaluate.py"""
import json
import time

from summarizer import summarize

with open("samples/sample_articles.json", encoding="utf-8") as f:
    samples = json.load(f)

rows, details = [], []
for s in samples:
    t0 = time.time()
    try:
        r = summarize(s["text"], s["title"])
        secs = time.time() - t0
        ok = len(r["summary"]) == 5 and len(r["key_points"]) == 3
        st = r["stats"]
        rows.append(f"| {s['id']} | {st['words_in']} | {st['words_out']} | {st['compression_pct']}% | "
                    f"{len(r['summary'])}/5 | {len(r['key_points'])}/3 | {secs:.1f}s | {'PASS' if ok else 'CHECK'} |")
        details.append(f"### {s['id']}: {r['headline']}\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(r["summary"], 1))
                       + "\n\nKey points:\n" + "\n".join(f"- {k}" for k in r["key_points"]) + "\n")
    except Exception as e:  # keep going so one failure does not stop the run
        rows.append(f"| {s['id']} | - | - | - | - | - | - | ERROR: {e} |")
    time.sleep(2)  # be gentle with free-tier rate limits

header = ("| Sample | Words in | Words out | Compression | Summary lines | Key points | Time | Result |\n"
          "|---|---|---|---|---|---|---|---|")
with open("test_results.md", "w", encoding="utf-8") as f:
    f.write("# Test results\n\n" + header + "\n" + "\n".join(rows) + "\n\n" + "\n".join(details))
print(header); print("\n".join(rows)); print("\nSaved to test_results.md")
