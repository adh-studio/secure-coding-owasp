"""Cross-Site Scripting reflechi (OWASP A03).

La version naive insere l'entree utilisateur dans le HTML sans echappement, ce
qui permet d'executer du script arbitraire. La version securisee echappe la
sortie et s'appuie sur une Content-Security-Policy restrictive.
"""

from __future__ import annotations

import html


def rendre_message_naif(message: str) -> str:
    """VERSION VULNERABLE (pedagogique, isolee).

    Le message est injecte tel quel : une balise <script> reste active.
    """
    return f"<div class='message'>{message}</div>"


def rendre_message_securise(message: str) -> str:
    """VERSION SECURISEE.

    html.escape neutralise les caracteres speciaux (< > & ' ") : le script est
    affiche comme du texte et non execute.
    """
    return f"<div class='message'>{html.escape(message)}</div>"
