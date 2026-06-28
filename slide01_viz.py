"""
Slide 01 시각화 — 1-1 & 1-2
1-1: 교권침해 실태 현황 (침해 유형별 + 결과 카스케이드)
1-2: 인권교육 역설 (참여율 ↑ vs 심의 건수 ↑)
"""
import pyreadstat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings('ignore')

# ── 한글 폰트 설정 ──────────────────────────────────────────
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

BASE = '/Users/baiohelseu/Desktop/Project/kossda/'

# ── 데이터 로드 ──────────────────────────────────────────────
df, meta = pyreadstat.read_sav(BASE + 'data/교원 인권상황 실태조사,2024/kor_data_20240073.sav')
df3, _   = pyreadstat.read_sav(BASE + 'data/초·중등 교원 인권교육 실태조사, 2021/kor_data_20210019.sav')
N = len(df)

# ── 핵심 수치 계산 ───────────────────────────────────────────
student_viol  = (df['B2_1'] == 1).mean() * 100   # 학생에 의한 침해
parent_viol   = (df['B3_1'] == 1).mean() * 100   # 보호자에 의한 침해
admin_viol    = (df['B5_1'] == 1).mean() * 100   # 관리자에 의한 침해
any_viol_mask = (df['B2_1'] == 1) | (df['B3_1'] == 1) | (df['B5_1'] == 1)
any_viol      = any_viol_mask.mean() * 100

turnover      = (df['A4'] == 1).mean() * 100
suicide       = (df['C4'] == 1).mean() * 100

# 정신건강 나쁨 (C1: 역코딩, 1=매우좋음 5=매우나쁨 → 4,5점)
mental_bad    = (df['C1'] >= 4).mean() * 100

# 인권교육 역설 수치 (D3)
d3_part = (df3['B1'] == 1).mean() * 100  # 2021 참여율

# 외부 통계 (교육부 행정 통계)
edu_timeline = {
    '2020': (1197, None),
    '2021': (2269, d3_part),
    '2022': (3035, None),
    '2023': (5050, 88.2),
}

print(f"전체 침해: {any_viol:.1f}%  학생: {student_viol:.1f}%  보호자: {parent_viol:.1f}%  관리자: {admin_viol:.1f}%")
print(f"이직 고려: {turnover:.1f}%  자살사고: {suicide:.1f}%  정신건강 나쁨: {mental_bad:.1f}%")
print(f"D3 인권교육 참여율(2021): {d3_part:.1f}%")

# ═══════════════════════════════════════════════════════════
#  FIG 1-1: 교권침해 유형별 경험률 (세로 막대, 무채색, 촘촘)
# ═══════════════════════════════════════════════════════════
ACCENT   = '#D62728'
BLUE1    = '#1F77B4'
ORANGE   = '#FF7F0E'
GRAY_BG  = '#F5F5F5'
DARK     = '#1A1A2E'
MUTED    = '#6B6B7B'

GRAY_BAR   = '#7A7A7A'   # 일반 막대 무채색
GRAY_TOTAL = '#2E2E2E'   # 전체 합계 막대 (더 진하게)

fig1, ax_bar = plt.subplots(figsize=(8, 5), facecolor='white')
fig1.patch.set_facecolor('white')
ax_bar.set_facecolor('#FAFAFA')

categories = ['전체\n(1개 이상)', '학생에 의한\n침해', '보호자에 의한\n침해', '관리자에 의한\n침해']
values     = [any_viol, student_viol, parent_viol, admin_viol]
tags       = ['합계', '주요 침해원', '주요 침해원', '주요 침해원']
bar_colors = [GRAY_TOTAL, GRAY_BAR, GRAY_BAR, GRAY_BAR]

x = range(len(categories))
bars = ax_bar.bar(x, values, color=bar_colors,
                  width=0.72, edgecolor='white', linewidth=1.2)

# 수치 라벨 (막대 위)
for bar, val, tag in zip(bars, values, tags):
    is_total = tag == '합계'
    ax_bar.text(bar.get_x() + bar.get_width() / 2, val + 0.8,
                f'{val:.1f}%', ha='center', va='bottom',
                fontsize=13 if is_total else 11,
                fontweight='bold' if is_total else 'normal',
                color=GRAY_TOTAL)

