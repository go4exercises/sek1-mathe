# HOWTO — Externe Videos und Aufgabensammlungen kuratieren

Dieser Leitfaden beschreibt den Workflow, mit dem die Sektion **„Externe Videos &amp; Aufgabensammlungen"** (Master-Schema §10) jeder Themenseite kuratiert wird. Adressat sind sowohl der Auftraggeber als auch Claude in jedem zukünftigen Chat.

Verwandte Dokumente: `STYLEGUIDE.md` §4 (allgemeine Konventionen zur Ressourcen-Sektion), `STYLEGUIDE.md` §6.1 (HTML-Container `.links-grid` und Karten `.lk` / `.lk aufg`), `HOWTO-neue-themenseite.md`, `CLAUDE.md` Abschnitt «Externe Ressourcen» (Kurzfassung).

---

## 1. Verbindliche Anbieter-Liste

Die Reihenfolge ist **strikt bindend**. Anbieter werden in genau dieser Reihenfolge geprüft, bis 4 Slots gefüllt sind (oder die Liste erschöpft ist).

### 1.1 Erklärvideos — bevorzugte YouTube-Kanäle

| # | Anbieter | YouTube-Handle | Charakter |
|---|---|---|---|
| 1 | MathemaTrick | @MathemaTrick (Susanne Scherer) | Sek I/II, breites Spektrum, viele Playlists |
| 2 | Lehrerschmidt | @lehrerschmidt (Kai Schmidt) | bis Klasse 10, sehr breit, klare thematische Playlists |
| 3 | Mathe SMI | Kanal-ID UCMC7Ds2wUva1vwDOKBgZR1g | FOS/BOS München, Klasse 11–13 → **BM-Niveau, sehr passend für TALS** |
| 4 | Mathehoch13 | @Mathehoch13 (Christoph Goemans) | Oberstufe/Abi, eigene Webseite mit Themen-Playlists |
| 5 | Magda liebt Mathe | @MagdaliebtMathe | Abi-fokussiert (Analysis, Stochastik, Vektoren) |
| 6 | Mathe by Daniel Jung | @MathebyDanielJung | breit, sowohl Sek-I- als auch Oberstufen-Themen |

### 1.2 Aufgabensammlungen — bevorzugte Plattformen

| # | Plattform | URL | Charakter |
|---|---|---|---|
| 1 | sos-mathe.ch | https://www.sos-mathe.ch/ | Schweizer Hauptquelle, klare RLP-nahe Struktur (G-Codes wie G21, G22) |
| 2 | serlo.org | https://de.serlo.org/mathe/ | frei lizenziert, sehr breit, oft mehrere passende Aufgabenseiten pro Thema |
| 3 | SwissEduc Munterbunt | https://www.swisseduc.ch/mathematik/ | Schweizer Lehrmittel-Quelle, weniger systematisch |

---

## 2. Regeln für die Auswahl

### 2.1 Videos
- **Maximal 4 Links** pro Themenseite.
- **Pro Anbieter höchstens eine Playlist** (Vielfalt vor Tiefe).
- **Playlists strikt bevorzugt.** Wenn ein Anbieter zum Thema keine Playlist hat, wird er übersprungen.
- **Falls nach Durchlauf aller 6 Anbieter weniger als 4 Playlists vorhanden sind**: mit Einzelvideos auffüllen, wieder in derselben Anbieter-Reihenfolge.
- **Falls weder Playlist noch Einzelvideo eines bevorzugten Anbieters auffindbar**: Sub-Sektion bleibt leer mit einem Platzhalter-Hinweis (siehe §6).

### 2.2 Aufgabensammlungen
- **Maximal 4 Links** pro Themenseite.
- **Pro Plattform sind mehrere Aufgabenseiten erlaubt** (z.B. serlo hat zu vielen Themen 2–4 passende Aufgabenseiten; alle in die 4-Slot-Grenze nehmen). Sinn: serlo deckt einzelne Aspekte (Steigung, Geradengleichung aufstellen, Anwendungen) auf eigenen Seiten ab — alle zugleich nützlich.
- **Lösungen müssen vorhanden sein**. Reine Aufgabenlisten ohne Musterlösung sind ausgeschlossen.
- **Reihenfolge bleibt strikt**: erst alle passenden Treffer von sos-mathe.ch, dann serlo.org, dann SwissEduc.

### 2.3 Was nicht erlaubt ist (Negativ-Liste)
- `mathebibel.de` — tauchte historisch oft in den Repo-Links auf, ist aber **nicht** in der Anbieter-Liste.
- `mathepower.com` — Online-Rechner, nicht in der Anbieter-Liste.
- `klassenarbeiten.de` — keine systematische Lösungen, raus.
- YouTube-Suchergebnis-URLs (`youtube.com/results?…`) — keine stabilen Links.
- YouTube-Kurz-URLs (`youtu.be/…`) — Lang-Form (`youtube.com/watch?v=…` oder `playlist?list=…`) bevorzugt.
- „UNI Mathe" (Kanal, dessen Playlist-IDs den Präfix `PLF29x0idI4l…` haben können — aber **Vorsicht**: nicht alle `PLF29x0idI4l…`-IDs gehören zu UNI Mathe! MathemaTrick nutzt teilweise denselben Präfix-Bereich. Siehe §3.)
- „Mathekanal" (verschiedene IDs mit Präfix `PLLTAHuUj-zH…`) — aber auch hier: **manche `PLLTAHuUj-zH…`-Playlists sind Daniel Jung**. Niemals nach Präfix entscheiden.

