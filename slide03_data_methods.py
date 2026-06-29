"""
슬라이드 03 — 데이터 선택 및 분석방법 v3
5개 데이터셋 전체 반영 / Brunner-Munzel Q3 이동
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
STRIPE='#16182C'

fig = plt.figure(figsize=(16, 9), facecolor=DARK)
ax  = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis('off')

# ── TITLE ────────────────────────────────────────────────────────
ax.text(0.55, 8.78, '3.', fontsize=24, fontweight='bold', color=ACCENT, va='center')
ax.text(1.25, 8.78, '데이터 선택 및 분석방법',
        fontsize=20, fontweight='bold', color=WHITE, va='center')
ax.add_patch(patches.Rectangle((0.5, 8.56), 15.0, 0.03, facecolor='#2C2C50'))

# ── QUESTION BOXES ───────────────────────────────────────────────
for qnum, qtxt, qc, qx in [
    ('Q1', '어떤 학교 구조의 교사가\n더 취약한가?',           BLUE1,  0.50),
    ('Q2', '교권침해를 유발하는\n잠재적 요인은 무엇인가?',     ACCENT, 5.63),
    ('Q3', '어떤 제도가 교권침해를\n실제로 예방할 수 있는가?', GREEN,  10.76),
]:
    ax.add_patch(FancyBboxPatch((qx, 7.72), 4.86, 0.76,
                                boxstyle='round,pad=0.06',
                                facecolor=qc, alpha=0.18, edgecolor=qc, linewidth=2.0))
    ax.add_patch(FancyBboxPatch((qx+0.08, 7.78), 0.60, 0.64,
                                boxstyle='round,pad=0.04', facecolor=qc, alpha=0.90))
    ax.text(qx+0.38, 8.10, qnum, fontsize=13, fontweight='bold',
            color=WHITE, ha='center', va='center')
    ax.text(qx+0.86, 8.10, qtxt, fontsize=10, color=WHITE,
            va='center', linespacing=1.5)

# ── SECTION 1: 데이터 소개 ───────────────────────────────────────
ax.text(0.55, 7.50, '① 데이터 소개', fontsize=11, fontweight='bold',
        color=WHITE, va='top')
ax.add_patch(patches.Rectangle((0.5, 7.36), 15.0, 0.028, facecolor='#2C2C50'))

THY, THH = 7.34, 0.28
ax.add_patch(patches.Rectangle((0.5, THY-THH), 15.0, THH, facecolor='#203060'))

# Columns: (x, w, label, align)
TC = [(0.52, 3.00, '데이터명',         'left'),
      (3.55, 2.10, '제공 출처',         'left'),
      (5.68, 5.95, '주요 사용 변수',    'left'),
      (11.66, 1.50, '표본',             'center'),
      (13.19, 0.68, 'Q1',              'center'),
      (13.90, 0.68, 'Q2',              'center'),
      (14.61, 0.68, 'Q3',              'center')]

for cx, cw, cl, ca in TC:
    xp = cx + cw/2 if ca == 'center' else cx + 0.08
    ax.text(xp, THY-THH/2, cl, fontsize=9, fontweight='bold',
            color=WHITE, ha=ca, va='center')

RH = 0.48
N_ROWS = 5
for cx, cw, *_ in TC[1:]:
    ax.add_patch(patches.Rectangle((cx-0.04, THY-THH-N_ROWS*RH), 0.03,
                                   THH+N_ROWS*RH, facecolor='#22224A'))

rows = [
    dict(name='D1  교원 인권상황 실태조사\n      (KOSSDA, 2024)',
         src='KOSSDA\nA1-2024-0073',
         var='B2_1·B3_1·B5_1 (침해), SQ2·4·5·8·9 (학교 구조)\nA1_12·13·C6_8·B8_1 (제도공백), D2_2·5·10·16 (수요)',
         n='n=10,888', q1=BLUE1, q2=ACCENT, q3=GREEN),
    dict(name='D3  초·중등 교원 인권교육\n      실태조사 (KOSSDA, 2021)',
         src='KOSSDA\nA1-2021-0019',
         var='B1 (인권교육 참여), B2_6 (교육 효과 만족도)\nB5_7 (학생인권 대비 교권 하락 인식)',
         n='n=9,553', q1=BLUE1, q2=None, q3=None, q1n='맥락'),
    dict(name='D2  예비교원 인권 인식조사\n      (KOSSDA, 2023)',
         src='KOSSDA\nA1-2023-0036',
         var='Q4_1 (학생 인권 존중도)\nQ4_2 (교사 인권 존중도)',
         n='n=1,002', q1=None, q2=None, q3=GREEN, q3n='보완'),
    dict(name='교권보호위원회 개최 현황\n      (교육부, 2024)',
         src='교육부\n교권보호위원회\n개최현황_20240229',
         var='학교급, 심의 건수(%), 모욕·명예훼손\n교육활동 반복·부당 간섭 (22.7%)',
         n='전국\n2020-2023', q1=BLUE1, q2=None, q3=None, q1n='맥락'),
    dict(name='교원 교권상담 실적\n      (한국교총, 2018)',
         src='한국교총\n교총_교권상담실적.xlsx',
         var='침해 주체 5종, 행위유형 (학생지도간섭·명예훼손)\n학교급·시도별',
         n='n=501건', q1=BLUE1, q2=None, q3=None, q1n='맥락'),
]

for ri, rd in enumerate(rows):
    ry = THY - THH - ri * RH
    cy = ry - RH / 2
    bg = CARD if ri % 2 == 0 else STRIPE
    ax.add_patch(patches.Rectangle((0.5, ry-RH), 15.0, RH, facecolor=bg))

    ax.text(TC[0][0]+0.08, cy, rd['name'], fontsize=8.5, color=WHITE,
            va='center', linespacing=1.3)
    ax.text(TC[1][0]+0.08, cy, rd['src'],  fontsize=7.5, color=MUTED,
            va='center', linespacing=1.25)
    ax.text(TC[2][0]+0.08, cy, rd['var'],  fontsize=7.8, color=LGRAY,
            va='center', linespacing=1.3)
    n_cx = TC[3][0] + TC[3][1]/2
    ax.text(n_cx, cy, rd['n'], fontsize=8, fontweight='bold',
            color=WHITE, ha='center', va='center', linespacing=1.2)

    for qk, tc in [('q1', TC[4]), ('q2', TC[5]), ('q3', TC[6])]:
        qc = rd.get(qk)
        qn = rd.get(qk+'n', '')
        qcx = tc[0] + tc[1]/2
        if qc:
            ax.add_patch(plt.Circle((qcx, cy), 0.16, color=qc, alpha=0.9, zorder=5))
            lbl = qn[:2] if qn else 'v'
            ax.text(qcx, cy, lbl, fontsize=6.5, fontweight='bold',
                    color=WHITE, ha='center', va='center', zorder=6)
        else:
            ax.add_patch(plt.Circle((qcx, cy), 0.13, fill=False,
                                   edgecolor='#303060', linewidth=1.2, zorder=5))

# ── SECTION 2: 분석기법 ──────────────────────────────────────────
S2Y = THY - THH - N_ROWS * RH - 0.10
ax.text(0.55, S2Y, '② 분석기법', fontsize=11, fontweight='bold',
        color=WHITE, va='top')
ax.add_patch(patches.Rectangle((0.5, S2Y-0.14), 15.0, 0.028, facecolor='#2C2C50'))

MY  = S2Y - 0.22
BH  = 0.80
BSP = 0.08

mdata = [
    (BLUE1, 'Q1', [
        ('이분형 로지스틱 회귀',  '구조적 변수를 통한 취약집단 회귀 분석', 'Pooled OR — 악성민원 2.49 [2.17-2.85]'),
        ('RandomForest + SHAP', '구조변수 기여도 측정',                  '변수 중요도 — 학교급·학급규모 상위'),
        ('K-means 군집분석',     '집단별 침해 프로파일링',                'k=3,  Silhouette=0.312 — 초등복합 71%'),
    ]),
    (ACCENT, 'Q2', [
        ('CFA (확인적 요인 분석)', 'SEM 측정모형 적합도 검증',               'CFI=0.917,  RMSEA=0.070'),
        ('Cronbach alpha',        '제도공백 잠재변수 4지표 내적 일관성',     'alpha=0.741'),
        ('SEM 구조방정식',         '인과 경로 검증 및 잠재요인 분석',         '제도공백 -> 침해지수  beta=0.454'),
        ('Bootstrap 매개효과',    'SEM 간접효과 신뢰구간 추정',              '이직 28%,  자살사고 40%'),
    ]),
    (GREEN, 'Q3', [
        ('Brunner-Munzel test',   '등분산 가정 없는 제도공백 통계 검증',     'p<.001 — 침해/비침해 집단 차이'),
        ('Mann-Whitney U 검정',   '침해·비침해 집단 정책 수요 격차 비교',    '4개 제도 전체 p<.001  악성민원 delta=+0.13'),
        ('PAF 시뮬레이션',         '인구기여위험분율로 제도 도입 효과 추정',  '악성민원 60% 정착 -> 보호자침해 -21.3%p'),
    ]),
]

MXS = [0.50, 5.63, 10.76]
MW  = 4.86

for (qc, qnum, meths), mx in zip(mdata, MXS):
    ax.add_patch(FancyBboxPatch((mx, MY-0.30), MW, 0.30,
                                boxstyle='round,pad=0.04',
                                facecolor=qc, alpha=0.85))
    ax.text(mx+MW/2, MY-0.15, qnum, fontsize=11, fontweight='bold',
            color=WHITE, ha='center', va='center')

    for mi, (mn, md1, md2) in enumerate(meths):
        by = MY - 0.30 - (BH+BSP)*(mi+1)
        ax.add_patch(FancyBboxPatch((mx, by), MW, BH,
                                    boxstyle='round,pad=0.04',
                                    facecolor=CARD, edgecolor=qc,
                                    linewidth=0.8, alpha=0.95))
        ax.add_patch(patches.Rectangle((mx, by), 0.09, BH,
                                       facecolor=qc, alpha=0.85))
        ax.text(mx+0.20, by+BH*0.76, mn,  fontsize=9.5, fontweight='bold',
                color=qc, va='center')
        ax.text(mx+0.20, by+BH*0.48, md1, fontsize=8.5, color=LGRAY, va='center')
        ax.text(mx+0.20, by+BH*0.20, md2, fontsize=7.5, color=MUTED,
                va='center', style='italic')

# Footer
ax.text(8.0, 0.15,
        'D1: KOSSDA A1-2024-0073 (n=10,888)  ·  D2: KOSSDA A1-2023-0036 (n=1,002)  ·  '
        'D3: KOSSDA A1-2021-0019 (n=9,553)  ·  분석도구: Python (semopy · scikit-learn · scipy · statsmodels)',
        fontsize=7.5, color=MUTED, ha='center', va='center', style='italic')

out = '/Users/baiohelseu/Desktop/Project/kossda/output/slide03_data_methods.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor=DARK)
plt.close()
print(f'저장: {out}')
print('완료')
