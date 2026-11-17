"""Prouve le XSS reflechi sur la version naive et sa mitigation."""

from __future__ import annotations

from app.risks.xss import rendre_message_naif, rendre_message_securise

CHARGE = "<script>alert('xss')</script>"


def test_version_naive_est_vulnerable():
    # La balise script est restituee intacte : elle s'executerait cote client.
    sortie = rendre_message_naif(CHARGE)
    assert "<script>" in sortie


def test_version_securisee_echappe_la_sortie():
    # Les chevrons sont echappes : le script devient du texte inerte.
    sortie = rendre_message_securise(CHARGE)
    assert "<script>" not in sortie
    assert "&lt;script&gt;" in sortie


def test_en_tete_csp_present(client):
    # Defense en profondeur : la CSP restreint l'execution de scripts.
    reponse = client.get("/xss/securise", params={"message": "bonjour"})
    assert "Content-Security-Policy" in reponse.headers


def test_endpoint_naif_reflete_le_script(client):
    reponse = client.get("/xss/naif", params={"message": CHARGE})
    assert "<script>" in reponse.text


def test_endpoint_securise_echappe_le_script(client):
    reponse = client.get("/xss/securise", params={"message": CHARGE})
    assert "<script>" not in reponse.text
    assert "&lt;script&gt;" in reponse.text
