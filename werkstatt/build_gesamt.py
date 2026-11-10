import asyncio, pathlib, sys
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter
import copy
REPO = pathlib.Path(sys.argv[1]); W = REPO/"werkstatt"/"pdf"; P = REPO/"pdf"; TMP = pathlib.Path(sys.argv[2])
async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for n in ["gesamt-extra","overlay"]:
            await pg.goto(f"file://{W}/{n}.html"); await pg.wait_for_timeout(300)
            ov = await pg.evaluate("[...document.querySelectorAll('.page')].map(p=>p.scrollHeight-p.clientHeight)")
            print(n, "overflow", ov)
            await pg.pdf(path=str(TMP/f"{n}.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(render())
extra = PdfReader(TMP/"gesamt-extra.pdf"); strip = PdfReader(TMP/"overlay.pdf").pages[0]
w = PdfWriter()
w.add_page(extra.pages[0])
for n in ["nation-im-kopf","gene-ohne-reisepass","nationalismus-demokratie"]:
    for pg in PdfReader(P/f"{n}-zusammenfassung.pdf").pages: w.add_page(pg)
w.add_page(extra.pages[1])
for pg in PdfReader(P/"erfundene-traditionen-zusammenfassung.pdf").pages:
    np = w.add_page(pg); np.merge_page(strip)
w.add_metadata({"/Title":"Nationalismus – Gesamtzusammenfassung","/Author":"Mario Walter"})
with open(P/"gesamtzusammenfassung-nationalismus.pdf","wb") as f: w.write(f)
print("pages", len(w.pages))
