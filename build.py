#!/usr/bin/env python3
"""Génère les pages write-ups et projets à partir des README de tes dépôts GitHub.

Usage : python3 build.py <dossier ctf-writeups> <dossier SMSI_training> <dossier AI-risk-assessment>
Nécessite pandoc. Les images sont copiées dans img/<slug>/.
"""
import html, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
CTF, SMSI, IA = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])

# Ordre d'affichage = ordre de cette liste. Pour ajouter un write-up, ajoute une ligne.
WRITEUPS = [
    dict(slug="sqli", src=CTF / "cisco/sql-injection", gh="ctf-writeups/tree/main/cisco/sql-injection",
         short="Injection SQL sur DVWA", platform="Cisco Ethical Hacker", tags=["web", "sqli"], level="Facile",
         teaser="D'un simple champ « User ID » jusqu'à l'extraction des identifiants de tous les comptes, en UNION-based."),
    dict(slug="idor", src=CTF / "bluefaculty/ch04-idor", gh="ctf-writeups/tree/main/bluefaculty/ch04-idor",
         short="IDOR sur BluePortal", platform="BlueFaculty", tags=["web", "idor"], level="Facile",
         teaser="Un mot de passe faible, un paramètre id=2 changé en id=1, et me voilà admin."),
    dict(slug="path", src=CTF / "bluefaculty/ch02-path-traversal", gh="ctf-writeups/tree/main/bluefaculty/ch02-path-traversal",
         short="Path Traversal sur File Viewer", platform="BlueFaculty", tags=["web", "path-traversal"], level="Facile",
         teaser="Lire des fichiers hors du dossier prévu grâce à un paramètre d'URL mal contrôlé."),
]
PROJETS = [
    dict(slug="smsi", src=SMSI, gh="SMSI_training", short="SMSI Orséa Banque",
         platform="Projet GRC", tags=["iso27001", "ebios-rm"], level=None,
         blob="https://github.com/YlayannMR/SMSI_training/blob/main/"),
    dict(slug="ia", src=IA, gh="AI-risk-assessment", short="IA Orséa Banque : ISO 42001",
         platform="Projet GRC", tags=["iso42001", "ai-act"], level=None,
         blob="https://github.com/YlayannMR/AI-risk-assessment/blob/main/"),
]

HEAD = (ROOT / "partials/head.html").read_text()
NAV = (ROOT / "partials/nav.html").read_text()
FOOT = (ROOT / "partials/foot.html").read_text()


def render(item, kind, prev=None, nxt=None):
    md = (item["src"] / "README.md").read_text()
    title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
    md = re.sub(r"^# .+\n", "", md, count=1)
    body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--no-highlight"],
                          input=md, capture_output=True, text=True, check=True).stdout
    body = body.replace('src="images/', f'src="../img/{item["slug"]}/')
    body = re.sub(r'<img ', '<img loading="lazy" ', body)
    if item.get("blob"):  # liens vers les livrables -> GitHub
        body = re.sub(r'href="((?:livrables|aims|smsi)/[^"]*)"', lambda m: f'href="{item["blob"]}{m.group(1)}" target="_blank" rel="noopener"', body)
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    minutes = max(1, round(words / 200))
    img = item["src"] / "images"
    if img.is_dir():
        dst = ROOT / "img" / item["slug"]
        dst.mkdir(parents=True, exist_ok=True)
        for f in img.iterdir():
            shutil.copy(f, dst / f.name)
    first = sorted((ROOT / "img" / item["slug"]).glob("*"))
    item.update(title=title, minutes=minutes, thumb=f'img/{item["slug"]}/{first[-1].name}' if first else "")
    section = "Write-ups" if kind == "writeups" else "Projets"
    chips = "".join(f'<span class="chip">{t}</span>' for t in item["tags"])
    lvl = f' · {item["level"]}' if item["level"] else ""
    nav_links = ""
    if prev or nxt:
        nav_links = '<div class="nextprev">' + \
            (f'<a class="btn" href="{prev["slug"]}.html">← {html.escape(prev["short"])}</a>' if prev else "<span></span>") + \
            (f'<a class="btn" href="{nxt["slug"]}.html">{html.escape(nxt["short"])} →</a>' if nxt else "") + "</div>"
    page = f"""{HEAD.replace("{{title}}", html.escape(item["short"]) + " · Ylayann Malouda-Ribardiere").replace("{{base}}", "../")}
<body>
{NAV.replace("{{base}}", "../index.html")}
<main class="article">
<div class="crumbs"><a href="../index.html">~</a> / <a href="../index.html#{"ctf" if kind == "writeups" else item["slug"]}">{section.lower()}</a> / {item["slug"]}</div>
<div class="head">
<div class="chips">{chips}</div>
<h1>{html.escape(title)}</h1>
<div class="mono" style="color:var(--muted);font-size:.85rem">{item["platform"]}{lvl} · {minutes} min de lecture · <a href="https://github.com/YlayannMR/{item["gh"]}" target="_blank" rel="noopener">source sur GitHub</a></div>
</div>
{body}
{nav_links}
</main>
{FOOT.replace("{{base}}", "../")}"""
    (ROOT / kind / f'{item["slug"]}.html').write_text(page)


for i, w in enumerate(WRITEUPS):
    render(w, "writeups", WRITEUPS[i - 1] if i else None, WRITEUPS[i + 1] if i + 1 < len(WRITEUPS) else None)
for p in PROJETS:
    render(p, "projets")

# Cartes des write-ups sur l'accueil
cards = []
for w in WRITEUPS:
    cards.append(f"""<a class="card reveal" href="writeups/{w["slug"]}.html" data-tags="{" ".join(w["tags"])}">
<div class="thumb" style="background-image:url('{w["thumb"]}')"></div>
<div class="body"><div class="meta"><span>{w["platform"]}</span><span class="lvl easy">{w["level"]}</span></div>
<h3>{html.escape(w["short"])}</h3><p>{html.escape(w["teaser"]) if "teaser" in w else ""}</p>
<div class="meta"><div class="chips">{"".join(f'<span class="chip">{t}</span>' for t in w["tags"])}</div><span>{w["minutes"]} min</span></div></div></a>""")
idx = ROOT / "index.html"
s = idx.read_text()
s = re.sub(r"(<!-- CARDS -->).*?(<!-- /CARDS -->)", lambda m: m.group(1) + "\n" + "\n".join(cards) + "\n" + m.group(2), s, flags=re.S)
idx.write_text(s)
print("OK :", ", ".join(w["slug"] for w in WRITEUPS + PROJETS))
