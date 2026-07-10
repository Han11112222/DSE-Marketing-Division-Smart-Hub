import urllib.request
import ssl
import csv
from io import StringIO
from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import webbrowser

SHEET_URL = "https://docs.google.com/spreadsheets/d/1gbjNJoejLzd1UOzg5_2wCt0GnHpJNjju7W8RyKN56ZY/export?format=csv&gid=0"

PRIMARY = get_color_from_hex("#1e40af")
BG = get_color_from_hex("#ffffff")
TEXT = get_color_from_hex("#333333")
DESC = get_color_from_hex("#555555")
STAR = get_color_from_hex("#f59e0b")
DIVIDER = get_color_from_hex("#e5e7eb")

TRASH = {"상세분류", "구분", "내용", "기능", "활용도", "Main 활용"}


def safe_str(val):
    if val is None:
        return ""
    return str(val).strip()


def get_data():
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.urlopen(SHEET_URL, context=ctx, timeout=15)
        raw = req.read().decode("utf-8").splitlines()

        header_idx = -1
        for i, line in enumerate(raw):
            if "구분" in line and "내용" in line:
                header_idx = i
                break

        if header_idx == -1:
            return [], "헤더를 찾을 수 없습니다."

        content = "\n".join(raw[header_idx:])
        reader = csv.DictReader(StringIO(content))
        rows = []
        last_category = ""

        for row in reader:
            row = {safe_str(k): safe_str(v) for k, v in row.items() if k is not None}
            if row.get("내용", "") in TRASH or row.get("내용", "") == "":
                continue
            if row.get("구분", "") in TRASH:
                continue
            if row.get("구분", "") == "":
                row["구분"] = last_category
            else:
                last_category = row["구분"]
            rows.append(row)

        return rows, None
    except Exception as e:
        return [], f"데이터 로드 실패: {safe_str(e)}"


