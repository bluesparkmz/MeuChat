import sys
from pathlib import Path

from fastapi import FastAPI

# Comentario: garante import absoluto quando executar como script.
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from MeuChat.database import Base, engine
from MeuChat.routers import user as user_router
from MeuChat.routers import messages as messages_router
from MeuChat.routers import websoket_router

app = FastAPI(title="MeuChat")

# Comentario: cria tabelas no startup (para prototipo).
Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
app.include_router(messages_router.router)
app.include_router(websoket_router.router)
