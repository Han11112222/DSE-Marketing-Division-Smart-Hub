import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="마케팅팀 _ Smart Marketing Hub",
    page_icon="🔥",
    layout="wide"
)

# 2. 스타일 꾸미기 (초슬림 버전)
st.markdown("""
<style>
    /* 1. 전체 여백 줄이기 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* 2. 링크 버튼 슬림하게 만들기 */
    div.stButton > button {
        width: 100%;
        padding: 2px 10px !important; /* 버튼 내부 여백 축소 */
        font-size: 14px !important;
        height: auto !important;
        min-height: 0px !important;
        border: 1px solid #4CAF50;
        color: #4CAF50;
        background-color: white;
    }
    div.stButton > button:hover {
        background-color: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }
    
    /* 3. 그룹 헤더 스타일 */
    .group-header {
        font-size: 20px;
        font-weight: 700;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* 4. 텍스트 스타일 (한 줄 보기용) */
    .compact-text {
        font-size: 16px;
        line-height: 2.0; /* 버튼 높이와 눈높이 맞춤 */
        color: #333;
    }
    .description-text {
        font-size: 14px;
        color: #666;
    }
    
    /* 5. 구분선(Divider) 간격 최소화 */
    hr {
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
@st.cache_data
def load_data():
    file_name = "marketing_hub.xlsx"
    
    if not os.path.exists(file_name):
        return None

    df = pd.read_excel(file_name, header=4)
    df['구분'] = df['구분'].ffill()
    df = df.dropna(subset=['링크', '내용'])
    return df

# 4. 메인 화면 구성
def main():
    # [수정 1] 타이틀 변경
    st.title("🔥 마케팅팀 _ Smart Marketing Hub")
    
    df = load_data()

    if df is None:
        st.error("❌ 'marketing_hub.xlsx' 파일을 찾을 수 없습니다!")
        return

    try:
        groups = df['구분'].unique()

        for group in groups:
            if pd.isna(group): continue

            # 그룹 제목
            st.markdown(f"<div class='group-header'>📂 {group}</div>", unsafe_allow_html=True)
            
            group_df = df[df['구분'] == group]

            for idx, row in group_df.iterrows():
                # [수정 2] 레이아웃 비율 조정 (설명 칸을 넓게, 버튼은 좁게)
                # 6.5 (내용) : 1.5 (별점) : 2 (버튼)
                c1, c2, c3 = st.columns([6.5, 1.5, 2])
                
                with c1:
                    # [수정 3] 제목 : 설명 형태의 한 줄 텍스트 생성
                    title = row['내용']
                    desc = f" : <span class='description-text'>{row['기능']}</span>" if pd.notna(row['기능']) else ""
                    
                    # HTML로 한 줄에 출력
                    st.markdown(f"<div class='compact-text'><b>{title}</b>{desc}</div>", unsafe_allow_html=True)
                
                with c2:
                    # 별점 (수직 정렬을 위해 줄바꿈 없이 출력)
                    if pd.notna(row['활용도']):
                        st.markdown(f"<div class='compact-text' style='text-align:center;'>{row['활용도']}</div>", unsafe_allow_html=True)
                
                with c3:
                    # 링크 버튼
                    if pd.notna(row['링크']):
                        st.link_button("Link 🔗", str(row['링크']), use_container_width=True)
                
                # [수정 4] 굵은 divider 대신 아주 얇은 구분선 사용
                st.markdown("<hr>", unsafe_allow_html=True)

    except Exception as e:
        st.error("오류가 발생했습니다.")
        st.code(str(e))

if __name__ == "__main__":
    main()
