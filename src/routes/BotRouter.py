from fastapi import APIRouter, Request, status, HTTPException

from ..bots.providers import OpenAIProvider
from ..stores.providers import ChromaProvider
from ..schemas import SignalResponse

router = APIRouter(
    prefix="/api/v1/bot",
    tags=["Bot"],
)


@router.post(
    "/chat/{course_name}/",
    response_model=SignalResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with the course content."
)
async def chat(request: Request, course_name: str, query: str, limit: int = 5):
    llm: OpenAIProvider = request.app.llm
    embeddings = llm.embed_text(texts=[query])

    vdb: ChromaProvider = request.app.vdb
    documents = vdb.search_by_victors(
        collection_name=course_name,
        victors=embeddings,
        limit=limit,
    )

    system_prompt = request.app.template_parser.get(
        "prompts",
        "system_prompt",
        {},
    )

    documents_prompt = "\n".join(
        [
            request.app.template_parser.get(
                "prompts",
                "document_prompt",
                {"doc_num": i + 1, "chunk_text": doc.document},
            )
            for i, doc in enumerate(documents)
        ]
    )

    footer_prompt = request.app.template_parser.get(
        "prompts",
        "footer_prompt",
        {},
    )

    chat_history = [
        llm.define_prompt(
            role=llm.roles.SYSTEM.value,
            content=system_prompt,
        )
    ]

    full_prompt = "\n\n".join([documents_prompt, footer_prompt])
    user_prompt = llm.define_prompt(
        role=llm.roles.USER.value,
        content=full_prompt,
    )

    try:
        answer = llm.generate_response(
            chat_history=chat_history,
            prompt=user_prompt,
        )
        return {"signal": answer}
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"LLM don't provide response! | {e}",
        )
