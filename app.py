import streamlit as st
import pandas as pd
import os

# --------------------------------------------------------------------------
# [설정] 페이지 기본 세팅
# --------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="마케팅팀 Smart Marketing Hub")

# --------------------------------------------------------------------------
# [디자인] CSS 스타일 (화면 꾸미기)
# --------------------------------------------------------------------------
st.markdown("""
<style>
    /* 1. 전체 폰트 및 색상 */
    body { font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; color: #333; }
    
    /* 2. 메인 타이틀 */
    .main-title {
        font-size: 28px; font-weight: 800; margin-bottom: 30px;
        color: #2c3e50; display: flex; align-items: center; gap: 10px;
    }
    
    /* 3. 섹션 헤더 (폴더 아이콘 있는 파란 제목) */
    .section-header {
        font-size: 18px; font-weight: 700; color: #1e40af;
        margin-top: 40px; margin-bottom: 10px;
        display: flex; align-items: center; gap: 8px;
    }
    
    /* 4. 파란색 구분선 */
    .divider-top { border-top: 2px solid #1e40af; margin-bottom: 0; }

    /* 5. 리스트 한 줄 (내용 - 별점 - 버튼) */
    .list-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 10px; border-bottom: 1px solid #e5e7eb;
    }

    /* 6. 내용 영역 (제목 + 설명) */
    .content-area { flex: 3; font-size: 15px; }
    .content-title { font-weight: 700; margin-right: 5px; }
    .content-desc { color: #555; font-size: 14px; }

    /* 7. 별점 영역 */
    .star-rating { flex: 0.5; text-align: center; font-size: 14px; letter-spacing: 2px; color: #333; }

    /* 8. 링크 버튼 영역 */
    .link-area { flex: 0.5; text-align: right; }
    .link-btn {
        display: inline-block; padding: 6px 20px;
        border: 1px solid #d1d5db; border-radius: 6px;
        background-color: white; text-decoration: none; color: #555;
        font-size: 13px; transition: background-color 0.2s;
    }
    .link-btn:hover { background-color: #f3f4f6; }
    
    /* 아이콘 색상 */
    .folder-icon { color: #fbbf24; }
    
    /* 에러 메시지 스타일 */
    .error-box {
        padding: 20px; background-color: #fef2f2; border: 1px solid #f87171;
        border-radius: 10px; color: #991b1b; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [기능] 데이터 로드 및 처리 함수 (안전장치 포함)
# --------------------------------------------------------------------------
def get_data_safely():
    file_name = 'marketing_hub.xlsx' # 1. 파일명 확인
    
    # 파일이 실제로 존재하는지 체크
    if not os.path.exists(file_name):
        return None, f"⚠️ '{file_name}' 파일을 찾을 수 없습니다. app.py와 같은 폴더에 엑셀 파일을 넣어주세요."
    
    try:
        # 엑셀 읽기
        df = pd.read_excel(file_name, engine='openpyxl')
        
        # 필수 컬럼이 있는지 검사 (없으면 에러 발생 방지)
        required_cols = ['구분', '내용', '활용도']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return None, f"⚠️ 엑셀 파일에 다음 컬럼(제목)이 없습니다: {missing_cols}. 엑셀 첫 줄을 확인해주세요."
            
        # 데이터가 비어있으면 빈 문자열로 채우기 (에러 방지)
        df = df.fillna("")
        return df, None
        
    except Exception as e:
        return None, f"⚠️ 엑셀 파일을 읽는 중 에러가 났습니다: {e}"

def make_stars(score):
    """숫자나 문자를 받아서 별(★)로 바꿔주는 함수"""
    try:
        if score == "": return "☆☆☆☆☆"
        # 숫자로 변환 시도
        score = int(float(score))
        return "★" * score
    except:
        return "☆☆☆☆☆" # 변환 실패 시 빈 별 표시

# --------------------------------------------------------------------------
# [화면] 메인 화면 그리기 로직
# --------------------------------------------------------------------------

# 1. 메인 타이틀
st.markdown('<div class="main-title">🔥 마케팅팀 _ Smart Marketing Hub</div>', unsafe_allow_html=True)

# 2. 데이터 가져오기
df, error_message = get_data_safely()

# 3. 데이터가 정상적으로 있으면 화면 출력, 없으면 에러 메시지 출력
if error_message:
    st.markdown(f'<div class="error-box">{error_message}</div>', unsafe_allow_html=True)
elif df is not None and not df.empty:
    # '구분' 순서대로 그룹핑
    categories = df['구분'].unique()

    for category in categories:
        # 섹션 헤더 그리기
        st.markdown(f"""
            <div class="section-header">
                <span class="folder-icon">📂</span> {category}
            </div>
            <div class="divider-top"></div>
        """, unsafe_allow_html=True)

        # 해당 카테고리 데이터만 뽑기
        section_data = df[df['구분'] == category]

        # 각 줄 그리기
        for index, row in section_data.iterrows():
            title = row['내용']
            # '설명' 컬럼이 있으면 가져오고 없으면 빈칸
            desc = row['설명'] if '설명' in df.columns else ""
            stars = make_stars(row['활용도'])
            # 'Link' 컬럼이 있고 값이 있으면 그 주소, 없으면 '#'
            link = row['Link'] if 'Link' in df.columns and row['Link'] != "" else "#"

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
        
        # 섹션 사이 간격
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

else:
    st.info("데이터가 비어있습니다. 엑셀 파일 내용을 확인해주세요.")
