import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(
    page_title="DSE Marketing Division | Smart Hub",
    page_icon="🧠",
    layout="wide"
)

# 2. 스타일 꾸미기 (버튼 디자인)
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
        border-color: #248bfb;
        color: #248bfb;
        background-color: #e6f3ff;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: 600;
        color: #1E3A8A; /* 남색 계열 */
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
@st.cache_data(ttl=60)
def load_data():
    # secrets.toml에 있는 정보로 구글 시트 연결
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # ★중요: 아까 만든 'App_DB' 시트를 읽습니다.
    # 만약 시트 이름을 다르게 했다면 worksheet="시트이름"을 수정해야 합니다.
    df = conn.read(worksheet="App_DB") 
    
    # 데이터 정리 (혹시 모를 빈칸 제거)
    df = df.dropna(subset=['링크', '내용'])
    return df

# 4. 메인 화면 구성
def main():
    st.title("🧠 DSE Marketing Division Smart Hub")
    st.markdown("##### 🚀 대구 도시가스 마케팅 본부 업무 통합 포털")
    st.divider()

    try:
        df = load_data()
        
        # '구분' 컬럼에 있는 그룹들을 가져옵니다 (Key Support, Operational Support 등)
        # 형님이 엑셀에 적은 순서대로 정렬하려면 리스트를 직접 적어주는 게 좋습니다.
        # 예: groups = ["Key Support", "Operational Support", "Analytical Support"]
        # 지금은 엑셀에 있는 순서대로 자동 추출합니다.
        groups = df['구분'].unique()

        for group in groups:
            st.markdown(f"<div class='big-font'>📂 {group}</div>", unsafe_allow_html=True)
            
            # 해당 그룹의 데이터만 뽑기
            group_df = df[df['구분'] == group]
            
            # 3열로 카드 배치
            cols = st.columns(3)
            for idx, row in group_df.iterrows():
                col = cols[idx % 3]
                with col:
                    # 링크 버튼 생성
                    st.link_button(
                        label=f"🔗 {row['내용']}", 
                        url=row['링크'],
                        help=f"📌 기능: {row['기능']}\n⭐ 활용도: {row['활용도']}",
                        use_container_width=True
                    )
            st.markdown("<br>", unsafe_allow_html=True) # 간격 띄우기

    except Exception as e:
        st.error("데이터를 불러오지 못했습니다. 아래 내용을 확인해주세요.")
        st.code(str(e))
        st.info("💡 팁: 구글 시트 이름이 'App_DB'가 맞는지, secrets 설정이 잘 되었는지 확인해보세요!")

if __name__ == "__main__":
    main()
