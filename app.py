import streamlit as st
import pandas as pd
import os

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
@st.cache_data
def load_data():
    file_name = "marketing_hub.xlsx"
    
    # [디버깅] 파일이 진짜 있는지 확인
    if not os.path.exists(file_name):
        return None

    # ★ 핵심 수정: header=4 (엑셀 5번째 줄이 제목이므로 0부터 세면 4)
    df = pd.read_excel(file_name, header=4)
    
    # 엑셀 '셀 병합' 처리 (비어있는 '구분' 칸 채우기)
    df['구분'] = df['구분'].ffill()
    
    # 데이터 정리 (링크나 내용이 없는 빈 줄 제거)
    df = df.dropna(subset=['링크', '내용'])
    return df

# 4. 메인 화면 구성
def main():
    st.title("🔥 대성에너지(주) 마케팅팀 Smart Hub")
    st.caption("🚀 Data-Driven Marketing Portal")
    st.divider()

    df = load_data()

    # 파일 못 찾았을 때 에러 메시지 띄우기
    if df is None:
        st.error("❌ 'marketing_hub.xlsx' 파일을 찾을 수 없습니다!")
        st.info(f"현재 폴더에 있는 파일들: {os.listdir()}") # 현재 폴더 파일 목록 보여줌
        return

    try:
        # 엑셀 순서대로 그룹핑
        groups = df['구분'].unique()

        for group in groups:
            # 그룹 이름이 비어있으면 건너뛰기
            if pd.isna(group): continue

            st.markdown(f"<div class='big-font'>📂 {group}</div>", unsafe_allow_html=True)
            
            group_df = df[df['구분'] == group]
            
            # 3열 카드 배치
            cols = st.columns(3)
            for idx, row in group_df.iterrows():
                col = cols[idx % 3]
                with col:
                    if pd.notna(row['링크']):
                        st.link_button(
                            label=f"🔗 {row['내용']}", 
                            url=str(row['링크']), # 링크를 문자열로 확실히 변환
                            help=f"📌 기능: {row['기능']}\n⭐ 활용도: {row['활용도']}",
                            use_container_width=True
                        )
            st.markdown("<br>", unsafe_allow_html=True)

    except Exception as e:
        st.error("데이터 처리 중 오류가 발생했습니다.")
        st.code(str(e))

if __name__ == "__main__":
    main()
