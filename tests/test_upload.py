"""Prouve la validation d'upload de fichier."""

from __future__ import annotations

import pytest

from app.risks.upload import (
    FichierEntrant,
    UploadRefuse,
    accepter_fichier_naif,
    accepter_fichier_securise,
)

IMAGE_VALIDE = FichierEntrant("photo.png", "image/png", b"\x89PNG contenu")
SCRIPT_MALVEILLANT = FichierEntrant("shell.php", "application/x-php", b"<?php ?>")
FICHIER_TROP_GROS = FichierEntrant("gros.png", "image/png", b"x" * (3 * 1024 * 1024))


def test_version_naive_accepte_tout():
    # L'attaque reussit : un script executable est accepte sans controle.
    assert "accepte" in accepter_fichier_naif(SCRIPT_MALVEILLANT)


def test_version_securisee_rejette_extension_dangereuse():
    with pytest.raises(UploadRefuse):
        accepter_fichier_securise(SCRIPT_MALVEILLANT)


def test_version_securisee_rejette_fichier_trop_gros():
    with pytest.raises(UploadRefuse):
        accepter_fichier_securise(FICHIER_TROP_GROS)


def test_version_securisee_rejette_mauvais_type_mime():
    mauvais_mime = FichierEntrant("photo.png", "text/html", b"<html>")
    with pytest.raises(UploadRefuse):
        accepter_fichier_securise(mauvais_mime)


def test_version_securisee_accepte_image_valide():
    assert "accepte apres validation" in accepter_fichier_securise(IMAGE_VALIDE)
