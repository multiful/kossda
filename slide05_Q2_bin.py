"""
Q2 보조 시각화 — 제도공백 점수 구간별 침해율 (Bin Analysis)
"제도가 작동하지 않을수록 침해율이 단조증가" — SEM β=0.454의 raw data 직접 근거
design.md 준수: 제목 없음, ACCENT/BLUE1/MUTED 3색, annotate 금지, footer
"""
import pyreadstat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
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

BASE = '/Users/baiohelseu/Desktop/Project/kossda/'
df, _ = pyreadstat.read_sav(
    BASE + 'data/교원 인권상황 실태조사,2024/kor_data_20240073.sav'
)

# ── 변수 수치화 ──────────────────────────────────────────────
for v in ['A1_12', 'A1_13', 'C6_8', 'B8_1', 'B2_1', 'B3_1', 'B5_1']:
    df[v] = pd.to_numeric(df[v], errors='coerce')

# ── 제도공백 지수 ────────────────────────────────────────────
# 원 변수: 낮을수록 제도 불작동 → 역전하여 높을수록 제도공백이 큰 지수
df['A1_12_r'] = 6 - df['A1_12']
df['A1_13_r'] = 6 - df['A1_13']
df['C6_8_r']  = 6 - df['C6_8']
df['B8_1_r']  = 6 - df['B8_1']
df['제도공백지수'] = df[['A1_12_r','A1_13_r','C6_8_r','B8_1_r']].mean(axis=1)

# ── 침해여부 ─────────────────────────────────────────────────
df['침해any'] = ((df['B2_1']==1)|(df['B3_1']==1)|(df['B5_1']==1)).astype(int)

d = df[['제도공백지수','침해any']].dropna()

# ── 5분위 구간 ───────────────────────────────────────────────
quantiles = d['제도공백지수'].quantile([0, .2, .4, .6, .8, 1.0]).values
d['구간'] = pd.cut(
    d['제도공백지수'],
    bins=quantiles,
    labels=False,
    include_lowest=True
)

bin_stats = (
    d.groupby('구간', observed=True)
     .agg(침해율=('침해any','mean'),
          n=('침해any','count'),
          se=('침해any', lambda x: x.std()/np.sqrt(len(x))))
     .reset_index()
)
bin_stats['침해율'] *= 100
bin_stats['se']     *= 100

# 구간별 점수 범위 라벨
range_labels = []
for i in range(5):
    lo, hi = quantiles[i], quantiles[i+1]
    range_labels.append(f'{lo:.1f}–{hi:.1f}점')

xlabels = [
    f'1분위\n(제도 잘 작동)\n{range_labels[0]}',
    f'2분위\n\n{range_labels[1]}',
    f'3분위\n\n{range_labels[2]}',
    f'4분위\n\n{range_labels[3]}',
    f'5분위\n(제도 미작동)\n{range_labels[4]}',
]

# ── 색상 그라디언트 (BLUE1 → ACCENT) ────────────────────────
cmap = LinearSegmentedColormap.from_list('ba', [BLUE1, ACCENT], N=5)
colors = [cmap(i / 4) for i in range(5)]

# ── 시각화 ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5.8), facecolor='white')
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

x = np.arange(5)

# 막대
ax.bar(x, bin_stats['침해율'], width=0.62,
       color=colors, edgecolor='white', linewidth=1.5, zorder=3)

# 95% CI 오차막대
ax.errorbar(x, bin_stats['침해율'], yerr=bin_stats['se'] * 1.96,
            fmt='none', color=DARK, capsize=5,
            linewidth=1.3, capthick=1.3, zorder=4)

# 침해율 수치 (막대 위)
for i, row in bin_stats.iterrows():
    ax.text(x[i], row['침해율'] + 2.2, f"{row['침해율']:.1f}%",
            ha='center', va='bottom', fontsize=12,
            fontweight='bold', color=colors[i])

# 표본 수 (막대 내부 하단)
for i, row in bin_stats.iterrows():
    ax.text(x[i], 2.5, f"n={row['n']:,}",
            ha='center', va='bottom', fontsize=8,
            color=WHITE, alpha=0.92)

# 트렌드 점선
z = np.polyfit(x, bin_stats['침해율'], 1)
p = np.poly1d(z)
x_line = np.linspace(-0.38, 4.38, 200)
ax.plot(x_line, p(x_line),
        color=DARK, lw=1.6, ls='--', alpha=0.45, zorder=5)

# 증가폭 Δ 표시 (1분위 → 5분위)
delta = bin_stats['침해율'].iloc[4] - bin_stats['침해율'].iloc[0]
ax.text(4.36, bin_stats['침해율'].iloc[4] + 5,
        f'Δ +{delta:.1f}%p\n(1분위→5분위)',
        ha='right', va='bottom', fontsize=9,
        color=ACCENT, fontweight='bold')

# 축 설정
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=9.5, color=DARK, linespacing=1.5)
ax.set_ylabel('교권침해 경험률 (%)', fontsize=10, color=MUTED, labelpad=6)
ax.set_ylim(0, 110)
ax.yaxis.grid(True, color='#EEEEEE', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', labelsize=9, colors=MUTED, length=0)

# 범례
legend = [
    mpatches.Patch(color=BLUE1,  label='제도 작동 (공백 낮음)'),
    mpatches.Patch(color=ACCENT, label='제도 미작동 (공백 높음)'),
]
ax.legend(handles=legend, loc='upper left',
          fontsize=9, frameon=False, bbox_to_anchor=(0.01, 0.99))

# footer
fig.text(0.5, -0.03,
         'D1 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073, n=10,888)  |  '
         '제도공백 지수 = A1_12·A1_13·C6_8·B8_1 역코딩 평균 (높을수록 제도 미작동)  |  '
         '오차막대: 95% CI  |  구간: 5분위수',
         ha='center', fontsize=7.5, color=MUTED, style='italic')

plt.tight_layout(pad=0.5)
out = BASE + 'output/slide05_Q2_제도공백빈분석.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'저장: {out}')

print('\n구간별 침해율:')
for i, row in bin_stats.iterrows():
    print(f'  {i+1}분위 [{range_labels[i]}]: {row["침해율"]:.1f}%  (n={row["n"]:,})')
print(f'\n  1→5분위 Δ = +{delta:.1f}%p')
print('✅ 완료')
