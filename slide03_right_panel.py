"""
슬라이드 03 우측 패널: 분석 흐름도 + 데이터 전처리 + 핵심 수치
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings('ignore')

for fp in ['/Library/Fonts/NanumGothicBold.ttf',
           '/Library/Fonts/NanumGothic.ttf',
           '/System/Library/Fonts/Supplemental/AppleGothic.ttf']:
    try:
        fm.fontManager.addfont(fp)
        plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
        break
    except: pass
plt.rcParams['axes.unicode_minus'] = False

DARK='#1A1A2E'; CARD='#1E2040'; ACCENT='#D62728'; BLUE1='#1F77B4'
GREEN='#2CA02C'; MUTED='#8888AA'; WHITE='#FFFFFF'; LGRAY='#B8B8CC'

fig = plt.figure(figsize=(8.5, 10), facecolor=DARK)
ax  = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 8.5); ax.set_ylim(0, 10); ax.axis('off')

# ═══ SECTION 1: 분석 흐름도 ════════════════════════════════════
ax.text(0.28, 9.80, '① 분석 흐름도', fontsize=11, fontweight='bold',
        color=WHITE, va='top')
ax.add_patch(patches.Rectangle((0.28, 9.60), 8.0, 0.03, facecolor='#2C2C50'))

# (데이터텍스트, 데이터색, Q텍스트, Q색, 결과텍스트, 중심Y)
BH = 0.72
DX, DW = 0.28, 1.62
QX, QW = 2.14, 1.92
RX, RW = 4.26, 3.96

flow = [
    ('배경 데이터\n(교육부·교총·D3)',  MUTED,  'Q1\n구조 취약성', BLUE1,  '취약집단 3군집\n초등복합 71%', 8.82),
    ('D1  n=10,888',                   BLUE1,  'Q2\n잠재요인',    ACCENT, '제도공백\nbeta=0.454',        7.62),
    ('D1 + D2',                        GREEN,  'Q3\n예방 제도',   GREEN,  'PAF\n-21.3%p',               6.42),
]

for dtxt, dc, qtxt, qc, rtxt, cy in flow:
    ax.add_patch(FancyBboxPatch((DX, cy-BH/2), DW, BH,
                                boxstyle='round,pad=0.05',
                                facecolor=dc, alpha=0.18, edgecolor=dc, linewidth=1.5))
    ax.text(DX+DW/2, cy, dtxt, fontsize=8.5, color=WHITE,
            ha='center', va='center', linespacing=1.35)
    ax.annotate('', xy=(QX-0.07, cy), xytext=(DX+DW+0.05, cy),
                arrowprops=dict(arrowstyle='->', color=dc, lw=2.0))
    ax.add_patch(FancyBboxPatch((QX, cy-BH/2), QW, BH,
                                boxstyle='round,pad=0.05', facecolor=qc, alpha=0.88))
    ax.text(QX+QW/2, cy, qtxt, fontsize=10, color=WHITE,
            ha='center', va='center', fontweight='bold', linespacing=1.4)
    ax.annotate('', xy=(RX-0.07, cy), xytext=(QX+QW+0.05, cy),
                arrowprops=dict(arrowstyle='->', color=qc, lw=2.0))
    ax.add_patch(FancyBboxPatch((RX, cy-BH/2), RW, BH,
                                boxstyle='round,pad=0.05',
                                facecolor=CARD, edgecolor=qc, linewidth=1.8))
    ax.text(RX+RW/2, cy, rtxt, fontsize=10, color=WHITE,
            ha='center', va='center', fontweight='bold', linespacing=1.4)

# 수직 ↓ 화살표 (Q박스 사이)
QCX = QX + QW/2
for (_, _, _, _, _, y1), (_, _, _, _, _, y2) in zip(flow[:-1], flow[1:]):
    ax.annotate('', xy=(QCX, y2+BH/2+0.07), xytext=(QCX, y1-BH/2-0.07),
                arrowprops=dict(arrowstyle='->', color='#6677AA', lw=2.0))

# ═══ SECTION 2: 데이터 전처리 ══════════════════════════════════
S2Y = 5.72
ax.text(0.28, S2Y+0.22, '② 데이터 전처리', fontsize=11, fontweight='bold',
        color=WHITE, va='top')
ax.add_patch(patches.Rectangle((0.28, S2Y), 8.0, 0.03, facecolor='#2C2C50'))

preps = [
    (BLUE1,  '결측 처리',         '기준 분석 변수 리스트와이즈 제거  /  제도수요 무응답 별도 처리'),
    (BLUE1,  '이상치 처리',        '연속형 변수 3표준편차(σ) 이상 극단값 제거'),
    (ACCENT, '침해지수 생성',      'B2_1 + B3_1 + B5_1 합산  (0~3점 척도)'),
    (ACCENT, '제도공백 잠재변수',  'A1_12·A1_13·C6_8·B8_1 역코딩 후 평균  (Cronbach a=0.741)'),
    (GREEN,  'K-means 전처리',    '군집 투입 변수 StandardScaler 표준화  (k=3, Silhouette=0.312)'),
]

for i, (sc, step, desc) in enumerate(preps):
    py = S2Y - 0.30 - i * 0.48
    ax.add_patch(plt.Circle((0.57, py), 0.17, color=sc, alpha=0.85, zorder=5))
    ax.text(0.57, py, str(i+1), fontsize=8, fontweight='bold',
            color=WHITE, ha='center', va='center', zorder=6)
    ax.text(0.88, py+0.10, step, fontsize=9.5, fontweight='bold', color=sc, va='center')
    ax.text(0.88, py-0.10, desc, fontsize=8, color=LGRAY, va='center')

# ═══ SECTION 3: 핵심 수치 미리보기 ════════════════════════════
S3Y = 2.55
ax.text(0.28, S3Y+0.22, '③ 핵심 분석 수치 미리보기', fontsize=11, fontweight='bold',
        color=WHITE, va='top')
ax.add_patch(patches.Rectangle((0.28, S3Y), 8.0, 0.03, facecolor='#2C2C50'))

kpis = [
    (BLUE1,  'Q1', [('악성민원 OR',    '2.49'),      ('초등복합 비중',  '71%')]),
    (ACCENT, 'Q2', [('제도공백 beta',  '0.454'),     ('Cronbach a',   '0.741')]),
    (GREEN,  'Q3', [('보호자침해 PAF', '-21.3%p'),   ('수요 격차',    'D=+0.13')]),
]
KXS = [0.28, 3.08, 5.88]
KW  = 2.40
KHH = 0.34   # Q header height
KHI = 0.50   # KPI item height
GAP = 0.07

for (qc, qnum, items), kx in zip(kpis, KXS):
    ky = S3Y - 0.10
    ax.add_patch(FancyBboxPatch((kx, ky-KHH), KW, KHH,
                                boxstyle='round,pad=0.04', facecolor=qc, alpha=0.85))
    ax.text(kx+KW/2, ky-KHH/2, qnum, fontsize=11, fontweight='bold',
            color=WHITE, ha='center', va='center')
    for ki, (kname, kval) in enumerate(items):
        iy = ky - KHH - GAP - ki*(KHI+GAP)
        ax.add_patch(FancyBboxPatch((kx, iy-KHI), KW, KHI,
                                    boxstyle='round,pad=0.04',
                                    facecolor=CARD, edgecolor=qc, linewidth=0.8))
        ax.text(kx+KW/2, iy-KHI*0.34, kval, fontsize=13, fontweight='bold',
                color=qc, ha='center', va='center')
        ax.text(kx+KW/2, iy-KHI*0.76, kname, fontsize=7.5, color=MUTED,
                ha='center', va='center')

# Footer
ax.text(4.25, 0.22,
        '분석도구: Python  (semopy · scikit-learn · scipy · statsmodels · matplotlib)',
        fontsize=7.5, color=MUTED, ha='center', va='center', style='italic')

out = '/Users/baiohelseu/Desktop/Project/kossda/output/slide03_right_panel.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor=DARK)
plt.close()
print(f'저장: {out}')
