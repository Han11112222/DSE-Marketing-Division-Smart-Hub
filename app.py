import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="마케팅팀 _ Smart Marketing Hub",
    page_icon="🔥",
    layout="wide"
)

# 2. 스타일 꾸미기 (초슬림 & 심플)
st.markdown("""
<style>
    /* 1. 전체 여백 설정 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* 2. 링크 버튼 디자인 */
    div.stButton > button {
        width: 100%;
        padding: 0px 10px !important;
        font-size: 13px !important;
        height: 32px !important;
        min-height: 0px !important;
        border: 1px solid #4CAF50;
        color: #4CAF50;
        background-color: white;
        border-radius: 5px;
    }
    div.stButton > button:hover {
        background-color: #4CAF50;
        color: white;
    }
    
    /* 3. 텍스트 스타일 (한 줄 보기용) */
    .compact-text {
        font-size: 16px;
        line-height: 2.0;
        color: #333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .description-text {
        font-size: 14px;
        color: #888;
        font-weight: 400;
    }
    
    /* 4. 항목 사이 구분선 (아주 얇게) */
    hr.item-divider {
        margin-top: 3px !important;
        margin-bottom: 3px !important;
        border-top: 1px solid #f0f0f0;
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
    st.title("🔥 마케팅팀 _ Smart Marketing Hub")
    
    df = load_data()

    if df is None:
        st.error("❌ 'marketing_hub.xlsx' 파일을 찾을 수 없습니다!")
        return

    try:
        # 그룹핑은 하되, 제목은 출력하지 않음
        groups = df['구분'].unique()

        for i, group in enumerate(groups):
            if pd.isna(group): continue
            
            # [핵심] 제목 출력 코드 삭제됨 (📂 Key Support 안 나옴)
            
            # 해당 그룹의 데이터 가져오기
            group_df = df[df['구분'] == group]

            for idx, row in group_df.iterrows():
                # 레이아웃: [내용(7) | 별점(1) | 버튼(2)]
                c1, c2, c3 = st.columns([7, 1, 2])
                
                with c1:
                    # 제목 : 설명
                    title = row['내용']
                    desc = f" : <span class='description-text'>{row['기능']}</span>" if pd.notna(row['기능']) else ""
                    st.markdown(f"<div class='compact-text'><b>{title}</b>{desc}</div>", unsafe_allow_html=True)
                
                with c2:
                    # 별점
                    if pd.notna(row['활용도']):
                        st.markdown(f"<div class='compact-text' style='text-align:center; font-size:14px;'>{row['활용도']}</div>", unsafe_allow_html=True)
                
                with c3:
                    # 링크 버튼
                    if pd.notna(row['링크']):
                        st.link_button("Link 🔗", str(row['링크']), use_container_width=True)
                
                # 항목 간 얇은 구분선
                st.markdown("<hr class='item-divider'>", unsafe_allow_html=True)
            
            # [핵심] 그룹이 끝날 때마다 넓은 간격(Gap) 추가 (마지막 그룹 제외)
            if i < len(groups) - 1:
                st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True) # 40px 만큼 띄우기

    except Exception as e:
        st.error("오류가 발생했습니다.")
        st.code(str(e))

if __name__ == "__main__":
    main()
