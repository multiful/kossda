"""
Q2 보조 시각화 — 교원 보호 정책 필요도 상위 8개 (D2 변수)
제도공백 논거 강화: 교사들이 가장 필요로 하는 것이 '법적 제도 보호'임을 실증
design.md 준수: 제목 없음, ACCENT/BLUE1/MUTED 3색, annotate 금지, footer
"""
import pyreadstat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

BASE = '/Users/baiohelseu/Desktop/Project/kossda/'
df, meta = pyreadstat.read_sav(
    BASE + 'data/교원 인권상황 실태조사,2024/kor_data_20240073.sav'
)

# ── 침해 집단 구분 ─────────────────────────────────────────
for v in ['B2_1', 'B3_1', 'B5_1']:
    df[v] = pd.to_numeric(df[v], errors='coerce')
df['침해any'] = ((df['B2_1']==1)|(df['B3_1']==1)|(df['B5_1']==1))

# ── D2 상위 8개 선별 (사전 계산된 순위 기준) ──────────────
items = [
    # (변수, 짧은 라벨, 카테고리)
    ('D2_2',  '아동학대 신고 시\n교원 보호 규정 강화',       'law'),
    ('D2_10', '악성민원 교원보호·\n가해자 패널티 법제화',     'law'),
    ('D2_22', '교원 휴식권·치유권\n강화 지원',               'infra'),
    ('D2_5',  '학생 분리 인력·\n예산·시설 확충',             'infra'),
    ('D2_21', '늘봄·방과후\n국가돌봄 책임제 전환',           'other'),
    ('D2_17', '교원 노동기본권\n조치 강화',                  'other'),
    ('D2_16', '과밀학급 해소·\n학급당 학생수 감축',          'infra'),
    ('D2_6',  '수업방해 학생 분리\n기준 법령화',              'law'),
]

# 집단별 평균 계산
rows = []
for var, label, cat in items:
    col = pd.to_numeric(df[var], errors='coerce')
    rows.append({
        'var': var,
        'label': label,
        'cat': cat,
        '전체': col.mean(),
        '침해': col[df['침해any']].mean(),
        '비침해': col[~df['침해any']].mean(),
    })

data = pd.DataFrame(rows)
# barh는 아래→위 → 낮은 값이 위에 오도록 역순 정렬
data = data.sort_values('전체', ascending=True).reset_index(drop=True)

# ── 색상 매핑 ─────────────────────────────────────────────
cat_color = {'law': ACCENT, 'infra': BLUE1, 'other': MUTED}
bar_colors = [cat_color[c] for c in data['cat']]

# ── 시각화 ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6), facecolor='white')
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

y = np.arange(len(data))
bar_h = 0.52

# 전체 평균 막대
bars = ax.barh(y, data['전체'], height=bar_h,
               color=bar_colors, alpha=0.88,
               edgecolor='white', linewidth=1.0, zorder=3)

# 침해 집단 점 (원, DARK)
ax.scatter(data['침해'], y, color=DARK, s=60, zorder=5,
           edgecolors='white', linewidths=0.8,
           label='침해 경험 집단 평균')

# 비침해 집단 점 (흰 점)
ax.scatter(data['비침해'], y, color=WHITE, s=60, zorder=5,
           edgecolors=DARK, linewidths=1.0,
           label='침해 미경험 집단 평균')

# 수치 라벨 (막대 오른쪽 — 흰 배경으로 잘림 방지)
for i, row in data.iterrows():
    ax.text(row['전체'] + 0.03, i, f"{row['전체']:.2f}",
            va='center', ha='left', fontsize=10,
            fontweight='bold', color=cat_color[row['cat']],
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                      edgecolor='none', alpha=0.85))

# y축 라벨
ax.set_yticks(y)
ax.set_yticklabels(data['label'], fontsize=10, color=DARK, linespacing=1.35)

# x축 범위·눈금
ax.set_xlim(3.0, 5.25)
ax.set_xticks([3.0, 3.5, 4.0, 4.5, 5.0])
ax.set_xticklabels(['3.0', '3.5', '4.0', '4.5', '5.0'],
                   fontsize=9, color=MUTED)
ax.set_xlabel('정책 필요도 평균 (1=전혀 동의 안 함 ~ 5=매우 동의)',
              fontsize=9, color=MUTED, labelpad=6)

# 기준선 4.5 (높은 동의 수준)
ax.axvline(4.5, color='#CCCCCC', lw=1.2, ls='--', zorder=1)
ax.text(4.51, len(data) - 0.3, '4.5점\n(높은 동의)',
        fontsize=7.5, color=MUTED, va='top')

# 그리드
ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(axis='y', length=0)
ax.tick_params(axis='x', length=0)

# 범례 — 차트 하단 외부, 가로 배치
legend_handles = [
    mpatches.Patch(color=ACCENT, label='법적 제도 공백 해소'),
    mpatches.Patch(color=BLUE1,  label='지원 인프라 확충'),
    mpatches.Patch(color=MUTED,  label='기타 권리 보장'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=DARK,
               markersize=7, label='침해 경험 집단'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=WHITE,
               markeredgecolor=DARK, markersize=7, label='침해 미경험 집단'),
]
ax.legend(handles=legend_handles,
          loc='upper center', bbox_to_anchor=(0.5, -0.13),
          fontsize=8.5, frameon=False, ncol=5)

# 인사이트 텍스트
fig.text(0.5, -0.08,
         '침해 경험 집단은 8개 항목 전체에서 비침해 집단보다 높은 정책 필요도를 인식 — '
         '제도 공백이 침해 당사자에게 더 절실히 체감됨',
         ha='center', fontsize=8.5, color=DARK, fontweight='bold')

# footer
fig.text(0.5, -0.12,
         'D1 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073, n=10,888)  |  '
         '5점 리커트 척도 (정책 동의도)  |  점: 침해/비침해 집단 평균',
         ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout(pad=0.5)
out = BASE + 'output/slide05_Q2_정책필요도.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'저장: {out}')

# 수치 확인 출력
print('\n정책 필요도 상위 8개 (전체 / 침해집단 / 비침해집단):')
for _, row in data.sort_values('전체', ascending=False).iterrows():
    print(f"  {row['var']} {row['전체']:.3f} | 침해:{row['침해']:.3f} 비침해:{row['비침해']:.3f}  [{row['cat']}]")
print('✅ 완료')
