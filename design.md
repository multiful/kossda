# PPT 시각화 디자인 표준 (KOSSDA 2026 공모전)

> 1-1, 1-2 차트를 기준으로 모든 슬라이드 이미지에 동일하게 적용한다.

---

## 1. 기본 캔버스

| 항목 | 값 |
|---|---|
| `figsize` | `(8, 5)` |
| `dpi` | `200` |
| `facecolor` | `white` (#FFFFFF) |
| 플롯 배경 (`ax.set_facecolor`) | `#FAFAFA` |

---

## 2. 컬러 팔레트

| 변수명 | HEX | 용도 |
|---|---|---|
| `DARK` | `#1A1A2E` | 제목, 수치 라벨, x축 레이블 |
| `MUTED` | `#6B6B7B` | y축 레이블, 출처 텍스트, tick |
| `GRAY_TOTAL` | `#2E2E2E` | 1-1 합계 막대 (강조) |
| `GRAY_BAR` | `#7A7A7A` | 1-1 일반 막대 (무채색) |
| `BLUE_BARS` | `['#BDD7EE','#7FBDE4','#4A9FD5','#1F77B4']` | 시계열 순서형 (연→진) |
| `ACCENT` | `#D62728` | 경고·강조 포인트 (최소 사용) |
| `ORANGE` | `#FF7F0E` | 보조 데이터 계열 |

---

## 3. 막대 차트 공통 설정

```python
width       = 0.72          # 막대 너비 (bar-gap 일정)
edgecolor   = 'white'
linewidth   = 1.2
```

---

## 4. 축 스타일

```python
# 스파인 (테두리)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')

# 그리드 (y축만)
ax.yaxis.grid(True, color='#E8E8E8', linewidth=1, linestyle='--')
ax.set_axisbelow(True)

# tick
ax.tick_params(axis='x', length=0)                     # x: 눈금선 없음
ax.tick_params(axis='y', labelsize=10, colors=MUTED)   # y: 연한 색
ax.set_xticklabels(..., fontsize=11, color=DARK)
```

---

## 5. 수치 라벨 (막대 위)

```python
# 일반
ax.text(x, val + offset, f'{val}', ha='center', va='bottom',
        fontsize=11, color=DARK)

# 강조 (합계/최대값)
ax.text(x, val + offset, f'{val}', ha='center', va='bottom',
        fontsize=13, fontweight='bold', color=DARK)
```

---

## 6. 절대 금지 사항

- **막대 내부에 텍스트 절대 금지** — [태그], 라벨, 설명 등 막대 안쪽에 글씨 쓰지 않음
- **화살표·annotate 절대 금지** — 강조 화살표(→), 곡선 화살표, annotate() 사용 금지
- **텍스트 잘림 금지** — xlim/ylim은 모든 라벨이 들어갈 여백을 확보할 것; bbox_inches='tight' 필수
- **불필요한 복잡성 금지** — 색상 3종 이하, 범례 항목 최소화; 5색 diverging·이중 축·그라데이션 피할 것
- 강조가 필요하면 **색상 차이(GRAY_TOTAL vs GRAY_BAR)** 또는 **수치 라벨 bold** 처리로 대체

## 7. 범주 태그 (막대 안쪽 하단 — 사용 안 함)

```python
ax.text(x, 1.5, f'[{tag}]', ha='center', va='bottom',
        fontsize=8, color='white', style='italic')
```
> 태그가 데이터 설명에 불필요하면 생략 (1-2처럼)

---

## 7. 제목 & 출처

```python
# 제목 — 짧고 명확하게 (10자 내외)
fig.suptitle('제목', fontsize=15, fontweight='bold', color=DARK, y=1.01)

# 출처 — 하단 중앙, 작게
fig.text(0.5, -0.04,
         '출처: ...', ha='center', fontsize=8, color=MUTED, style='italic')
```

---

## 8. 저장

```python
fig.savefig('output/slide##_#-#_이름.png',
            dpi=200, bbox_inches='tight', facecolor='white')
```

파일명 규칙: `slide{슬라이드번호}_{차트번호}_{내용설명}.png`
예) `slide01_1-1_침해실태.png`, `slide02_2-1_문제제기.png`

---

## 9. 폰트 로드 (스크립트 최상단 공통)

```python
import matplotlib.font_manager as fm
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
```
