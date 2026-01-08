import streamlit as st
import pandas as pd
import os

# --------------------------------------------------------------------------
# 1. 디자인 설정 (Han형님이 좋아하신 그 디자인)
# --------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

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
    
    .error-box {
        padding: 20px; background-color: #fef2f2; border: 1px solid #f87171;
        border-radius: 10px; color: #991b1b; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2. 데이터 로드 (핵심 수정 부분!)
# --------------------------------------------------------------------------
def load_data():
    file_name = 'marketing_hub.xlsx' 
    
    if not os.path.exists(file_name):
        st.error(f"⚠️ '{file_name}' 파일이 없습니다. 폴더 위치를 확인해주세요.")
        return pd.DataFrame()
    
    try:
        # [수정 1] header=3 : 위에서 3줄(0,1,2행)은 건너뛰고 4번째 줄을 제목으로 씁니다.
        df = pd.read_excel(file_name, engine='openpyxl', header=3)
        
        # [수정 2] '구분'이 합쳐진 셀일 경우 NaN(빈칸)으로 나올 수 있어서, 위쪽 값을 복사해옵니다.
        df['구분'] = df['구분'].ffill()
        
        # 데이터가 없는 빈 행 제거
        df = df.dropna(subset=['내용'])
        
        return df
    except Exception as e:
        st.error(f"엑셀 읽기 오류: {e}")
        return pd.DataFrame()

# --------------------------------------------------------------------------
# 3. 화면 출력
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # 엑셀에 있는 '구분' 순서대로 출력
    categories = df['구분'].unique()

    for category in categories:
        st.markdown(f"""
            <div class="section-header">
                <span class="folder-icon">📂</span> {category}
            </div>
            <div class="divider-top"></div>
        """, unsafe_allow_html=True)

        section_data = df[df['구분'] == category]

        for index, row in section_data.iterrows():
            title = row['내용']
            # [수정 3] 엑셀 컬럼명이 '기능'이라서 '기능'을 가져옵니다.
            desc = row['기능'] if '기능' in df.columns else ""
            if pd.isna(desc): desc = "" # 내용이 비어있으면 빈칸 처리
            
            # [수정 4] 엑셀에 이미 별(★)이 있으므로 변환 없이 그대로 가져옵니다.
            stars = row['활용도'] 
            if pd.isna(stars): stars = ""

            # 링크 처리 (링크가 없거나 NaN이면 #)
            link = row['링크'] if '링크' in df.columns and not pd.isna(row['링크']) else "#"

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
        
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

else:
    # 데이터 로드 실패 시에도 안내 메시지 표시
    st.info("데이터를 불러올 수 없습니다. 엑셀 파일 형식(헤더 위치 등)을 확인해주세요.")
