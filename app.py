import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(
    page_title="대성에너지(주) 마케팅팀 Smart Hub",
    page_icon="🔥",
    layout="wide"
)

# 2. 스타일 꾸미기
st.markdown("""
<style>
    div.stButton > button {
        width: 100%;
        text-align: left;
        border: 1px solid #dce0e6;
        background-color: #f8f9fa;
        color: #262730;
    }
    div.stButton > button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: #fff0f0;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: 600;
        color: #333333;
        margin-top: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
@st.cache_data(ttl=60)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # [cite_start][수정 완료] 형님이 주신 정확한 주소입니다! [cite: 1]
    sheet_url = "https://docs.google.com/spreadsheets/d/1wXoZ5kOL-4C6hWOZv-uy5UTE-RVCTiKIumnQGLHM4gg/edit"
    
    # ★중요★: 구글 시트 하단 탭 이름을 꼭 'App_DB'로 만드셔야 합니다.
    df = conn.read(spreadsheet=sheet_url, worksheet="App_DB") 
    
    # 데이터 정리
    df = df.dropna(subset=['링크', '내용'])
    return df

# 4. 메인 화면 구성
def main():
    st.title("🔥 대성에너지(주) 마케팅팀 Smart Hub")
    st.caption("🚀 Data-Driven Marketing Portal")
    st.divider()

    try:
        df = load_data()
        
        # 엑셀 데이터 순서대로 그룹핑
        groups = df['구분'].unique()

        for group in groups:
            st.markdown(f"<div class='big-font'>📂 {group}</div>", unsafe_allow_html=True)
            
            group_df = df[df['구분'] == group]
            
            # 3열 카드 배치
            cols = st.columns(3)
            for idx, row in group_df.iterrows():
                col = cols[idx % 3]
                with col:
                    st.link_button(
                        label=f"🔗 {row['내용']}", 
                        url=row['링크'],
                        help=f"📌 기능: {row['기능']}\n⭐ 활용도: {row['활용도']}",
                        use_container_width=True
                    )
            st.markdown("<br>", unsafe_allow_html=True)

    except Exception as e:
        st.error("데이터를 불러오지 못했습니다.")
        st.info("💡 확인해주세요: 구글 시트 하단 탭(시트) 이름이 'App_DB'가 맞나요?")
        st.code(str(e))

if __name__ == "__main__":
    main()
