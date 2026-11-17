"""Injection SQL (OWASP A03).

La version naive concatene l'entree utilisateur dans la requete SQL, ce qui
permet d'alterer la logique de la clause WHERE. La version securisee utilise une
requete parametree : la valeur n'est jamais interpretee comme du code SQL.
"""

from __future__ import annotations

import sqlite3


def rechercher_utilisateur_naif(
    connection: sqlite3.Connection, email: str
) -> list[sqlite3.Row]:
    """VERSION VULNERABLE (pedagogique, isolee).

    L'email est injecte directement dans la chaine SQL. Une charge du type
    "x' OR '1'='1" renvoie l'integralite de la table.
    """
    requete = f"SELECT id, nom, email FROM utilisateurs WHERE email = '{email}'"
    return connection.execute(requete).fetchall()


def rechercher_utilisateur_securise(
    connection: sqlite3.Connection, email: str
) -> list[sqlite3.Row]:
    """VERSION SECURISEE.

    La valeur est liee via un parametre : le moteur la traite comme une donnee,
    jamais comme du code. La meme charge ne renvoie aucune ligne.
    """
    requete = "SELECT id, nom, email FROM utilisateurs WHERE email = ?"
    return connection.execute(requete, (email,)).fetchall()
