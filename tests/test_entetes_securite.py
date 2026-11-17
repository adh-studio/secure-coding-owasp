"""Verifie la presence des en-tetes de securite sur les reponses."""

from __future__ import annotations

import pytest

ENTETES_ATTENDUS = [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
    "Referrer-Policy",
]


@pytest.mark.parametrize("entete", ENTETES_ATTENDUS)
def test_entete_present(client, entete):
    reponse = client.get("/xss/securise", params={"message": "ok"})
    assert entete in reponse.headers


def test_nosniff_actif(client):
    reponse = client.get("/xss/securise", params={"message": "ok"})
    assert reponse.headers["X-Content-Type-Options"] == "nosniff"