---

## 3. Verifikationsmethode — Wichtigste Lerneinheit dieses Projekts

> **Playlist-ID-Präfixe sind keine zuverlässigen Kanal-Indikatoren.**
>
> Ein und derselbe YouTube-Kanal kann mehrere Präfix-Familien nutzen. Beispiel: Die Playlist `PLLTAHuUj-zHgTV0cdQhkHn1gLJuzp9RD0` „Lineare Funktionen (Geraden), y=m*x+n" gehört zu **Mathe by Daniel Jung**, obwohl der Präfix oft mit „Mathekanal" assoziiert wird. Andere `PLLTAHuUj-zH…`-Playlists gehören tatsächlich zu „Mathekanal". Heuristik aus dem Präfix → falscher Anbieter → falsche Karte auf der Themenseite.

### 3.1 Die zuverlässige Methode: `web_fetch` auf die Playlist-URL

```
web_fetch("https://www.youtube.com/playlist?list=<PLAYLIST_ID>")
```

Antwort enthält den **Owner-Namen** und die **Videoanzahl**. Beispiel:

```
# Lineare Funktionen
**Owner:** Mathe SMI
**Count:** 8 videos
```

Damit ist der Anbieter eindeutig identifiziert. Diese Verifikation kostet **einen einzigen Tool-Aufruf** pro Kandidat — das ist billiger als jede Heuristik, die später Fehler korrigieren muss.

### 3.2 Standard-Suchanfragen pro Anbieter

Diese Such-Pattern haben sich bewährt:

```
<Anbieter-Name> <Thema> playlist youtube
<Anbieter-Name> <Thema> youtube.com/playlist
"<Playlist-ID>" channel
```

Für **Mathe SMI** und **Mathehoch13** funktioniert oft auch der direkte Weg über die eigene Webseite:
- Mathehoch13 hat eine kuratierte Themenübersicht: `https://mathehoch13.de/Youtube-Videos.php?category=<Kategorie>` (Kategorien: `LineareFunktionen`, `LGS_II`, `ZusgF` etc.). Jede Kategorie-Seite enthält oben die Playlist-URL.
- Mathe SMI hat eine Skript-Struktur über eduki.com; die Playlists lassen sich oft besser über `web_fetch` auf eine vermutete Playlist-ID prüfen als über Suche.

### 3.3 Fallstricke

| Symptom | Ursache | Lösung |
|---|---|---|
| Suche liefert nur die Kanal-About-Seite | YouTube-Channel-Seiten geben Playlists nicht crawlbar aus | direkte `web_fetch` auf vermutete Playlist-URLs |
| Playlist-Titel passt, aber Owner unbekannt | Playlist-ID-Präfix-Familie ist mehrdeutig | immer `web_fetch` zur Owner-Verifikation |
| Anbieter „hat doch keine Playlist" | falsche Schlussfolgerung aus 1 Suche | mehrere Pattern probieren, dann erst aufgeben |
| Serlo-Link ergibt 404 oder leitet ins Leere | pfadbasierte Serlo-URLs (`/mathe/zahlen-grossen/...`, `/mathe/terme-gleichungen/...`) werden umbenannt, **ohne Redirect** | immer **ID-basierte URLs** verwenden: `https://de.serlo.org/mathe/{ID}/{slug}` (z.B. `/mathe/23665/aufgaben-zu-den-potenzgesetzen`). Der `canonical`-Eintrag im HTML-Header einer Serlo-Seite zeigt die kanonische ID-URL. Bei Bestandspflege regelmässig prüfen. |

### 3.4 Effizienz-Regeln (Lehre aus dem s3-2-Lauf, Juli 2026)

Qualität heisst: Owner verifiziert + Niveau passt. Der Weg dorthin ist budgetiert:

1. **Zuerst die Anbieter-Map (§8) konsultieren** — bereits verifizierte IDs nie neu recherchieren.
2. **Ein Discovery-Abruf pro Thema:** die YouTube-Suchergebnis-Seite einmal abrufen (nur zur
   Kandidaten-Findung — Suchergebnis-URLs werden nie verlinkt!), daraus die Playlist-IDs der
   bevorzugten Anbieter ziehen. Danach **je Kandidat genau ein direkter Playlist-Abruf** — der
   liefert Titel, Owner und Videoanzahl autoritativ in einem Schritt.
3. **Kein Kanal-Seiten-Scraping.** Die Playlist-Übersichten der Kanäle liefern Titel und IDs in
   getrennten Datenstrukturen — die Zuordnung ist fehleranfällig (verschobene Paarungen im
   s3-2-Lauf). Der direkte Playlist-Abruf ist billiger und eindeutig.
4. **Niveau-Passung am Playlist-Titel entscheiden**, nicht durch Sichten der Einzelvideos.
   Nur bei mehrdeutigem Titel einen Blick in die ersten Videotitel werfen.
5. **Abruf-Budget: max. ~6 Abrufe pro Sub-Sektion** (Videos bzw. Aufgaben). Ist das Budget
   erschöpft, Platzhalter setzen (§6) und weiterarbeiten — Platzhalter sind reversibel, verlorene
   Session-Zeit nicht.
