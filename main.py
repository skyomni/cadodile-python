"""
main.py — Cadodile Trivia Quest
Grade 5 Math — CA Common Core — Randomized Questions
Pixel-art retro game theme. Optimized: BG renders to a small
texture and scales up, so the GPU does the heavy lifting.
Vertical touchscreen (600x1024).
"""

import random
import math

from kivy.config import Config
from config import SCREEN_WIDTH, SCREEN_HEIGHT
Config.set("graphics", "width", str(SCREEN_WIDTH))
Config.set("graphics", "height", str(SCREEN_HEIGHT))
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import (
    Color, Rectangle, RoundedRectangle, Ellipse, Line,
)
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from config import *
import hardware
from question_generator import get_chapter_list, generate_questions


def hc(h):
    return get_color_from_hex(h)

C_ACCENT = hc(COLOR_ACCENT)
C_GOLD = hc(COLOR_ACCENT_GOLD)
C_TEXT = hc(COLOR_TEXT_LIGHT)
C_OK = hc(COLOR_CORRECT)
C_BAD = hc(COLOR_WRONG)


# ─────────────────────────────────────
# PIXEL BACKGROUND — renders to small buffer, scales up
# ─────────────────────────────────────
class PixelBG(Widget):
    """
    Draws the entire scene into a tiny pixel buffer (150x256),
    then blits it scaled up to fill the screen. This is MUCH
    faster than drawing hundreds of Kivy canvas shapes every frame.
    """
    # Buffer size — the actual "pixel art" resolution
    BW, BH = 150, 256

    def __init__(self, **kw):
        super().__init__(**kw)
        self._t = 0.0
        # Pre-allocate pixel buffer (RGBA)
        self._buf = bytearray(self.BW * self.BH * 4)
        self._tex = Texture.create(size=(self.BW, self.BH), colorfmt='rgba')
        self._tex.mag_filter = 'nearest'  # Crisp pixel scaling
        self._tex.min_filter = 'nearest'

        # Pre-generate static elements
        random.seed(42)
        self._stars = [(random.randint(0, self.BW - 1),
                        random.randint(self.BH // 3, self.BH - 1),
                        random.uniform(0.5, 2.5), random.uniform(0, 6.28))
                       for _ in range(25)]
        self._clouds = [(random.randint(0, self.BW), random.randint(self.BH * 2 // 3, self.BH - 20),
                         random.randint(15, 28)) for _ in range(4)]
        self._coins = [(random.randint(15, self.BW - 15), random.randint(self.BH // 3, self.BH * 2 // 3),
                        random.uniform(0, 6.28)) for _ in range(5)]
        random.seed()

        self.bind(size=self._redraw, pos=self._redraw)
        Clock.schedule_interval(self._tick, 1 / 20.0)  # 20 FPS for BG is plenty

    def _tick(self, dt):
        self._t += dt
        self._render_buffer()
        self._redraw()

    def _px(self, x, y, r, g, b, a=255):
        """Set a pixel in the buffer. Origin = bottom-left."""
        x, y = int(x), int(y)
        if 0 <= x < self.BW and 0 <= y < self.BH:
            i = (y * self.BW + x) * 4
            self._buf[i] = r
            self._buf[i + 1] = g
            self._buf[i + 2] = b
            self._buf[i + 3] = a

    def _rect(self, x, y, w, h, r, g, b, a=255):
        """Draw a filled rectangle in the buffer."""
        x0, y0 = max(0, int(x)), max(0, int(y))
        x1 = min(self.BW, int(x + w))
        y1 = min(self.BH, int(y + h))
        for py in range(y0, y1):
            row = py * self.BW
            for px in range(x0, x1):
                i = (row + px) * 4
                self._buf[i] = r
                self._buf[i + 1] = g
                self._buf[i + 2] = b
                self._buf[i + 3] = a

    def _ellipse(self, cx, cy, rx, ry, r, g, b, a=255):
        """Draw a filled ellipse."""
        x0 = max(0, int(cx - rx))
        x1 = min(self.BW, int(cx + rx))
        y0 = max(0, int(cy - ry))
        y1 = min(self.BH, int(cy + ry))
        for py in range(y0, y1):
            dy = (py - cy) / max(ry, 0.1)
            for px in range(x0, x1):
                dx = (px - cx) / max(rx, 0.1)
                if dx * dx + dy * dy <= 1.0:
                    i = (py * self.BW + px) * 4
                    self._buf[i] = r
                    self._buf[i + 1] = g
                    self._buf[i + 2] = b
                    self._buf[i + 3] = a

    def _render_buffer(self):
        """Render entire pixel scene into the byte buffer."""
        BW, BH = self.BW, self.BH
        t = self._t
        buf = self._buf

        # ── Clear with sky gradient ──
        for y in range(BH):
            frac = y / BH
            r = int(26 + frac * 33)
            g = int(26 + frac * 55)
            b = int(46 + frac * 100)
            row = y * BW
            for x in range(BW):
                i = (row + x) * 4
                buf[i] = r; buf[i+1] = g; buf[i+2] = b; buf[i+3] = 255

        # ── Stars ──
        for sx, sy, spd, ph in self._stars:
            alpha = math.sin(t * spd + ph)
            if alpha > 0.2:
                self._px(sx, sy, 255, 255, 230)
                if alpha > 0.7:
                    self._px(sx + 1, sy, 255, 255, 200)

        # ── Moon ──
        mx, my = BW - 18, BH - 18
        self._ellipse(mx, my, 6, 6, 250, 250, 220)
        self._ellipse(mx + 2, my + 1, 4, 4, 255, 255, 235)

        # ── Clouds (blocky) ──
        for cx0, cy0, cw in self._clouds:
            cx = int((cx0 + t * 3) % (BW + cw)) - cw // 2
            bw = cw // 4
            self._rect(cx, cy0, cw, bw, 255, 255, 255, 40)
            self._rect(cx + bw, cy0 + bw, cw - bw * 2, bw, 255, 255, 255, 35)
            self._rect(cx + 2, cy0 - bw, cw - 4, bw, 255, 255, 255, 30)

        # ── Distant hills ──
        for i in range(0, BW + 20, 20):
            hh = int(18 + math.sin(i * 0.08) * 8)
            hy = int(BH * 0.28)
            self._ellipse(i, hy + hh // 2, 16, hh // 2, 30, 58, 95)

        # ── Ground ──
        gt = int(BH * 0.22)  # ground top y
        # Dirt fill
        self._rect(0, 0, BW, gt, 146, 64, 14)
        # Dark dirt bottom
        self._rect(0, 0, BW, int(BH * 0.07), 120, 53, 15)
        # Dirt texture
        for i in range(0, BW, 6):
            for j in range(0, gt - 4, 6):
                if (i + j) % 12 == 0:
                    self._px(i, j, 115, 55, 10)

        # Grass strip
        self._rect(0, gt - 2, BW, 5, 34, 197, 94)
        self._rect(0, gt + 3, BW, 2, 22, 163, 74)

        # Grass tufts
        for i in range(0, BW, 6):
            bob = int(math.sin(t * 2 + i * 0.4) * 1.5)
            self._rect(i, gt + 5 + bob, 2, 4, 74, 222, 128)
            self._rect(i + 3, gt + 4 + bob, 2, 3, 34, 197, 94)

        # ── Brick blocks ──
        self._draw_brick(12, int(BH * 0.38))
        self._draw_brick(BW - 22, int(BH * 0.42))

        # ── Question block ──
        self._draw_qblock(BW // 2 - 5, int(BH * 0.36), t)

        # ── Pipes ──
        self._draw_pipe(4, gt + 3, 12, 22)
        self._draw_pipe(BW - 18, gt + 3, 12, 17)

        # ── Coins ──
        for cx, cy, ph in self._coins:
            cy2 = int(cy + math.sin(t * 2.5 + ph) * 3)
            stretch = abs(math.sin(t * 1.8 + ph))
            cw = max(1, int(4 * stretch))
            ox = (4 - cw) // 2
            self._rect(cx + ox, cy2, cw, 5, 251, 191, 36)
            if cw > 2:
                self._rect(cx + ox + 1, cy2 + 1, cw - 2, 3, 245, 158, 11)

        # ── Bushes ──
        for bx in range(10, BW, 30):
            bob = int(math.sin(t * 1.2 + bx * 0.2) * 1)
            self._ellipse(bx + 5, gt + 8 + bob, 6, 4, 34, 197, 94)
            self._ellipse(bx + 5, gt + 9 + bob, 4, 3, 22, 163, 74)

        # ── Character ──
        self._draw_char(BW // 2 - 4, gt + 5, t)

        # Upload buffer to texture
        self._tex.blit_buffer(bytes(self._buf), colorfmt='rgba', bufferfmt='ubyte')

    def _draw_brick(self, bx, by):
        sz = 10
        self._rect(bx, by, sz, sz, 220, 38, 38)
        self._rect(bx, by + sz // 2, sz, 1, 153, 27, 27)
        self._rect(bx + sz // 2, by, 1, sz, 153, 27, 27)
        # Highlight
        self._rect(bx, by + sz - 1, sz, 1, 255, 80, 80)

    def _draw_qblock(self, bx, by, t):
        sz = 10
        self._rect(bx, by, sz, sz, 251, 191, 36)
        # Border
        self._rect(bx, by, sz, 1, 180, 83, 9)
        self._rect(bx, by + sz - 1, sz, 1, 180, 83, 9)
        self._rect(bx, by, 1, sz, 180, 83, 9)
        self._rect(bx + sz - 1, by, 1, sz, 180, 83, 9)
        # ? mark
        self._rect(bx + 3, by + sz - 3, 4, 1, 26, 26, 46)
        self._rect(bx + 5, by + sz - 5, 2, 2, 26, 26, 46)
        self._rect(bx + 4, by + sz - 6, 3, 1, 26, 26, 46)
        self._px(bx + 4, by + 2, 26, 26, 46)  # dot
        # Shimmer
        if math.sin(t * 4) > 0.5:
            self._px(bx + 1, by + sz - 2, 255, 255, 255)

    def _draw_pipe(self, px, py, pw, ph):
        self._rect(px + 2, py, pw - 4, ph, 22, 163, 74)
        self._rect(px, py + ph - 4, pw, 5, 21, 128, 61)
        # Highlight
        self._rect(px + 3, py, 2, ph, 34, 197, 94, 120)

    def _draw_char(self, cx, cy, t):
        bounce = int(abs(math.sin(t * 2.5)) * 2)
        cy += bounce
        # Shadow
        self._rect(cx, cy - bounce - 1, 8, 2, 0, 0, 0, 50)
        # Feet
        self._rect(cx, cy, 3, 2, 146, 64, 14)
        self._rect(cx + 5, cy, 3, 2, 146, 64, 14)
        # Body (blue)
        self._rect(cx + 1, cy + 2, 6, 5, 59, 130, 246)
        # Head (gold/skin)
        self._rect(cx + 1, cy + 7, 6, 5, 251, 191, 36)
        # Hat (red)
        self._rect(cx, cy + 12, 8, 3, 233, 69, 96)
        self._rect(cx + 1, cy + 15, 6, 2, 233, 69, 96)
        # Eyes
        blink = math.sin(t * 1.5) > -0.9
        if blink:
            self._px(cx + 2, cy + 9, 255, 255, 255)
            self._px(cx + 5, cy + 9, 255, 255, 255)
            self._px(cx + 2, cy + 8, 0, 0, 0)
            self._px(cx + 5, cy + 8, 0, 0, 0)
        else:
            self._px(cx + 2, cy + 9, 0, 0, 0)
            self._px(cx + 5, cy + 9, 0, 0, 0)

    def _redraw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(texture=self._tex, pos=self.pos, size=self.size)


# ─────────────────────────────────────
# PIXEL STYLED BUTTON
# ─────────────────────────────────────
class PixelButton(Button):
    def __init__(self, bg_color=COLOR_BUTTON, text_color=COLOR_TEXT_LIGHT, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = hc(text_color)
        self.font_size = dp(FONT_SIZE_BUTTON)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(BUTTON_HEIGHT)
        self._bg = hc(bg_color)
        self._pr = hc(COLOR_BUTTON_HOVER)
        self.bind(pos=self._u, size=self._u, state=self._u)
        Clock.schedule_once(self._u, 0)

    def _u(self, *a):
        self.canvas.before.clear()
        c = self._pr if self.state == "down" else self._bg
        with self.canvas.before:
            Color(0, 0, 0, 0.35)
            RoundedRectangle(pos=(self.x + 3, self.y - 3),
                             size=self.size, radius=[dp(BUTTON_RADIUS)])
            Color(*c)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(BUTTON_RADIUS)])
            Color(1, 1, 1, 0.18)
            RoundedRectangle(pos=(self.x + 2, self.y + self.height * 0.5),
                             size=(self.width - 4, self.height * 0.48),
                             radius=[dp(BUTTON_RADIUS - 2), dp(BUTTON_RADIUS - 2), 0, 0])


class ChapterCard(Button):
    def __init__(self, ch_data, bg_color=COLOR_BG_LIGHT, **kw):
        super().__init__(**kw)
        self.ch_data = ch_data
        self.text = (f"[b]{ch_data['icon']}[/b]\n"
                     f"[b]{ch_data['title']}[/b]\n"
                     f"[size=13]{ch_data['subtitle']}[/size]")
        self.markup = True
        self.halign = "center"
        self.valign = "middle"
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = hc(COLOR_TEXT_LIGHT)
        self.font_size = dp(17)
        self.size_hint_y = None
        self.height = dp(110)
        self._bg = hc(bg_color)
        self._pr = hc(COLOR_BUTTON_HOVER)
        self.bind(pos=self._u, size=self._u, state=self._u)
        Clock.schedule_once(lambda dt: setattr(self, "text_size",
                                                (self.width - dp(20), None)), 0)
        Clock.schedule_once(self._u, 0)

    def _u(self, *a):
        self.canvas.before.clear()
        c = self._pr if self.state == "down" else self._bg
        with self.canvas.before:
            Color(0, 0, 0, 0.3)
            RoundedRectangle(pos=(self.x + 3, self.y - 3),
                             size=self.size, radius=[dp(10)])
            Color(*c)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(*hc(COLOR_COIN))
            RoundedRectangle(pos=(self.x, self.y + self.height - dp(4)),
                             size=(self.width, dp(4)),
                             radius=[dp(10), dp(10), 0, 0])
            Color(1, 1, 1, 0.06)
            RoundedRectangle(pos=(self.x + 2, self.y + self.height * 0.5),
                             size=(self.width - 4, self.height * 0.48),
                             radius=[dp(8), dp(8), 0, 0])


class PixelScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bg = PixelBG()
        self.add_widget(self.bg)

    def add_content(self, w):
        self.add_widget(w)


def make_title(text, size=FONT_SIZE_TITLE, color=COLOR_ACCENT_GOLD):
    lbl = Label(text=text, font_size=dp(size), bold=True,
                color=hc(color), halign="center", valign="middle")
    lbl.bind(size=lbl.setter("text_size"))
    return lbl


# ─────────────────────────────────────
# SPLASH
# ─────────────────────────────────────
class SplashScreen(PixelScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        ly = BoxLayout(orientation="vertical", spacing=dp(16),
                       padding=[dp(40), dp(50), dp(40), dp(40)])
        ly.add_widget(Widget(size_hint_y=0.10))
        t = make_title("CADODILE\nTRIVIA\nQUEST", size=48)
        t.size_hint_y = 0.28
        ly.add_widget(t)
        ly.add_widget(Label(text="Grade 5 Math Adventure!", font_size=dp(18),
                            color=hc(COLOR_COIN), size_hint_y=0.05))
        ly.add_widget(Label(text="Randomized Questions Every Time", font_size=dp(14),
                            color=hc("#94a3b8"), size_hint_y=0.04))
        ly.add_widget(Widget(size_hint_y=0.06))
        b1 = PixelButton(text=">> SINGLEPLAYER <<", bg_color=COLOR_BUTTON)
        b1.bind(on_release=lambda x: self._go("single"))
        ly.add_widget(b1)
        ly.add_widget(Widget(size_hint_y=0.015))
        b2 = PixelButton(text=">> MULTIPLAYER <<", bg_color=COLOR_ACCENT)
        b2.bind(on_release=lambda x: setattr(self.manager, "current", "mp_setup"))
        ly.add_widget(b2)
        ly.add_widget(Widget(size_hint_y=0.015))
        b3 = PixelButton(text="SETTINGS", bg_color="#475569")
        b3.bind(on_release=lambda x: setattr(self.manager, "current", "settings"))
        ly.add_widget(b3)
        ly.add_widget(Widget(size_hint_y=0.16))
        ly.add_widget(Label(text="SELECT A MODE TO BEGIN", font_size=dp(13),
                            color=hc("#64748b"), size_hint_y=0.04))
        ly.add_widget(Widget(size_hint_y=0.03))
        self.add_content(ly)

    def _go(self, mode):
        app = App.get_running_app()
        app.pending_mode = mode
        app.pending_players = 1
        self.manager.current = "chapters"


# ─────────────────────────────────────
# MULTIPLAYER SETUP
# ─────────────────────────────────────
class MPSetupScreen(PixelScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.num = 2
        ly = BoxLayout(orientation="vertical", spacing=dp(16),
                       padding=[dp(50), dp(70), dp(50), dp(40)])
        ly.add_widget(Widget(size_hint_y=0.06))
        t = make_title("MULTIPLAYER\nSETUP", size=40)
        t.size_hint_y = 0.14
        ly.add_widget(t)
        ly.add_widget(Widget(size_hint_y=0.04))
        self.cl = Label(text="PLAYERS: 2", font_size=dp(FONT_SIZE_HEADING), bold=True,
                        color=hc(COLOR_COIN), size_hint_y=0.07)
        ly.add_widget(self.cl)
        row = BoxLayout(orientation="horizontal", spacing=dp(10),
                        size_hint_y=None, height=dp(BUTTON_HEIGHT))
        for n in range(2, MAX_PLAYERS + 1):
            b = PixelButton(text=str(n), bg_color=COLOR_ACCENT if n == 2 else COLOR_BG_LIGHT)
            b.pn = n
            b.bind(on_release=self._set)
            row.add_widget(b)
        ly.add_widget(row)
        ly.add_widget(Widget(size_hint_y=0.08))
        bn = PixelButton(text=">> CHOOSE CHAPTER <<", bg_color=COLOR_BUTTON)
        bn.bind(on_release=lambda x: self._go())
        ly.add_widget(bn)
        ly.add_widget(Widget(size_hint_y=0.02))
        bb = PixelButton(text="BACK", bg_color="#475569")
        bb.bind(on_release=lambda x: setattr(self.manager, "current", "splash"))
        ly.add_widget(bb)
        ly.add_widget(Widget(size_hint_y=0.2))
        self.add_content(ly)

    def _set(self, btn):
        self.num = btn.pn
        self.cl.text = f"PLAYERS: {self.num}"

    def _go(self):
        app = App.get_running_app()
        app.pending_mode = "multi"
        app.pending_players = self.num
        self.manager.current = "chapters"


# ─────────────────────────────────────
# CHAPTER SELECT
# ─────────────────────────────────────
class ChapterScreen(PixelScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._built = False

    def on_enter(self, *a):
        if not self._built:
            self._build()
            self._built = True

    def _build(self):
        chapters = get_chapter_list()
        ly = BoxLayout(orientation="vertical", spacing=dp(8),
                       padding=[dp(25), dp(25), dp(25), dp(15)])
        t = make_title("SELECT CHAPTER", size=36)
        t.size_hint_y = None; t.height = dp(50)
        ly.add_widget(t)
        ly.add_widget(Label(text="New random questions each game!",
                            font_size=dp(14), color=hc("#94a3b8"),
                            size_hint_y=None, height=dp(20)))
        ly.add_widget(Widget(size_hint_y=None, height=dp(6)))
        sv = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        cl = BoxLayout(orientation="vertical", spacing=dp(10),
                       size_hint_y=None, padding=[dp(4), dp(4), dp(4), dp(4)])
        cl.bind(minimum_height=cl.setter("height"))
        ac = ChapterCard(ch_data={"id": "all", "title": "ALL CHAPTERS (Mixed)",
                                   "subtitle": "Random from every topic", "icon": "ALL"},
                         bg_color=COLOR_ACCENT_DARK)
        ac.bind(on_release=lambda x: self._pick("all"))
        cl.add_widget(ac)
        bgs = [COLOR_BG_LIGHT, COLOR_BG_MID]
        for i, ch in enumerate(chapters):
            cd = ChapterCard(ch_data=ch, bg_color=bgs[i % 2])
            cd.bind(on_release=lambda x, cid=ch["id"]: self._pick(cid))
            cl.add_widget(cd)
        sv.add_widget(cl)
        ly.add_widget(sv)
        ly.add_widget(Widget(size_hint_y=None, height=dp(6)))
        bb = PixelButton(text="BACK", bg_color="#475569")
        bb.bind(on_release=lambda x: setattr(self.manager, "current", "splash"))
        ly.add_widget(bb)
        ly.add_widget(Widget(size_hint_y=None, height=dp(6)))
        self.add_content(ly)

    def _pick(self, cid):
        app = App.get_running_app()
        app.start_game(mode=app.pending_mode, num_players=app.pending_players, chapter_id=cid)


# ─────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────
class SettingsScreen(PixelScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        ly = BoxLayout(orientation="vertical", spacing=dp(11),
                       padding=[dp(50), dp(55), dp(50), dp(35)])
        ly.add_widget(Widget(size_hint_y=0.02))
        t = make_title("SETTINGS", size=38); t.size_hint_y = 0.07
        ly.add_widget(t)
        ly.add_widget(Widget(size_hint_y=0.03))
        self.stub_l = Label(text="STUB MODE: ON", font_size=dp(FONT_SIZE_BODY), bold=True,
                            color=hc(COLOR_COIN), size_hint_y=0.04)
        ly.add_widget(self.stub_l)
        bs = PixelButton(text="TOGGLE STUB MODE", bg_color=COLOR_BG_LIGHT)
        bs.bind(on_release=self._ts)
        ly.add_widget(bs)
        ly.add_widget(Widget(size_hint_y=0.015))
        self.snd_l = Label(text="SOUND: ON (PLACEHOLDER)", font_size=dp(FONT_SIZE_BODY), bold=True,
                           color=hc(COLOR_COIN), size_hint_y=0.04)
        ly.add_widget(self.snd_l)
        bsn = PixelButton(text="TOGGLE SOUND", bg_color=COLOR_BG_LIGHT)
        bsn.bind(on_release=self._tsn)
        ly.add_widget(bsn)
        ly.add_widget(Widget(size_hint_y=0.015))
        ly.add_widget(Label(text="UI BRIGHTNESS", font_size=dp(FONT_SIZE_BODY), bold=True,
                            color=hc(COLOR_COIN), size_hint_y=0.04))
        sl = Slider(min=0.3, max=1.0, value=1.0, size_hint_y=None, height=dp(38))
        sl.bind(value=lambda s, v: setattr(Window, "clearcolor", (0, 0, 0, 1.0 - v * 0.7)))
        ly.add_widget(sl)
        ly.add_widget(Widget(size_hint_y=0.02))
        bt = PixelButton(text="TEST DISPENSE", bg_color=COLOR_ACCENT)
        bt.bind(on_release=lambda x: hardware.dispense_block())
        ly.add_widget(bt)
        ly.add_widget(Widget(size_hint_y=0.03))
        bb = PixelButton(text="BACK", bg_color="#475569")
        bb.bind(on_release=lambda x: setattr(self.manager, "current", "splash"))
        ly.add_widget(bb)
        ly.add_widget(Widget(size_hint_y=0.1))
        self.add_content(ly)
        self._stub = True; self._snd = True

    def _ts(self, *a):
        self._stub = not self._stub
        self.stub_l.text = f"STUB MODE: {'ON' if self._stub else 'OFF'}"
        hardware.init_hardware(stub_mode=self._stub)

    def _tsn(self, *a):
        self._snd = not self._snd
        self.snd_l.text = f"SOUND: {'ON' if self._snd else 'OFF'} (PLACEHOLDER)"


# ─────────────────────────────────────
# TRIVIA
# ─────────────────────────────────────
class TriviaScreen(PixelScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ly = BoxLayout(orientation="vertical", spacing=dp(10),
                            padding=[dp(30), dp(35), dp(30), dp(25)])
        self.header = Label(text="", font_size=dp(16), color=hc(COLOR_COIN), bold=True,
                            size_hint_y=0.05, halign="center")
        self.header.bind(size=self.header.setter("text_size"))
        self.ly.add_widget(self.header)
        self.ch_label = Label(text="", font_size=dp(13), color=hc("#94a3b8"),
                              size_hint_y=0.025, halign="center")
        self.ch_label.bind(size=self.ch_label.setter("text_size"))
        self.ly.add_widget(self.ch_label)
        self.cnt_label = Label(text="", font_size=dp(14), color=hc("#cbd5e1"),
                               size_hint_y=0.025)
        self.ly.add_widget(self.cnt_label)
        self.ly.add_widget(Widget(size_hint_y=0.015))
        self.q_label = Label(text="", font_size=dp(FONT_SIZE_HEADING), bold=True,
                             color=C_TEXT, halign="center", valign="middle", size_hint_y=0.22)
        self.q_label.bind(size=self.q_label.setter("text_size"))
        self.ly.add_widget(self.q_label)
        self.ly.add_widget(Widget(size_hint_y=0.02))
        self.ans_box = BoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=0.43)
        self.ly.add_widget(self.ans_box)
        self.fb_label = Label(text="", font_size=dp(FONT_SIZE_HEADING), bold=True,
                              color=C_TEXT, size_hint_y=0.08)
        self.ly.add_widget(self.fb_label)
        self.ly.add_widget(Widget(size_hint_y=0.04))
        self.add_content(self.ly)

    def on_enter(self, *a):
        self._show()

    def _show(self):
        app = App.get_running_app()
        q = app.get_current_question()
        if q is None:
            self.manager.current = "end"; return
        self.fb_label.text = ""
        self.ch_label.text = app.sel_chapter_title
        if app.game_mode == "single":
            self.header.text = f"SCORE: {app.scores[0]}"
        else:
            sc = "  ".join(f"P{i+1}:{s}" for i, s in enumerate(app.scores))
            self.header.text = f"PLAYER {app.current_player + 1}'S TURN  |  {sc}"
        self.cnt_label.text = f"Q {app.q_idx + 1} / {app.total_q}"
        self.q_label.text = q["question"]
        self.ans_box.clear_widgets()
        choices = ["True", "False"] if q["type"] == "true_false" else list(q["choices"])
        colors = [COLOR_BUTTON, COLOR_ACCENT, "#7c3aed", "#0891b2"]
        for i, ch in enumerate(choices):
            b = PixelButton(text=ch, bg_color=colors[i % len(colors)])
            b.bind(on_release=lambda btn, c=ch: self._ans(c))
            self.ans_box.add_widget(b)
        for _ in range(4 - len(choices)):
            self.ans_box.add_widget(Widget())

    def _ans(self, chosen):
        app = App.get_running_app()
        ans = app.get_current_question()["answer"]
        ok = chosen == ans
        for ch in self.ans_box.children:
            if isinstance(ch, Button):
                ch.disabled = True
        if ok:
            app.scores[app.current_player] += 1
            self.fb_label.color = C_OK
            self.fb_label.text = "CORRECT! +1 COIN!"
            hardware.dispense_block()
            hardware.blink_led(1.0)
        else:
            self.fb_label.color = C_BAD
            self.fb_label.text = f"WRONG!\nAnswer: {ans}"
        Clock.schedule_once(self._nxt, 2.0)

    def _nxt(self, dt):
        app = App.get_running_app()
        app.advance()
        if app.q_idx >= app.total_q:
            self.manager.current = "end"
        else:
            self._show()


# ─────────────────────────────────────
# END SCREEN
# ─────────────────────────────────────
class EndScreen(PixelScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ly = BoxLayout(orientation="vertical", spacing=dp(16),
                            padding=[dp(50), dp(70), dp(50), dp(40)])
        self.ly.add_widget(Widget(size_hint_y=0.08))
        self.tl = make_title("GAME OVER!", size=44)
        self.tl.size_hint_y = 0.10
        self.ly.add_widget(self.tl)
        self.sl = Label(text="", font_size=dp(FONT_SIZE_HEADING), color=C_TEXT,
                        halign="center", valign="middle", size_hint_y=0.22)
        self.sl.bind(size=self.sl.setter("text_size"))
        self.ly.add_widget(self.sl)
        self.ly.add_widget(Widget(size_hint_y=0.04))
        ba = PixelButton(text=">> PLAY AGAIN (NEW Qs) <<", bg_color=COLOR_BUTTON)
        ba.bind(on_release=lambda x: self._again())
        self.ly.add_widget(ba)
        self.ly.add_widget(Widget(size_hint_y=0.015))
        bc = PixelButton(text="PICK CHAPTER", bg_color=COLOR_ACCENT)
        bc.bind(on_release=lambda x: setattr(self.manager, "current", "chapters"))
        self.ly.add_widget(bc)
        self.ly.add_widget(Widget(size_hint_y=0.015))
        bh = PixelButton(text="HOME", bg_color="#475569")
        bh.bind(on_release=lambda x: setattr(self.manager, "current", "splash"))
        self.ly.add_widget(bh)
        self.ly.add_widget(Widget(size_hint_y=0.18))
        self.add_content(self.ly)

    def on_enter(self, *a):
        app = App.get_running_app()
        if app.game_mode == "single":
            self.sl.text = f"FINAL SCORE\n{app.scores[0]} / {app.total_q} COINS"
            r = app.scores[0] / max(app.total_q, 1)
            self.tl.text = "PERFECT RUN!" if r == 1 else "GREAT JOB!" if r >= 0.7 else "GAME OVER!"
        else:
            lines = [f"P{i+1}: {s} COINS" for i, s in enumerate(app.scores)]
            w = max(range(len(app.scores)), key=lambda i: app.scores[i])
            lines.append(f"\nPLAYER {w+1} WINS!")
            self.sl.text = "\n".join(lines)
            self.tl.text = "FINAL SCORES"

    def _again(self):
        app = App.get_running_app()
        app.start_game(mode=app.game_mode, num_players=len(app.scores),
                       chapter_id=app.sel_chapter_id)


# ─────────────────────────────────────
# APP
# ─────────────────────────────────────
class CadodileApp(App):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.game_questions = []
        self.q_idx = 0
        self.total_q = QUESTIONS_PER_GAME
        self.scores = [0]
        self.current_player = 0
        self.game_mode = "single"
        self.pending_mode = "single"
        self.pending_players = 1
        self.sel_chapter_id = "all"
        self.sel_chapter_title = "All Chapters"

    def build(self):
        self.title = "Cadodile Trivia Quest"
        hardware.init_hardware(stub_mode=True)
        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MPSetupScreen(name="mp_setup"))
        sm.add_widget(ChapterScreen(name="chapters"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(TriviaScreen(name="trivia"))
        sm.add_widget(EndScreen(name="end"))
        return sm

    def start_game(self, mode="single", num_players=1, chapter_id="all"):
        self.game_mode = mode
        self.scores = [0] * num_players
        self.current_player = 0
        self.q_idx = 0
        self.sel_chapter_id = chapter_id
        if chapter_id == "all":
            self.sel_chapter_title = "ALL CHAPTERS (MIXED)"
        else:
            for ch in get_chapter_list():
                if ch["id"] == chapter_id:
                    self.sel_chapter_title = ch["title"]; break
        self.game_questions = generate_questions(chapter_id, QUESTIONS_PER_GAME)
        self.total_q = len(self.game_questions)
        self.root.current = "trivia"

    def get_current_question(self):
        if self.q_idx >= len(self.game_questions):
            return None
        return self.game_questions[self.q_idx]

    def advance(self):
        self.q_idx += 1
        if self.game_mode == "multi":
            self.current_player = (self.current_player + 1) % len(self.scores)

    def on_stop(self):
        hardware.stop_all()


if __name__ == "__main__":
    CadodileApp().run()
