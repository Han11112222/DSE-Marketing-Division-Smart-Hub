<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>마케팅팀 Smart Marketing Hub</title>
    <style>
        body {
            font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
            color: #333;
            margin: 0;
            padding: 40px;
            background-color: #ffffff;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        /* 메인 타이틀 */
        h1 {
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 40px;
            color: #2c3e50;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* 섹션 헤더 (Key Support, 모니터링 등) */
        .section-header {
            font-size: 18px;
            font-weight: 700;
            color: #1e40af; /* 파란색 텍스트 */
            margin-top: 40px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* 상단 구분선 */
        .divider-top {
            border-top: 2px solid #1e40af;
            margin-bottom: 0;
        }

        /* 리스트 아이템 행 */
        .list-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 10px;
            border-bottom: 1px solid #e5e7eb; /* 연한 회색 줄 */
        }

        /* 텍스트 영역 */
        .content-area {
            flex: 2;
            font-size: 14px;
        }
        .content-title {
            font-weight: 700;
            margin-right: 5px;
        }
        .content-desc {
            color: #555;
        }

        /* 별점 영역 */
        .star-rating {
            flex: 0.5;
            text-align: center;
            font-size: 14px;
            letter-spacing: 2px;
            color: #333;
        }

        /* 링크 버튼 영역 */
        .link-area {
            flex: 0.5;
            text-align: right;
        }
        .link-btn {
            display: inline-block;
            padding: 8px 30px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            background-color: white;
            text-decoration: none;
            color: #555;
            font-size: 14px;
            transition: background-color 0.2s;
        }
        .link-btn:hover {
            background-color: #f3f4f6;
        }
        
        /* 유틸리티 */
        .folder-icon {
            color: #fbbf24; /* 노란색 폴더 아이콘 */
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>🔥 마케팅팀 _ Smart Marketing Hub</h1>

        <div class="section-header">
            <span class="folder-icon">📂</span> Key Support
        </div>
        
        <div class="divider-top"></div>

        <div class="list-row">
            <div class="content-area">
                <span class="content-title">공동주택 지도 시각화 Dashboard :</span>
                <span class="content-desc">공동주택, 지역난방 시각화, 판매량 비교 등</span>
            </div>
            <div class="star-rating">★★★★★</div>
            <div class="link-area">
                <a href="#" class="link-btn">Link 🔗</a>
            </div>
        </div>

        <div class="list-row">
            <div class="content-area">
                <span class="content-title">판매량분석(full ver) :</span>
                <span class="content-desc">고객명별, 상품별 전년동월대비 판매량분석</span>
            </div>
            <div class="star-rating">★★★★★</div>
            <div class="link-area">
                <a href="#" class="link-btn">Link 🔗</a>
            </div>
        </div>

        <div class="list-row">
            <div class="content-area">
                <span class="content-title">판매량분석(simple ver) :</span>
                <span class="content-desc">상품별, 산업용, 일반용(업종별, 고객별 분석 등)</span>
            </div>
            <div class="star-rating">★★★★</div>
            <div class="link-area">
                <a href="#" class="link-btn">Link 🔗</a>
            </div>
        </div>

        <div class="list-row">
            <div class="content-area">
                <span class="content-title">일 공급량 실적관리 :</span>
                <span class="content-desc">일일계획 및 실적관리, 랭킹관리, 실적관리, 기온 구간평 공급량 분석 등</span>
            </div>
            <div class="star-rating">★★★★★</div>
            <div class="link-area">
                <a href="#" class="link-btn">Link 🔗</a>
            </div>
        </div>

        <div class="list-row">
            <div class="content-area">
                <span class="content-title">입주율 분석 Dashboard :</span>
                <span class="content-desc">입주율 저조 단지, 계획대비 실적 분석 등</span>
            </div>
            <div class="star-rating">★★★</div>
            <div class="link-area">
                <a href="#" class="link-btn">Link 🔗</a>
            </div>
        </div>

        <div class="list-row">
            <div class="content-area">
                <span class="content-title">뉴스 모니터링 (Client) :</span>
                <span class="content-desc">대성에너지 주요 고객 뉴스 모니터링(중대재해 등)</span>
            </div>
            <div class="star-rating">★★★</div>
            <div class="link-area">
                <a href="#" class="link-btn">Link 🔗</a>
            </div>
        </div>

        <div class="section-header" style="margin-top: 60px;">
            <span class="folder-icon">📂</span> 모니터링(Monitoring)
        </div>
        <div class="divider-top"></div>

    </div>

</body>
</html>
