"""learn-pdm-lite-hgd 정답 스크립트 — Block 1 판정표와 그래프 한 장을 만든다.

사용: 센서 CSV가 있는 작업 폴더에서 실행한다.
    python build_lite.py
만드는 것: judgement.md, index.html, expected.json
"""
import csv
import json
import statistics as st
from pathlib import Path

SENSOR = Path("Day5_설비센서_50건_가상.csv")
COL = "진동(mm/s)"

expected = {}


def put(key, value, block, decimals=None):
    expected[key] = {"value": value, "decimals": decimals, "block": block}


with open(SENSOR, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
put("rows_sensor", len(rows), 0, 0)

# 설비별 진동 시계열: 설비A → [(시각, 값)]
series = {}
for r in rows:
    series.setdefault(r["설비"].split("(")[0], []).append((r["시간"][-5:], float(r[COL])))

result = {}
for eq, pts in series.items():
    vals = [v for _, v in pts]
    m, s = st.mean(vals), st.stdev(vals)          # 표본표준편차(n-1)
    lo, hi = m - 2 * s, m + 2 * s
    out = [i for i, (_, v) in enumerate(pts) if not lo <= v <= hi]
    first = out[0]
    # 다음 시점에 평상 범위로 돌아오면 노이즈, 직전부터 오르다 넘었으면 추세
    nxt = pts[first + 1][1] if first + 1 < len(pts) else None
    if nxt is not None and lo <= nxt <= hi:
        verdict, start = "노이즈", None
    elif pts[first - 1][1] < pts[first][1]:
        verdict = "추세"
        i = first
        while i - 1 >= 0 and pts[i - 1][1] < pts[i][1]:   # 직전보다 커진 구간을 거슬러 올라간다
            i -= 1
        start = pts[i + 1][0] if i < first else pts[first][0]   # 처음 오르기 시작한(직전보다 커진) 시각
    else:
        verdict, start = "판정 보류", None
    result[eq] = {"lo": lo, "hi": hi, "out": [pts[i] for i in out], "verdict": verdict, "start": start, "first": first}


def fmt_out(eq):
    return "·".join(f"{t} {v:g}" for t, v in result[eq]["out"])


A, B = result["설비A"], result["설비B"]
put("a_vib_low", round(A["lo"], 2), 1, 2)
put("a_vib_high", round(A["hi"], 2), 1, 2)
put("a_outliers", fmt_out("설비A"), 1)
put("a_judgement", A["verdict"], 1)
put("b_vib_low", round(B["lo"], 2), 1, 2)
put("b_vib_high", round(B["hi"], 2), 1, 2)
put("b_outliers", fmt_out("설비B"), 1)
put("b_judgement", B["verdict"], 1)
put("b_start", B["start"], 1)
put("anomaly_total", sum(len(r["out"]) for r in result.values()), 1, 0)
pa, pb = series["설비A"], series["설비B"]
put("noise_window", f"{pa[A['first'] - 3][0]}~{pa[A['first'] + 1][0]}", 1)   # 원본 실습과제 2 노이즈 수열 5개 값
put("trend_window", f"{pb[-5][0]}~{pb[-1][0]}", 1)                            # 원본 실습과제 2 추세 수열 5개 값

lines = ["# 진동 노이즈 vs 추세 판정 (실습용 가상 데이터)", "",
         "| 설비 | 평상 범위 (mm/s) | 이상 후보 | 판정 | 정비 필요 시점 |", "|---|---|---|---|---|"]
for eq, r in result.items():
    lines.append(f"| {eq} | {r['lo']:.2f} ~ {r['hi']:.2f} | {fmt_out(eq)} | {r['verdict']} | {r['start'] or '—'} |")
Path("judgement.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ── 그래프 한 장 ──
W, H, L, R, T, Bm = 640, 300, 40, 14, 18, 28
allv = [v for pts in series.values() for _, v in pts]
ymin, ymax = 0, max(allv) * 1.1
n = len(pa)
x = lambda i: L + i * (W - L - R) / (n - 1)
y = lambda v: T + (ymax - v) * (H - T - Bm) / (ymax - ymin)
colors = {"설비A": "var(--a)", "설비B": "var(--b)"}
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="설비A·설비B 진동 추이">']
for v in (0, 1, 2, 3):
    svg.append(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="grid"/>'
               f'<text x="{L - 6}" y="{y(v) + 4:.1f}" class="tick" text-anchor="end">{v}</text>')
for i in range(0, n, 6):
    svg.append(f'<text x="{x(i):.1f}" y="{H - 8}" class="tick" text-anchor="middle">{pa[i][0]}</text>')
for eq, pts in series.items():
    r, c = result[eq], colors[eq]
    svg.append(f'<line x1="{L}" x2="{W - R}" y1="{y(r["hi"]):.1f}" y2="{y(r["hi"]):.1f}" stroke="{c}" class="limit"/>')
    d = " ".join(f"{'M' if i == 0 else 'L'}{x(i):.1f},{y(v):.1f}" for i, (_, v) in enumerate(pts))
    svg.append(f'<path d="{d}" stroke="{c}" class="line"/>')
    for i, (t, v) in enumerate(pts):
        if (t, v) in r["out"]:
            svg.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="5" class="dot"><title>{eq} {t} {v:g} mm/s</title></circle>')
    if r["start"]:
        i = [t for t, _ in pts].index(r["start"])
        svg.append(f'<line x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{T}" y2="{H - Bm}" class="start"/>'
                   f'<text x="{x(i) - 4:.1f}" y="{T + 10}" class="start-label" text-anchor="end">정비 필요 시점 {r["start"]}</text>')
svg.append("</svg>")

page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>진동 노이즈 vs 추세</title>
<style>
:root {{ --bg:#f7f7f5; --card:#fff; --ink:#1d1d1b; --muted:#6b6b66; --border:#e3e2dd; --a:#8a8f98; --b:#2f5d8a; --dot:#c0392b; --start:#b7791f; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#161615; --card:#21211f; --ink:#ecebe6; --muted:#a3a29c; --border:#33332f; --a:#9aa0a8; --b:#7fb0e0; --dot:#ff6b5b; --start:#e3a84a; }} }}
:root[data-theme="dark"] {{ --bg:#161615; --card:#21211f; --ink:#ecebe6; --muted:#a3a29c; --border:#33332f; --a:#9aa0a8; --b:#7fb0e0; --dot:#ff6b5b; --start:#e3a84a; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.55 system-ui,-apple-system,"Malgun Gothic","Apple SD Gothic Neo",sans-serif; }}
main {{ max-width:760px; margin:0 auto; padding:24px 16px 40px; }}
h1 {{ font-size:1.35rem; margin:6px 0; }} .muted {{ color:var(--muted); }}
.note {{ display:inline-block; font-size:.8rem; padding:2px 8px; border:1px solid var(--border); border-radius:99px; color:var(--muted); }}
figure {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px; margin:16px 0 0; }}
svg {{ width:100%; height:auto; display:block; }}
.grid {{ stroke:var(--border); }} .tick {{ fill:var(--muted); font-size:11px; }}
.line {{ fill:none; stroke-width:2; }} .limit {{ stroke-dasharray:5 4; stroke-width:1.2; opacity:.8; }}
.dot {{ fill:var(--dot); }} .start {{ stroke:var(--start); stroke-width:1.5; stroke-dasharray:3 3; }} .start-label {{ fill:var(--start); font-size:11px; }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 16px; font-size:.85rem; color:var(--muted); margin-top:8px; }}
.sw {{ display:inline-block; width:14px; height:3px; vertical-align:middle; margin-right:4px; }}
footer {{ margin-top:16px; font-size:.82rem; color:var(--muted); }} a {{ color:var(--b); }}
</style></head>
<body><main>
<span class="note">실습용 가상 데이터</span>
<h1>한 번의 튐인가, 꾸준한 상승인가</h1>
<p>설비A 진동 {fmt_out('설비A')}은 곧 돌아온 <b>{A['verdict']}</b>, 설비B 진동 {fmt_out('설비B')}는 <b>{B['verdict']}</b>다. 설비B의 정비 필요 시점은 상승이 시작된 <b>{B['start']}</b>.</p>
<figure>{"".join(svg)}
<div class="legend"><span><i class="sw" style="background:var(--a)"></i>설비A 프레스 메인모터</span><span><i class="sw" style="background:var(--b)"></i>설비B 차체 용접로봇 감속기</span><span>점선 = 설비별 평상 범위 상한(평균 + 2σ)</span><span style="color:var(--dot)">● 이상 후보</span></div>
</figure>
<footer>데이터: KMA 자동차특화 AI 융합 전문가 과정 강의 저장소 <a href="https://github.com/keerhee/kma-auto-genai-3-1">keerhee/kma-auto-genai-3-1</a> data/Day5 — 실습용 가상 데이터. 평상 범위는 설비별 평균 ± 2 × 표본표준편차. 만든 방법: Claude Code 수업 learn-pdm-lite-hgd.</footer>
</main></body></html>
"""
Path("index.html").write_text(page, encoding="utf-8")
Path("expected.json").write_text(json.dumps({"values": expected}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"완료: 이상 후보 {expected['anomaly_total']['value']}건, 설비B 정비 필요 시점 {B['start']}")
