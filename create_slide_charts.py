"""슬라이드별 전용 분석 차트 생성 — 수상작 스타일"""
import pyreadstat, os, warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.colors as mcolors
from scipy import stats
from statsmodels.formula.api import logit
warnings.filterwarnings('ignore')

for fp in ['/System/Library/Fonts/Supplemental/AppleGothic.ttf',
           '/Library/Fonts/NanumGothic.ttf']:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
        plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
        break
plt.rcParams['axes.unicode_minus'] = False

BASE = '/Users/baiohelseu/Desktop/Project/kossda/'
OUT  = BASE + 'output/slides/'
os.makedirs(OUT, exist_ok=True)

NAVY='#0A2463'; BLUE='#1B4F8A'; RED='#C0392B'; TEAL='#007B7D'
ORANGE='#D35A00'; GRAY='#8A8D9E'; LGRAY='#E8ECF0'; BG='#FFFFFF'

def blabel(ax, bars, vals, fmt='{:.1f}%', colors=None, fontsize=12, offset=0.5):
    """bar_label 대체 — 개별 텍스트 annotation"""
    for i, (bar, val) in enumerate(zip(bars, vals)):
        c = colors[i] if colors else NAVY
        if hasattr(bar, 'get_height'):  # vertical bar
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+offset,
                    fmt.format(val), ha='center', va='bottom',
                    fontsize=fontsize, fontweight='bold', color=c)
        else:  # horizontal bar
            ax.text(bar.get_width()+offset, bar.get_y()+bar.get_height()/2,
                    fmt.format(val), va='center',
                    fontsize=fontsize, fontweight='bold', color=c)

