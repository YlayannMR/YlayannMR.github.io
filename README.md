# Portfolio · Ylayann Malouda-Ribardiere

Site statique (HTML/CSS/JS, sans dépendance) publié avec GitHub Pages.

- `index.html` : page d'accueil
- `writeups/`, `projets/` : pages générées à partir des README de [ctf-writeups](https://github.com/YlayannMR/ctf-writeups) et [SMSI_training](https://github.com/YlayannMR/SMSI_training) et [AI-risk-assessment](https://github.com/YlayannMR/AI-risk-assessment)
- `build.py` : régénère ces pages (nécessite pandoc)

```bash
git clone https://github.com/YlayannMR/ctf-writeups ../ctf-writeups
git clone https://github.com/YlayannMR/SMSI_training ../SMSI_training
git clone https://github.com/YlayannMR/AI-risk-assessment ../AI-risk-assessment
python3 build.py ../ctf-writeups ../SMSI_training ../AI-risk-assessment
```

Pour ajouter un write-up : une entrée dans la liste `WRITEUPS` de `build.py`, puis relancer le script.
