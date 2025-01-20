
from nexy.app import Nexy


def main():
    # Exemple de logique d'application, ici on lance une application FastAPI
    app = Nexy(title="Mon Application FastAPI")
    
    # Si vous utilisez FastAPI, vous pouvez démarrer le serveur
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
