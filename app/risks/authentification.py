"""Authentification (OWASP A07).

La version naive stocke les mots de passe en clair et les compare avec ==. La
version securisee impose une politique de robustesse, hache avec PBKDF2 et
compare en temps constant.
"""

from __future__ import annotations

from app.security import (
    hacher_mot_de_passe,
    mot_de_passe_conforme,
    verifier_mot_de_passe,
)


class MotDePasseFaible(Exception):
    """Levee lorsqu'un mot de passe ne respecte pas la politique."""


class RegistreNaif:
    """VERSION VULNERABLE (pedagogique, isolee).

    Stocke les mots de passe en clair : une fuite de la base expose tous les
    comptes et aucune politique n'est appliquee.
    """

    def __init__(self) -> None:
        self._comptes: dict[str, str] = {}

    def inscrire(self, identifiant: str, mot_de_passe: str) -> None:
        self._comptes[identifiant] = mot_de_passe

    def verifier(self, identifiant: str, mot_de_passe: str) -> bool:
        return self._comptes.get(identifiant) == mot_de_passe

    def mot_de_passe_stocke(self, identifiant: str) -> str:
        return self._comptes[identifiant]


class RegistreSecurise:
    """VERSION SECURISEE.

    Applique la politique de robustesse, ne conserve que des condenses PBKDF2
    sales et verifie en temps constant.
    """

    def __init__(self) -> None:
        self._condenses: dict[str, str] = {}

    def inscrire(self, identifiant: str, mot_de_passe: str) -> None:
        if not mot_de_passe_conforme(mot_de_passe):
            raise MotDePasseFaible(
                "Le mot de passe ne respecte pas la politique de robustesse"
            )
        self._condenses[identifiant] = hacher_mot_de_passe(mot_de_passe)

    def verifier(self, identifiant: str, mot_de_passe: str) -> bool:
        condense = self._condenses.get(identifiant)
        if condense is None:
            return False
        return verifier_mot_de_passe(mot_de_passe, condense)

    def condense_stocke(self, identifiant: str) -> str:
        return self._condenses[identifiant]
