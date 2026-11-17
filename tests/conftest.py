"""Fixtures partagees par la suite de tests."""

from __future__ import annotations

import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.db import build_connection
from app.main import create_app


@pytest.fixture()
def connexion() -> sqlite3.Connection:
    """Fournit une base SQLite en memoire fraiche et isolee par test."""
    conn = build_connection()
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture()
def client() -> TestClient:
    """Client HTTP de test sur une instance neuve de l'application."""
    return TestClient(create_app())
