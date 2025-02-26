from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from .config import get_settings
from .routes import StoresRouter, BotRouter, DataRouter
from .bots import LLMFactory, LLMProvider, TemplateParser
from .stores import VictorsFactory, VectorsEnums, ChromaDistanceEnums

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    llm_factory = LLMFactory()
    app.llm = llm_factory.create(provider=LLMProvider.OLLAMA.value)
    app.llm.set_embedding_model(settings.EMBED_MODEL_NAME)
    app.llm.set_generation_model(settings.GENERATION_MODEL_NAME)

    vdb_factory = VictorsFactory(
        path=settings.VDB_PATH,
        distance_method=ChromaDistanceEnums.COSINE.value,
    )
    app.vdb = vdb_factory.create(provider=VectorsEnums.CHROMA.value)
    app.vdb.connect()

    app.template_parser = TemplateParser(default=settings.DEFAULT_LANGUAGE)
    yield


app = FastAPI(
    title="🌞Course Chat Assistant API",
    description="\n".join(
        [
            "- The Course Chat Assistant API empowers educators and learners to interact with course content in a dynamic way. ",
            "- Users can create courses, upload files, and process these files by chunking and embedding the content into a vector store. ",
            "- Leveraging semantic search and a powerful language model, the API then provides context-aware, conversational responses to user queries based on the course material. ",
            "- Whether for educational support or content management, this API bridges static course content with interactive, intelligent chat capabilities.",
        ]
    ),
    version="0.0.1",
    contact={
        "name": "Ramy Ibrahim",
        "url": "https://www.linkedin.com/in/ramy-ibrahim-020304262/",
        "email": "ramyibrahim.ai@gmail.com",
    },
    lifespan=lifespan,
)

app.include_router(DataRouter.router)
app.include_router(StoresRouter.router)
app.include_router(BotRouter.router)

app.mount("/static", StaticFiles(directory="src/views/static"), name="static")
templates = Jinja2Templates(directory="src/views/templates")


@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
