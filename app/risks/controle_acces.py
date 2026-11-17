"""Controle d'acces et IDOR (OWASP A01).

La version naive renvoie n'importe quel document a partir de son identifiant,
sans verifier que l'appelant en est proprietaire. La version securisee controle
la propriete avant de restituer la ressource.
"""

from __future__ import annotations

import sqlite3


class AccesRefuse(Exception):
    """Levee lorsqu'un utilisateur tente d'acceder a une ressource non autorisee."""


def lire_document_naif(
    connection: sqlite3.Connection, document_id: int
) -> sqlite3.Row | None:
    """VERSION VULNERABLE (pedagogique, isolee).

    Aucun controle de propriete : l'utilisateur courant peut lire le document
    d'un autre en changeant l'identifiant (IDOR).
    """
    return connection.execute(
        "SELECT id, proprietaire_id, titre, contenu FROM documents WHERE id = ?",
        (document_id,),
    ).fetchone()


def lire_document_securise(
    connection: sqlite3.Connection, utilisateur_id: int, document_id: int
) -> sqlite3.Row:
    """VERSION SECURISEE.

    La requete contraint l'acces au proprietaire. Si le document n'appartient
    pas a l'utilisateur, une exception AccesRefuse est levee.
    """
    ligne = connection.execute(
        "SELECT id, proprietaire_id, titre, contenu FROM documents "
        "WHERE id = ? AND proprietaire_id = ?",
        (document_id, utilisateur_id),
    ).fetchone()
    if ligne is None:
        raise AccesRefuse(
            f"L'utilisateur {utilisateur_id} ne peut pas acceder au document {document_id}"
        )
    return ligne
