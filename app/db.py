"""Acces aux donnees.

Une base SQLite en memoire sert de bac a sable pour les demonstrations. Elle est
recreee a chaque appel de build_connection afin que les tests restent isoles et
reproductibles. Deux tables suffisent pour illustrer l'injection SQL et le
controle d'acces (IDOR).
"""

from __future__ import annotations

import sqlite3


def build_connection() -> sqlite3.Connection:
    """Construit une connexion SQLite en memoire alimentee par un jeu d'essai.

    Chaque connexion est independante : les demonstrations ne partagent pas
    d'etat, ce qui garantit des tests deterministes.
    """
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    _seed(connection)
    return connection


def _seed(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.executescript(
        """
        CREATE TABLE utilisateurs (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            secret TEXT NOT NULL
        );

        CREATE TABLE documents (
            id INTEGER PRIMARY KEY,
            proprietaire_id INTEGER NOT NULL,
            titre TEXT NOT NULL,
            contenu TEXT NOT NULL
        );
        """
    )
    cursor.executemany(
        "INSERT INTO utilisateurs (id, nom, email, secret) VALUES (?, ?, ?, ?)",
        [
            (1, "Alice", "alice@example.com", "jeton-prive-alice"),
            (2, "Bob", "bob@example.com", "jeton-prive-bob"),
        ],
    )
    cursor.executemany(
        "INSERT INTO documents (id, proprietaire_id, titre, contenu) VALUES (?, ?, ?, ?)",
        [
            (10, 1, "Note d'Alice", "Confidentiel: budget interne"),
            (20, 2, "Note de Bob", "Confidentiel: feuille de route"),
        ],
    )
    connection.commit()
