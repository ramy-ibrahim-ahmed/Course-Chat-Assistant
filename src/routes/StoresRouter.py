from typing import List
from fastapi import APIRouter, Request, status, HTTPException

from ..bots.providers import OpenAIProvider
from ..stores.providers import ChromaProvider
from ..schemas import SignalResponse, CollectionInfo, RetrievedDocument

router = APIRouter(
    prefix="/api/v1/stores",
    tags=["Stores"],
)


@router.post(
    "/create/",
    response_model=SignalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a course.",
)
async def create_course(request: Request, course_name: str):
    vdb: ChromaProvider = request.app.vdb

    try:
        course_name = course_name.strip().replace(" ", "-")
        vdb.create_collection(collection_name=course_name)
        return {"signal": f"Sucessfully Created {course_name}!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while Creation {course_name}! | {e}",
        )


@router.get(
    "/courses/",
    status_code=status.HTTP_200_OK,
    summary="Get all courses's names.",
)
async def all_collections(request: Request):
    vdb: ChromaProvider = request.app.vdb

    try:
        collections = vdb.list_all_collections()
        return {"signal": collections}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while getting all collections! | {e}",
        )


@router.get(
    "/info/{course_name}/",
    response_model=CollectionInfo,
    status_code=status.HTTP_200_OK,
    summary="Get course collection info on vdb.",
)
async def collection_information(request: Request, course_name: str):
    vdb: ChromaProvider = request.app.vdb

    try:
        info = vdb.get_collection_info(collection_name=course_name)
        return CollectionInfo(**info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while getting info of {course_name}! | {e}",
        )


@router.get(
    "/search/{course_name}/",
    response_model=List[RetrievedDocument],
    status_code=status.HTTP_200_OK,
    summary="Semantic search on the course content.",
)
async def semantic_search(
    request: Request, course_name: str, query: str, limit: int = 5
):
    llm: OpenAIProvider = request.app.llm
    vdb: ChromaProvider = request.app.vdb

    try:
        embeddings = llm.embed_text(texts=[query])
        results = vdb.search_by_victors(
            collection_name=course_name,
            victors=embeddings,
            limit=limit,
        )
        return [doc.model_dump() for doc in results]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while searching on {course_name}! | {e}",
        )


@router.delete(
    "/delete/{course_name}/",
    response_model=SignalResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete course collection from vdb.",
)
async def delete_course(request: Request, course_name: str):
    vdb: ChromaProvider = request.app.vdb

    try:
        vdb.delete_collection(collection_name=course_name)
        return {"signal": f"Successfully deleted {course_name}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while deleting {course_name}! | {e}",
        )
