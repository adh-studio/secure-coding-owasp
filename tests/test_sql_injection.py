"""Prouve l'injection SQL sur la version naive et sa mitigation."""

from __future__ import annotations

from app.risks.injection_sql import (
    rechercher_utilisateur_naif,
    rechercher_utilisateur_securise,
)

# Charge classique : la clause OR '1'='1' rend la condition toujours vraie.
CHARGE = "inconnu@example.com' OR '1'='1"


def test_version_naive_est_vulnerable(connexion):
    # L'attaque reussit : toutes les lignes de la table sont exfiltrees.
    resultats = rechercher_utilisateur_naif(connexion, CHARGE)
    assert len(resultats) == 2


def test_version_securisee_bloque_l_injection(connexion):
    # L'attaque echoue : la charge est traitee comme une simple valeur.
    resultats = rechercher_utilisateur_securise(connexion, CHARGE)
    assert resultats == []


def test_version_securisee_reste_fonctionnelle(connexion):
    # La recherche legitime fonctionne toujours.
    resultats = rechercher_utilisateur_securise(connexion, "alice@example.com")
    assert len(resultats) == 1
    assert resultats[0]["nom"] == "Alice"
