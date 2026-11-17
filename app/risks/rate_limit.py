"""Limitation de debit contre la force brute (OWASP A07).

La version naive autorise un nombre illimite de tentatives de connexion. La
version securisee bloque temporairement un identifiant apres un seuil d'echecs.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class LimiteurTentatives:
    """Compteur de tentatives par identifiant avec fenetre de blocage.

    Implementation en memoire, suffisante pour la demonstration. En production
    un magasin partage (Redis) permettrait la mise a l'echelle horizontale.
    """

    seuil: int = 5
    duree_blocage_s: float = 300.0
    _etat: dict[str, tuple[int, float]] = field(default_factory=dict)

    def est_bloque(self, identifiant: str) -> bool:
        """Indique si l'identifiant est actuellement bloque."""
        tentatives, bloque_jusqu_a = self._etat.get(identifiant, (0, 0.0))
        if bloque_jusqu_a and time.monotonic() < bloque_jusqu_a:
            return True
        return False

    def enregistrer_echec(self, identifiant: str) -> None:
        """Comptabilise un echec et declenche le blocage au-dela du seuil."""
        tentatives, _ = self._etat.get(identifiant, (0, 0.0))
        tentatives += 1
        bloque_jusqu_a = 0.0
        if tentatives >= self.seuil:
            bloque_jusqu_a = time.monotonic() + self.duree_blocage_s
        self._etat[identifiant] = (tentatives, bloque_jusqu_a)

    def reinitialiser(self, identifiant: str) -> None:
        """Remet le compteur a zero apres une connexion reussie."""
        self._etat.pop(identifiant, None)
