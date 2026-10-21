import sys, asyncio
from playwright.async_api import async_playwright
SRC, OUT = sys.argv[1], sys.argv[2]; names = sys.argv[3:]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for n in names:
            await pg.goto(f"file://{SRC}/{n}.html"); await pg.wait_for_timeout(400)
            # Überlauf-Prüfung: Inhalt darf die Seite nicht sprengen
            ov = await pg.evaluate("""[...document.querySelectorAll('.page')].map(p=>{return p.scrollHeight-p.clientHeight})""")
            await pg.pdf(path=f"{OUT}/{n}-zusammenfassung.pdf", format="A4", print_background=True, prefer_css_page_size=True)
            print(n, "overflow px per page:", ov)
        await b.close()
asyncio.run(main())