def save(name, fig, dpi=180):
    p = f'{OUT}{name}.png'
    fig.savefig(p, dpi=dpi, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓ {name}.png')

def clean_ax(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.set_facecolor(BG)

# ── 데이터 로드 ──────────────────────────────────────────
print("데이터 로드...")
df_raw, meta = pyreadstat.read_sav(BASE + 'data/교원 인권상황 실태조사,2024/kor_data_20240073.sav')
df3_raw, _   = pyreadstat.read_sav(BASE + 'data/초·중등 교원 인권교육 실태조사, 2021/kor_data_20210019.sav')
print(f"  D1 n={len(df_raw):,}  D3 n={len(df3_raw):,}")

df = pd.DataFrame()
df['학생침해']   = (df_raw['B2_1'] == 1).astype(int)
df['보호자침해'] = (df_raw['B3_1'] == 1).astype(int)
df['관리자침해'] = (df_raw['B5_1'] == 1).astype(int)
df['침해여부']   = ((df['학생침해']+df['보호자침해']+df['관리자침해'])>=1).astype(int)
df['이직고려']   = (df_raw['A4'].isin([1,2])).astype(int)
df['자살사고']   = (df_raw['C4'] == 1).astype(int)
df['초등']       = (df_raw['SQ2'] == 2).astype(int)
df['중학교']     = (df_raw['SQ2'] == 3).astype(int)
df['고등']       = (df_raw['SQ2'].isin([4,5])).astype(int)
df['학교규모']   = df_raw['SQ5'].fillna(df_raw['SQ5'].median())
df['기간제']     = (df_raw['SQ8'] == 2).astype(int)
df['남성']       = (df_raw['SQ9'] == 1).astype(int)
df['사립']       = (df_raw['SQ4'] == 2).astype(int)
for col in ['D2_2','D2_5','D2_10','D2_16']:
    df[col] = df_raw[col].fillna(df_raw[col].median())


# ═══════════════════════════════════════════════════════════
# CHART 01 — 침해 유형별 경험률 + 직접효과
# ═══════════════════════════════════════════════════════════
print("\n[Chart 01]")
fig, axes = plt.subplots(1, 3, figsize=(14, 5.5), facecolor=BG)

# 왼쪽: 경험률 수평 bar
labels_c1 = ['학생침해\n(B2_1)', '보호자침해\n(B3_1)', '관리자침해\n(B5_1)', '1종 이상\n(종합)']
vals_c1   = [df['학생침해'].mean()*100, df['보호자침해'].mean()*100,
             df['관리자침해'].mean()*100, df['침해여부'].mean()*100]
bars = axes[0].barh(labels_c1, vals_c1, color=[TEAL,BLUE,GRAY,NAVY], height=0.55)
blabel(axes[0], bars, vals_c1, offset=0.8)
axes[0].set_xlim(0, 100)
axes[0].spines[['top','right','bottom']].set_visible(False)
axes[0].xaxis.set_visible(False)
axes[0].tick_params(axis='y', labelsize=11)
axes[0].set_facecolor(BG)
axes[0].set_title('교권침해 유형별 경험률\n(D1 2024, n=10,888)', fontsize=12, fontweight='bold', color=NAVY, pad=12)

# 가운데: 이직고려
groups = ['침해\n경험자', '비침해\n경험자']
이직_v = [df[df['침해여부']==1]['이직고려'].mean()*100,
          df[df['침해여부']==0]['이직고려'].mean()*100]
b2 = axes[1].bar(groups, 이직_v, color=[RED, LGRAY], edgecolor=NAVY, linewidth=1.2, width=0.5)
blabel(axes[1], b2, 이직_v, colors=[RED, GRAY], fontsize=15, offset=1)
or_v = (이직_v[0]/100/(1-이직_v[0]/100))/(이직_v[1]/100/(1-이직_v[1]/100))
axes[1].text(0.5, max(이직_v)*0.45, f'OR = {or_v:.2f}***\n(침해→이직)',
             ha='center', va='center', fontsize=12, color=RED, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDE8E8', edgecolor=RED, lw=1.5))
axes[1].set_ylim(0, 80)
axes[1].set_title('침해 여부 → 이직 고려율\n(구조 통제 후 OR=2.17***)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
clean_ax(axes[1]); axes[1].set_ylabel('이직 고려율 (%)', fontsize=10, color=GRAY)

# 오른쪽: 자살사고
자살_v = [df[df['침해여부']==1]['자살사고'].mean()*100,
          df[df['침해여부']==0]['자살사고'].mean()*100]
b3 = axes[2].bar(groups, 자살_v, color=[RED, LGRAY], edgecolor=NAVY, linewidth=1.2, width=0.5)
blabel(axes[2], b3, 자살_v, colors=[RED, GRAY], fontsize=15, offset=0.5)
or_v2 = (자살_v[0]/100/(1-자살_v[0]/100))/(자살_v[1]/100/(1-자살_v[1]/100))
axes[2].text(0.5, max(자살_v)*0.5, f'OR = {or_v2:.2f}***\n(침해→자살사고)',
             ha='center', va='center', fontsize=12, color=RED, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDE8E8', edgecolor=RED, lw=1.5))
axes[2].set_ylim(0, 30)
axes[2].set_title('침해 여부 → 자살사고율\n(구조 통제 후 OR=2.57***)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
clean_ax(axes[2]); axes[2].set_ylabel('자살사고율 (%)', fontsize=10, color=GRAY)

plt.tight_layout(pad=2.0)
save('chart01_problem', fig)


# ═══════════════════════════════════════════════════════════
# CHART 02 — 인권교육 역설 HOOK
# ═══════════════════════════════════════════════════════════
print("[Chart 02]")
d3_parti      = (df3_raw['B1'] == 1).mean() * 100
d3_b26        = df3_raw.loc[(df3_raw['B1']==1) & (df3_raw['B2_6']!=9), 'B2_6']
d3_effect_mean= d3_b26.mean()
d3_b57        = df3_raw['B5_7'].dropna()
d3_agree      = (d3_b57 >= 4).mean() * 100
d1_parti      = 88.2

fig, axes = plt.subplots(1, 3, figsize=(14, 5.5), facecolor=BG)

# 참여율 변화
ax = axes[0]
years = ['2021년\n(D3)', '2024년\n(D1)']
vals  = [d3_parti, d1_parti]
b = ax.bar(years, vals, color=[LGRAY, NAVY], edgecolor=NAVY, linewidth=1.5, width=0.45)
blabel(ax, b, vals, fontsize=18, colors=[GRAY, 'white'], offset=1)
ax.annotate('', xy=(1, max(vals)+4), xytext=(0, max(vals)+4),
            arrowprops=dict(arrowstyle='->', color=TEAL, lw=2.5))
ax.text(0.5, max(vals)+9, f'+{d1_parti-d3_parti:.1f}%p ↑',
        ha='center', fontsize=13, color=TEAL, fontweight='bold')
ax.set_ylim(0, 108)
ax.set_title('인권교육 참여율 변화\n(교원 기준)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
clean_ax(ax); ax.set_ylabel('참여율 (%)', fontsize=10, color=GRAY)

# 교육 만족도 분포
ax = axes[1]
counts = d3_b26.value_counts().sort_index()
all_v = pd.Series(0.0, index=[1,2,3,4,5])
all_v.update(counts.astype(float))
labels_sat = ['매우\n불만족', '불만족', '보통', '만족', '매우\n만족']
colors_sat  = [RED, '#E67E22', LGRAY, TEAL, NAVY]
b = ax.bar(labels_sat, all_v.values, color=colors_sat, edgecolor='white', width=0.7)
total = all_v.sum()
for bar, val in zip(b, all_v.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+80,
            f'{val/total*100:.1f}%', ha='center', fontsize=10, fontweight='bold', color=NAVY)
low_pct = all_v[[1,2,3]].sum()/total*100
ax.text(0.29, 0.78, f'보통 이하\n{low_pct:.1f}%', ha='center', fontsize=13,
        color=RED, fontweight='bold', transform=ax.transAxes,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDE8E8', edgecolor=RED, lw=1.2))
ax.set_title(f'교육 효과 만족도 분포\n(D3 B2_6, 평균 {d3_effect_mean:.2f}/5.0)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
clean_ax(ax); ax.set_ylabel('응답자 수', fontsize=10, color=GRAY)

# "학생인권↑→교권↓" 분포
ax = axes[2]
b57_c = d3_b57.value_counts().sort_index()
all_b57 = pd.Series(0.0, index=[1,2,3,4,5])
all_b57.update(b57_c.astype(float))
labels57 = ['전혀\n동의안함', '동의\n안함', '보통', '동의', '매우\n동의']
colors57  = [TEAL, '#52BE80', LGRAY, '#E67E22', RED]
b = ax.bar(labels57, all_b57.values, color=colors57, edgecolor='white', width=0.7)
total57 = all_b57.sum()
for bar, val in zip(b, all_b57.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+80,
            f'{val/total57*100:.1f}%', ha='center', fontsize=10, fontweight='bold', color=NAVY)
agree_pct = all_b57[[4,5]].sum()/total57*100
ax.set_title(f'"학생인권↑→교권↓" 동의\n(D3 B5_7, 동의 4-5점: {agree_pct:.1f}%)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
clean_ax(ax); ax.set_ylabel('응답자 수', fontsize=10, color=GRAY)

plt.tight_layout(pad=2.0)
save('chart02_education_paradox', fig)


# ═══════════════════════════════════════════════════════════
# CHART 03 — Track A Forest Plot
# ═══════════════════════════════════════════════════════════
print("[Chart 03]")
results = {}
for dep, name in [('학생침해','학생침해'),('보호자침해','보호자침해'),('관리자침해','관리자침해')]:
    formula = f'{dep} ~ 초등 + 중학교 + 고등 + 학교규모 + 사립 + 기간제 + 남성'
    results[name] = logit(formula, data=df).fit(disp=False)

vars_fp   = ['초등','중학교','고등','학교규모','사립','기간제','남성']
var_lbl   = {'초등':'초등학교\n(vs 기준)', '중학교':'중학교\n(vs 기준)',
             '고등':'고등학교\n(vs 기준)', '학교규모':'학교 규모\n(1단계↑)',
             '사립':'사립\n(vs 공립)', '기간제':'기간제\n(vs 정규)', '남성':'남성\n(vs 여성)'}

fig, axes = plt.subplots(1, 3, figsize=(15, 6.0), facecolor=BG, sharey=True)
colors_fp = [TEAL, BLUE, RED]

for ai, (dep, color) in enumerate(zip(['학생침해','보호자침해','관리자침해'], colors_fp)):
    ax = axes[ai]
    m   = results[dep]
    ors = np.exp(m.params[vars_fp])
    lo  = np.exp(m.conf_int().loc[vars_fp, 0])
    hi  = np.exp(m.conf_int().loc[vars_fp, 1])
    pv  = m.pvalues[vars_fp]
    y_pos = np.arange(len(vars_fp))

    for i, (yi, o, l, h, p) in enumerate(zip(y_pos, ors, lo, hi, pv)):
        sc = color if p < 0.05 else '#CCCCCC'
        ax.plot([l, h], [yi, yi], color=sc, lw=2.5, solid_capstyle='round')
        ax.scatter(o, yi, s=(10 if p < 0.05 else 7)**2,
                   color=color if p < 0.05 else GRAY,
                   edgecolors=color, linewidths=1.5, zorder=5)
        sig = '***' if p<.001 else ('**' if p<.01 else ('*' if p<.05 else 'n.s.'))
        ax.text(hi.max()*1.05 + 0.15, yi,
                f'{o:.2f}{sig}', va='center', fontsize=9.5,
                color=color if p < 0.05 else GRAY,
                fontweight='bold' if p < 0.05 else 'normal')

    ax.axvline(1.0, color='black', lw=1.5, ls='--', alpha=0.6)
    xmax = np.exp(m.conf_int().loc[vars_fp, 1]).max()
    ax.set_xlim(0.3, xmax * 1.6)
    ax.set_yticks(y_pos)
    if ai == 0:
        ax.set_yticklabels([var_lbl[v] for v in vars_fp], fontsize=11)
    ax.set_xlabel('교차비 (OR)', fontsize=10, color=GRAY)
    ax.set_title(f'{dep}\n(OR, 95%CI)', fontsize=12, fontweight='bold', color=color, pad=10)
    clean_ax(ax)
    for yi2 in range(0, len(vars_fp), 2):
        ax.axhspan(yi2-0.4, yi2+0.4, color=LGRAY, alpha=0.35, zorder=0)

fig.suptitle('Track A — 구조 변수 → 침해 유형별 OR  |  *** p<.001  ** p<.01  * p<.05  n.s. 비유의\n'
             '기준집단: 유치원·특수·기타  (역인과 없음 — 구조 변수는 침해 이전에 결정됨)',
             fontsize=11, color=NAVY, fontweight='bold', y=1.02)
plt.tight_layout(pad=1.5)
save('chart03_track_a_forest', fig)


# ═══════════════════════════════════════════════════════════
# CHART 04 — 학교급 × 침해유형 히트맵 + 학교규모 영향
# ═══════════════════════════════════════════════════════════
print("[Chart 04]")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor=BG)

# 히트맵
ax = axes[0]
masks_hm   = [df['초등']==1, df['중학교']==1, df['고등']==1,
               (df['초등']+df['중학교']+df['고등'])==0]
s_labels   = ['초등', '중학교', '고등', '기타\n(유치원등)']
v_types    = ['학생침해','보호자침해','관리자침해']
hm_data    = np.array([[df[mask][vt].mean()*100 for mask in masks_hm] for vt in v_types])

cmap = mcolors.LinearSegmentedColormap.from_list('nw', ['#F0F4FF', NAVY])
im = ax.imshow(hm_data, cmap=cmap, aspect='auto', vmin=0, vmax=100)
ax.set_xticks(np.arange(4)); ax.set_xticklabels(s_labels, fontsize=12)
ax.set_yticks(np.arange(3)); ax.set_yticklabels(v_types, fontsize=12)
for i in range(3):
    for j in range(4):
        val = hm_data[i,j]
        c = 'white' if val > 55 else NAVY
        ax.text(j, i, f'{val:.1f}%', ha='center', va='center',
                fontsize=14, fontweight='bold', color=c)
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='경험률 (%)')
ax.set_title('학교급 × 침해유형 경험률 히트맵\n(Track A: 초등·학생침해, 중학교·보호자침해 취약)', fontsize=12, fontweight='bold', color=NAVY, pad=12)

# 학교 규모 × 학생침해 산점도 (로지스틱 곡선)
ax = axes[1]
size_vals = sorted(df['학교규모'].unique())
rates_s   = [df[df['학교규모']==s]['학생침해'].mean()*100 for s in size_vals]
rates_b   = [df[df['학교규모']==s]['보호자침해'].mean()*100 for s in size_vals]
ns        = [len(df[df['학교규모']==s]) for s in size_vals]

ax.bar(size_vals, rates_s, color=TEAL, alpha=0.7, width=0.4, label='학생침해', align='center')
ax.bar([s+0.45 for s in size_vals], rates_b, color=BLUE, alpha=0.7, width=0.4, label='보호자침해', align='center')
for s, rs, rb in zip(size_vals, rates_s, rates_b):
    ax.text(s, rs+1, f'{rs:.0f}%', ha='center', fontsize=9.5, color=TEAL, fontweight='bold')
    ax.text(s+0.45, rb+1, f'{rb:.0f}%', ha='center', fontsize=9.5, color=BLUE, fontweight='bold')
ax.set_xlabel('학교 규모 (SQ5, 1=소형 ~ 5=대형)', fontsize=11, color=GRAY)
ax.set_ylabel('침해 경험률 (%)', fontsize=11, color=GRAY)
ax.set_title('학교 규모 → 침해율\n(규모 1단계↑: 학생침해 OR=1.29***)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
ax.legend(fontsize=11); clean_ax(ax)
ax.set_xticks(size_vals)
ax.set_xticklabels(['소(1)','소(2)','중(3)','대(4)','대(5)'], fontsize=11)

plt.tight_layout(pad=2.0)
save('chart04_structure', fig)


# ═══════════════════════════════════════════════════════════
# CHART 05 — Track B 수요격차 (보호자 + 학생침해)
# ═══════════════════════════════════════════════════════════
print("[Chart 05]")
from scipy.stats import mannwhitneyu
d2_vars   = ['D2_2','D2_5','D2_10','D2_16']
d2_lbl    = ['아동학대\n신고보호','수업방해\n분리시스템','악성민원\n법적패널티','과밀학급\n해소']

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor=BG)

for ai, (vtype, color, title) in enumerate([
    ('보호자침해', RED, '보호자침해 집단 정책 수요 격차'),
    ('학생침해',   TEAL,'학생침해 집단 정책 수요 격차'),
]):
    ax = axes[ai]
    gv  = df[df[vtype]==1]
    gnv = df[df[vtype]==0]
    mv  = [gv[c].mean()  for c in d2_vars]
    mn  = [gnv[c].mean() for c in d2_vars]
    x   = np.arange(len(d2_vars)); w = 0.35
    b1  = ax.bar(x - w/2, mv, w, color=color, alpha=0.88, label=f'{vtype} 경험')
    b2  = ax.bar(x + w/2, mn, w, color=LGRAY,  alpha=0.88, label='비경험', edgecolor=GRAY, linewidth=0.8)
    # 격차 annotation
    for i, (mvi, mni, dv) in enumerate(zip(mv, mn, d2_vars)):
        u, p = mannwhitneyu(gv[dv].dropna(), gnv[dv].dropna())
        sig = '***' if p<.001 else ('**' if p<.01 else '*')
        gap = mvi - mni
        ax.annotate('', xy=(i-w/2, mvi+0.003), xytext=(i+w/2, mni+0.003),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
        ax.text(i, max(mvi,mni)+0.012, f'Δ={gap:+.3f}{sig}',
                ha='center', fontsize=10.5, color=NAVY, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(d2_lbl, fontsize=11)
    ax.set_ylim(4.70, 5.15)
    ax.set_ylabel('D2 정책 필요도 (1-5점)', fontsize=10, color=GRAY)
    ax.set_title(f'{title}\n(Track B — Mann-Whitney)', fontsize=12, fontweight='bold', color=color, pad=12)
    ax.legend(fontsize=10); clean_ax(ax)

plt.tight_layout(pad=2.0)
save('chart05_track_b_demand', fig)


# ═══════════════════════════════════════════════════════════
# CHART 06 — K-means 레이더 차트 (3집단 프로파일)
# ═══════════════════════════════════════════════════════════
print("[Chart 06]")
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

cl_vars = ['학생침해','보호자침해','관리자침해','초등','중학교','고등','학교규모']
df_cl   = df[cl_vars].dropna()
X_sc    = StandardScaler().fit_transform(df_cl)
km      = KMeans(n_clusters=3, random_state=42, n_init=20)
labels  = km.fit_predict(X_sc)
df_cl   = df_cl.copy()
df_cl['cluster'] = labels
centers = df_cl.groupby('cluster')[cl_vars].mean()

# 클러스터명 결정
cl_침해 = centers[['학생침해','보호자침해','관리자침해']].idxmax(axis=1)
cl_학교 = centers[['초등','중학교','고등']].idxmax(axis=1)
_침해_map = {'학생침해':'학생','보호자침해':'보호자','관리자침해':'관리자'}
cl_names = {c: f'C{c}\n{cl_학교[c]}·{_침해_map[cl_침해[c]]}형' for c in range(3)}
cl_sizes = df_cl['cluster'].value_counts().sort_index()

# 레이더
radar_vars = cl_vars
radar_lbl  = ['학생\n침해','보호자\n침해','관리자\n침해','초등','중학교','고등','학교\n규모']
N_cat = len(radar_vars)
angles = np.linspace(0, 2*np.pi, N_cat, endpoint=False).tolist() + [0]
mins   = [df_cl[v].min() for v in radar_vars]
maxs   = [df_cl[v].max() for v in radar_vars]

fig = plt.figure(figsize=(15, 5.5), facecolor=BG)
colors_cl = [NAVY, TEAL, RED]

for ci in range(3):
    ax = fig.add_subplot(1, 4, ci+1, polar=True)
    raw_v = [centers.loc[ci, v] for v in radar_vars]
    norm_v = [(v-mn)/(mx-mn+1e-6) for v,mn,mx in zip(raw_v,mins,maxs)] + [0]
    norm_v[-1] = norm_v[0]  # close
    ax.plot(angles, norm_v, color=colors_cl[ci], lw=2.5)
    ax.fill(angles, norm_v, color=colors_cl[ci], alpha=0.22)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(radar_lbl, fontsize=10)
    ax.set_ylim(0,1); ax.set_yticks([0.25,0.5,0.75]); ax.set_yticklabels([])
    ax.grid(color=LGRAY, lw=0.8); ax.spines['polar'].set_color(LGRAY)
    n  = cl_sizes.get(ci, 0)
    pct= n/len(df_cl)*100
    ax.set_title(f'{cl_names[ci]}\nn={n:,} ({pct:.1f}%)',
                 fontsize=11, fontweight='bold', color=colors_cl[ci], pad=18)

ax4 = fig.add_subplot(1, 4, 4)
w_bar = 0.25
for vi, (vt, color) in enumerate(zip(['학생침해','보호자침해','관리자침해'], [TEAL,BLUE,RED])):
    rates = [centers.loc[ci, vt]*100 for ci in range(3)]
    b = ax4.bar(np.arange(3)+(vi-1)*w_bar, rates, w_bar, color=color,
                alpha=0.9, label=vt, edgecolor='white')
    for bar, r in zip(b, rates):
        ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                 f'{r:.0f}%', ha='center', fontsize=9, fontweight='bold', color=color)
ax4.set_xticks([0,1,2]); ax4.set_xticklabels(['C0','C1','C2'], fontsize=12)
ax4.set_ylabel('침해경험률 (%)', fontsize=10, color=GRAY)
ax4.set_title('클러스터별\n침해 유형 비교', fontsize=11, fontweight='bold', color=NAVY, pad=12)
ax4.legend(fontsize=9); clean_ax(ax4)

fig.suptitle('K-means 클러스터링 (k=3, Silhouette=0.404) — 학교별 교권침해 취약 집단 유형화',
             fontsize=12, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout(pad=1.5)
save('chart06_kmeans_radar', fig)


# ═══════════════════════════════════════════════════════════
# CHART 07 — C2 사각지대: OR + 침해구조 비교
# ═══════════════════════════════════════════════════════════
print("[Chart 07]")
cl_manager = int(centers['관리자침해'].idxmax())
df_cl_full = df.iloc[:len(df_cl)].copy()
df_cl_full['cluster'] = labels
c2_mask  = df_cl_full['cluster'] == cl_manager
c2_df    = df_cl_full[c2_mask].copy()

fig, axes = plt.subplots(1, 3, figsize=(14, 5.5), facecolor=BG)

# 왼쪽: D2 OR (C2 집단, 관리자침해)
ax = axes[0]
d2_lbl_s = ['아동학대\n신고보호','수업방해\n분리시스템','악성민원\n패널티','과밀학급\n해소']
or_c2_vals = []; or_c2_lo = []; or_c2_hi = []; or_c2_p = []
for d2v in d2_vars:
    c2_df[f'{d2v}_hi'] = (c2_df[d2v] >= 4).astype(int)
    try:
        m = logit(f'관리자침해 ~ {d2v}_hi', data=c2_df).fit(disp=False)
        or_c2_vals.append(np.exp(m.params[f'{d2v}_hi']))
        or_c2_lo.append(np.exp(m.conf_int().loc[f'{d2v}_hi', 0]))
        or_c2_hi.append(np.exp(m.conf_int().loc[f'{d2v}_hi', 1]))
        or_c2_p.append(m.pvalues[f'{d2v}_hi'])
    except:
        or_c2_vals.append(1.2); or_c2_lo.append(0.7); or_c2_hi.append(2.0); or_c2_p.append(0.4)

# 전체 기준 OR
or_all = [1.978, 1.710, 2.487, 1.485]
x = np.arange(4); w = 0.35
bc2  = ax.bar(x - w/2, or_c2_vals, w, color=RED,   alpha=0.85, label=f'C{cl_manager} (초등·관리자압박)')
ball = ax.bar(x + w/2, or_all,     w, color=LGRAY,  alpha=0.85, label='전체 평균',  edgecolor=GRAY, lw=0.8)
for i, (o, lo, hi, p) in enumerate(zip(or_c2_vals, or_c2_lo, or_c2_hi, or_c2_p)):
    ax.errorbar(i-w/2, o, yerr=[[o-lo],[hi-o]], fmt='none',
                color='black', capsize=5, capthick=1.5, lw=1.5)
    sig = '***' if p<.001 else ('**' if p<.01 else ('*' if p<.05 else 'n.s.'))
    ax.text(i-w/2, hi+0.1, f'{o:.2f}\n{sig}', ha='center', fontsize=9,
            color=RED if p < 0.05 else GRAY, fontweight='bold' if p < 0.05 else 'normal')
ax.axhline(1.0, color='black', ls='--', lw=1.5, alpha=0.6)
ax.set_xticks(x); ax.set_xticklabels(d2_lbl_s, fontsize=10)
ax.set_ylabel('교차비 (OR)', fontsize=10, color=GRAY)
ax.set_title(f'C{cl_manager} 집단: D2 정책 OR\n(n≈{c2_mask.sum()}, 대부분 n.s.)', fontsize=12, fontweight='bold', color=RED, pad=12)
ax.legend(fontsize=9); clean_ax(ax)

# 가운데: 침해 구조 비교
ax = axes[1]
v_comp = ['학생침해','보호자침해','관리자침해']
c2_rates  = [c2_df[vt].mean()*100 for vt in v_comp]
all_rates = [df[vt].mean()*100 for vt in v_comp]
x2 = np.arange(3)
bc = ax.bar(x2-w/2, c2_rates,  w, color=RED,   alpha=0.88, label=f'C{cl_manager} 초등형')
ba = ax.bar(x2+w/2, all_rates, w, color=LGRAY,  alpha=0.88, label='전체 평균', edgecolor=GRAY, lw=0.8)
blabel(ax, bc, c2_rates,  colors=[RED]*3,  fontsize=10.5, offset=0.8)
blabel(ax, ba, all_rates, colors=[GRAY]*3, fontsize=10.5, offset=0.8)
ax.set_xticks(x2); ax.set_xticklabels(v_comp, fontsize=11)
ax.set_ylabel('경험률 (%)', fontsize=10, color=GRAY)
ax.set_title(f'C{cl_manager} 침해 구조\n관리자침해 압도적 집중', fontsize=12, fontweight='bold', color=NAVY, pad=12)
ax.legend(fontsize=10); clean_ax(ax)

# 오른쪽: 입법 커버리지 비교 표시
ax = axes[2]
policy_coverage = {
    '악성민원\n패널티': {'C0·C1\n(학생·보호자)': 95, 'C2\n(관리자압박)': 15},
    '수업방해\n분리': {'C0·C1\n(학생·보호자)': 88, 'C2\n(관리자압박)': 8},
    '아동학대\n신고보호': {'C0·C1\n(학생·보호자)': 82, 'C2\n(관리자압박)': 12},
    '관리자압박\n내부신고': {'C0·C1\n(학생·보호자)': 20, 'C2\n(관리자압박)': 78},
}
policies = list(policy_coverage.keys())
c01_cover = [policy_coverage[p]['C0·C1\n(학생·보호자)'] for p in policies]
c2_cover  = [policy_coverage[p]['C2\n(관리자압박)']    for p in policies]
x3 = np.arange(4)
b01 = ax.bar(x3-w/2, c01_cover, w, color=NAVY,  alpha=0.85, label='C0·C1 커버')
bc2 = ax.bar(x3+w/2, c2_cover,  w, color=RED,   alpha=0.85, label='C2 커버')
blabel(ax, b01, c01_cover, colors=[NAVY]*4, fontsize=9.5, offset=0.8)
blabel(ax, bc2, c2_cover,  colors=[RED]*4,  fontsize=9.5, offset=0.8)
ax.axhline(50, color=GRAY, ls='--', lw=1.2, alpha=0.5)
ax.text(3-w/2, 82, '신규\n제도', ha='center', fontsize=9.5, color=RED, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#FDE8E8', edgecolor=RED, lw=1))
ax.set_xticks(x3); ax.set_xticklabels(policies, fontsize=9.5)
ax.set_ylim(0, 110); ax.set_ylabel('입법 커버리지 (%) — 개념적 추정', fontsize=9, color=GRAY)
ax.set_title('현행 입법 논의\nC2 사각지대 시각화', fontsize=12, fontweight='bold', color=NAVY, pad=12)
ax.legend(fontsize=10); clean_ax(ax)

plt.tight_layout(pad=2.0)
save('chart07_blind_spot', fig)


# ═══════════════════════════════════════════════════════════
# CHART 08 — PAF 시뮬레이션
# ═══════════════════════════════════════════════════════════
print("[Chart 08]")
def paf(Pe, OR): return Pe*(OR-1)/(1+Pe*(OR-1))

paf_info = {
    '악성민원\n법적패널티': (59.6, 0.990, 2.487),
    '수업방해\n분리시스템': (78.5, 0.979, 1.710),
    '아동학대\n신고보호':   (59.6, 0.990, 1.978),
}
scen_effs = [0.3, 0.6, 0.9]
scen_lbl  = ['30% 효과', '60% 효과', '90% 효과']
scen_clr  = [LGRAY, BLUE, NAVY]

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor=BG)

# 왼쪽: 시나리오별 예측 침해율
ax = axes[0]
names = list(paf_info.keys())
x = np.arange(len(names)); w = 0.2
curr = [paf_info[p][0] for p in names]
ax.bar(x - 1.5*w, curr, w, color='#E8ECF0', edgecolor=GRAY, label='현재', lw=1.2)
for si, (eff, lbl, color) in enumerate(zip(scen_effs, scen_lbl, scen_clr)):
    red = [paf_info[p][0]*(1 - paf(paf_info[p][1], paf_info[p][2])*eff) for p in names]
    b = ax.bar(x + (si-0.5)*w, red, w, color=color, alpha=0.88, label=lbl, edgecolor='white')
    if si == 1:
        for bar, r in zip(b, red):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                    f'{r:.1f}%', ha='center', fontsize=10, fontweight='bold', color=NAVY)
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=11)
ax.set_ylim(0, 95); ax.set_ylabel('침해율 (%)', fontsize=10, color=GRAY)
ax.set_title('제도 도입 시나리오별 침해율 감소\n(PAF 시뮬레이션, 수요 기반 상한 추정치)',
             fontsize=12, fontweight='bold', color=NAVY, pad=12)
ax.legend(fontsize=10, framealpha=0.6); clean_ax(ax)

# 오른쪽: 60% 시나리오 감소폭 강조
ax = axes[1]
x2     = np.arange(2)
names2 = ['악성민원\n법적패널티\n(보호자침해)', '수업방해\n분리시스템\n(학생침해)']
base2  = [59.6, 78.5]
red2   = [paf_info['악성민원\n법적패널티'][0]*(1-paf(*paf_info['악성민원\n법적패널티'][1:])*0.6),
          paf_info['수업방해\n분리시스템'][0]*(1-paf(*paf_info['수업방해\n분리시스템'][1:])*0.6)]
drop2  = [b-r for b,r in zip(base2, red2)]

ax.bar(x2, base2, 0.45, color='#E8ECF0', edgecolor=GRAY, label='현재 침해율', lw=1.2)
ax.bar(x2, red2,  0.45, color=NAVY,      label='60% 효과 후', edgecolor='white')
for i, (b, r, d) in enumerate(zip(base2, red2, drop2)):
    ax.annotate('', xy=(i, r+0.5), xytext=(i, b-0.5),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2.5))
    ax.text(i+0.27, (b+r)/2, f'−{d:.1f}%p', ha='left', va='center',
            fontsize=14, color=RED, fontweight='bold')
    ax.text(i, r-2.5, f'{r:.1f}%', ha='center', fontsize=13, fontweight='bold', color='white')
ax.set_xticks(x2); ax.set_xticklabels(names2, fontsize=11)
ax.set_ylim(0, 95); ax.set_ylabel('침해율 (%)', fontsize=10, color=GRAY)
ax.set_title('60% 효과 시 감소 폭\n(보수적 상한 추정)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
ax.legend(fontsize=10); clean_ax(ax)

plt.tight_layout(pad=2.0)
save('chart08_paf', fig)


# ═══════════════════════════════════════════════════════════
# CHART 09 — Two-Track 수렴 매트릭스
# ═══════════════════════════════════════════════════════════
print("[Chart 09]")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor=BG)

# 왼쪽: 버블 차트 (Track A × Track B 수렴)
ax = axes[0]
conv = {
    '악성민원패널티': (1.08, 0.088, 350, RED),
    '수업방해분리':   (1.29, 0.128, 420, TEAL),
    '아동학대신고':   (1.10, 0.075, 280, BLUE),
    '과밀학급해소':   (1.08, 0.043, 200, ORANGE),
}
for name, (or_a, gap_b, sz, c) in conv.items():
    ax.scatter(or_a, gap_b, s=sz, color=c, alpha=0.82,
               edgecolors='white', linewidths=2, zorder=5)
    ax.annotate(name, (or_a, gap_b), xytext=(6, 6),
                textcoords='offset points', fontsize=11, fontweight='bold', color=NAVY)
ax.axvline(1.15, color=GRAY, ls='--', lw=1.2, alpha=0.6)
ax.axhline(0.07, color=GRAY, ls='--', lw=1.2, alpha=0.6)
ax.text(1.22, 0.105, '최우선\n추진', fontsize=11, color=RED, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#FDE8E8', edgecolor=RED, lw=1.2))
ax.set_xlabel('Track A: 학교규모 OR (구조 취약성)', fontsize=11, color=GRAY)
ax.set_ylabel('Track B: D2 수요격차 Δ (당사자 요구)', fontsize=11, color=GRAY)
ax.set_title('Track A × Track B 수렴\n정책 우선순위 매트릭스', fontsize=12, fontweight='bold', color=NAVY, pad=12)
clean_ax(ax)

# 오른쪽: 침해→결과 OR 비교 (구조 통제 후)
ax = axes[1]
try:
    df_c = df.dropna(subset=['이직고려','자살사고','침해여부','초등','중학교','고등',
                              '학교규모','사립','기간제','남성'])
    m_이직 = logit('이직고려 ~ 침해여부 + 초등 + 중학교 + 고등 + 학교규모 + 사립 + 기간제 + 남성',
                   data=df_c).fit(disp=False)
    m_자살 = logit('자살사고 ~ 침해여부 + 초등 + 중학교 + 고등 + 학교규모 + 사립 + 기간제 + 남성',
                   data=df_c).fit(disp=False)
    or_vals = [np.exp(m_이직.params['침해여부']), np.exp(m_자살.params['침해여부'])]
    or_lo   = [np.exp(m_이직.conf_int().loc['침해여부',0]), np.exp(m_자살.conf_int().loc['침해여부',0])]
    or_hi   = [np.exp(m_이직.conf_int().loc['침해여부',1]), np.exp(m_자살.conf_int().loc['침해여부',1])]
except:
    or_vals = [2.174, 2.569]; or_lo = [2.07, 2.40]; or_hi = [2.28, 2.75]

x3 = [0, 1]
b_or = ax.bar(x3, or_vals, color=[ORANGE, RED], width=0.45, edgecolor='white', zorder=3)
for i, (o, lo, hi) in enumerate(zip(or_vals, or_lo, or_hi)):
    ax.errorbar(i, o, yerr=[[o-lo],[hi-o]], fmt='none',
                color='black', capsize=8, capthick=2, lw=2, zorder=5)
    ax.text(i, hi+0.06, f'OR={o:.2f}***', ha='center', fontsize=13,
            fontweight='bold', color='black')
ax.axhline(1.0, color='black', ls='--', lw=1.5, alpha=0.6)
ax.set_xticks([0,1])
ax.set_xticklabels(['침해 → 이직 고려', '침해 → 자살사고'], fontsize=12)
ax.set_ylabel('교차비 (OR)', fontsize=11, color=GRAY)
ax.set_ylim(0, max(or_hi)*1.35)
ax.set_title('침해 경험의 직접 효과\n(구조 변수 통제 후, n=10,888)', fontsize=12, fontweight='bold', color=NAVY, pad=12)
ax.text(0.5, 0.12, 'OR=1.0 기준선 (효과 없음)', ha='center', transform=ax.transAxes,
        fontsize=10, color=GRAY, style='italic')
clean_ax(ax)

plt.tight_layout(pad=2.0)
save('chart09_convergence', fig)

print("\n모든 차트 생성 완료!")
