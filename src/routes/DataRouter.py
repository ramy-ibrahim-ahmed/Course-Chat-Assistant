import os
from fastapi import APIRouter, Request, status, HTTPException, UploadFile

from ..schemas import SignalResponse, ChunkRequest, FileUploadResponse
from ..services import DataService, ChunkService

router = APIRouter(
    prefix="/api/v1/data",
    tags=["Data"],
)


@router.post(
    "/upload/{course_name}/",
    response_model=FileUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload a file on the course.",
)
async def upload(course_name: str, file: UploadFile):
    data_service = DataService()

    try:
        data_service.validate_file_type(file=file)
        await data_service.upload_file(
            file=file,
            course_name=course_name,
            original_name=file.filename,
        )
        return {
            "signal": f"File {file.filename} is uploaded successfully!",
            "file_id": data_service.file_id,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while uploading {file.filename} | {e}",
        )


@router.post(
    "/chunk/{course_name}/",
    response_model=SignalResponse,
    status_code=status.HTTP_200_OK,
    summary="Chunk the file content and embed it to stores.",
)
async def chunk(request: Request, course_name: str, chunk_request: ChunkRequest):
    chunk_service = ChunkService(course_name=course_name)

    content = chunk_service.get_file_content(file_name=chunk_request.file_name)
    if not content or len(content) == 0:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get file content for {chunk_request.file_name}",
        )

    chunks = chunk_service.process_file_content(
        file_content=content,
        chunk_size=chunk_request.chunk_size,
        chunk_overlap=chunk_request.chunk_overlap,
    )
    if not chunks or len(chunks) == 0:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get file content for {chunk_request.file_name}",
        )

    llm = request.app.llm
    vdb = request.app.vdb

    try:
        if chunk_request.do_reset:
            vdb.create_collection(collection_name=course_name, do_reset=True)

        embeddings = llm.embed_text(chunks)
        vdb.insert_documents(
            collection_name=course_name,
            documents=chunks,
            embeddings=embeddings,
        )
        file_path = chunk_service.file_path
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"signal": f"Sucessfully inserted {len(chunks)} chunks!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while insertion in {course_name}! | {e}",
        )
