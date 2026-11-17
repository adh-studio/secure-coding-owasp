"""Prouve la gestion des secrets par l'environnement."""

from __future__ import annotations

import pytest

from app.risks.secrets_config import (
    recuperer_cle_api_naif,
    recuperer_cle_api_securise,
)


def test_version_naive_expose_le_secret():
    # Le secret est present dans le source : fuite inevitable via le depot.
    assert recuperer_cle_api_naif().startswith("sk_live_")


def test_version_securisee_echoue_sans_variable(monkeypatch):
    monkeypatch.delenv("CLE_API", raising=False)
    with pytest.raises(RuntimeError):
        recuperer_cle_api_securise()


def test_version_securisee_lit_la_variable(monkeypatch):
    monkeypatch.setenv("CLE_API", "valeur-injectee-par-l-environnement")
    assert recuperer_cle_api_securise() == "valeur-injectee-par-l-environnement"
