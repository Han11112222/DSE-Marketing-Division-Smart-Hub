import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

# 2. 디자인(CSS) - Han형님이 원하시던 그 디자인
st.markdown("""
<style>
    body { font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; color: #333; }
    
    .main-title {
        font-size: 28px; font-weight: 800; margin-bottom: 30px;
        color: #2c3e50; display: flex; align-items: center; gap: 10px;
    }
    
    .section-header {
        font-size: 18px; font-weight: 700; color: #1e40af;
        margin-top: 40px; margin-bottom: 10px;
        display: flex; align-items: center; gap: 8px;
    }
    
    .divider-top { border-top: 2px solid #1e40af; margin-bottom: 0; }

    .list-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 10px; border-bottom: 1px solid #e5e7eb;
    }

    .content-area { flex: 3; font-size: 15px; }
    .content-title { font-weight: 700; margin-right: 5px; }
    .content-desc { color: #555; font-size: 14px; }

    .star-rating { flex: 0.5; text-align: center; font-size: 14px; letter-spacing: 2px; color: #333; }

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

# 3. 데이터 로드 함수 (엑셀 파일 읽기)
def load_data():
    file_name = 'marketing_hub.xlsx' # Han형님 파일명
    
    if os.path.exists(file_name):
        try:
            # 엑셀 파일 읽기
            df = pd.read_excel(file_name) 
            # 데이터 전처리: 비어있는 값은 빈 문자열로 채움
            df = df.fillna("")
            return df
        except Exception as e:
            st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
            return pd.DataFrame()
    else:
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. app.py와 같은 폴더에 엑셀 파일을 넣어주세요.")
        return pd.DataFrame()

# 별점 생성 함수
def make_stars(score):
    try:
        # 엑셀에서 숫자가 아닌 값이 들어올 경우를 대비
        if score == "": return "☆☆☆☆☆"
        score = int(float(score)) # 소수점이 있을 경우 정수로 변환
        return "★" * score
    except:
        return "☆☆☆☆☆"

# 4. 메인 화면 출력
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # '구분' 컬럼의 순서를 유지하며 가져오기 (엑셀에 적힌 순서대로)
    categories = df['구분'].unique()

    for category in categories:
        # 섹션 헤더 (Key Support, Monitoring 등)
        st.markdown(f"""
            <div class="section-header">
                <span class="folder-icon">📂</span> {category}
            </div>
            <div class="divider-top"></div>
        """, unsafe_allow_html=True)

        # 해당 카테고리의 데이터만 필터링
        section_data = df[df['구분'] == category]

        # 각 줄 출력
        for index, row in section_data.iterrows():
            title = row['내용']
            # 엑셀에 '설명' 컬럼이 없으면 빈칸, 있으면 표시
            desc = row['설명'] if '설명' in row else "" 
            stars = make_stars(row['활용도'])
            link = row['Link'] if row['Link'] != "" else "#"

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
        
        # 섹션 간 여백
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
