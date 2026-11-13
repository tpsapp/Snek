from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

cell_size = 32
cell_count = 20
width = cell_count * cell_size
height = cell_count * cell_size

framerate = 60
timer_rate = 125

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
overlay_bg = (0, 0, 0, 160)

font_face = str(BASE_DIR / 'Fonts' / 'ds-digi.ttf')
font_size = 32
sound_beep = str(BASE_DIR / 'Sounds' / 'beep.wav')
sound_error = str(BASE_DIR / 'Sounds' / 'error.wav')

