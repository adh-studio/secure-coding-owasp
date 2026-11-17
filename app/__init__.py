"""Vitrine de codage securise base sur l'OWASP Top 10.

Chaque risque est isole dans son propre module (voir app/risks). Pour chaque
risque, une implementation "naive" volontairement vulnerable cohabite avec une
implementation "securisee". Les tests (dossier tests/) prouvent que l'attaque
reussit sur la version naive et echoue sur la version securisee.
"""

__all__ = ["create_app"]

from app.main import create_app
