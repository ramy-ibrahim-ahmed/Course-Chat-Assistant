# Course Chat Assistant

A robust and intelligent API designed to facilitate interactive learning experiences through conversational AI. The Course Chat Assistant enables users to create courses, upload and process educational materials, and engage in semantic search-driven discussions about course content.

Leveraging advanced language models, vector embeddings, and semantic search capabilities, this system transforms static educational content into a dynamic and interactive learning tool.

## Architecture

The system is designed with modularity and scalability in mind, utilizing the factory pattern to ensure seamless integration with various language model and vector database providers.

- **Factory Pattern**: Facilitates extensibility and provider interchangeability
  - `LLMFactory`: Instantiates language model providers
  - `VectorsFactory`: Instantiates vector database providers
- **Abstract Interfaces**: Define standardized interactions
  - `LLMInterface`: Common interface for language model operations
  - `VectorsInterface`: Common interface for vector database operations
- **FastAPI-Based Services**:
  - `ChunkService`: Handles document ingestion and segmentation
  - `DataService`: Manages file uploads and preprocessing
- **API Route Separation**: Ensures clear and maintainable service boundaries

## API Endpoints

### Course Management

- **Create Course**
  - `POST /api/v1/stores/create/`
  - **Parameters**: `course_name` (string)
  - **Description**: Creates a new collection in the vector database
  - **Response**: Confirmation message

- **List All Courses**
  - `GET /api/v1/stores/courses/`
  - **Description**: Retrieves all available courses
  - **Response**: Array of course names

- **Get Course Information**
  - `GET /api/v1/stores/info/{course_name}/`
  - **Parameters**: `course_name` (string)
  - **Description**: Returns metadata for a course
  - **Response**: Collection details, including document count and embedding dimensions

- **Delete Course**
  - `DELETE /api/v1/stores/delete/{course_name}/`
  - **Parameters**: `course_name` (string)
  - **Description**: Removes a course from the vector database
  - **Response**: Confirmation message

### File Processing

- **Upload File**
  - `POST /api/v1/data/upload/{course_name}/`
  - **Parameters**: `course_name` (string), `file` (form-data)
  - **Description**: Uploads a document to the specified course
  - **Response**: Upload confirmation and file ID

- **Process File**
  - `POST /api/v1/data/chunk/{course_name}/`
  - **Parameters**:
    - `file_name` (string)
    - `chunk_size` (integer, default: 100)
    - `chunk_overlap` (integer, default: 20)
    - `do_reset` (boolean, default: false)
  - **Description**: Segments the uploaded file and embeds the content into the vector database
  - **Response**: Confirmation with chunking details

### Semantic Search and Chat

- **Semantic Search**
  - `GET /api/v1/stores/search/{course_name}/`
  - **Parameters**:
    - `course_name` (string)
    - `query` (string)
    - `limit` (integer, default: 5)
  - **Description**: Searches for the most relevant course content
  - **Response**: Retrieved document segments with similarity scores

- **Chat with Course**
  - `POST /api/v1/bot/chat/{course_name}/`
  - **Parameters**:
    - `course_name` (string)
    - `query` (string)
    - `limit` (integer, default: 5)
  - **Description**: Engages in a contextual conversation based on course materials
  - **Response**: AI-generated answer utilizing retrieved course content

## Data Flow

1. **Course Creation**: Initializes a course collection in the vector database
2. **File Upload**: Users upload educational documents
3. **Content Processing**: Documents are segmented and embedded
4. **User Query**: Users ask questions related to course content
5. **Semantic Search**: The system retrieves the most relevant content
6. **Context Assembly**: Relevant data is structured for LLM input
7. **Response Generation**: The language model produces a meaningful response

## Technologies Used

- **FastAPI**: High-performance API framework
- **Langchain**: Framework for LLM-powered applications
- **Chromadb**: Vector database for efficient content retrieval
- **OpenAI/Ollama**: Language model integration for chat-based learning
- **Pydantic**: Data validation and configuration management
- **PyMuPDF**: PDF processing library
- **AsyncIO/aiofiles**: Asynchronous file handling
- **String Templating**: Structured prompt engineering

## Implementation Details

- **Document Handling**: Supports TXT and PDF formats with extensibility for others
- **Vector Embeddings**: Utilizes embedding models for content similarity search
- **Prompt Engineering**: Customizable prompt structures for effective LLM responses
- **Error Handling**: Robust error reporting with descriptive HTTP responses
- **Logging**: Comprehensive system logging for debugging and monitoring

This project provides an efficient and scalable solution for integrating conversational AI into educational platforms, enabling interactive and personalized learning experiences.
