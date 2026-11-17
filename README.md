# Vitrine de codage securise - OWASP Top 10

Projet de demonstration de codage securise. Pour chacun des risques majeurs de
l'OWASP Top 10, le depot propose une implementation **naive (vulnerable)** et une
implementation **securisee**, accompagnees d'un **test automatise** qui prouve que
l'attaque reussit sur la version naive et echoue sur la version securisee.

L'objectif n'est pas de livrer une application metier mais de montrer, de maniere
verifiable, la maitrise des mecanismes de defense et de la demarche de preuve par
les tests.

## Contexte

Le code naif est volontairement vulnerable, isole dans des fonctions dediees et
documente comme pedagogique. Les attaques ne sont jouees que dans le bac a sable
des tests (base SQLite en memoire, application de test), jamais sur une ressource
reelle.

## Stack

- **Python 3.13** et **FastAPI** pour les demonstrations exposees en HTTP.
- **SQLite en memoire** comme bac a sable pour l'injection SQL et l'IDOR.
- **pytest** pour la preuve de chaque mitigation.
- Primitives de securite issues de la **bibliotheque standard** (hashlib PBKDF2,
  hmac, secrets) pour rester auditable, sans dependance cryptographique opaque.

## Architecture

```
app/
  security.py        Primitives transverses (hachage, CSRF, secrets, en-tetes)
  db.py              Bac a sable SQLite en memoire (donnees d'essai)
  main.py            Application FastAPI (middleware d'en-tetes, endpoints)
  risks/
    __init__.py          Catalogue des risques (alimente la page de synthese)
    injection_sql.py     A03 - requete concatenee vs parametree
    xss.py               A03 - sortie non echappee vs echappee + CSP
    controle_acces.py    A01 - IDOR vs verification de propriete
    authentification.py  A07 - clair vs PBKDF2 sale + politique
    rate_limit.py        A07 - tentatives illimitees vs blocage
    secrets_config.py    A05 - secret en dur vs variable d'environnement
    upload.py            A04 - upload non controle vs validation type/taille
tests/                 Un fichier de test par risque (36 tests)
docs/index.html        Tableau recapitulatif publiable (statut reel des tests)
generate_docs.py       Generateur de la page de synthese
```

Chaque risque suit le meme contrat : une fonction naive, une fonction securisee,
et des tests qui demontrent la bascule. Les modules sont independants (faible
couplage), ce qui respecte la separation des responsabilites et facilite la revue.

## Risques couverts

| OWASP | Risque | Mitigation demontree |
|-------|--------|----------------------|
| A03 | Injection SQL | Requete parametree (liaison des valeurs) |
| A03 | XSS reflechi | Echappement HTML + Content-Security-Policy |
| A01 | CSRF | Jeton signe HMAC lie a la session |
| A07 | Authentification | Hachage PBKDF2 sale + comparaison temps constant + politique |
| A01 | Controle d'acces (IDOR) | Verification de propriete avant restitution |
| A05 | En-tetes de securite | HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy |
| A07 | Limitation de debit | Blocage temporaire apres seuil d'echecs |
| A05 | Gestion des secrets | Chargement depuis l'environnement, echec si absent |
| A04 | Upload de fichier | Validation extension, type MIME et taille |

## Installation

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest
```

## Commande de test unique

```bash
python -m pytest
```

La suite est deterministe : chaque test reconstruit son bac a sable. Pour
regenerer la page de synthese avec le statut reel des tests :

```bash
python generate_docs.py
```

La page produite dans `docs/index.html` est publiable sur GitHub Pages (voir
`PUBLISH.md`).

## Ce que ce projet demontre pour un poste Full Stack

- **Securite applicative** : couverture concrete de l'OWASP Top 10 (injection,
  XSS, CSRF, controle d'acces, authentification, en-tetes, limitation de debit,
  gestion des secrets, upload), chaque mitigation etant prouvee par un test.
- **Authentification et autorisation** : hachage PBKDF2 sale, comparaison en temps
  constant, politique de robustesse, verification de propriete (IDOR).
- **Backend Python / API RESTful** : application FastAPI structuree, endpoints
  testes via le client de test, intergiciel d'en-tetes de securite.
- **Bases de donnees SQL** : requetes parametrees sur SQLite, demonstration de
  l'injection et de sa mitigation.
- **Genie logiciel** : clean architecture, modules a responsabilite unique,
  faible couplage, code commente avec sobriete, tests unitaires et d'integration
  reels.
- **CI/CD** : workflow GitHub Actions qui installe la toolchain, lance les tests
  et regenere la page de synthese a chaque push.
- **Documentation technique** : README structure, catalogue des risques, page de
  synthese generee automatiquement avec le statut des tests.
