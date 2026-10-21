# Nation im Kopf – Interaktives Lernlabor

Unterrichtsmaterial für das Wahlfach Demokratiebildung bzw. Geschichte mit Gemeinschaftskunde.
Leitfrage: **Wann bin ich Teil einer Nation – und wer entscheidet darüber?**

| Seite | Inhalt | PDF |
|---|---|---|
| `index.html` | Lernlabor „Nation im Kopf“: vier Theorien (Anderson, Gellner, Hobsbawm, Smith), fünf Länderfälle, Kontinuum, biografische Reflexion, Abschlussurteil | – |
| `gene-ohne-reisepass.html` | Vertiefung „Gene ohne Reisepass“: DNA, Abstammung und Nation | `pdf/gene-ohne-reisepass-zusammenfassung.pdf` |
| `erfundene-traditionen.html` | Vertiefung „Erfundene Traditionen“: Hobsbawm vs. Smith am Kaiserreich, an Frankreich und Schottland | `pdf/erfundene-traditionen-zusammenfassung.pdf` |
| `nationalismus-demokratie.html` | Vertiefung „Nationalismus als Gefahr für die Demokratie?“ (J1): Begriffe, Kipp-Punkte, Grundgesetz, Urteilsbildung | `pdf/nationalismus-demokratie-zusammenfassung.pdf` |

Die Seiten speichern keine Daten. Alle Eingaben bleiben im Browser der Nutzenden.

## Werkstatt (für Änderungen)

Der Ordner `werkstatt/` enthält die Quelltexte der Vertiefungsmodule und der PDF-Zusammenfassungen:

- `werkstatt/module/build.py` setzt gemeinsames Design, Kopfzeile und Modulübersicht in die Module ein:
  `python3 werkstatt/module/build.py werkstatt/module .`
- `werkstatt/pdf/*.html` sind die A4-Vorlagen der Zusammenfassungen; `werkstatt/render_pdf.py` erzeugt daraus die PDFs (benötigt Python-Playwright):
  `python3 werkstatt/render_pdf.py werkstatt/pdf pdf erfundene-traditionen nationalismus-demokratie gene-ohne-reisepass`
