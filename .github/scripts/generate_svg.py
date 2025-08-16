import requests
from datetime import datetime, UTC
import os

BIRTHDATE = datetime(2011, 11, 14, tzinfo=UTC)
USERNAME = "KadenDaya"
LIGHT_TEMPLATE = "../template_light_mode.svg"
DARK_TEMPLATE = "../template_dark_mode.svg"
LIGHT_OUTPUT = "../light_mode.svg"
DARK_OUTPUT = "../dark_mode.svg"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def Calc_Age():
    now = datetime.now(UTC)
    delta = now - BIRTHDATE
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = delta.days % 30
    return [f"{years:02d}", f"{months:02d}", f"{days:02d}"]

def generate_svg():
    age = Calc_Age()
    
    with open(LIGHT_TEMPLATE, "r") as file:
        svg_light = file.read()
    
    with open(DARK_TEMPLATE, "r") as file:
        svg_dark = file.read()

    svg_light = svg_light.replace("{{YEARS}}", age[0])
    svg_light = svg_light.replace("{{MONTHS}}", age[1])
    svg_light = svg_light.replace("{{DAYS}}", age[2])

    svg_dark = svg_dark.replace("{{YEARS}}", age[0])
    svg_dark = svg_dark.replace("{{MONTHS}}", age[1])
    svg_dark = svg_dark.replace("{{DAYS}}", age[2])

    with open(LIGHT_OUTPUT, "w") as file:
        file.write(svg_light)

    with open(DARK_OUTPUT, "w") as file:
        file.write(svg_dark)

if __name__ == "__main__":
    generate_svg()