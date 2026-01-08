import streamlit as st
import pandas as pd
import os

# --------------------------------------------------------------------------
# 1. 페이지 및 디자인 설정 (형님이 만족하신 그 디자인!)
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
    
    .alert-box { padding: 10px; background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; border-radius: 5px; margin-bottom: 20px; font-size: 14px;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2. 데이터 로드 및 필터링 (청소 기능 추가!)
# --------------------------------------------------------------------------
def get_data():
    file_name = 'marketing_hub.xlsx'
    
    # 1. 비상용 데이터 (엑셀 파일 없을 때)
    backup_data = [
        {"구분": "Key Support", "내용": "샘플 데이터입니다", "기능": "엑셀 파일을 연결해주세요", "활용도": 5, "링크": "#"}
    ]
    
    if not os.path.exists(file_name):
        return pd.DataFrame(backup_data), "⚠️ 엑셀 파일을 찾지 못해 '비상용 데이터'를 보여주고 있습니다."

    try:
        # 2. 엑셀 파일 읽기 (모든 줄을 일단 다 가져옴)
        df = pd.read_excel(file_name, engine='openpyxl', header=None)
        
        # '구분' 글자가 있는 진짜 헤더 위치 찾기
        header_idx = -1
        for i, row in df.iterrows():
            row_str = " ".join(row.astype(str))
            if "구분" in row_str and "내용" in row_str:
                header_idx = i
                break
        
        if header_idx == -1:
             return pd.DataFrame(backup_data), "⚠️ 엑셀 형식이 맞지 않습니다. ('구분', '내용' 헤더를 못 찾음)"

        # 진짜 헤더를 기준으로 다시 읽기
        df = pd.read_excel(file_name, engine='openpyxl', header=header_idx)
        df = df.fillna("") # 빈칸 채우기
        
        # 3. [핵심] 불필요한 헤더 행('상세분류', '구분' 등) 제거하기
        if '내용' in df.columns:
            # 삭제할 단어들 목록 (여기에 더 추가하셔도 됩니다)
            trash_words = ['상세분류', '구분', '내용', '기능', '활용도']
            
            # '내용' 컬럼에 저 단어들이 들어간 줄은 싹 지워버립니다.
            df = df[~df['내용'].isin(trash_words)]
            
            # 혹시 '내용'이 비어있는 줄도 삭제
            df = df[df['내용'] != ""]

        # 4. '구분'이 합쳐진 셀(Merged Cell) 처리 (위쪽 값 복사)
        if '구분' in df.columns:
            df['구분'] = df['구분'].replace("", pd.NA).ffill()
        
        return df, None

    except Exception as e:
        return pd.DataFrame(backup_data), f"⚠️ 에러 발생 ({e}). 비상용 데이터를 보여줍니다."

# --------------------------------------------------------------------------
# 3. 화면 그리기
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

df, alert_msg = get_data()

if alert_msg:
    st.markdown(f'<div class="alert-box">{alert_msg}</div>', unsafe_allow_html=True)

if not df.empty:
    # 컬럼 이름 공백 제거
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]
    
    if '구분' in df.columns:
        categories = df['구분'].unique()
        for category in categories:
            if not category or pd.isna(category): continue

            # 섹션 헤더 출력
            st.markdown(f"""
                <div class="section-header"><span class="folder-icon">📂</span> {category}</div>
                <div class="divider-top"></div>
            """, unsafe_allow_html=True)

            section_data = df[df['구분'] == category]
            
            for _, row in section_data.iterrows():
                # 데이터 매칭 (유연하게)
                title = row.get('내용', row.get('Title', ''))
                
                # [안전장치] 만약 제목이 비어있거나 '상세분류' 등이 뚫고 들어오면 건너뜀
                if not title or title in ['상세분류', '구분']: continue

                desc = row.get('기능', row.get('설명', ''))
                stars_val = row.get('활용도', row.get('별점', 0))
                link = row.get('링크', row.get('Link', '#'))
                
                # 별점 처리
                try:
                    if isinstance(stars_val, str) and "★" in stars_val:
                        stars = stars_val
                    else:
                        stars = "★" * int(float(stars_val)) if stars_val else "☆☆☆☆☆"
                except:
                    stars = "☆☆☆☆☆"

                # 최종 출력
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