6. **serlo immer über die Sitemap:** `https://de.serlo.org/sitemap.xml` einmal abrufen und lokal
   nach Thema greppen — ein Abruf liefert alle ID-basierten Aufgaben-URLs. Die Such-Seite von
   serlo ist clientseitig und für Fetches leer.
7. **sos-mathe über die Code-Map (§8.1)** — nicht blind G-Codes durchprobieren.
8. **Ressourcen vom Seitenbau entkoppeln:** Neue Themenseiten dürfen mit Platzhaltern committet
   werden; die Ressourcen-Kuratierung läuft als eigener Cluster-Lauf pro Lerngebiet (§7).

---

## 4. Schritt-für-Schritt-Verfahren pro Themenseite

### 4.1 Ist-Zustand aufnehmen
Externe Links der Themenseite extrahieren — am einfachsten mit:

```bash
python3 -c "
import re
with open('grundlagen/g3-2-lineare-funktionen.html') as h: t = h.read()
m = re.search(r'<h2 id=\"ressourcen\".*?(?=</main|<footer)', t, re.S)
print(m.group(0))
"
```

### 4.2 Videos kuratieren
Anbieter in Reihenfolge durchgehen:
1. Suche `<Anbieter> <Thema> playlist`.
2. Kandidaten-Playlist per `web_fetch` verifizieren — bestätigt **Owner**.
3. **Niveau-Passung prüfen** (Owner ≠ Passung): Playlist-Titel und Beschreibung lesen, mit dem h2-Schema und dem RLP-Anspruch der Themenseite vergleichen. Eine Sek-I-Playlist auf einer BM-Themenseite ist genauso falsch wie eine Sek-II-Analysis-Playlist auf einer Grundlagen-Einführungsseite. Eine Sek-II-Analysis-Playlist mit Beschreibung „Anwendung, Geschwindigkeit, Klausur" gehört nicht auf eine Themenseite zum allgemeinen Funktionsbegriff — auch wenn der Owner verifiziert ist.
4. Falls Owner stimmt **und** Niveau passt: in Auswahl aufnehmen.
5. Falls Owner nicht stimmt oder Niveau nicht passt: nächster Anbieter.
6. Stop bei 4 verifizierten Playlists oder nach Durchlauf aller 6 Anbieter.
7. Falls weniger als 4 Playlists vorhanden: Einzelvideos in Anbieter-Reihenfolge ergänzen (auch wieder per `watch?v=`-URL, Owner notfalls per `web_fetch`).

**Lieber leer als unpassend.** Wenn nach Durchlauf aller 6 Anbieter keine Playlist und kein Einzelvideo das Niveau trifft, bleibt die Sub-Sektion mit dem Platzhalter aus § 6 leer. **Keine Notbehelfs-Verlinkung**, nur weil ein Anbieter „irgendwas verifiziert Verfügbares" hat. Begründung in den CHANGELOG-Eintrag schreiben („Anbieter X hat zwar Y, aber Niveau passt nicht — Sub-Sektion bleibt leer").

### 4.3 Aufgaben kuratieren
Plattformen in Reihenfolge durchgehen:
1. sos-mathe.ch: passende G-Code-Seite suchen (`https://www.sos-mathe.ch/g/g<n>/g<n><m>/aufg_g<n><m>.html`).
2. serlo.org: 1–3 passende Aufgabenseiten suchen — **immer ID-basierte URL** `https://de.serlo.org/mathe/<id>/<slug>` verwenden, nicht die pfadbasierte Form `de.serlo.org/mathe/<theme>/<sub>/...` (letztere ist instabil, siehe §3.3 Fallstricke).
3. SwissEduc Munterbunt: wenn noch Slots frei.
4. Stop bei 4 Links.

### 4.4 HTML-Patch

**Replacement-Pattern (verbindlich):** Bei Block-Ersetzungen der Ressourcen-Sektion endet das Pattern immer mit einem Lookahead auf `</main>`, nie mit einem `</div>`-Endmarker mitten im Block. Non-greedy Patterns auf interne Tags stoppen zu früh, wenn das gleiche Tag-Muster vorher schon vorkommt (was bei `</div></div>` in beiden Sub-Sektionen der Fall ist).

```python
import re
PAT = re.compile(r'<h2 id="ressourcen".*?(?=\s*</main>)', re.S)
new_text, n = PAT.subn(new_block, file_text)
assert n == 1, f"expected exactly 1 replacement, got {n}"
```

Der `(?=\s*</main>)`-Lookahead frisst das `</main>` nicht mit auf, sodass es nach dem Replacement noch da ist. `subn` mit `assert n == 1` garantiert, dass weder gar nicht noch mehrfach ersetzt wurde.

**Struktur des neuen Blocks** gemäss STYLEGUIDE §6.1:

```html
<h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>
<div class="ressourcen-subtitel">🎬 Erklärvideos (Playlists)</div>
<div class="links-grid">
  <a href="…" target="_blank" rel="noopener" class="lk">
    <span class="lk-ic">▶️</span>
    <div>
      <div class="lk-t">⟪Playlist-Titel⟫ — Playlist</div>
      <div class="lk-s">⟪Anbieter⟫ · ⟪Video-Count oder Beschreibung⟫</div>
    </div>
  </a>
  …
</div>
<div class="ressourcen-subtitel">📝 Aufgabensammlungen</div>
<div class="links-grid">
  <a href="…" target="_blank" rel="noopener" class="lk aufg">
    <span class="lk-ic">📝</span>
    <div>
      <div class="lk-t">⟪Plattform⟫ — ⟪Thema-Bezeichnung⟫</div>
      <div class="lk-s">⟪Aspekt der Aufgaben⟫ · ⟪mit Lösungen⟫</div>
    </div>
  </a>
  …
</div>
```

