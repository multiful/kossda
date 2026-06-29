"""
슬라이드 7 추가 시각화 2종
(A) 군집별 침해지수 비교 bar
(B) 이직 고려율 + 자살 사고율 dual bar
design.md 준수: 제목 없음, ACCENT/BLUE1/MUTED 3색, footer
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
PURPLE = '#7B3F9E'
WHITE  = '#FFFFFF'

BASE = '/Users/baiohelseu/Desktop/Project/kossda/output/'

clusters = ['초등·복합\n고위험형\n(71%)', '중등·관리자\n혼재형\n(22%)', '고등·저위험형\n(6%)']
colors   = [ACCENT, PURPLE, BLUE1]

# ──────────────────────────────────────────────
# CHART A — 군집별 침해지수 비교
# ──────────────────────────────────────────────
injury_idx = [1.69, 1.48, 1.30]

fig, ax = plt.subplots(figsize=(7, 3.6), facecolor='white')
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

y = np.arange(3)
bars = ax.barh(y, injury_idx, height=0.52,
               color=colors, edgecolor='white', linewidth=1.5, zorder=3)

# 누적 배경 바
for i in range(3):
    ax.barh(y[i], injury_idx[i], height=0.52,
            color=colors[i], alpha=0.10, edgecolor='none', zorder=2)

# 수치 라벨
for i, v in enumerate(injury_idx):
    ax.text(v + 0.01, y[i], f'{v:.2f}',
            va='center', ha='left', fontsize=13,
            fontweight='bold', color=colors[i])

# Δ 표시 (최고-최저)
delta = injury_idx[0] - injury_idx[2]
ax.annotate('', xy=(injury_idx[0], 2.35), xytext=(injury_idx[2], 2.35),
            arrowprops=dict(arrowstyle='<->', color=DARK, lw=1.4))
ax.text((injury_idx[0]+injury_idx[2])/2, 2.48,
        f'Δ {delta:.2f}', ha='center', va='bottom',
        fontsize=9, color=DARK, fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels(clusters, fontsize=10, color=DARK, linespacing=1.4)
ax.set_xlim(1.0, 1.95)
ax.set_xlabel('교권침해지수 (B2_1+B3_1+B5_1 합산, 0~3)', fontsize=9, color=MUTED, labelpad=6)
ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(axis='y', length=0)
ax.tick_params(axis='x', labelsize=9, colors=MUTED, length=0)

# 기준선
ax.axvline(1.49, color='#CCCCCC', lw=1.0, ls='--', zorder=1)
ax.text(1.495, -0.6, '전체 평균', fontsize=7.5, color=MUTED, va='top')

fig.text(0.5, -0.05,
         'D1 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073, n=10,888)  |  '
         'K-means(k=3, Silhouette=0.312)  |  침해지수 = B2_1+B3_1+B5_1 합산',
         ha='center', fontsize=7.5, color=MUTED, style='italic')

plt.tight_layout(pad=0.5)
out_a = BASE + 'slide07_침해지수비교.png'
fig.savefig(out_a, dpi=200, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'저장: {out_a}')


# ──────────────────────────────────────────────
# CHART B — 이직 고려율 + 자살 사고율 dual bar
# ──────────────────────────────────────────────
quit_rate    = [48, 44, 36]   # 이직 고려율
suicide_rate = [17.5, 15.9, 14.7]  # 자살 사고율

fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='white')
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

x = np.arange(3)
w = 0.36

# 이직 고려율 bar
b1 = ax.bar(x - w/2, quit_rate, width=w,
            color=colors, alpha=0.92, edgecolor='white', linewidth=1.5, zorder=3)

# 자살 사고율 bar (해치 + 투명도)
b2 = ax.bar(x + w/2, suicide_rate, width=w,
            color=colors, alpha=0.45, edgecolor=colors,
            linewidth=1.5, zorder=3, hatch='////')

# 수치 라벨
for i in range(3):
    ax.text(x[i]-w/2, quit_rate[i]+0.8, f'{quit_rate[i]}%',
            ha='center', va='bottom', fontsize=11,
            fontweight='bold', color=colors[i])
    ax.text(x[i]+w/2, suicide_rate[i]+0.8, f'{suicide_rate[i]}%',
            ha='center', va='bottom', fontsize=11,
            fontweight='bold', color=colors[i], alpha=0.8)

# 순서 화살표 (초등→고등 감소 표시)
for rate, yoff in [(quit_rate, 55), (suicide_rate, 22)]:
    ax.annotate('', xy=(x[2], rate[2]+yoff*0.18), xytext=(x[0], rate[0]+yoff*0.18),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.2, alpha=0.5))

ax.set_xticks(x)
ax.set_xticklabels(clusters, fontsize=10, color=DARK, linespacing=1.4)
ax.set_ylabel('비율 (%)', fontsize=10, color=MUTED, labelpad=6)
ax.set_ylim(0, 62)
ax.yaxis.grid(True, color='#EEEEEE', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', labelsize=9, colors=MUTED, length=0)

# 범례
legend_handles = [
    mpatches.Patch(color=DARK, alpha=0.85, label='이직 고려율'),
    mpatches.Patch(color=DARK, alpha=0.40, hatch='////', label='자살 사고율'),
]
ax.legend(handles=legend_handles, loc='upper right',
          fontsize=9, frameon=False, bbox_to_anchor=(1.0, 1.0))

# 인사이트 텍스트
ax.text(2.55, 57,
        '두 지표 모두\n침해지수 순서와 일치',
        ha='center', va='top', fontsize=8.5, color=DARK,
        style='italic', alpha=0.75)

fig.text(0.5, -0.04,
         'D1 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073, n=10,888)  |  '
         '이직: A4==1  |  자살사고: C4==1  |  군집별 학교급 구성 반영(초등형 97%·고등형 100%)',
         ha='center', fontsize=7.5, color=MUTED, style='italic')

plt.tight_layout(pad=0.5)
out_b = BASE + 'slide07_이직자살비교.png'
fig.savefig(out_b, dpi=200, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'저장: {out_b}')
print('✅ 완료')
