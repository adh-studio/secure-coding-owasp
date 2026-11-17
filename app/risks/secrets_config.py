"""Gestion des secrets (OWASP A05).

La version naive code une cle d'API directement dans le source : toute personne
ayant acces au depot la connait. La version securisee lit le secret depuis
l'environnement et echoue explicitement s'il est absent.
"""

from __future__ import annotations

from app.security import charger_secret

# VERSION VULNERABLE (pedagogique) : un secret code en dur reste dans
# l'historique Git et fuite avec le code source.
CLE_API_EN_DUR = "sk_live_1234567890_secret_code_en_dur"


def recuperer_cle_api_naif() -> str:
    """Retourne le secret code en dur (a ne jamais faire en production)."""
    return CLE_API_EN_DUR


def recuperer_cle_api_securise() -> str:
    """Charge le secret depuis la variable d'environnement CLE_API.

    Leve une RuntimeError si la variable n'est pas definie, ce qui empeche tout
    repli silencieux sur une valeur par defaut dangereuse.
    """
    return charger_secret("CLE_API")