### 4.5 Verifikation
Nach Patch (vor ZIP-Packen):
- **Standard-Pre-Flight** aus `STYLEGUIDE.md` §6.1 (Marker-Anwesenheit, Phantom-Klassen).
- **Strukturelle Integritäts-Checks** aus dem Pre-Flight (`.claude/skills/preflight/preflight.py`: Eindeutigkeit der Marker, Tag-Bilanz, Slot-Limits ≤ 4). Diese fangen den Fail-Modus ab, bei dem ein unsauberes Block-Ersatz-Pattern einen Müll-Schwanz aus dem alten Block hinterlässt — der Standard-Pre-Flight zeigt dann trotzdem grün, der Browser aber Layout-Bruch.
- **Negativlisten-Check**:
  ```bash
  grep -cE 'mathebibel\.de|mathepower\.com|klassenarbeiten\.de|youtube\.com/results|youtu\.be/' <datei>
  # Erwartet: 0
  ```
- Stichprobenartig 1–2 URLs im Browser öffnen (manuell durch den Auftraggeber, nicht durch Claude — Tool-Budget schonen).

---

## 5. Übertragung auf das Schwerpunktfach

Identisches Verfahren, identische Anbieter-Reihenfolge. Erwartete Verteilung:

- **Sek-I-affine Themen** (s1-1 bis s1-3 Arithmetik, s2-1/2.2 Gleichungen): MathemaTrick und Lehrerschmidt dominieren.
- **Funktionen** (s3-1 bis s3-5): Mathe SMI und Mathehoch13 werden öfter Treffer haben, weil sie 11.–13. Klasse abdecken (entspricht BM-Niveau).
- **Geometrie/Vektoren** (s4-1 bis s4-3): Magda liebt Mathe wird relevanter (Abi-Vektorgeometrie).

Für Schwerpunkt-spezifische Themen (Logarithmen, Polynomfunktionen, Vektorgeometrie) sind sos-mathe.ch S-Codes (`/s/s<n>/s<n><m>/aufg_s<n><m>.html`) der erste Anlauf.

---

## 6. Platzhalter, wenn nichts gefunden wird

Falls ein bevorzugter Anbieter und alle Fallbacks erschöpft sind und die Sektion leer wäre, **niemals** einen leeren `<div class="links-grid"></div>` stehen lassen. Stattdessen:

```html
<div class="ressourcen-subtitel">🎬 Erklärvideos (Playlists)</div>
<div class="links-grid">
  <a class="lk" style="opacity:0.6;cursor:default;" aria-disabled="true">
    <span class="lk-ic">⏳</span>
    <div>
      <div class="lk-t">In Vorbereitung</div>
      <div class="lk-s">Zu diesem Thema sind noch keine passenden Erklärvideos der bevorzugten Anbieter kuratiert.</div>
    </div>
  </a>
</div>
```

Analog für Aufgabensammlungen. Solche Platzhalter werden bei einem späteren Recherche-Lauf ersetzt.

---

## 7. Quoten-Hygiene beim Recherche-Lauf

Pro Themenseite sind ca. **4–8 Tool-Aufrufe** realistisch (Suchen + `web_fetch`-Verifikationen). Für alle 19 Grundlagen-Themen oder die 13 Schwerpunkt-Themen entsprechend ca. **75–150 Tool-Aufrufe**.

**Empfehlung:** Den Recherche-Lauf in Cluster aufteilen — z.B. pro Lerngebiet eine Chat-Sitzung:
- Cluster A: g1-1 bis g1-4 (Algebra)
- Cluster B: g2-1 bis g2-3 (Gleichungen)
- Cluster C: g3-1 bis g3-3 (Funktionen)
- Cluster D: g4-1 bis g4-3 (Datenanalyse)
- Cluster E: g5-1 bis g5-5 (Geometrie/Trigonometrie)

Pro Cluster ca. 30–50 Tool-Aufrufe — entspannt im Budget eines Chats.

Schwerpunkt analog:
- Cluster S1: s1-1 bis s1-3 (Arithmetik)
- Cluster S2: s2-1, s2-2 (Gleichungen)
- Cluster S3: s3-1 bis s3-5 (Funktionen)
- Cluster S4: s4-1 bis s4-3 (Geometrie/Vektoren)

---

## 8. Bisher recherchierte Anbieter-Map (Stand: Juli 2026 — deckt alle Themenseiten beider Bereiche ab)

Diese Tabelle wird mit jedem abgeschlossenen Thema erweitert. So muss eine bereits verifizierte Playlist nicht erneut recherchiert werden.

