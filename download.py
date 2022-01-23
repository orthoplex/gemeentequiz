#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re

xml = requests.get('https://www.gemeentenatlas.nl/', auth=('user', 'pass')).text
soup = BeautifulSoup(xml, "lxml")

areas = dict()

for e in soup.find_all("area"):
    title = e["title"]
    title = title.replace("%20", " ")
    title = re.sub(r"(?<=[a-z])(?=[A-Z])", "-", title)
    if title == "Korendijk":
        title = "Hoeksche Waard"
    if title == "Bussum":
        title = "Gooise Meren"
    if not title in areas:
        areas[title] = []
    area = " ".join(e["coords"].split(", "))
    areas[title].append(area)

with open("map.js", "w") as outfile:
    w = outfile.write
    w("areas={")
    for e in sorted(areas):
        w(f'"{e}":[')
        for area in areas[e]:
            w(f"'{area}',")
        w("],")
    w("};")
