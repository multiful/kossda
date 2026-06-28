"""
Slide 04 — Q2 SEM v2 경로도 (제도공백 잠재변수)
- 우리 가설: 제도공백(잠재) → 침해지수 → 정신건강역 → {이직고려, 자살사고}
- design.md 준수: 제목 없음, DARK/ACCENT/BLUE1 3색, annotate 금지, footer 출처
- 화살표: FancyArrowPatch (annotate 아님 — SEM 경로도 구조상 필수)
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings('ignore')

for fp in [
    '/Library/Fonts/NanumGothicBold.ttf',
    '/Library/Fonts/NanumGothic.ttf',
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
]:
    try:
        fm.fontManager.addfont(fp)
        plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
        break
    except Exception:
        pass
plt.rcParams['axes.unicode_minus'] = False

DARK   = '#1A1A2E'
MUTED  = '#6B6B7B'
ACCENT = '#D62728'
BLUE1  = '#1F77B4'
WHITE  = '#FFFFFF'

fig, ax = plt.subplots(figsize=(13, 5.5), facecolor='white')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.set_xlim(0, 13)
ax.set_ylim(0, 5.5)
ax.axis('off')

# ── 노드 정의 ──────────────────────────────────────────────
# (cx, cy, w, h, label, subtext, facecolor)
NODES = [
    (1.55, 2.75, 2.1, 2.0,  '제도공백',    '(잠재변수)\n분리제도·민원응대\n공식절차·교권위 불신',   ACCENT),
    (5.3,  2.75, 2.1, 1.5,  '침해지수',    '85.6% 경험',                                          DARK),
    (8.9,  2.75, 2.1, 1.5,  '정신건강 악화', '우울·심리위기',                                     BLUE1),
    (12.1, 4.3,  1.7, 1.05, '이직 고려',   '46.3%',                                               ACCENT),
    (12.1, 1.2,  1.7, 1.05, '자살 사고',   '16.9%',                                               ACCENT),
]

for (cx, cy, w, h, label, sub, fc) in NODES:
    box = mpatches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.12',
        facecolor=fc, edgecolor='white', linewidth=1.8,
        zorder=3
    )
    ax.add_patch(box)
    lines = sub.split('\n')
    n = len(lines)
    # label
    ax.text(cx, cy + 0.22, label,
            ha='center', va='center',
            fontsize=11, fontweight='bold', color=WHITE, zorder=4)
    # subtext — i=0이 맨 위에 오도록 부호 반전
    spacing = 0.30
    for i, line in enumerate(lines):
        offset = ((n - 1) / 2 - i) * spacing
        ax.text(cx, cy - 0.18 + offset - (n - 1) * 0.10,
                line, ha='center', va='center',
                fontsize=8, color=WHITE, alpha=0.88, zorder=4)

# ── 화살표 (FancyArrowPatch, annotate 금지) ────────────────
def arrow(x1, y1, x2, y2, color, lw=2.3, ls='solid', rad=0.0):
    p = mpatches.FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=mpatches.ArrowStyle('->', head_length=0.2, head_width=0.13),
        mutation_scale=18,
        color=color, linewidth=lw, linestyle=ls,
        connectionstyle=f'arc3,rad={rad}',
        zorder=2
    )
    ax.add_patch(p)

def blabel(x, y, text, color, bold=False):
    ax.text(x, y, text,
            ha='center', va='center',
            fontsize=9.5, color=color,
            fontweight='bold' if bold else 'normal',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='white',
                      edgecolor='none', alpha=0.92),
            zorder=5)

# 1. 제도공백 → 침해지수  (ACCENT, solid, thick)
arrow(2.60, 2.75, 4.24, 2.75, ACCENT, lw=3.2)
blabel(3.42, 3.15, 'β = 0.454***', ACCENT, bold=True)

# 2. 침해지수 → 정신건강역  (BLUE1, solid)
arrow(6.35, 2.75, 7.84, 2.75, BLUE1, lw=2.3)
blabel(7.10, 3.13, 'β = 0.350***', BLUE1)

# 3. 정신건강역 → 이직고려  (BLUE1, solid)
arrow(9.95, 3.18, 11.25, 4.08, BLUE1, lw=2.0)
blabel(10.45, 3.95, 'β = 0.141***', BLUE1)

# 4. 정신건강역 → 자살사고  (BLUE1, solid)
arrow(9.95, 2.32, 11.25, 1.50, BLUE1, lw=2.0)
blabel(10.45, 1.65, 'β = 0.129***', BLUE1)

# 5. 침해지수 → 이직고려 직접  (BLUE1, dashed, arc up)
arrow(5.3, 3.50, 11.25, 4.10, BLUE1, lw=1.6, ls='dashed', rad=-0.22)
blabel(7.95, 4.55, 'β = 0.125*** (직접)', BLUE1)

# 6. 침해지수 → 자살사고 직접  (BLUE1, dashed, arc down)
arrow(5.3, 2.00, 11.25, 1.38, BLUE1, lw=1.6, ls='dashed', rad=0.22)
blabel(7.95, 0.80, 'β = 0.067*** (직접)', BLUE1)

# ── 매개비율 주석 (텍스트 박스, annotate 아님) ────────────
ax.text(8.9, 0.35,
        '정신건강 매개비율  이직 ~28%  ·  자살 ~40%  (Bootstrap 추정)',
        ha='center', va='center', fontsize=8.5, color=MUTED,
        style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F5F5',
                  edgecolor='#DDDDDD', linewidth=0.8),
        zorder=4)

# ── 범례 ──────────────────────────────────────────────────
legend = [
    Line2D([0], [0], color=ACCENT, lw=3.2, label='핵심 경로 (제도공백)'),
    Line2D([0], [0], color=BLUE1,  lw=2.3, label='매개 경로 (정신건강역)'),
    Line2D([0], [0], color=BLUE1,  lw=1.6, ls='dashed', label='직접 경로'),
]
ax.legend(handles=legend, loc='lower left', fontsize=8.5,
          frameon=False, ncol=3, bbox_to_anchor=(0.0, -0.10))

# ── 출처 footer ───────────────────────────────────────────
fig.text(0.5, -0.04,
         'D1 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073, n=10,888)  |  '
         'SEM v2 (semopy)  |  CFI=0.917  RMSEA=0.070  Cronbach α=0.741  |  전 경로 p<.001',
         ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout(pad=0.3)
out = '/Users/baiohelseu/Desktop/Project/kossda/output/slide04_4-2_제도공백SEM_경로도.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
print(f'저장: {out}')
plt.close(fig)
print('✅ 완료')
