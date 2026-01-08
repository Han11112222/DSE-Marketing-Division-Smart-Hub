import streamlit as st
import pandas as pd
import os

# --------------------------------------------------------------------------
# 1. 페이지 및 디자인 설정 (형님이 좋아하신 스타일)
# --------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

st.markdown("""
<style>
    body { font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; color: #333; }
    .main-title { font-size: 28px; font-weight: 800; margin-bottom: 30px; color: #2c3e50; display: flex; align-items: center; gap: 10px; }
    .section-header { font-size: 18px; font-weight: 700; color: #1e40af; margin-top: 40px; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    .divider-top { border-top: 2px solid #1e40af; margin-bottom: 0; }
    .list-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 10px; border-bottom: 1px solid #e5e7eb; }
    .content-area { flex: 3; font-size: 15px; }
    .content-title { font-weight: 700; margin-right: 5px; }
    .content-desc { color: #555; font-size: 14px; }
    .star-rating { flex: 0.5; text-align: center; font-size: 14px; letter-spacing: 2px; color: #333; }
    .link-area { flex: 0.5; text-align: right; }
    .link-btn { display: inline-block; padding: 6px 20px; border: 1px solid #d1d5db; border-radius: 6px; background-color: white; text-decoration: none; color: #555; font-size: 13px; transition: background-color 0.2s; }
    .link-btn:hover { background-color: #f3f4f6; }
    .folder-icon { color: #fbbf24; }
    .alert-box { padding: 10px; background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; border-radius: 5px; margin-bottom: 20px; font-size: 14px;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2. 데이터 로드 (비상용 데이터 탑재!)
# --------------------------------------------------------------------------
def get_data():
    # [비상용 데이터] 엑셀이 안 읽히면 이 데이터가 나옵니다.
    backup_data = [
        {"구분": "Key Support", "내용": "공동주택 지도 시각화 Dashboard", "기능": "공동주택, 지역난방 시각화, 판매량 비교 등", "활용도": 5, "링크": "#"},
        {"구분": "Key Support", "내용": "판매량분석(full ver)", "기능": "고객명별, 상품별 전년동월대비 판매량분석", "활용도": 5, "링크": "#"},
        {"구분": "Key Support", "내용": "판매량분석(simple ver)", "기능": "상품별, 산업용, 일반용(업종별, 고객별 분석 등)", "활용도": 4, "링크": "#"},
        {"구분": "Key Support", "내용": "일 공급량 실적관리", "기능": "일일계획 및 실적관리, 랭킹관리 등", "활용도": 5, "링크": "#"},
        {"구분": "모니터링(Monitoring)", "내용": "뉴스 모니터링 (Client)", "기능": "대성에너지 주요 고객 뉴스 모니터링", "활용도": 3, "링크": "#"},
        {"구분": "모니터링(Monitoring)", "내용": "입주율 분석 Dashboard", "기능": "입주율 저조 단지, 계획대비 실적 분석", "활용도": 3, "링크": "#"},
    ]
    
    file_name = 'marketing_hub.xlsx'
    
    # 1. 파일이 없으면 -> 비상용 데이터 사용
    if not os.path.exists(file_name):
        return pd.DataFrame(backup_data), "⚠️ 엑셀 파일을 찾지 못해 '비상용 데이터'를 보여주고 있습니다. 파일을 폴더에 넣어주세요."

    try:
        # 2. 엑셀 파일 읽기 시도 (엔진 변경: openpyxl)
        # 헤더를 찾기 위해 일단 읽어봄
        df = pd.read_excel(file_name, engine='openpyxl', header=None)
        
        # '구분'이라는 글자가 있는 행 찾기 (자동 탐지)
        header_idx = -1
        for i, row in df.iterrows():
            row_str = " ".join(row.astype(str))
            if "구분" in row_str:
                header_idx = i
                break
        
        if header_idx == -1:
             return pd.DataFrame(backup_data), "⚠️ 엑셀에서 '구분'이라는 제목을 못 찾아서 '비상용 데이터'를 보여줍니다."

        # 제대로 다시 읽기
        df = pd.read_excel(file_name, engine='openpyxl', header=header_idx)
        df = df.fillna("") # 빈칸 채우기
        
        # '구분'이 합쳐진 셀(Merged Cell) 처리
        if '구분' in df.columns:
            df['구분'] = df['구분'].replace("", pd.NA).ffill()
        
        return df, None # 성공! 에러 없음

    except Exception as e:
        # 3. 읽다가 에러나면 -> 비상용 데이터 사용
        return pd.DataFrame(backup_data), f"⚠️ 엑셀 읽기 에러 발생 ({e}). 대신 '비상용 데이터'를 보여줍니다."

# --------------------------------------------------------------------------
# 3. 화면 그리기
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

df, alert_msg = get_data()

# 경고 메시지가 있으면(엑셀 실패 시) 상단에 노란 박스로 살짝 알려줌
if alert_msg:
    st.markdown(f'<div class="alert-box">{alert_msg}</div>', unsafe_allow_html=True)

if not df.empty:
    # 컬럼 이름 정리 (혹시 모를 공백 제거)
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]
    
    # '구분' 컬럼이 있는지 확인
    if '구분' in df.columns:
        categories = df['구분'].unique()
        for category in categories:
            if not category or pd.isna(category): continue

            st.markdown(f"""
                <div class="section-header"><span class="folder-icon">📂</span> {category}</div>
                <div class="divider-top"></div>
            """, unsafe_allow_html=True)

            section_data = df[df['구분'] == category]
            for _, row in section_data.iterrows():
                # 컬럼명 매칭 시도 (유연하게)
                title = row.get('내용', row.get('Title', ''))
                desc = row.get('기능', row.get('설명', ''))
                stars_val = row.get('활용도', row.get('별점', 0))
                link = row.get('링크', row.get('Link', '#'))
                
                # 별점 처리
                try:
                    # 엑셀에 ★ 문자가 있으면 그대로 쓰고, 숫자면 변환
                    if isinstance(stars_val, str) and "★" in stars_val:
                        stars = stars_val
                    else:
                        stars = "★" * int(float(stars_val)) if stars_val else "☆☆☆☆☆"
                except:
                    stars = "☆☆☆☆☆"

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
