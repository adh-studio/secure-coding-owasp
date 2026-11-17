"""Prouve l'IDOR sur la version naive et sa mitigation."""

from __future__ import annotations

import pytest

from app.risks.controle_acces import (
    AccesRefuse,
    lire_document_naif,
    lire_document_securise,
)

# Alice (id 1) tente d'acceder au document 20 qui appartient a Bob (id 2).
ALICE = 1
DOCUMENT_DE_BOB = 20
DOCUMENT_D_ALICE = 10


def test_version_naive_permet_idor(connexion):
    # L'attaque reussit : Alice lit le document de Bob.
    document = lire_document_naif(connexion, DOCUMENT_DE_BOB)
    assert document is not None
    assert document["proprietaire_id"] == 2


def test_version_securisee_bloque_idor(connexion):
    # L'attaque echoue : la verification de propriete leve AccesRefuse.
    with pytest.raises(AccesRefuse):
        lire_document_securise(connexion, ALICE, DOCUMENT_DE_BOB)


def test_version_securisee_autorise_le_proprietaire(connexion):
    document = lire_document_securise(connexion, ALICE, DOCUMENT_D_ALICE)
    assert document["titre"] == "Note d'Alice"
