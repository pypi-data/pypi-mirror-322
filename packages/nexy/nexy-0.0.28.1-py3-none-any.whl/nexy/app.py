import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference
from .router import Router

# Données SVG de l'icône
SVG_DATA_URI = """data:image/svg+xml;base64,<svg width='100' height='100' viewBox='0 0 100 100' fill='none' xmlns='http://www.w3.org/2000/svg'>
        <rect width='100' height='100' fill='#CBECE3'/>
        <path d='M27 78V22H30.1379L69.2414 60.0575V22H72.2184V78H27Z' fill='#1CB68D'/>
        </svg>
        """


def Nexy(title: str = None, favicon: str = SVG_DATA_URI, **args) -> FastAPI:
    """
    Crée une instance de FastAPI avec les configurations de base.

    :param title: Titre de l'application (par défaut, le nom du répertoire courant).
    :param favicon: URL ou données de l'icône (par défaut les données SVG définies ci-dessus).
    :param args: Arguments supplémentaires à passer à FastAPI.
    :return: Instance FastAPI configurée.
    """
    
    # Si aucun titre n'est passé, utiliser le nom du répertoire courant
    if title is None:
        title = Path.cwd().name 

    # Création de l'instance FastAPI
    app: FastAPI = FastAPI(
        title=title,
        docs_url="/122xxxxxx2345",
        redoc_url="/xx123n134",
        **args
    )

    @app.get("/docs", include_in_schema=False)
    async def scalar_html():  
        """
        Fournit une vue personnalisée de la documentation OpenAPI avec l'icône définie.
        """
        return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=app.title,
            scalar_favicon_url=favicon
        )

    # Montée du dossier statique si il existe
    static_dir = "public"
    if os.path.exists(static_dir):
        app.mount("/public", StaticFiles(directory=static_dir), name="Public")

    # Inclusion du routeur
    app.include_router(Router())

    # Configuration du cache
    cache_dir = Path('./__pycache__/nexy')
    cache_dir.mkdir(exist_ok=True)
    sys.pycache_prefix = str(cache_dir)

    return app
