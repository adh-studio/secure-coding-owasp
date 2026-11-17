# Publication

Le depot est initialise en local (branche `main`) mais n'est pas pousse. Commandes
exactes a executer pour publier sous le compte GitHub `adh-studio`.

## 1. Creer le depot distant et pousser

```bash
cd /Users/wize/fullstack-entretien/projets/secure-coding-owasp
gh repo create secure-coding-owasp \
  --public \
  --description "Vitrine de codage securise OWASP Top 10 : versions vulnerable vs securisee, chaque mitigation prouvee par un test" \
  --source . \
  --push
```

## 2. Activer GitHub Pages (artefact visuel)

La page de synthese se trouve dans `docs/index.html`. L'activer sur la branche
`main`, dossier `/docs` :

```bash
gh api -X POST repos/adh-studio/secure-coding-owasp/pages \
  -f "source[branch]=main" \
  -f "source[path]=/docs"
```

URL de la page une fois publiee :
`https://adh-studio.github.io/secure-coding-owasp/`

## 3. Verifier la CI

Le workflow `.github/workflows/ci.yml` se declenche automatiquement au push. Il
installe Python 3.13, les dependances et lance `pytest`, puis regenere la page.

```bash
gh run list --limit 1
gh run watch
```
