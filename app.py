import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

# 2. 디자인(CSS) 설정 - Han형님이 만족하셨던 그 디자인 그대로입니다.
st.markdown("""
<style>
    /* 기본 폰트 설정 */
    body { font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; color: #333; }
    
    /* 메인 타이틀 */
    .main-title {
        font-size: 28px; font-weight: 800; margin-bottom: 30px;
        color: #2c3e50; display: flex; align-items: center; gap: 10px;
    }

    /* 섹션 헤더 (Key Support 등) */
    .section-header {
        font-size: 18px; font-weight: 700; color: #1e40af;
        margin-top: 40px; margin-bottom: 15px;
        display: flex; align-items: center; gap: 8px;
    }
    
    /* 파란색 구분선 */
    .divider-top { border-top: 2px solid #1e40af; margin-bottom: 0; }

    /* 리스트 한 줄 스타일 */
    .list-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 10px; border-bottom: 1px solid #e5e7eb;
    }

    /* 내용 영역 */
    .content-area { flex: 3; font-size: 15px; }
    .content-title { font-weight: 700; margin-right: 5px; }
    .content-desc { color: #555; font-size: 14px; }

    /* 별점 영역 */
    .star-rating { flex: 0.5; text-align: center; font-size: 14px; letter-spacing: 2px; color: #333; }

    /* 링크 버튼 영역 */
    .link-area { flex: 0.5; text-align: right; }
    .link-btn {
        display: inline-block; padding: 6px 20px;
        border: 1px solid #d1d5db; border-radius: 6px;
        background-color: white; text-decoration: none; color: #555;
        font-size: 13px; transition: background-color 0.2s;
    }
    .link-btn:hover { background-color: #f3f4f6; }
    
    .folder-icon { color: #fbbf24; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 준비 (엑셀 파일 없이도 돌아가도록 데이터를 여기에 넣었습니다)
# 나중에 엑셀이 확실히 연결되면 이 부분을 pd.read_excel로 바꾸면 됩니다.
data = [
    # Key Support 섹션 데이터
    {"category": "Key Support", "title": "공동주택 지도 시각화 Dashboard", "desc": "공동주택, 지역난방 시각화, 판매량 비교 등", "stars": 5, "link": "#"},
    {"category": "Key Support", "title": "판매량분석(full ver)", "desc": "고객명별, 상품별 전년동월대비 판매량분석", "stars": 5, "link": "#"},
    {"category": "Key Support", "title": "판매량분석(simple ver)", "desc": "상품별, 산업용, 일반용(업종별, 고객별 분석 등)", "stars": 4, "link": "#"},
    {"category": "Key Support", "title": "일 공급량 실적관리", "desc": "일일계획 및 실적관리, 랭킹관리, 기온 구간평 공급량 분석 등", "stars": 5, "link": "#"},
    {"category": "Key Support", "title": "입주율 분석 Dashboard", "desc": "입주율 저조 단지, 계획대비 실적 분석 등", "stars": 3, "link": "#"},
    {"category": "Key Support", "title": "뉴스 모니터링 (Client)", "desc": "대성에너지 주요 고객 뉴스 모니터링(중대재해 등)", "stars": 3, "link": "#"},
    
    # Monitoring 섹션 데이터 (여기에 추가하면 화면 아래에 계속 생깁니다)
    {"category": "모니터링(Monitoring)", "title": "실시간 공급 현황", "desc": "권역별 실시간 공급 압력 및 유량 모니터링", "stars": 5, "link": "#"},
    {"category": "모니터링(Monitoring)", "title": "VOC 현황판", "desc": "고객 민원 접수 및 처리 현황 실시간 조회", "stars": 4, "link": "#"},
]

# 4. 화면에 그리기 (로직)
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

# 데이터를 카테고리별로 묶어서 출력
categories = []
for item in data:
    if item["category"] not in categories:
        categories.append(item["category"])

for category in categories:
    # 섹션 헤더 출력
    st.markdown(f"""
        <div class="section-header">
            <span class="folder-icon">📂</span> {category}
        </div>
        <div class="divider-top"></div>
    """, unsafe_allow_html=True)

    # 해당 카테고리의 아이템들 출력
    for item in data:
        if item["category"] == category:
            star_mark = "★" * item["stars"]
            st.markdown(f"""
            <div class="list-row">
                <div class="content-area">
                    <span class="content-title">{item['title']} :</span>
                    <span class="content-desc">{item['desc']}</span>
                </div>
                <div class="star-rating">{star_mark}</div>
                <div class="link-area"><a href="{item['link']}" class="link-btn">Link 🔗</a></div>
            </div>
            """, unsafe_allow_html=True)

    # 섹션 간 간격 띄우기
    st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)
