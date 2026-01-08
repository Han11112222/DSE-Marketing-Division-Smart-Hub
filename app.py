import streamlit as st

# 페이지 기본 설정 (전체 화면 사용)
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

# HTML/CSS 디자인 코드를 파이썬 문자열로 담기
html_design = """
<style>
    /* 전체 폰트 및 스타일 설정 */
    body {
        font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
        color: #333;
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 30px;
        color: #2c3e50;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* 섹션 헤더 (Key Support 등) */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1e40af; /* 파란색 텍스트 */
        margin-top: 30px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* 파란색 구분선 */
    .divider-top {
        border-top: 2px solid #1e40af;
        margin-bottom: 0;
    }

    /* 리스트 한 줄 스타일 */
    .list-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 10px;
        border-bottom: 1px solid #e5e7eb; /* 연한 회색 줄 */
    }

    /* 텍스트 영역 */
    .content-area {
        flex: 3;
        font-size: 15px;
    }
    .content-title {
        font-weight: 700;
        margin-right: 5px;
    }
    .content-desc {
        color: #555;
        font-size: 14px;
    }

    /* 별점 영역 */
    .star-rating {
        flex: 1;
        text-align: center;
        font-size: 14px;
        letter-spacing: 2px;
        color: #333;
    }

    /* 링크 버튼 영역 */
    .link-area {
        flex: 1;
        text-align: right;
    }
    .link-btn {
        display: inline-block;
        padding: 6px 20px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        background-color: white;
        text-decoration: none;
        color: #555;
        font-size: 13px;
        transition: background-color 0.2s;
    }
    .link-btn:hover {
        background-color: #f3f4f6;
    }
    
    .folder-icon { color: #fbbf24; }
</style>

<div class="main-title">
    🔥 마케팅팀 _ Smart Marketing Hub
</div>

<div class="section-header">
    <span class="folder-icon">📂</span> Key Support
</div>
<div class="divider-top"></div>

<div class="list-row">
    <div class="content-area">
        <span class="content-title">공동주택 지도 시각화 Dashboard :</span>
        <span class="content-desc">공동주택, 지역난방 시각화, 판매량 비교 등</span>
    </div>
    <div class="star-rating">★★★★★</div>
    <div class="link-area"><a href="#" class="link-btn">Link 🔗</a></div>
</div>

<div class="list-row">
    <div class="content-area">
        <span class="content-title">판매량분석(full ver) :</span>
        <span class="content-desc">고객명별, 상품별 전년동월대비 판매량분석</span>
    </div>
    <div class="star-rating">★★★★★</div>
    <div class="link-area"><a href="#" class="link-btn">Link 🔗</a></div>
</div>

<div class="list-row">
    <div class="content-area">
        <span class="content-title">판매량분석(simple ver) :</span>
        <span class="content-desc">상품별, 산업용, 일반용(업종별, 고객별 분석 등)</span>
    </div>
    <div class="star-rating">★★★★</div>
    <div class="link-area"><a href="#" class="link-btn">Link 🔗</a></div>
</div>

<div class="list-row">
    <div class="content-area">
        <span class="content-title">일 공급량 실적관리 :</span>
        <span class="content-desc">일일계획 및 실적관리, 랭킹관리, 기온 구간평 공급량 분석 등</span>
    </div>
    <div class="star-rating">★★★★★</div>
    <div class="link-area"><a href="#" class="link-btn">Link 🔗</a></div>
</div>

<div class="list-row">
    <div class="content-area">
        <span class="content-title">입주율 분석 Dashboard :</span>
        <span class="content-desc">입주율 저조 단지, 계획대비 실적 분석 등</span>
    </div>
    <div class="star-rating">★★★</div>
    <div class="link-area"><a href="#" class="link-btn">Link 🔗</a></div>
</div>

<div class="list-row">
    <div class="content-area">
        <span class="content-title">뉴스 모니터링 (Client) :</span>
        <span class="content-desc">대성에너지 주요 고객 뉴스 모니터링(중대재해 등)</span>
    </div>
    <div class="star-rating">★★★</div>
    <div class="link-area"><a href="#" class="link-btn">Link 🔗</a></div>
</div>

<div class="section-header" style="margin-top: 50px;">
    <span class="folder-icon">📂</span> 모니터링(Monitoring)
</div>
<div class="divider-top"></div>
"""

# Streamlit에 HTML 렌더링 (unsafe_allow_html=True 필수)
st.markdown(html_design, unsafe_allow_html=True)
