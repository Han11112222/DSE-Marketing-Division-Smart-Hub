import flet as ft

def main(page: ft.Page):
    # 모바일 앱 기본 설정
    page.title = "Smart Marketing Hub"
    page.scroll = "auto" # 화면을 위아래로 스크롤할 수 있게 설정
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # 1. 상단 타이틀 영역
    title = ft.Text("🔥 마케팅팀 _ Smart Marketing Hub", size=22, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("📁 Key Support", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800)
    
    # 2. 마케팅본부 주요 업무 리스트 데이터
    tasks = [
        {"name": "공동주택 지도 시각화 Dashboard", "desc": "공동주택, 지역난방 시각화, 판매량 비교 등", "stars": "★★★★★", "url": "#"},
        {"name": "판매량분석 (full ver)", "desc": "고객명별, 상품별 전년동월대비 판매량분석", "stars": "★★★★★", "url": "#"},
        {"name": "판매량분석 (simple ver)", "desc": "상품별_산업용, 일반용(업종별, 고객별 분석 등)", "stars": "★★★★", "url": "#"},
        {"name": "일 공급량 실적관리", "desc": "일일계획 및 실적관리, 랭킹관리, 실적관리, 기온 구간별 공급량 분석 등", "stars": "★★★★★", "url": "#"},
        {"name": "배관투자 승인 내역 관리", "desc": "배관투자 승인 내역 조회", "stars": "★★★", "url": "#"},
        {"name": "신규배관 경제성 분석 Simulation", "desc": "경제성 분석 (Enhanced version) _ 최소 계량기등급 추정기능", "stars": "★★★★", "url": "#"},
        {"name": "입주율 분석 Dashboard", "desc": "입주율 저조 단지, 계획대비 실적 분석 등", "stars": "★★★", "url": "#"},
        {"name": "뉴스 모니터링 (Client)", "desc": "주요 고객 뉴스 모니터링(중대재해 등)", "stars": "★★★", "url": "#"}
    ]
    
    # 3. 데이터를 모바일 화면에 맞는 '카드 리스트' 형태로 그리기
    list_view = ft.ListView(expand=True, spacing=15)
    
    for task in tasks:
        list_view.controls.append(
            ft.Container(
                content=ft.Column([
                    # 업무 이름
                    ft.Text(task['name'], weight=ft.FontWeight.BOLD, size=16),
                    # 업무 설명
                    ft.Text(task['desc'], color=ft.colors.GREY_700, size=13),
                    # 별점과 링크 버튼을 가로로 배치
                    ft.Row([
                        ft.Text(task['stars'], color=ft.colors.AMBER_500, size=14),
                        ft.ElevatedButton("Link 🔗", url=task['url'], style=ft.ButtonStyle(padding=5))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                bgcolor=ft.colors.WHITE
            )
        )
        
    # 4. 구성한 화면을 페이지에 추가
    page.add(
        title,
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        subtitle,
        ft.Divider(height=10, color=ft.colors.BLUE_200),
        list_view
    )

ft.app(target=main)