| Thema | MathemaTrick | Lehrerschmidt | Mathe SMI | Mathehoch13 | Magda | Daniel Jung |
|---|---|---|---|---|---|---|
| g1-1 Strukturen algebraischer Ausdrücke | `PLF29x0idI4lWPWBvEXDrcCEZ54ZdtYazp` (64 Vid „Terme vereinfachen") | `PLa0u3J0uzAzmBhxJfVgJ9pTv2QeqJsbO_` (27 Vid „Terme & Gleichungen") | — | — | — | — |
| g1-2 Zahlen und Grundoperationen | `PLF29x0idI4lUDQ1_6S13Jol663DF2CQfq` (65 Vid „Alles über Brüche") | `PLa0u3J0uzAzkM5G1elN_rZV-Z4oQU0kpj` (24 Vid „Brüche & Bruchrechnung") | — | — | — | `PLLTAHuUj-zHhk-YUb4y3NGM324XnkyGY-` (47 Vid „Bruchrechnung, Brüche") |
| g1-3 Algebraische Terme | `PLF29x0idI4lWPWBvEXDrcCEZ54ZdtYazp` (64 Vid „Terme vereinfachen") | `PLa0u3J0uzAzmBhxJfVgJ9pTv2QeqJsbO_` (27 Vid „Terme & Gleichungen") | — | — | — | `PLLTAHuUj-zHjM0_gGTkVHw5tD61_5QzCn` (54 Vid „Terme/Gleichungen") |
| g1-4 Zehnerpotenzen und Quadratwurzeln | `PLF29x0idI4lW8nLkmt32wPfuRjZylkOzq` (22 Vid „Alles über Potenzen") | `PLa0u3J0uzAzlbi-rSRqX-4Dm3D1_2s46K` (39 Vid „Potenz- und Wurzelrechnung") | — | — | — | `PLLTAHuUj-zHiz2awITczKHwCrwj9Z5pY1` (36 Vid „Potenzen, Potenzgesetze") |
| g2-1 Grundlagen Gleichungen | `PLF29x0idI4lWPWBvEXDrcCEZ54ZdtYazp` (64 Vid „Terme vereinfachen") | `PLa0u3J0uzAzmBhxJfVgJ9pTv2QeqJsbO_` (27 Vid „Terme & Gleichungen") | — | — | — | — |
| g2-2a Lineare Gleichungen | `PLF29x0idI4lWPWBvEXDrcCEZ54ZdtYazp` (64 Vid „Terme vereinfachen") | `PLa0u3J0uzAzmBhxJfVgJ9pTv2QeqJsbO_` (27 Vid „Terme & Gleichungen") | — | — | — | `PLLTAHuUj-zHjM0_gGTkVHw5tD61_5QzCn` (54 Vid „Terme/Gleichungen") |
| g2-2b Quadratische Gleichungen | — *(keine eigene quad-Gleichungen-Playlist)* | `PLa0u3J0uzAzl5hAVeVOwWassi_01eoBMO` (32 Vid „Parabeln/quad. Gleichungen") | — | — | — | `PLLTAHuUj-zHiRkoZnu2dIFv94wddmJRMi` (35 Vid „Quad. Gleichungen, PQ-Formel") |
| g2-3 Lineare Gleichungssysteme | `PLF29x0idI4lW2LRLspaxkT0CgStgZrSws` (25 Vid „LGS lösen") | `PLa0u3J0uzAznhoG1e0j7GxX7eT1aXuuNh` (komplett „Lineare Funktion & LGS") | — | — | — | — *(viele Einzelvideos, keine eigene LGS-Playlist gefunden)* |
| g3-2 Lineare Funktionen | `PLF29x0idI4lU6F9lF8CBWHnrhfak852OT` (17 Videos) | `PLa0u3J0uzAznhoG1e0j7GxX7eT1aXuuNh` (komplett) | `PL2jCdV8ykKMrHbuEroHB3WgVTFoHlpdBk` (8 Videos) | `PLLkr4Hf_IwvMz2bl7A7TCq_z2BtJMBdon` (komplett) | — | `PLLTAHuUj-zHgTV0cdQhkHn1gLJuzp9RD0` (50 Videos) |
| g3-1 Grundlagen Funktionen | — | — | — | — | — | — *(kein bevorzugter Anbieter führt zum allgemeinen Funktionsbegriff Material auf BM-Niveau: Sek-I-Anbieter bleiben zu elementar, Sek-II-Playlists steigen direkt in Analysis ein. Video-Sektion bleibt mit Platzhalter leer; passende Videos sind in 3.2 und 3.3 verlinkt.)* |
| g3-3 Quadratische Funktionen | `PLF29x0idI4lVDfsit7iy1j6Nmx3znS5bV` (42 Vid „Alles über PARABELN") | `PLa0u3J0uzAzl5hAVeVOwWassi_01eoBMO` (32 Vid „Parabeln/quad. Gleichungen") | — | `PLLkr4Hf_IwvMts1O-fD_YBbcDiq8bvXHU` (32 Vid „Quadratische Funktionen und Gleichungen") | — | `PLLTAHuUj-zHhRwBDeNqYk1edYRHmx8Qd1` (48 Vid „Quadratische Funktionen, Parabeln") |
| g4-1 Grundlagen Statistik | — | `PLa0u3J0uzAznKJ7-xAyq6tOtqQYzs5_38` (35 Vid „Statistische Grundbegriffe & Diagramme") | — | — | — | `PLLTAHuUj-zHifw_3OhBTvQq2EGX5NedOy` (31 Vid „Statistik") |
| g4-2 Diagramme | — | `PLa0u3J0uzAznKJ7-xAyq6tOtqQYzs5_38` (siehe g4-1) | — | — | — | `PLLTAHuUj-zHifw_3OhBTvQq2EGX5NedOy` (siehe g4-1) |
| g4-3 Masszahlen | — | `PLa0u3J0uzAznKJ7-xAyq6tOtqQYzs5_38` (siehe g4-1) | — | — | — | `PLLTAHuUj-zHifw_3OhBTvQq2EGX5NedOy` (siehe g4-1) |
| g5-1 Grundlagen (Winkel) | — | `PLa0u3J0uzAznYTqIZtyPBmorX8BxF7TY9` (37 Vid „Geometrie-Grundlagen") | — | — | — | `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr` (Trigonometrie) |
| g5-2 Planimetrie | `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (60 Vid „GEOMETRIE Dreieck/Kreis/Trapez") | `PLa0u3J0uzAznYTqIZtyPBmorX8BxF7TY9` (siehe g5-1) | — | — | — | — |
| g5-2a Dreiecke | `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (siehe g5-2, Dreieck-Anteile) | `PLa0u3J0uzAznju8Er07GiFuaHGegrGtUe` (15 Vid „Dreiecke konstruieren — geometrische Grundkonstruktionen") | — | — | — | `PLLTAHuUj-zHgCcNWha7A2N_gR6UGAeQe2` (25 Vid „Satzgruppe des Pythagoras, Berechnungen am Dreieck") |
| g5-2b Vierecke | `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (siehe g5-2, Trapez-/Vierecks-Anteile) | `PLa0u3J0uzAzmX2iRZzdG8KuHJZA6sayy0` (30 Vid „Vierecke — Geometrie") + `PLa0u3J0uzAzk7Iw3l2Uxe7ftYXHmZ0Jhw` (12 Vid „Geometrie — Vierecke" Kurzversion) | — | — | — | — |
| g5-2c Kreis und Kreisteile | `PLF29x0idI4lVRLFql-2N3u5-2ZgWp9A7-` (siehe g5-2, Kreis-Anteile) | `PLa0u3J0uzAzlkQcJpE9CODCaM_vg_t2Ea` (19 Vid „Fläche — Flächenberechnung") + `PLa0u3J0uzAznYTqIZtyPBmorX8BxF7TY9` (37 Vid „Geometrie-Grundlagen") | — | — | — | — *(keine kreis-spezifische Playlist mit eindeutigem Owner-Match gefunden)* |
| g5-3 Trigonometrische Berechnungen | — | `PLa0u3J0uzAzlIHjv0J_R8sIj-xn8cVs0J` (20 Vid „Trigonometrie") | — | — | — | `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr` (siehe g5-1) |
| g5-4 Einheitskreis | — | `PLa0u3J0uzAzlIHjv0J_R8sIj-xn8cVs0J` (siehe g5-3) | — | — | — | `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr` (siehe g5-1) |
| g5-5 Trigonometrische Gleichungen | — | `PLa0u3J0uzAzlIHjv0J_R8sIj-xn8cVs0J` (siehe g5-3) | — | — | — | `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr` (siehe g5-1) |
| s3-2a Potenzfunktionen | — *(nur Einzelvideo `watch?v=eOYTlV0Af3o` „Potenzfunktionen aufstellen mit 2 Punkten")* | — *(nur „Potenz- und Wurzelrechnung" = Rechnen, Thema passt nicht)* | `PL2jCdV8ykKMrnQfRszg204hlZYiGnkpqq` (24 Vid „Gebrochen-rationale Funktionen" — Asymptoten/Polstellen, deckt Hyperbel-Teil) | `PLLkr4Hf_IwvPyPsggHjtOLlj_6R3T9MlW` (14 Vid „gebrochen-rationale Funktionen") | — | — *(nur Einzelvideo `watch?v=OVWF5UATHVc` „Potenzfunktionen Übersicht")* |
| s3-2b Wurzelfunktionen | `PLF29x0idI4lXu1WcPP0oXEF_AnfOtYjkw` (56 Vid „Alles über WURZELN" — Wurzelrechnung als Grundlage; Einzelvideo `watch?v=GMjEAYtCHQg` „Definitionsmenge Wurzelterm") | — | — | — | — | `PLLTAHuUj-zHiqJlnyr_iYcbxsL7ztyWp8` (31 Vid „Wurzel, Wurzelrechnungen, Wurzelfunktionen"; Einzelvideo `watch?v=_ZA-ZB-SqTc` „Wertebereich und Umkehrfunktion") |
| s3-3 Polynomfunktionen | — *(Einzelvideo `watch?v=QrC4wTZoj8k` „Linearfaktorzerlegung")* | — | — | `PLLkr4Hf_IwvN-lbzbyC4Zol0uSLuDleqL` („Ganzrationale Funktionen") | — | `PLLTAHuUj-zHjqKr3k2YwD8m1tzhqlHHr0` („Ganzrationale Funktionen, Polynomfunktionen, Analysis"; Einzelvideo `watch?v=Lb5sQlgKDeU` „Doppelte und dreifache Nullstellen") |
| s3-4a Exponentialfunktionen | `PLF29x0idI4lVs82KN0GTG3hQMpTM_84lV` (22 Vid „Exponentialgleichungen lösen") | — | `PL2jCdV8ykKMpkosfUPe8-mJDM5UI9AzOb` (25 Vid „Exponentialfunktionen") | `PLLkr4Hf_IwvPCVVWwpJ6QQJt3-kqxZEaP` (31 Vid „Exponentialfunktionen und Exponentialgleichungen") | — | `PLLTAHuUj-zHgfDNg5jmBmfnvDHcc4y_Ey` (39 Vid „Exponentialfunktionen, Logarithmus, Gleichungen" — deckt 3.4a+3.4b) |
| s3-4b Logarithmusfunktionen | `PLF29x0idI4lXSN6xlwAQUjS71Tv-jdQ49` (12 Vid „Alles über LOGARITHMUS") | — | — | — | — | `PLLTAHuUj-zHgfDNg5jmBmfnvDHcc4y_Ey` (siehe s3-4a) |
| s3-5 Trigonometrische Funktionen | — | `PLa0u3J0uzAzlIHjv0J_R8sIj-xn8cVs0J` (siehe g5-3, trig. Grundlagen) | — | — | — | `PLLTAHuUj-zHgXgsj5jy-qDE41UePZveqr` (siehe g5-1/g5-3) — *ohne neue Abrufe aus der Map übernommen; Aufgaben via serlo-Sitemap (allg. Sinusfunktion 112676, Verschieben/Strecken 54054, Einheitskreis 30679)* |
| s3-1 Grundlagen (Werkzeugkasten) | `PLF29x0idI4lVDfsit7iy1j6Nmx3znS5bV` (siehe g3-3 «Alles über PARABELN» — Transformations-Training) | — | — | `PLLkr4Hf_IwvMts1O-fD_YBbcDiq8bvXHU` (siehe g3-3) | — | — *(Discovery-Lauf 2026-07 fand keine allgemeine Transformations-Playlist der bevorzugten Anbieter; Aufgaben via serlo-Sitemap: Extremwertprobleme 159266, Schnittpunkte Geraden 160385, Symmetrie 26411)* |
| s2-2a Potenz-/Wurzel-/rationale Gleichungen | `PLF29x0idI4lXu1WcPP0oXEF_AnfOtYjkw` (siehe s3-2b «Alles über WURZELN») | — | — | — | — | `PLLTAHuUj-zHiqJlnyr_iYcbxsL7ztyWp8` (siehe s3-2b) — *Aufgaben: sos-mathe G33 + G32 aus Code-Map §8.1* |
| s2-2b Exponential-/log. Gleichungen | `PLF29x0idI4lVs82KN0GTG3hQMpTM_84lV` + `PLF29x0idI4lXSN6xlwAQUjS71Tv-jdQ49` (siehe s3-4a/b) | — | — | `PLLkr4Hf_IwvPCVVWwpJ6QQJt3-kqxZEaP` (siehe s3-4a) | — | — *(Aufgaben via serlo-Sitemap: 40846, 26262, 23768)* |
| s2-2c Betrag/Polynom/Ungleichungen | — | — | — | — | — | Einzelvideo `watch?v=XjEOu4nzpyo` «Betragsungleichungen, Fälle bestimmt, jetzt lösen» (owner-verifiziert 2026-07-11) — *keine Betrags-Playlist der bevorzugten Anbieter; Einzelvideo-Fallback §2.1. Aufgaben: sos-mathe G35 + serlo-Sitemap 169291, 223589)* |
| s2-1 Grundlagen (Gleichungs-Werkzeugkasten) | `PLF29x0idI4lWPWBvEXDrcCEZ54ZdtYazp` (siehe g1-1/g2-1 «Terme vereinfachen») | `PLa0u3J0uzAzmBhxJfVgJ9pTv2QeqJsbO_` (siehe g2-1 «Terme &amp; Gleichungen») | — | — | — | — *(Aufgaben: serlo-Sitemap 25103 gemischte Gleichungen, 26259 quadratische + sos-mathe G31)* |
| s3-6 Betragsfunktionen (Ergänzung TALS) | — | — | — | — | — | Einzelvideo `watch?v=vaASPgrhO2o` «Betragsfunktionen, -gleichungen, -ungleichungen, Übersicht grob» (owner-verifiziert 2026-07-11) — *keine Betrags-Playlist der bevorzugten Anbieter (Discovery 2026-07: 3 Playlist-Kandidaten themenfremd); Einzelvideo-Fallback §2.1. Aufgaben: serlo-Sitemap 26406 Betragsfunktion, 223589 Betrag einer Zahl)* |
| s4-3a–d Vektorgeometrie (4 Sub-Seiten) | `PLF29x0idI4lUv5XsdfGTvuMZG0rX9tnR3` «Alles über VEKTOREN» (41 Videos, owner-verifiziert im s3-6-Discovery-Lauf 2026-07) — auf allen vier Seiten | — | — | — | — | — *(Aufgaben via serlo-Sitemap: 31860 Vektor zwischen Punkten, 107944/107945 Skalarprodukt 2D/3D, 30683 Winkel, 24573 Geraden im Raum, 30686 Lage zweier Geraden, 30687 Gerade–Ebene, 30688 zwei Ebenen — ohne neue Abrufe)* |
| s4-2a–c Stereometrie (3 Sub-Seiten) | — | `PLa0u3J0uzAzm2EWHP7iGUWq_WTR0TtuJz` «Körper — Oberfläche & Volumen berechnen» (Lehrerschmidt, 72 Videos, owner-verifiziert 2026-07) | — | — | — | `PLLTAHuUj-zHju4BlmGqAs9pC5HEPJ4V3F` «Körper/Stereometrie» (Daniel Jung, 20 Videos, owner-verifiziert) — *beide auf allen drei Seiten; Aufgaben via serlo-Sitemap: 50462 Würfel/Quader, 174501 Prismen/Zylinder, 65267 Pyramide, 62627 Kegel, 62757 Kugel-Volumen, 58818 zusammengesetzte Körper (5 Abrufe: 1 Discovery + 4 Verifikation)* |
| s4-1 Grundlagen (Geometrie-Werkzeugkasten) | — | `PLa0u3J0uzAzm2EWHP7iGUWq_WTR0TtuJz` (siehe s4-2a–c, Lehrerschmidt) | — | — | — | `PLLTAHuUj-zHju4BlmGqAs9pC5HEPJ4V3F` (siehe s4-2a–c, Daniel Jung) — *ohne neue Abrufe aus der Map übernommen; Aufgaben via serlo-Sitemap: 177185 Schrägbilder zeichnen, 60957 Grundkörper* |
| s1-1 Grundlagen (Struktur-Blick Algebra) | `PLF29x0idI4lWPWBvEXDrcCEZ54ZdtYazp` (siehe g1-1/g2-1 «Terme vereinfachen») | `PLa0u3J0uzAzmBhxJfVgJ9pTv2QeqJsbO_` (siehe g2-1 «Terme & Gleichungen») | — | — | — | — *(ohne neue Abrufe; Aufgaben via serlo-Sitemap: 26312 binomische Formeln, 28874 Faktorisieren)* |
| s1-2 Potenzen | `PLF29x0idI4lXu1WcPP0oXEF_AnfOtYjkw` (siehe s3-2b «Alles über WURZELN» — rationale Exponenten) | — | — | — | — | — *(ohne neue Abrufe; Aufgaben via serlo-Sitemap: 23665 Potenzgesetze, 78888 rationale Exponenten)* |
| s1-3 Logarithmen | `PLF29x0idI4lXSN6xlwAQUjS71Tv-jdQ49` (siehe s3-4b «Alles über LOGARITHMUS») | — | — | — | — | — *(ohne neue Abrufe; Aufgaben via serlo-Sitemap: 23768 Rechnen mit Logarithmen, 26262 Exp./Log.-Gleichungen)* |

*Diese Tabelle wird bei jedem neuen Recherche-Lauf erweitert. Bei Erweiterung: pro Thema eine Zeile, Playlist-IDs nur eintragen, wenn per `web_fetch` verifiziert. Wenn ein Anbieter zum Thema nichts hat: `—`.*

### 8.1 sos-mathe.ch Code-Map (verifizierte Aufgabenseiten)

URL-Schema: `https://www.sos-mathe.ch/g/g<n>/g<nm>/aufg_g<nm>.html`. Kein Sitemap, keine
Übersichtsseite — darum hier die bereits verifizierten Codes festhalten (Stand: Juli 2026):

| Code | Thema | verwendet auf |
|---|---|---|
| G01–G05 | Arithmetik-Grundlagen | g1-x |
| G11 | Quadratwurzeln | g1-4 |
| G12 | Potenzen und Wurzeln (Rechnen) | g1-4 |
| G21 | Lineare Funktion | g3-2 |
| G22 | Funktion 2. Grades (Parabel, Extremalwertaufgaben) | g3-3 |
| G31 | Quadratische Gleichungen | g2-2b |
| G32 | Gleichungen höheren Grades (Potenzgleichungen) | s3-2a |
| G33 | Wurzelgleichungen | s3-2b |
| G34a/b | Gleichungssysteme mit zwei Unbekannten | g2-3 |
| G35 | Lineare Ungleichungen, lineare Optimierung | — |
| G41–G44 | Datenanalyse | g4-x |
| G60–G66 | Geometrie/Trigonometrie | g5-x |

*Nicht existent (2026-07 geprüft): G23, G24, G25. Bei neuen Codes: erst per Abruf verifizieren, dann hier ergänzen.*

---

## 9. Schnell-Checkliste

Vor jedem Recherche-Lauf:
- [ ] Aktuellen Ressourcen-Block der Themenseite ausgelesen
- [ ] Anbieter-Reihenfolge präsent (Videos: M → L → SMI → M13 → Magda → DJ; Aufgaben: sos-mathe → serlo → SwissEduc)
- [ ] Negativ-Liste präsent (kein Mathebibel, kein Mathepower, keine YouTube-Suchergebnisse)

Pro Playlist-Kandidat:
- [ ] Owner per `web_fetch` verifiziert
- [ ] Thematische Passung kurz beurteilt (Playlist-Titel + Beschreibung gelesen)

Nach Patch:
- [ ] 4 Slots gefüllt (oder Platzhalter gesetzt, wenn nichts gefunden)
- [ ] Reihenfolge stimmt (in der Card-Liste wie in der Anbieter-Hierarchie)
- [ ] Pre-Flight grün (STYLEGUIDE §6.1)
- [ ] Anbieter-Map in §8 dieses HOWTOs erweitert

---

*Bei Pflege: §8 (Anbieter-Map) erweitern, §1 (Anbieter-Liste) nur ändern, wenn der Auftraggeber die Liste ändert. Reihenfolge ist verbindlich.*
