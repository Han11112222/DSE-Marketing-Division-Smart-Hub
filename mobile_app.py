import flet as ft
import pandas as pd
import urllib.request
import ssl

SHEET_URL = "https://docs.google.com/spreadsheets/d/1gbjNJoejLzd1UOzg5_2wCt0GnHpJNjju7W8RyKN56ZY/export?format=csv&gid=0"

STAR_COLOR = "#f59e0b"
PRIMARY_COLOR = "#1e40af"
BG_COLOR = "#f8f9fa"
DIVIDER_COLOR = "#e5e7eb"
TEXT_COLOR = "#333333"
DESC_COLOR = "#555555"


def get_data():
    backup = [{"구분": "Key Support", "내용": "샘플 데이터", "기능": "스프레드시트 연결 필요", "활용도": 3, "링크": "#"}]
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.urlopen(SHEET_URL, context=ctx, timeout=10)
        raw = req.read().decode("utf-8").splitlines()

        header_idx = -1
        for i, line in enumerate(raw):
            if "구분" in line and "내용" in line:
                header_idx = i
                break

        if header_idx == -1:
            return pd.DataFrame(backup), "⚠️ 헤더를 찾을 수 없습니다."

        from io import StringIO
        content = "\n".join(raw[header_idx:])
        df = pd.read_csv(StringIO(content))
        df = df.fillna("")

        trash = ["상세분류", "구분", "내용", "기능", "활용도", "Main 활용"]
        if "내용" in df.columns:
            df = df[~df["내용"].isin(trash)]
            df = df[df["내용"] != ""]
        if "구분" in df.columns:
            df = df[~df["구분"].isin(trash)]
            df["구분"] = df["구분"].replace("", pd.NA).ffill()

        return df, None
    except Exception as e:
        return pd.DataFrame(backup), f"⚠️ 에러: {e}"


def make_stars(val):
    try:
        if isinstance(val, str) and "★" in val:
            return val
        n = int(float(val)) if val else 0
        return "★" * n + "☆" * (5 - n)
    except:
        return "☆☆☆☆☆"


def main(page: ft.Page):
    page.title = "마케팅팀 Smart Hub"
    page.bgcolor = "#ffffff"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.fonts = {"NotoSans": "https://fonts.gstatic.com/s/notosanskr/v36/PbykFmXiEBPT4ITbgNA5Cgm20xz64px_1hVWr0wuPNGmlQNMEfD4.woff2"}
    page.theme = ft.Theme(font_family="NotoSans")

    # ---------- 로딩 표시 ----------
    loading = ft.Column(
        [ft.ProgressRing(), ft.Text("데이터 불러오는 중...", size=14, color=DESC_COLOR)],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    content_col = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)

    def build_ui(e=None):
        content_col.controls.clear()
        df, err = get_data()

        # 타이틀
        content_col.controls.append(
            ft.Container(
                content=ft.Text(
                    "🔥 마케팅팀 Smart Marketing Hub",
                    size=20, weight=ft.FontWeight.W_800, color=TEXT_COLOR,
                ),
                padding=ft.padding.only(left=16, top=20, bottom=16, right=16),
            )
        )

        if err:
            content_col.controls.append(
                ft.Container(
                    content=ft.Text(err, size=13, color="#856404"),
                    bgcolor="#fff3cd",
                    border=ft.border.all(1, "#ffeeba"),
                    border_radius=6,
                    padding=10,
                    margin=ft.margin.symmetric(horizontal=16),
                )
            )

        if df.empty:
            content_col.controls.append(ft.Text("데이터 없음", color=DESC_COLOR, size=14))
            page.update()
            return

        df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

        if "구분" not in df.columns:
            content_col.controls.append(ft.Text("'구분' 컬럼을 찾을 수 없습니다.", color="red"))
            page.update()
            return

        categories = df["구분"].dropna().unique()

        for category in categories:
            if not category or str(category).strip() == "":
                continue

            # 섹션 헤더
            content_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text("📂", size=16),
                        ft.Text(str(category), size=16, weight=ft.FontWeight.W_700, color=PRIMARY_COLOR),
                    ]),
                    padding=ft.padding.only(left=16, top=24, bottom=6, right=16),
                )
            )
            # 구분선
            content_col.controls.append(
                ft.Divider(height=1, color=PRIMARY_COLOR, thickness=2)
            )

            # 컬럼 헤더
            content_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text("업무 내용", size=13, weight=ft.FontWeight.W_700, color=DESC_COLOR, expand=3),
                        ft.Text("활용도", size=13, weight=ft.FontWeight.W_700, color=DESC_COLOR, width=70, text_align=ft.TextAlign.CENTER),
                        ft.Text("링크", size=13, weight=ft.FontWeight.W_700, color=DESC_COLOR, width=70, text_align=ft.TextAlign.CENTER),
                    ]),
                    bgcolor=BG_COLOR,
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    border=ft.border.only(bottom=ft.BorderSide(2, DIVIDER_COLOR)),
                )
            )

            # 데이터 행
            section_df = df[df["구분"] == category]
            for _, row in section_df.iterrows():
                title = str(row.get("내용", "")).strip()
                if not title or title in ["상세분류", "구분"]:
                    continue

                desc = str(row.get("기능", "")).strip()
                stars = make_stars(row.get("활용도", 0))
                link = str(row.get("링크", "#")).strip()

                def open_link(e, url=link):
                    if url and url != "#":
                        page.launch_url(url)

                content_col.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(title, size=14, weight=ft.FontWeight.W_700, color=TEXT_COLOR),
                                        ft.Text(desc, size=12, color=DESC_COLOR) if desc else ft.Container(),
                                    ],
                                    spacing=2,
                                    expand=3,
                                ),
                                ft.Text(stars, size=12, color=STAR_COLOR, width=70, text_align=ft.TextAlign.CENTER),
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        "Link 🔗",
                                        on_click=open_link,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.WHITE,
                                            color=DESC_COLOR,
                                            side=ft.BorderSide(1, DIVIDER_COLOR),
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        ),
                                    ),
                                    width=70,
                                    alignment=ft.alignment.center,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        border=ft.border.only(bottom=ft.BorderSide(1, DIVIDER_COLOR)),
                    )
                )

            content_col.controls.append(ft.Container(height=20))

        page.update()

    # 새로고침 버튼
    refresh_btn = ft.IconButton(
        icon=ft.icons.REFRESH,
        tooltip="새로고침",
        on_click=build_ui,
        icon_color=PRIMARY_COLOR,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Smart Hub", color="white", size=16, weight=ft.FontWeight.W_700),
        bgcolor=PRIMARY_COLOR,
        actions=[refresh_btn],
    )

    page.add(content_col)
    build_ui()


ft.app(target=main)
