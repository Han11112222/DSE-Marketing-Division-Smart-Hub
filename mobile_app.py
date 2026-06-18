import flet as ft

def main(page: ft.Page):
    # 모바일 화면 UI 설정
    page.title = "마케팅본부 스마트 허브"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text("📊 대성에너지 마케팅 스마트 허브", size=24, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("현재 데이터 대기 중...", size=16, color="grey")

    def load_data(e):
        status_text.value = "✔️ marketing_hub.xlsx 연동 준비 완료!"
        status_text.color = "blue"
        page.update()

    load_btn = ft.ElevatedButton("모바일 데이터 불러오기", on_click=load_data)
    page.add(title, status_text, load_btn)

ft.app(target=main)
