"""Primitives de securite transverses.

Ce module regroupe les briques reutilisees par plusieurs demonstrations :
hachage de mots de passe, jetons anti-CSRF, chargement des secrets depuis
l'environnement et politique de mot de passe. Le code s'appuie uniquement sur la
bibliotheque standard afin de rester auditable.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets

# Parametres de hachage PBKDF2. Un cout eleve ralentit les attaques par force
# brute hors ligne. La valeur est volontairement explicite et commentee.
_ALGORITHME = "sha256"
_ITERATIONS = 200_000
_TAILLE_SEL = 16


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    """Hache un mot de passe avec PBKDF2 et un sel aleatoire par utilisateur.

    Le format retourne est "pbkdf2$<iterations>$<sel_hex>$<empreinte_hex>".
    Deux hachages du meme mot de passe different grace au sel.
    """
    sel = secrets.token_bytes(_TAILLE_SEL)
    empreinte = hashlib.pbkdf2_hmac(
        _ALGORITHME, mot_de_passe.encode("utf-8"), sel, _ITERATIONS
    )
    return f"pbkdf2${_ITERATIONS}${sel.hex()}${empreinte.hex()}"


def verifier_mot_de_passe(mot_de_passe: str, condense: str) -> bool:
    """Verifie un mot de passe en temps constant contre un condense stocke."""
    try:
        schema, iterations, sel_hex, empreinte_hex = condense.split("$")
    except ValueError:
        return False
    if schema != "pbkdf2":
        return False
    sel = bytes.fromhex(sel_hex)
    attendu = bytes.fromhex(empreinte_hex)
    calcule = hashlib.pbkdf2_hmac(
        _ALGORITHME, mot_de_passe.encode("utf-8"), sel, int(iterations)
    )
    # hmac.compare_digest evite les attaques temporelles sur la comparaison.
    return hmac.compare_digest(calcule, attendu)


# Expression de la politique de mot de passe : au moins 12 caracteres, une
# minuscule, une majuscule, un chiffre et un caractere special.
_POLITIQUE = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{12,}$"
)


def mot_de_passe_conforme(mot_de_passe: str) -> bool:
    """Indique si un mot de passe respecte la politique de robustesse."""
    return bool(_POLITIQUE.match(mot_de_passe))


# Cle de signature des jetons CSRF. En production elle provient d'un secret
# d'environnement ; ici une valeur de session est generee au demarrage.
_CLE_CSRF = secrets.token_bytes(32)


def generer_jeton_csrf(session_id: str) -> str:
    """Genere un jeton CSRF lie a une session (schema signe HMAC)."""
    message = session_id.encode("utf-8")
    signature = hmac.new(_CLE_CSRF, message, hashlib.sha256).hexdigest()
    return signature


def jeton_csrf_valide(session_id: str, jeton: str) -> bool:
    """Valide un jeton CSRF en temps constant."""
    attendu = generer_jeton_csrf(session_id)
    return hmac.compare_digest(attendu, jeton or "")


def charger_secret(nom: str) -> str:
    """Charge un secret depuis l'environnement.

    Lever une erreur explicite en l'absence du secret evite les valeurs par
    defaut dangereuses codees en dur.
    """
    valeur = os.environ.get(nom)
    if not valeur:
        raise RuntimeError(
            f"Secret manquant: {nom}. Definir la variable d'environnement."
        )
    return valeur


# En-tetes de securite appliques a toutes les reponses de l'application.
EN_TETES_SECURITE = {
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'self'; object-src 'none'; frame-ancestors 'none'",
}
