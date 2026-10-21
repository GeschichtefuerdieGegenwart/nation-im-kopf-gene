#!/usr/bin/env python3
"""Baut die Vertiefungsmodule: setzt Basis-CSS, Kopfzeile, Modulübersicht und gemeinsames JS ein."""
import re, sys, pathlib

SRC = pathlib.Path(sys.argv[1])
REPO = pathlib.Path(sys.argv[2])

base_css = re.search(r"<style>(.*?)</style>", (REPO / "gene-ohne-reisepass.html").read_text(encoding="utf-8"), re.S).group(1)
if "/* === Gemeinsame Erweiterungen" in base_css:
    base_css = base_css.split("/* === Gemeinsame Erweiterungen")[0]
extra_css = (SRC / "extra.css").read_text(encoding="utf-8")

MODULES = [
    ("index.html", "Lernlabor „Nation im Kopf“", "Leitfrage, vier Theorien, Länderfälle und Abschlussurteil", None),
    ("gene-ohne-reisepass.html", "Gene ohne Reisepass", "DNA, Abstammung und Nation: Was zeigt die Forschung?", "pdf/gene-ohne-reisepass-zusammenfassung.pdf"),
    ("erfundene-traditionen.html", "Erfundene Traditionen", "Hobsbawm und Smith am Kaiserreich, an Frankreich und Schottland", "pdf/erfundene-traditionen-zusammenfassung.pdf"),
    ("nationalismus-demokratie.html", "Nationalismus als Gefahr für die Demokratie?", "Begriffe, Kipp-Punkte, Grundgesetz und Urteilsbildung", "pdf/nationalismus-demokratie-zusammenfassung.pdf"),
]

PAGES = {
    "erfundene-traditionen.html": dict(
        brand="Erfundene Traditionen",
        toc=[("schaetzen", "Schätzen"), ("these", "These"), ("kaiserreich", "Kaiserreich"), ("vergleich", "Vergleich"), ("duell", "Duell"), ("gegenwart", "Gegenwart"), ("aufgaben", "Aufgaben"), ("check", "Check")],
        icon='<path d="M12 3v18M5 21h14M7 8h10M9 3h6"/>',
    ),
    "nationalismus-demokratie.html": dict(
        brand="Nationalismus & Demokratie",
        toc=[("begriffe", "Begriffe"), ("ambivalenz", "Ambivalenz"), ("kipppunkte", "Kipp-Punkte"), ("grundgesetz", "Grundgesetz"), ("volk", "Wer ist das Volk?"), ("gegenwart", "Gegenwart"), ("kontroverse", "Kontroverse"), ("urteil", "Urteil"), ("aufgaben", "Aufgaben"), ("check", "Check")],
        icon='<path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/>',
    ),
}

PDF_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M12 12v6M9 15l3 3 3-3"/></svg>'
HOME = '<a class="icon-btn home-btn" href="index.html" aria-label="Zurück zum Lernlabor „Nation im Kopf“" title="Zum Lernlabor"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></svg></a>'
THEME = '<button class="icon-btn" id="themeBtn" aria-label="Hell/Dunkel wechseln" title="Hell/Dunkel"><svg id="themeIcon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button>'


def pdf_of(fname):
    return next(m[3] for m in MODULES if m[0] == fname)


def pdf_link(fname, cls="pdf-btn"):
    return f'<a class="{cls}" href="{pdf_of(fname)}" download aria-label="Zusammenfassung als PDF herunterladen" title="Zusammenfassung als PDF">{PDF_ICON}<span>PDF</span></a>'


def header(fname):
    p = PAGES[fname]
    toc = "".join(f'<a href="#{i}">{t}</a>' for i, t in p["toc"])
    return f'''<header class="appbar"><div class="appbar-inner">
 <div class="brand"><svg class="mark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">{p["icon"]}</svg><div><span>{p["brand"]}</span><small>Vertiefung zu „Nation im Kopf“</small></div></div>
 <nav class="toc" aria-label="Abschnitte">{toc}</nav>
 {HOME}
 {pdf_link(fname)}
 {THEME}
 <div class="read-bar" id="readBar"></div>
</div></header>'''