# 범주 태그 (막대 하단 안쪽)
for bar, tag in zip(bars, tags):
    ax_bar.text(bar.get_x() + bar.get_width() / 2, 1.5,
                f'[{tag}]', ha='center', va='bottom',
                fontsize=8, color='white', style='italic')

ax_bar.set_xticks(list(x))
ax_bar.set_xticklabels(categories, fontsize=11, color=DARK, linespacing=1.3)
ax_bar.set_ylabel('경험률 (%)', fontsize=11, color=MUTED, labelpad=6)
ax_bar.set_ylim(0, 100)
ax_bar.tick_params(axis='y', labelsize=10, colors=MUTED)
ax_bar.tick_params(axis='x', length=0)
ax_bar.spines[['top', 'right', 'left']].set_visible(False)
ax_bar.spines['bottom'].set_color('#DDDDDD')
ax_bar.yaxis.grid(True, color='#E8E8E8', linewidth=1, linestyle='--')
ax_bar.set_axisbelow(True)

fig1.suptitle('교권침해 실태 현황', fontsize=15, fontweight='bold',
              color=DARK, y=1.01)
fig1.text(0.5, -0.04,
          '출처: 윤정향, 교원 인권상황 실태조사 2024 (KOSSDA A1-2024-0073) | n=10,888',
          ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout()
out1 = BASE + 'output/slide01_1-1_침해실태.png'
fig1.savefig(out1, dpi=200, bbox_inches='tight', facecolor='white')
print(f"저장: {out1}")
plt.close(fig1)


# ═══════════════════════════════════════════════════════════
#  FIG 1-2: 교권보호위 심의 건수 추이 (1-1과 동일 양식)
# ═══════════════════════════════════════════════════════════
years    = ['2020년', '2021년', '2022년', '2023년']
심의건수  = [1197, 2269, 3035, 5050]
tags2    = ['행정통계', '행정통계', '행정통계', '행정통계']

BLUE_BARS = ['#BDD7EE', '#7FBDE4', '#4A9FD5', '#1F77B4']

fig2, ax2 = plt.subplots(figsize=(8, 5), facecolor='white')
fig2.patch.set_facecolor('white')
ax2.set_facecolor('#FAFAFA')

x2 = range(len(years))
bars2 = ax2.bar(x2, 심의건수, color=BLUE_BARS,
                width=0.72, edgecolor='white', linewidth=1.2)

# 수치 라벨 (막대 위)
for bar, val in zip(bars2, 심의건수):
    ax2.text(bar.get_x() + bar.get_width() / 2, val + 50,
             f'{val:,}건', ha='center', va='bottom',
             fontsize=11, color=DARK)


ax2.set_xticks(list(x2))
ax2.set_xticklabels(years, fontsize=11, color=DARK)
ax2.set_ylabel('심의 건수 (건)', fontsize=11, color=MUTED, labelpad=6)
ax2.set_ylim(0, 6500)
ax2.tick_params(axis='y', labelsize=10, colors=MUTED)
ax2.tick_params(axis='x', length=0)
ax2.spines[['top', 'right', 'left']].set_visible(False)
ax2.spines['bottom'].set_color('#DDDDDD')
ax2.yaxis.grid(True, color='#E8E8E8', linewidth=1, linestyle='--')
ax2.set_axisbelow(True)

fig2.suptitle('교권보호위 심의 건수 추이', fontsize=15, fontweight='bold',
              color=DARK, y=1.01)
fig2.text(0.5, -0.04,
          '출처: 교육부 교권보호위원회 심의 현황(2024)',
          ha='center', fontsize=8, color=MUTED, style='italic')

plt.tight_layout()
out2 = BASE + 'output/slide01_1-2_인권교육역설.png'
fig2.savefig(out2, dpi=200, bbox_inches='tight', facecolor='white')
print(f"저장: {out2}")
plt.close(fig2)

print("\n✅ 1-1, 1-2 생성 완료")