def make_stars(val):
    try:
        val = safe_str(val)
        if "★" in val:
            return val
        n = int(float(val)) if val else 0
        n = max(0, min(5, n))
        return "★" * n + "☆" * (5 - n)
    except:
        return "☆☆☆☆☆"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = BG
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical")

        # 상단 앱바
        header = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=56,
            padding=[16, 8],
            spacing=8,
        )
        header.canvas.before.clear()
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*PRIMARY)
            self.header_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header, size=self._update_header)

        title = Label(
            text="Smart Hub",
            color=(1, 1, 1, 1),
            font_size="18sp",
            bold=True,
            halign="left",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))

        refresh_btn = Button(
            text="↻",
            size_hint=(None, None),
            size=(40, 40),
            background_color=(1, 1, 1, 0.2),
            color=(1, 1, 1, 1),
            font_size="20sp",
        )
        refresh_btn.bind(on_press=self.load_data)

        header.add_widget(title)
        header.add_widget(refresh_btn)

        # 로딩 표시
        self.loading_label = Label(
            text="⏳ 데이터 불러오는 중...",
            color=(*DESC, 1),
            font_size="16sp",
            size_hint=(1, None),
            height=60,
        )

        # 스크롤 컨텐츠
        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=0,
            padding=[0, 0, 0, 20],
        )
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)

        root.add_widget(header)
        root.add_widget(self.loading_label)
        root.add_widget(self.scroll)

        self.add_widget(root)
        self.load_data()

    def _update_header(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def load_data(self, *args):
        self.loading_label.text = "⏳ 데이터 불러오는 중..."
        self.loading_label.opacity = 1
        self.content.clear_widgets()

        def _fetch():
            rows, err = get_data()
            Clock.schedule_once(lambda dt: self.render(rows, err))

        Thread(target=_fetch, daemon=True).start()

    def render(self, rows, err):
        self.loading_label.opacity = 0
        self.content.clear_widgets()

        if err:
            self.content.add_widget(Label(
                text=f"⚠️ {err}",
                color=(*TEXT, 1),
                font_size="14sp",
                size_hint=(1, None),
                height=60,
                halign="center",
            ))

        if not rows:
            self.content.add_widget(Label(
                text="데이터 없음",
                color=(*DESC, 1),
                font_size="14sp",
                size_hint=(1, None),
                height=60,
            ))
            return

        # 카테고리별 그룹핑
        categories = []
        cat_map = {}
        for row in rows:
            cat = safe_str(row.get("구분", "기타")) or "기타"
            if cat not in cat_map:
                cat_map[cat] = []
                categories.append(cat)
            cat_map[cat].append(row)

        for category in categories:
            # 카테고리 헤더
            cat_label = Label(
                text=f"📂 {category}",
                color=(*PRIMARY, 1),
                font_size="16sp",
                bold=True,
                size_hint=(1, None),
                height=48,
                halign="left",
                padding=[16, 0],
            )
            cat_label.bind(size=cat_label.setter("text_size"))
            self.content.add_widget(cat_label)

            # 구분선
            from kivy.uix.widget import Widget
            from kivy.graphics import Color, Rectangle
            divider = Widget(size_hint=(1, None), height=2)
            with divider.canvas:
                Color(*PRIMARY)
                Rectangle(pos=divider.pos, size=divider.size)
            divider.bind(
                pos=lambda w, v: setattr(w.canvas.children[-1], 'pos', v),
                size=lambda w, v: setattr(w.canvas.children[-1], 'size', v),
            )
            self.content.add_widget(divider)

            # 컬럼 헤더
            col_header = BoxLayout(
                orientation="horizontal",
                size_hint=(1, None),
                height=40,
                padding=[16, 4],
            )
            with col_header.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                Rectangle(pos=col_header.pos, size=col_header.size)
            col_header.bind(
                pos=lambda w, v: None,
                size=lambda w, v: None,
            )
            col_header.add_widget(Label(text="업무 내용", color=(*DESC, 1), font_size="12sp", bold=True, size_hint=(3, 1), halign="left"))
            col_header.add_widget(Label(text="활용도", color=(*DESC, 1), font_size="12sp", bold=True, size_hint=(1, 1), halign="center"))
            col_header.add_widget(Label(text="링크", color=(*DESC, 1), font_size="12sp", bold=True, size_hint=(1, 1), halign="center"))
            self.content.add_widget(col_header)

            # 데이터 행
            for row in cat_map[category]:
                try:
                    title = safe_str(row.get("내용", ""))
                    if not title or title in TRASH:
                        continue
                    desc = safe_str(row.get("기능", ""))
                    stars = make_stars(row.get("활용도", "0"))
                    link = safe_str(row.get("링크", "#")) or "#"

                    row_height = 64 if desc else 48
                    row_layout = BoxLayout(
                        orientation="horizontal",
                        size_hint=(1, None),
                        height=row_height,
                        padding=[16, 4],
                        spacing=4,
                    )

                    # 제목 + 설명
                    text_col = BoxLayout(orientation="vertical", size_hint=(3, 1))
                    title_lbl = Label(
                        text=title,
                        color=(*TEXT, 1),
                        font_size="14sp",
                        bold=True,
                        halign="left",
                        valign="middle",
                        size_hint=(1, 1),
                    )
                    title_lbl.bind(size=title_lbl.setter("text_size"))
                    text_col.add_widget(title_lbl)

                    if desc:
                        desc_lbl = Label(
                            text=desc,
                            color=(*DESC, 1),
                            font_size="11sp",
                            halign="left",
                            valign="top",
                            size_hint=(1, 1),
                        )
                        desc_lbl.bind(size=desc_lbl.setter("text_size"))
                        text_col.add_widget(desc_lbl)

                    # 별점
                    star_lbl = Label(
                        text=stars,
                        color=(*STAR, 1),
                        font_size="12sp",
                        halign="center",
                        valign="middle",
                        size_hint=(1, 1),
                    )
                    star_lbl.bind(size=star_lbl.setter("text_size"))

                    # 링크 버튼
                    def make_link_btn(url):
                        btn = Button(
                            text="🔗",
                            size_hint=(1, None),
                            height=36,
                            background_color=(0.9, 0.9, 0.9, 1),
                            color=(*TEXT, 1),
                            font_size="14sp",
                        )
                        btn.bind(on_press=lambda x, u=url: webbrowser.open(u) if u != "#" else None)
                        return btn

                    link_box = BoxLayout(size_hint=(1, 1), padding=[4, 4])
                    link_box.add_widget(make_link_btn(link))

                    row_layout.add_widget(text_col)
                    row_layout.add_widget(star_lbl)
                    row_layout.add_widget(link_box)
                    self.content.add_widget(row_layout)

                    # 행 구분선
                    div = Widget(size_hint=(1, None), height=1)
                    with div.canvas:
                        Color(0.9, 0.9, 0.9, 1)
                        Rectangle(pos=div.pos, size=div.size)
                    self.content.add_widget(div)

                except Exception:
                    continue

            self.content.add_widget(Label(size_hint=(1, None), height=20))


class SmartHubApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        return sm


if __name__ == "__main__":
    SmartHubApp().run()
