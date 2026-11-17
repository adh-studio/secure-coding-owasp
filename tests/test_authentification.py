"""Prouve les faiblesses du registre naif et la robustesse du securise."""

from __future__ import annotations

import pytest

from app.risks.authentification import (
    MotDePasseFaible,
    RegistreNaif,
    RegistreSecurise,
)

MOT_DE_PASSE_FORT = "Str0ng!Passphrase42"


def test_registre_naif_stocke_en_clair():
    registre = RegistreNaif()
    registre.inscrire("alice", "secret")
    # Le mot de passe est lisible tel quel : fuite directe en cas de vol de base.
    assert registre.mot_de_passe_stocke("alice") == "secret"


def test_registre_securise_ne_stocke_pas_en_clair():
    registre = RegistreSecurise()
    registre.inscrire("alice", MOT_DE_PASSE_FORT)
    condense = registre.condense_stocke("alice")
    assert MOT_DE_PASSE_FORT not in condense
    assert condense.startswith("pbkdf2$")


def test_registre_securise_verifie_correctement():
    registre = RegistreSecurise()
    registre.inscrire("alice", MOT_DE_PASSE_FORT)
    assert registre.verifier("alice", MOT_DE_PASSE_FORT) is True
    assert registre.verifier("alice", "mauvais") is False


def test_politique_rejette_mot_de_passe_faible():
    registre = RegistreSecurise()
    with pytest.raises(MotDePasseFaible):
        registre.inscrire("alice", "123456")


def test_sel_rend_les_condenses_uniques():
    registre = RegistreSecurise()
    registre.inscrire("alice", MOT_DE_PASSE_FORT)
    registre.inscrire("bob", MOT_DE_PASSE_FORT)
    # Meme mot de passe, condenses differents grace au sel aleatoire.
    assert registre.condense_stocke("alice") != registre.condense_stocke("bob")
