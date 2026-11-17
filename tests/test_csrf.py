"""Prouve la protection CSRF de l'action sensible."""

from __future__ import annotations


def test_action_sans_jeton_est_refusee(client):
    # Requete forgee depuis un tiers, sans jeton : rejetee avec 403.
    reponse = client.post("/csrf/virement", data={"montant": 1000})
    assert reponse.status_code == 403


def test_action_avec_jeton_invalide_est_refusee(client):
    reponse = client.post(
        "/csrf/virement",
        data={"montant": 1000, "jeton_csrf": "jeton-bidon"},
    )
    assert reponse.status_code == 403


def test_action_avec_jeton_valide_est_acceptee(client):
    entetes = {"X-Session-Id": "session-alice"}
    jeton = client.get("/csrf/jeton", headers=entetes).json()["jeton_csrf"]
    reponse = client.post(
        "/csrf/virement",
        data={"montant": 1000, "jeton_csrf": jeton},
        headers=entetes,
    )
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "virement accepte"
