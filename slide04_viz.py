"""
Slide 04 시각화
4-1: Q1 — 어떤 학교 구조의 교사가 더 취약한가? (Track A OR 포레스트)
4-2: Q2 — 잠재적 요인은 무엇인가? (SEM v2 제도공백 β 경로)
design.md 기준 준수 — 화살표 없음, 막대 내부 텍스트 없음, 심플
"""
import pyreadstat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# ── 폰트 ──
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

BASE   = '/Users/baiohelseu/Desktop/Project/kossda/'
DARK   = '#1A1A2E'
MUTED  = '#6B6B7B'
ACCENT = '#D62728'
BLUE1  = '#1F77B4'
GRAY   = '#AAAAAA'

# ── 데이터 로드 ──
df_raw, _ = pyreadstat.read_sav(
    BASE + 'data/교원 인권상황 실태조사,2024/kor_data_20240073.sav'
)

df = pd.DataFrame()
df['B3_1']   = (df_raw['B3_1'] == 1).astype(int)
df['B2_1']   = (df_raw['B2_1'] == 1).astype(int)
df['초등']   = (df_raw['SQ2'] == 2).astype(int)
df['중학교'] = (df_raw['SQ2'] == 3).astype(int)
df['학교규모'] = df_raw['SQ5'].fillna(df_raw['SQ5'].median())
df['사립']   = (df_raw['SQ4'] == 2).astype(int)
df['기간제'] = (df_raw['SQ8'] == 2).astype(int)
df['남성']   = (df_raw['SQ9'] == 1).astype(int)
df = df.dropna()

struct_vars = ['초등', '중학교', '학교규모', '사립', '기간제', '남성']
labels_kr   = ['초등학교', '중학교', '학교규모 (1단계↑)', '사립학교', '기간제 교원', '남성']

def compute_ors(y_col):
    X = sm.add_constant(df[struct_vars])
    m = sm.Logit(df[y_col], X).fit(disp=0)
    ci = np.exp(m.conf_int())
    ors = np.exp(m.params[struct_vars]).values
    los = ci.loc[struct_vars, 0].values
    his = ci.loc[struct_vars, 1].values
    ps  = m.pvalues[struct_vars].values
    return ors, los, his, ps

def sig_star(p):
    if p < 0.001: return '***'
    if p < 0.01:  return '**'
    if p < 0.05:  return '*'
    return ''

ors_par, los_par, his_par, ps_par = compute_ors('B3_1')
ors_stu, los_stu, his_stu, ps_stu = compute_ors('B2_1')

# ═══════════════════════════════════════════════════════════
# FIG 4-1: Q1 — 학교 구조별 OR (보호자침해 / 학생침해)
# ═══════════════════════════════════════════════════════════
fig1, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True, facecolor='white')
fig1.patch.set_facecolor('white')

# 중요도 순서: 초등(최고 OR) → 위, 남성 → 아래 (역순 배치)
labels_rev = labels_kr[::-1]
ors_par_r  = ors_par[::-1];  los_par_r = los_par[::-1];  his_par_r = his_par[::-1];  ps_par_r = ps_par[::-1]
ors_stu_r  = ors_stu[::-1];  los_stu_r = los_stu[::-1];  his_stu_r = his_stu[::-1];  ps_stu_r = ps_stu[::-1]

y_pos = np.arange(len(labels_rev))
xmax  = max(his_par_r.max(), his_stu_r.max()) + 0.45

for ax, ors, los, his, ps, color, title in [
    (axes[0], ors_par_r, los_par_r, his_par_r, ps_par_r, ACCENT, '보호자침해'),
    (axes[1], ors_stu_r, los_stu_r, his_stu_r, ps_stu_r, BLUE1,  '학생침해'),
]:
    ax.set_facecolor('white')
    for i in range(len(y_pos)):
        ax.plot([los[i], his[i]], [y_pos[i], y_pos[i]],
                color=GRAY, lw=1.8, zorder=2, solid_capstyle='round')
    ax.scatter(ors, y_pos, color=color, s=75, zorder=3,
               edgecolors='white', linewidths=0.8)
    ax.axvline(1.0, color='#999999', linestyle='--', linewidth=1.0, zorder=1)
    for i, (OR, lo, hi, p) in enumerate(zip(ors, los, his, ps)):
        star = sig_star(p)
        col_lbl = color if p < 0.05 else MUTED
        ax.text(hi + 0.06, y_pos[i], f'{OR:.2f}{star}',
                va='center', fontsize=9.5, color=col_lbl)
    ax.set_xlim(0.25, xmax)
    ax.set_xlabel('Odds Ratio (95% CI)', fontsize=9, color=MUTED, labelpad=6)
    ax.set_title(title, fontsize=12, fontweight='bold', color=color, pad=8)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(axis='x', labelsize=9, colors=MUTED, length=0)
    ax.tick_params(axis='y', length=0)
    ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.8)
    ax.set_axisbelow(True)

axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(labels_rev, fontsize=11, color=DARK)

fig1.text(0.5, -0.04,
          '출처: 윤정향, 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073) | n=10,888 | '
          '이분형 로지스틱 회귀, 기준집단=고등학교',
          ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout()
out1 = BASE + 'output/slide04_4-1_구조취약성OR.png'
fig1.savefig(out1, dpi=200, bbox_inches='tight', facecolor='white')
print(f'저장: {out1}')
plt.close(fig1)

print('✅ 4-1 완료')

# ═══════════════════════════════════════════════════════════
# FIG 4-2: Q2 — 제도공백이 잠재 핵심요인 (SEM v2 β 경로)
# ═══════════════════════════════════════════════════════════
# SEM v2 검증 결과 — 인과 흐름 순서로 역배치 (제도공백이 맨 위)
# (barh는 아래→위 순이므로 중요도 낮은 것부터 입력)
paths = [
    ('정신건강역 → 자살사고',          0.129, '***', False),
    ('정신건강역 → 이직고려',          0.141, '***', False),
    ('침해지수 → 자살사고 (직접)',     0.067, '***', False),
    ('침해지수 → 이직고려 (직접)',     0.125, '***', False),
    ('침해지수 → 정신건강역',          0.350, '***', False),
    ('제도공백 → 침해지수',           0.454, '***', True),
]

labels_sem = [p[0] for p in paths]
betas      = [p[1] for p in paths]
stars_sem  = [p[2] for p in paths]
is_key     = [p[3] for p in paths]
colors_sem = [ACCENT if k else BLUE1 for k in is_key]

fig2, ax2 = plt.subplots(figsize=(10, 5), facecolor='white')
fig2.patch.set_facecolor('white')
ax2.set_facecolor('white')

y_sem = np.arange(len(labels_sem))
ax2.barh(y_sem, betas, height=0.52,
         color=colors_sem, edgecolor='white', linewidth=0.8)

for i, (β, star, key) in enumerate(zip(betas, stars_sem, is_key)):
    col = ACCENT if key else BLUE1
    ax2.text(β + 0.010, i, f'β = {β:.3f}{star}',
             va='center', fontsize=10.5, color=col,
             fontweight='bold' if key else 'normal')

ax2.set_yticks(y_sem)
ax2.set_yticklabels(labels_sem, fontsize=11, color=DARK)
ax2.set_xlim(0, 0.72)   # 충분한 오른쪽 여백으로 라벨 겹침 방지
ax2.set_xlabel('표준화 경로계수 (β)', fontsize=10, color=MUTED, labelpad=6)
ax2.tick_params(axis='x', labelsize=9, colors=MUTED, length=0)
ax2.tick_params(axis='y', length=0)
ax2.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax2.xaxis.grid(True, color='#EEEEEE', linewidth=0.8)
ax2.set_axisbelow(True)

# 범례를 upper right (상단)으로 올려 라벨과 겹침 방지
legend_patches = [
    mpatches.Patch(color=ACCENT, label='핵심 경로 (제도공백)'),
    mpatches.Patch(color=BLUE1,  label='매개·결과 경로'),
]
ax2.legend(handles=legend_patches, loc='upper right', fontsize=9, frameon=False)

fig2.text(0.5, -0.05,
          '출처: D1(2024) | SEM v2 (analysis_sem_v2.py) | CFI=0.917  RMSEA=0.070  Cronbach α=0.741 | '
          '전 경로 p<.001',
          ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout()
out2 = BASE + 'output/slide04_4-2_제도공백SEM.png'
fig2.savefig(out2, dpi=200, bbox_inches='tight', facecolor='white')
print(f'저장: {out2}')
plt.close(fig2)

print('✅ 4-2 완료')
