import streamlit as st
import pandas as pd

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

# 3. 데이터 로드 함수 (엑셀 파일 읽기)
@st.cache_data
def load_data():
    # ★중요: 깃허브에 올린 엑셀 파일 이름이 'marketing_hub.xlsx' 라고 가정했습니다.
    # 만약 이름이 다르면 아래 "marketing_hub.xlsx" 부분을 형님 파일명으로 고쳐주세요!
    # header=5는 엑셀의 6번째 줄(구분, 내용...)부터 읽으라는 뜻입니다.
    df = pd.read_excel("marketing_hub.xlsx", header=5)
    
    # 엑셀 '셀 병합' 처리: 비어있는 '구분' 컬럼을 위 내용으로 채우기
    df['구분'] = df['구분'].ffill()
    
    # 데이터 정리 (링크 없는 행 제거)
    df = df.dropna(subset=['링크', '내용'])
    return df

# 4. 메인 화면 구성
def main():
    st.title("🔥 대성에너지(주) 마케팅팀 Smart Hub")
    st.caption("🚀 Data-Driven Marketing Portal (Excel Ver.)")
    st.divider()

    try:
        df = load_data()
        
        # 엑셀 순서대로 그룹핑
        groups = df['구분'].unique()

        for group in groups:
            st.markdown(f"<div class='big-font'>📂 {group}</div>", unsafe_allow_html=True)
            
            group_df = df[df['구분'] == group]
            
            # 3열 카드 배치
            cols = st.columns(3)
            for idx, row in group_df.iterrows():
                col = cols[idx % 3]
                with col:
                    # 링크가 있는지 한 번 더 확인
                    if pd.notna(row['링크']):
                        st.link_button(
                            label=f"🔗 {row['내용']}", 
                            url=row['링크'],
                            help=f"📌 기능: {row['기능']}\n⭐ 활용도: {row['활용도']}",
                            use_container_width=True
                        )
            st.markdown("<br>", unsafe_allow_html=True)

    except Exception as e:
        st.error("엑셀 파일을 불러오지 못했습니다.")
        st.warning("혹시 깃허브에 올린 파일 이름이 'marketing_hub.xlsx'가 맞는지 확인해주세요!")
        st.code(str(e))

if __name__ == "__main__":
    main()
