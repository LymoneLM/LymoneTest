import math
import pyautogui

radius = 400.0
min_angle = 0.0
max_angle = 360.0
spacing = 3
duration = 0.000
x, y = 2600.0, 320.0
pyautogui.moveTo(x + radius, y, duration)
pyautogui.mouseDown()
while min_angle < max_angle:
    min_angle += spacing
    x2 = x + radius * math.cos(min_angle * math.pi / 180.0)
    y2 = y + radius * math.sin(min_angle * math.pi / 180.0)
    pyautogui.moveTo(round(x2), round(y2), duration)
pyautogui.mouseUp()