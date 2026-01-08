import streamlit as st
import pandas as pd
import os

# --------------------------------------------------------------------------
# 1. 페이지 설정 및 디자인 (CSS)
# --------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

# CSS 스타일 정의
st.markdown("""
<style>
    /* 폰트 및 기본 설정 */
    body { font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; color: #333; }
    
    /* 메인 타이틀 */
    .main-title {
        font-size: 28px; font-weight: 800; margin-bottom: 30px;
        color: #2c3e50; display: flex; align-items: center; gap: 10px;
    }

    /* 섹션 헤더 (Key Support, 모니터링 등) */
    .section-header {
        font-size: 18px; font-weight: 700; color: #1e40af;
        margin-top: 40px; margin-bottom: 10px;
        display: flex; align-items: center; gap: 8px;
    }
    
    /* 구분선 */
    .divider-top { border-top: 2px solid #1e40af; margin-bottom: 0; }

    /* 리스트 아이템 행 */
    .list-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 10px; border-bottom: 1px solid #e5e7eb;
    }

    /* 텍스트 영역 */
    .content-area { flex: 3; font-size: 15px; }
    .content-title { font-weight: 700; margin-right: 5px; }
    .content-desc { color: #555; font-size: 14px; }

    /* 별점 영역 */
    .star-rating {
        flex: 1; text-align: center; font-size: 14px; letter-spacing: 2px; color: #333;
    }

    /* 링크 버튼 */
    .link-area { flex: 1; text-align: right; }
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

# --------------------------------------------------------------------------
# 2. 데이터 불러오기 및 처리 함수
# --------------------------------------------------------------------------
def load_data():
    # 파일명은 실제 엑셀 파일명으로 수정해주세요 (예: marketing_hub.xlsx)
    # 여기서는 csv로 가정하고 작성했지만, xlsx라면 pd.read_excel('파일명.xlsx') 사용
    try:
        # Han형님이 업로드하신 파일명을 기준으로 로드합니다.
        # 실제 환경에서는 'marketing_hub.xlsx' 또는 'marketing_hub.csv'로 맞춰주세요.
        df = pd.read_csv('marketing_hub.xlsx - Sheet1.csv') 
        return df
    except Exception as e:
        st.error(f"데이터 파일을 찾을 수 없습니다. (에러: {e})")
        return pd.DataFrame()

def make_stars(score):
    """숫자(1~5)를 받아서 별 문자열(★★★★★)로 변환"""
    try:
        score = int(score)
        return "★" * score
    except:
        return "☆☆☆☆☆" # 에러 시 빈 별

# --------------------------------------------------------------------------
# 3. 메인 화면 그리기
# --------------------------------------------------------------------------

# 타이틀 출력
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

# 데이터 로드
df = load_data()

if not df.empty:
    # '구분' 컬럼에 있는 값들(Key Support, Monitoring 등)을 기준으로 그룹을 나눕니다.
    # 엑셀의 순서를 유지하기 위해 unique() 사용
    categories = df['구분'].unique()

    for category in categories:
        # 1. 섹션 헤더 출력
        st.markdown(f"""
            <div class="section-header">
                <span class="folder-icon">📂</span> {category}
            </div>
            <div class="divider-top"></div>
        """, unsafe_allow_html=True)

        # 2. 해당 섹션에 속하는 데이터만 필터링
        section_data = df[df['구분'] == category]

        # 3. 각 행(Row)을 돌면서 리스트 출력
        for index, row in section_data.iterrows():
            title = row['내용']      # 엑셀 컬럼명 '내용' (업무명)
            desc = "" # 설명이 엑셀에 따로 없다면 비워둠, 있다면 row['설명']
            
            # 별점 변환 (숫자 -> 별)
            stars = make_stars(row['활용도']) 
            
            link = row['Link'] if 'Link' in row else '#' # 링크 컬럼 확인

            # HTML 생성 및 출력
            st.markdown(f"""
            <div class="list-row">
                <div class="content-area">
                    <span class="content-title">{title}</span>
                    <span class="content-desc">{desc}</span>
                </div>
                <div class="star-rating">{stars}</div>
                <div class="link-area"><a href="{link}" target="_blank" class="link-btn">Link 🔗</a></div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("엑셀 파일을 같은 폴더에 넣어주세요.")
