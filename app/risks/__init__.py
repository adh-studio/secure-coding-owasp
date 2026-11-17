"""Catalogue des risques OWASP demontres.

Chaque module expose une paire de fonctions ou d'endpoints : une version naive
(vulnerable, isolee et documentee comme pedagogique) et une version securisee.
Le registre CATALOGUE ci-dessous alimente la page recapitulative docs/index.html.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FicheRisque:
    """Decrit un risque pour la page de synthese."""

    identifiant: str
    titre: str
    attaque: str
    mitigation: str
    test: str


CATALOGUE: list[FicheRisque] = [
    FicheRisque(
        "A03",
        "Injection SQL",
        "Charge utile ' OR '1'='1 dans un champ concatene a la requete",
        "Requete parametree avec liaison des valeurs",
        "test_sql_injection.py",
    ),
    FicheRisque(
        "A03",
        "Cross-Site Scripting (XSS)",
        "Injection d'une balise <script> dans un contenu reflete",
        "Echappement HTML de la sortie et en-tete Content-Security-Policy",
        "test_xss.py",
    ),
    FicheRisque(
        "A01",
        "CSRF",
        "Requete d'etat sans jeton depuis un site tiers",
        "Jeton anti-CSRF signe, lie a la session et verifie",
        "test_csrf.py",
    ),
    FicheRisque(
        "A07",
        "Authentification",
        "Mots de passe en clair et comparaison faible",
        "Hachage PBKDF2 avec sel et politique de robustesse",
        "test_authentification.py",
    ),
    FicheRisque(
        "A01",
        "Controle d'acces (IDOR)",
        "Acces au document d'un autre utilisateur via son identifiant",
        "Verification de propriete avant restitution de la ressource",
        "test_controle_acces.py",
    ),
    FicheRisque(
        "A05",
        "En-tetes de securite",
        "Absence de HSTS, CSP et X-Content-Type-Options",
        "Intergiciel appliquant les en-tetes de securite a chaque reponse",
        "test_entetes_securite.py",
    ),
    FicheRisque(
        "A07",
        "Limitation de debit (force brute)",
        "Essais de connexion illimites sur un compte",
        "Compteur de tentatives avec blocage temporaire par identifiant",
        "test_rate_limit.py",
    ),
    FicheRisque(
        "A05",
        "Gestion des secrets",
        "Secret d'API code en dur dans le source",
        "Chargement du secret depuis l'environnement, erreur si absent",
        "test_secrets.py",
    ),
    FicheRisque(
        "A04",
        "Upload de fichier",
        "Depot d'un fichier .php ou surdimensionne sans controle",
        "Validation du type MIME, de l'extension et de la taille",
        "test_upload.py",
    ),
]
