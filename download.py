#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re

xml = requests.get('https://www.gemeentenatlas.nl/').text
soup = BeautifulSoup(xml, "lxml")

areas = dict()

for match in soup.find_all("area"):
    name = match["title"]

    # clean-up and corrections
    name = name.replace("%20", " ")
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", "-", name)
    if name == "Korendijk":
        name = "Hoeksche Waard"
    if name == "Bussum":
        name = "Gooise Meren"
    if not name in areas:
        areas[name] = []

    area = " ".join(match["coords"].split(", "))
    areas[name].append(area)

with open("map.js", "w") as outfile:
    w = outfile.write
    w("areas={")
    for name in sorted(areas):
        w(f'"{name}":[')
        for area in areas[name]:
            w(f"'{area}',")
        w("],")
    w("};")
