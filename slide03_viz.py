"""
Slide 03 시각화
3-1: 인권교육 역설 — 참여율·효과·제로섬 인식 3개 지표
3-2: Track A 학교 구조별 침해 오즈비 (보호자·학생 침해)
design.md 기준 준수
"""
import pyreadstat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# ── 폰트 ──────────────────────────────────────────────────
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

BASE  = '/Users/baiohelseu/Desktop/Project/kossda/'
DARK  = '#1A1A2E'
MUTED = '#6B6B7B'
GRAY_TOTAL = '#2E2E2E'
GRAY_BAR   = '#7A7A7A'
BLUE1 = '#1F77B4'
ACCENT = '#D62728'

# ═══════════════════════════════════════════════════════════
#  FIG 3-1: 인권교육 역설 — 3구간 100% 누적 수평바
# ═══════════════════════════════════════════════════════════
# [Review] 3구간으로 단순화: 부정(1-2) / 중립(3) / 긍정(4-5)
# 라벨은 bar 외부(오른쪽 여백)에 배치 → 겹침 없음
# figsize 가로 확장으로 y축 라벨 잘림 방지

rows = ['교육 효과 만족도\n(B2_6, 참여자 n=6,440)', '"학생인권↑ = 교권↓"\n동의 여부 (B5_7, n=9,553)']
neg  = [6.2,  28.6]   # 1+2점
neu  = [32.9, 24.0]   # 3점
pos  = [60.9, 47.3]   # 4+5점
summary = ['긍정(4-5점) 60.9%', '동의(4-5점) 47.3%']

C_NEG = '#4A4A4A'
C_NEU = '#C0C0C0'
C_POS = '#1F77B4'

fig1, ax = plt.subplots(figsize=(10, 4), facecolor='white')
fig1.patch.set_facecolor('white')
ax.set_facecolor('white')

bar_h = 0.38
y_pos = [1, 0]

for i, yp in enumerate(y_pos):
    # 부정
    ax.barh(yp, neg[i], left=0,            height=bar_h, color=C_NEG, edgecolor='white', linewidth=0.8)
    # 중립
    ax.barh(yp, neu[i], left=neg[i],       height=bar_h, color=C_NEU, edgecolor='white', linewidth=0.8)
    # 긍정
    ax.barh(yp, pos[i], left=neg[i]+neu[i],height=bar_h, color=C_POS, edgecolor='white', linewidth=0.8)

    # 세그먼트 내부 수치 (너무 좁으면 생략)
    for val, start_x, col in [
        (neg[i], 0,              'white'),
        (neu[i], neg[i],         DARK),
        (pos[i], neg[i]+neu[i],  'white'),
    ]:
        if val >= 8:
            ax.text(start_x + val/2, yp, f'{val:.0f}%',
                    ha='center', va='center', fontsize=10,
                    color=col, fontweight='bold')

    # 오른쪽 요약 — bar 끝(100%)에서 여백 두고 배치
    ax.text(103, yp, summary[i], va='center', ha='left',
            fontsize=10, color=C_POS, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(rows, fontsize=11, color=DARK, linespacing=1.5)
ax.set_xlim(0, 145)   # 오른쪽 여백 충분히
ax.set_xlabel('응답 비율 (%)', fontsize=10, color=MUTED, labelpad=6)
ax.tick_params(axis='x', labelsize=9, colors=MUTED)
ax.tick_params(axis='y', length=0)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.xaxis.set_ticks([0, 25, 50, 75, 100])
ax.xaxis.grid(True, color='#EEEEEE', linewidth=1)
ax.set_axisbelow(True)

# 범례 (3개만)
patches = [
    mpatches.Patch(color=C_NEG, label='부정(1-2점)'),
    mpatches.Patch(color=C_NEU, label='중립(3점)'),
    mpatches.Patch(color=C_POS, label='긍정(4-5점)'),
]
ax.legend(handles=patches, loc='lower right', bbox_to_anchor=(0.72, -0.35),
          ncol=3, fontsize=9, frameon=False)

fig1.text(0.5, -0.1,
          '출처: 김병준, 초·중등 교원 인권교육 실태조사 2021 (KOSSDA A1-2021-0019) | n=9,553',
          ha='center', fontsize=8, color=MUTED, style='italic')

plt.subplots_adjust(left=0.28, right=0.72, top=0.88, bottom=0.18)
out1 = BASE + 'output/slide03_3-1_인권교육역설.png'
fig1.savefig(out1, dpi=200, bbox_inches='tight', facecolor='white')
print(f'저장: {out1}')
plt.close(fig1)

print('✅ 3-1 완료')