def modules_section(current):
    cur_cls, cur_attr = " current", ' aria-current="page"'
    cards = "".join(
        f'<a class="module-card{cur_cls if f == current else ""}" href="{f}"{cur_attr if f == current else ""}><b>{t}</b><span>{d}</span></a>'
        for f, t, d, _ in MODULES)
    return f'''<section id="module" class="reveal">
 <span class="eyebrow">Weiterlernen</span>
 <h2 class="title">Alle Module im Überblick</h2>
 <div class="modules">{cards}</div>
</section>'''


def pdf_cta(fname):
    return f'''<section id="pdf" class="reveal">
 <div class="pdf-cta">
  <div class="doc" aria-hidden="true"></div>
  <div><h3>Zusammenfassung als PDF</h3><p>Zwei Seiten mit den wichtigsten Begriffen, Befunden, Schaubildern und Merksätzen – zum Wiederholen, Ausdrucken oder für die Prüfungsvorbereitung. Enthält keine persönlichen Eingaben.</p></div>
  <a class="btn primary" href="{pdf_of(fname)}" download style="display:inline-flex;align-items:center;gap:8px;text-decoration:none">{PDF_ICON} Herunterladen</a>
 </div>
</section>'''


COMMON_JS = r'''(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const root=document.documentElement;
let theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';root.dataset.theme=theme;
const moon='<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',sun='<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>';
const setIcon=()=>{$('#themeIcon').innerHTML=theme==='dark'?sun:moon};setIcon();
$('#themeBtn').addEventListener('click',()=>{theme=theme==='dark'?'light':'dark';root.dataset.theme=theme;setIcon()});
const secs=$$('main section[id]'),links=$$('.toc a');
addEventListener('scroll',()=>{const p=scrollY/Math.max(1,document.body.scrollHeight-innerHeight);$('#readBar').style.width=(p*100)+'%';let cur='';secs.forEach(s=>{if(s.getBoundingClientRect().top<160)cur=s.id});links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+cur))},{passive:true});
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.05});$$('.reveal').forEach(el=>io.observe(el))}else{$$('.reveal').forEach(el=>el.classList.add('in'))}
})();'''

css = base_css + "\n" + extra_css
for fname in PAGES:
    s = (SRC / fname).read_text(encoding="utf-8")
    s = (s.replace("{{CSS}}", css).replace("{{HEADER}}", header(fname))
          .replace("{{MODULES}}", modules_section(fname)).replace("{{PDFCTA}}", pdf_cta(fname))
          .replace("{{COMMONJS}}", COMMON_JS))
    assert "{{" not in s, fname
    (REPO / fname).write_text(s, encoding="utf-8")
    print("built", fname, len(s))

# Gene-Modul: Erweiterungen, PDF-Button und Modulübersicht einsetzen (idempotent)
g = (REPO / "gene-ohne-reisepass.html").read_text(encoding="utf-8")
if "/* === Gemeinsame Erweiterungen" not in g:
    g = g.replace("</style>", extra_css + "\n</style>", 1)
else:
    g = re.sub(r"/\* === Gemeinsame Erweiterungen.*?(?=\n</style>)", lambda m: extra_css.rstrip(), g, count=1, flags=re.S)
if 'class="pdf-btn"' not in g:
    g = g.replace(' <button class="icon-btn" id="themeBtn"', " " + pdf_link("gene-ohne-reisepass.html") + "\n <button class=\"icon-btn\" id=\"themeBtn\"", 1)
if 'id="module"' not in g:
    g = g.replace('<!-- QUELLEN -->', pdf_cta("gene-ohne-reisepass.html") + "\n\n" + modules_section("gene-ohne-reisepass.html") + "\n\n<!-- QUELLEN -->", 1)
(REPO / "gene-ohne-reisepass.html").write_text(g, encoding="utf-8")
print("updated gene-ohne-reisepass.html")
