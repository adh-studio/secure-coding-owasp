"""Validation d'upload de fichier (OWASP A04 / A08).

La version naive accepte tout fichier. La version securisee controle
l'extension, le type MIME declare et la taille avant d'accepter le depot.
"""

from __future__ import annotations

from dataclasses import dataclass

# Types et extensions autorises pour la demonstration (images uniquement).
_EXTENSIONS_AUTORISEES = {".png", ".jpg", ".jpeg", ".webp"}
_TYPES_MIME_AUTORISES = {"image/png", "image/jpeg", "image/webp"}
_TAILLE_MAX_OCTETS = 2 * 1024 * 1024  # 2 Mio


class UploadRefuse(Exception):
    """Levee lorsqu'un fichier ne respecte pas la politique d'upload."""


@dataclass(frozen=True)
class FichierEntrant:
    """Represente un fichier soumis (metadonnees et contenu)."""

    nom: str
    type_mime: str
    contenu: bytes


def accepter_fichier_naif(fichier: FichierEntrant) -> str:
    """VERSION VULNERABLE (pedagogique, isolee).

    Aucun controle : un script .php ou un fichier enorme est accepte.
    """
    return f"Fichier {fichier.nom} accepte sans controle"


def accepter_fichier_securise(fichier: FichierEntrant) -> str:
    """VERSION SECURISEE.

    Rejette toute extension, tout type MIME ou toute taille non conformes.
    """
    extension = _extension(fichier.nom)
    if extension not in _EXTENSIONS_AUTORISEES:
        raise UploadRefuse(f"Extension non autorisee: {extension}")
    if fichier.type_mime not in _TYPES_MIME_AUTORISES:
        raise UploadRefuse(f"Type MIME non autorise: {fichier.type_mime}")
    if len(fichier.contenu) > _TAILLE_MAX_OCTETS:
        raise UploadRefuse("Fichier trop volumineux")
    return f"Fichier {fichier.nom} accepte apres validation"


def _extension(nom: str) -> str:
    point = nom.rfind(".")
    return nom[point:].lower() if point != -1 else ""
