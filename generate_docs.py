"""Genere docs/index.html a partir du catalogue de risques.

Le script execute la suite pytest de chaque risque et reporte le statut reel
(reussi / echoue) dans la page de synthese. La page est auto-contenue (CSS
integre) et publiable telle quelle sur GitHub Pages.
"""

from __future__ import annotations

import html
import subprocess
import sys
from datetime import date
from pathlib import Path

from app.risks import CATALOGUE, FicheRisque

RACINE = Path(__file__).resolve().parent
DOSSIER_TESTS = RACINE / "tests"
SORTIE = RACINE / "docs" / "index.html"


def _statut_test(fichier_test: str) -> bool:
    """Execute le fichier de test et renvoie True si tout passe."""
    resultat = subprocess.run(
        [sys.executable, "-m", "pytest", str(DOSSIER_TESTS / fichier_test), "-q"],
        cwd=RACINE,
        capture_output=True,
        text=True,
    )
    return resultat.returncode == 0


def _ligne(fiche: FicheRisque, reussi: bool) -> str:
    badge = "reussi" if reussi else "echoue"
    classe = "ok" if reussi else "ko"
    return f"""      <tr>
        <td><span class="tag">{html.escape(fiche.identifiant)}</span></td>
        <td class="titre">{html.escape(fiche.titre)}</td>
        <td>{html.escape(fiche.attaque)}</td>
        <td>{html.escape(fiche.mitigation)}</td>
        <td><code>{html.escape(fiche.test)}</code></td>
        <td><span class="statut {classe}">{badge}</span></td>
      </tr>"""


def construire() -> str:
    lignes = []
    tous_verts = True
    for fiche in CATALOGUE:
        reussi = _statut_test(fiche.test)
        tous_verts = tous_verts and reussi
        lignes.append(_ligne(fiche, reussi))
    corps_table = "\n".join(lignes)
    bandeau = "Tous les tests sont au vert" if tous_verts else "Des tests echouent"
    return _GABARIT.format(
        corps=corps_table,
        date=date.today().isoformat(),
        bandeau=html.escape(bandeau),
        nombre=len(CATALOGUE),
    )


_GABARIT = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vitrine de codage securise - OWASP Top 10</title>
  <style>
    :root {{ color-scheme: light dark; }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: #0f172a; color: #e2e8f0; line-height: 1.5;
    }}
    header {{ padding: 2.5rem 1.5rem 1.5rem; max-width: 1100px; margin: 0 auto; }}
    h1 {{ margin: 0 0 .4rem; font-size: 1.8rem; }}
    .sous-titre {{ color: #94a3b8; margin: 0 0 1rem; }}
    .bandeau {{
      display: inline-block; background: #064e3b; color: #6ee7b7;
      padding: .4rem .9rem; border-radius: 999px; font-weight: 600; font-size: .9rem;
    }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 0 1.5rem 3rem; }}
    .table-wrap {{ overflow-x: auto; border-radius: 12px; border: 1px solid #1e293b; }}
    table {{ border-collapse: collapse; width: 100%; min-width: 820px; background: #111827; }}
    th, td {{ padding: .75rem .9rem; text-align: left; border-bottom: 1px solid #1e293b; vertical-align: top; font-size: .92rem; }}
    th {{ background: #1e293b; color: #cbd5e1; position: sticky; top: 0; font-weight: 600; }}
    .titre {{ font-weight: 600; color: #f1f5f9; }}
    .tag {{ background: #312e81; color: #c7d2fe; padding: .15rem .5rem; border-radius: 6px; font-size: .78rem; font-weight: 600; }}
    code {{ background: #0b1220; padding: .15rem .4rem; border-radius: 5px; font-size: .82rem; color: #a5b4fc; }}
    .statut {{ padding: .2rem .6rem; border-radius: 999px; font-size: .78rem; font-weight: 700; }}
    .statut.ok {{ background: #064e3b; color: #6ee7b7; }}
    .statut.ko {{ background: #7f1d1d; color: #fecaca; }}
    footer {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; color: #64748b; font-size: .85rem; }}
    @media (prefers-color-scheme: light) {{
      body {{ background: #f8fafc; color: #0f172a; }}
      table {{ background: #fff; }}
      th {{ background: #e2e8f0; color: #334155; }}
      .table-wrap {{ border-color: #e2e8f0; }}
      th, td {{ border-color: #e2e8f0; }}
      .titre {{ color: #0f172a; }}
      code {{ background: #f1f5f9; color: #4338ca; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Vitrine de codage securise - OWASP Top 10</h1>
    <p class="sous-titre">{nombre} risques demontres, chacun avec une version vulnerable, une version securisee et un test automatise qui prouve la mitigation.</p>
    <span class="bandeau">{bandeau}</span>
  </header>
  <main>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>OWASP</th>
            <th>Risque</th>
            <th>Attaque demontree</th>
            <th>Mitigation</th>
            <th>Test</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
{corps}
        </tbody>
      </table>
    </div>
  </main>
  <footer>
    Page generee le {date}. Chaque statut provient de l'execution reelle de la suite pytest correspondante.
  </footer>
</body>
</html>
"""


if __name__ == "__main__":
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(construire(), encoding="utf-8")
    print(f"Page generee: {SORTIE}")
