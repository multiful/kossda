"""
Slide 04 보조 시각화 — 제도공백 4개 지표 실측값
Cleveland dot plot: 침해집단 vs 비침해집단 평균 + r값
design.md 준수: 제목 없음, ACCENT/BLUE1/MUTED 3색, annotate 금지
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np
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
GRAY   = '#DDDDDD'

# ── 데이터 (r 약한 것부터 → barh는 아래→위이므로 역순 입력) ──
indicators = [
    # (변수코드, 라벨, 침해집단, 비침해집단, r)
    ('C6_8',  '문제 해결하는\n공식 절차 존재',       2.600, 3.070, -0.126),
    ('B8_1',  '교권보호위원회\n처리 절차 신뢰',      2.010, 2.529, -0.184),
    ('A1_12', '방해학생 분리제도\n취지에 맞게 운영', 2.066, 2.731, -0.217),
    ('A1_13', '민원응대 제도\n취지에 맞게 운영',    2.040, 2.823, -0.255),
]

codes  = [d[0] for d in indicators]
labels = [d[1] for d in indicators]
inf_g  = np.array([d[2] for d in indicators])   # 침해집단
noninf = np.array([d[3] for d in indicators])   # 비침해집단
rs     = [d[4] for d in indicators]

n = len(indicators)
y = np.arange(n)

fig, ax = plt.subplots(figsize=(10, 4.5), facecolor='white')
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

# ── 연결선 (두 점 잇기) ─────────────────────────────────────
for i in range(n):
    ax.plot([inf_g[i], noninf[i]], [y[i], y[i]],
            color=GRAY, lw=2.5, zorder=1, solid_capstyle='round')

# ── 침해집단 점 (ACCENT) ─────────────────────────────────────
ax.scatter(inf_g, y, color=ACCENT, s=110, zorder=3,
           edgecolors='white', linewidths=1.0, label='침해 경험 집단')

# ── 비침해집단 점 (BLUE1) ────────────────────────────────────
ax.scatter(noninf, y, color=BLUE1, s=110, zorder=3,
           edgecolors='white', linewidths=1.0, label='침해 미경험 집단')

# ── 수치 라벨 ────────────────────────────────────────────────
for i in range(n):
    ax.text(inf_g[i] - 0.07, y[i], f'{inf_g[i]:.2f}',
            ha='right', va='center', fontsize=9, color=ACCENT, fontweight='bold')
    ax.text(noninf[i] + 0.07, y[i], f'{noninf[i]:.2f}',
            ha='left', va='center', fontsize=9, color=BLUE1, fontweight='bold')

# ── r 값 오른쪽 끝 ───────────────────────────────────────────
for i, r in enumerate(rs):
    ax.text(4.05, y[i], f'r = {r:.3f}***',
            ha='left', va='center', fontsize=9, color=MUTED)

# ── 전체 평균 기준선 (1~5 중간=3) ───────────────────────────
ax.axvline(3.0, color=GRAY, lw=1.2, ls='--', zorder=0)
ax.text(3.02, n - 0.6, '중립(3점)', fontsize=8, color=MUTED)

# ── 축 설정 ──────────────────────────────────────────────────
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10.5, color=DARK, linespacing=1.4)
ax.set_xlim(1.5, 4.4)
ax.set_xlabel('제도 운영 인식 평균 (1=전혀 아님 ~ 5=매우 그렇다)', fontsize=9, color=MUTED, labelpad=6)
ax.xaxis.set_ticks([1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color(GRAY)
ax.tick_params(axis='x', labelsize=9, colors=MUTED, length=0)
ax.tick_params(axis='y', length=0)

# ── 변수코드 작게 표시 ────────────────────────────────────────
for i, code in enumerate(codes):
    ax.text(1.52, y[i], code, fontsize=7.5, color=MUTED,
            va='center', style='italic')

# ── 범례 ─────────────────────────────────────────────────────
legend = [
    mpatches.Patch(color=ACCENT, label='침해 경험 집단 (n≈9,300)'),
    mpatches.Patch(color=BLUE1,  label='침해 미경험 집단 (n≈1,588)'),
]
ax.legend(handles=legend, loc='upper right', fontsize=9, frameon=False,
          bbox_to_anchor=(1.0, 0.55))

# ── 출처 ─────────────────────────────────────────────────────
fig.text(0.5, -0.04,
         'D1 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073, n=10,888)  |  '
         '피어슨 r, 전 변수 p<.001  |  5점 리커트 (낮을수록 제도 미작동)',
         ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout(pad=0.5)
out = '/Users/baiohelseu/Desktop/Project/kossda/output/slide04_4-3_제도공백지표.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
print(f'저장: {out}')
plt.close(fig)
print('✅ 완료')
