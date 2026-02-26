"""
config.py — Cadodile Jungle Trivia Configuration
Pixel-art retro game theme (Mario/Pokemon inspired).
"""

# ── Hardware Pins ──
LED_GPIO = 18
SERVO_CHANNEL = 0

# ── Servo Angles ──
SERVO_CENTER = 90
DISPENSE_OPEN_ANGLE = 140
DISPENSE_CLOSED_ANGLE = 40
DISPENSE_OPEN_TIME_SEC = 0.6
DISPENSE_PAUSE_SEC = 0.2

# ── Game Settings ──
QUESTIONS_PER_GAME = 10
MAX_PLAYERS = 4

# ── UI Colors (Pixel Game / Retro Theme) ──
COLOR_BG_DARK = "#1a1a2e"        # Deep night sky
COLOR_BG_MID = "#16213e"         # Mid dark blue
COLOR_BG_LIGHT = "#0f3460"       # Lighter blue
COLOR_ACCENT = "#e94560"         # Retro red (like Mario red)
COLOR_ACCENT_DARK = "#c23152"    # Darker red
COLOR_ACCENT_GOLD = "#f4a62a"    # Coin gold
COLOR_TEXT_LIGHT = "#ffffff"     # White text
COLOR_TEXT_DARK = "#1a1a2e"      # Dark text
COLOR_CORRECT = "#4ade80"        # Pixel green
COLOR_WRONG = "#ef4444"          # Pixel red
COLOR_BUTTON = "#3b82f6"         # Bright blue button
COLOR_BUTTON_HOVER = "#2563eb"   # Darker blue hover
COLOR_SKY_TOP = "#1a1a2e"        # Night sky top
COLOR_SKY_BOT = "#3b82f6"        # Sky bottom
COLOR_GRASS = "#22c55e"          # Bright pixel grass
COLOR_GRASS_DARK = "#16a34a"     # Darker grass
COLOR_DIRT = "#92400e"           # Dirt brown
COLOR_DIRT_DARK = "#78350f"      # Darker dirt
COLOR_BRICK = "#dc2626"          # Brick red
COLOR_BRICK_DARK = "#991b1b"     # Dark brick
COLOR_PIPE_GREEN = "#16a34a"     # Pipe green
COLOR_COIN = "#fbbf24"           # Coin yellow
COLOR_CLOUD = "#e0f2fe"          # Cloud white-blue
COLOR_STAR = "#fde047"           # Star yellow

# ── UI Sizes ──
FONT_SIZE_TITLE = 42
FONT_SIZE_HEADING = 28
FONT_SIZE_BODY = 20
FONT_SIZE_BUTTON = 24
BUTTON_HEIGHT = 62
BUTTON_RADIUS = 12

# ── Display Orientation ──
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1024
SCREEN_ORIENTATION = "vertical"
