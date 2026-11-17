"""Prouve la limitation de debit contre la force brute."""

from __future__ import annotations

from app.risks.rate_limit import LimiteurTentatives


def test_blocage_apres_seuil():
    limiteur = LimiteurTentatives(seuil=3, duree_blocage_s=60.0)
    identifiant = "alice"
    assert limiteur.est_bloque(identifiant) is False
    for _ in range(3):
        limiteur.enregistrer_echec(identifiant)
    assert limiteur.est_bloque(identifiant) is True


def test_reinitialisation_apres_succes():
    limiteur = LimiteurTentatives(seuil=3, duree_blocage_s=60.0)
    identifiant = "alice"
    for _ in range(3):
        limiteur.enregistrer_echec(identifiant)
    limiteur.reinitialiser(identifiant)
    assert limiteur.est_bloque(identifiant) is False


def test_endpoint_connexion_bloque_la_force_brute(client):
    donnees = {"identifiant": "victime", "mot_de_passe": "faux"}
    # Les 5 premiers echecs renvoient 401.
    for _ in range(5):
        reponse = client.post("/connexion", data=donnees)
        assert reponse.status_code == 401
    # Le compte est ensuite bloque : 429.
    reponse = client.post("/connexion", data=donnees)
    assert reponse.status_code == 429
