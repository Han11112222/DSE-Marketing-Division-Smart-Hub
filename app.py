import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="대성에너지(주) 마케팅팀 Smart Hub",
    page_icon="🔥",
    layout="wide"
)

# 2. 스타일 꾸미기 (테이블 느낌 살리기)
st.markdown("""
<style>
    /* 전체 폰트 및 여백 조정 */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* 링크 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        border: 1px solid #4CAF50; /* 초록색 테두리 (엑셀 느낌) */
        color: #4CAF50;
        background-color: white;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }

    /* 그룹 헤더 스타일 */
    .group-header {
        font-size: 24px;
        font-weight: 700;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    /* 각 행의 스타일 */
    .row-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }
    .row-desc {
        font-size: 15px;
        color: #666;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
@st.cache_data
def load_data():
    file_name = "marketing_hub.xlsx"
    
    if not os.path.exists(file_name):
        return None

    # header=4: 엑셀 5번째 줄이 제목
    df = pd.read_excel(file_name, header=4)
    
    # 엑셀 '셀 병합' 처리
    df['구분'] = df['구분'].ffill()
    
    # 데이터 정리
    df = df.dropna(subset=['링크', '내용'])
    return df

# 4. 메인 화면 구성
def main():
    st.title("🔥 대성에너지(주) 마케팅팀 Smart Hub")
    st.markdown("##### 🚀 업무 효율화를 위한 AI & 데이터 분석 포털")
    
    df = load_data()

    if df is None:
        st.error("❌ 'marketing_hub.xlsx' 파일을 찾을 수 없습니다!")
        return

    try:
        groups = df['구분'].unique()

        for group in groups:
            if pd.isna(group): continue

            # [1] 그룹 제목 (예: Key Support)
            st.markdown(f"<div class='group-header'>📂 {group}</div>", unsafe_allow_html=True)
            
            # 해당 그룹 데이터 가져오기
            group_df = df[df['구분'] == group]

            # [2] 리스트 형태로 한 줄씩 출력
            for idx, row in group_df.iterrows():
                # 화면 분할: [이름&설명(5) | 별점(1.5) | 버튼(1.5)] 비율로 나눔
                c1, c2, c3 = st.columns([5, 1.5, 1.5])
                
                with c1:
                    # 제목
                    st.markdown(f"<div class='row-title'>{row['내용']}</div>", unsafe_allow_html=True)
                    # 설명 (기능) - 형님이 원하셨던 부분!
                    if pd.notna(row['기능']):
                        st.markdown(f"<div class='row-desc'>└ 💡 {row['기능']}</div>", unsafe_allow_html=True)
                
                with c2:
                    # 활용도 (별점) 중앙 정렬
                    st.write("") # 줄맞춤용 공백
                    if pd.notna(row['활용도']):
                        st.markdown(f"**{row['활용도']}**")
                
                with c3:
                    # 링크 버튼
                    st.write("") # 줄맞춤용 공백
                    if pd.notna(row['링크']):
                        st.link_button("바로가기 🔗", str(row['링크']), use_container_width=True)
                
                # 각 줄 사이에 얇은 구분선
                st.divider()

    except Exception as e:
        st.error("오류가 발생했습니다.")
        st.code(str(e))

if __name__ == "__main__":
    main()
