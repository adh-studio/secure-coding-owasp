"""Application FastAPI assemblant les demonstrations exposees en HTTP.

Toutes les reponses passent par un intergiciel qui applique les en-tetes de
securite. Les endpoints illustrent le XSS reflechi, la protection CSRF et la
limitation de debit a l'echelle d'une API.
"""

from __future__ import annotations

from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

from app.risks import xss
from app.risks.rate_limit import LimiteurTentatives
from app.security import (
    EN_TETES_SECURITE,
    generer_jeton_csrf,
    jeton_csrf_valide,
)


def create_app() -> FastAPI:
    """Fabrique l'application (pattern factory, pratique pour les tests)."""
    application = FastAPI(title="Vitrine OWASP - codage securise")
    limiteur = LimiteurTentatives(seuil=5, duree_blocage_s=300.0)

    @application.middleware("http")
    async def appliquer_entetes_securite(request: Request, call_next):
        """Applique les en-tetes de securite a chaque reponse."""
        reponse: Response = await call_next(request)
        for cle, valeur in EN_TETES_SECURITE.items():
            reponse.headers[cle] = valeur
        return reponse

    @application.get("/xss/naif", response_class=HTMLResponse)
    def xss_naif(message: str) -> str:
        """Reflete le message sans echappement (vulnerable, pedagogique)."""
        return xss.rendre_message_naif(message)

    @application.get("/xss/securise", response_class=HTMLResponse)
    def xss_securise(message: str) -> str:
        """Reflete le message echappe (securise)."""
        return xss.rendre_message_securise(message)

    @application.get("/csrf/jeton")
    def csrf_jeton(request: Request) -> JSONResponse:
        """Fournit un jeton CSRF lie a la session de l'appelant."""
        session_id = request.headers.get("X-Session-Id", "session-demo")
        return JSONResponse({"jeton_csrf": generer_jeton_csrf(session_id)})

    @application.post("/csrf/virement")
    def csrf_virement(
        request: Request,
        montant: int = Form(...),
        jeton_csrf: str = Form(default=""),
    ) -> JSONResponse:
        """Action sensible protegee par un jeton CSRF obligatoire."""
        session_id = request.headers.get("X-Session-Id", "session-demo")
        if not jeton_csrf_valide(session_id, jeton_csrf):
            raise HTTPException(status_code=403, detail="Jeton CSRF invalide")
        return JSONResponse({"statut": "virement accepte", "montant": montant})

    @application.post("/connexion")
    def connexion(
        identifiant: str = Form(...),
        mot_de_passe: str = Form(...),
    ) -> JSONResponse:
        """Endpoint de connexion protege par limitation de debit.

        Le secret attendu est volontairement fixe pour la demonstration ; le
        point demontre est le blocage apres plusieurs echecs.
        """
        if limiteur.est_bloque(identifiant):
            raise HTTPException(
                status_code=429, detail="Trop de tentatives, compte bloque"
            )
        if mot_de_passe != "MotDePasseCorrect1!":
            limiteur.enregistrer_echec(identifiant)
            raise HTTPException(status_code=401, detail="Identifiants invalides")
        limiteur.reinitialiser(identifiant)
        return JSONResponse({"statut": "connecte"})

    return application


app = create_app()
