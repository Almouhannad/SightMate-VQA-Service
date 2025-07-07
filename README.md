# SightMate - VQA Service

<div align="center">
  <img src="screenshots/3.jpg" alt="SightMate VQA Service Screenshot" width="800"/>
</div>

A Visual Question Answering (VQA) microservice built with FastAPI and a hexagonal architecture pattern. This service provides endpoints for image captioning and question answering about images.

## 🏗️ Architecture

The project follows a hexagonal (ports and adapters) architecture pattern, which provides clear separation of concerns and makes the system highly extensible:

```
src/
├── api/           # API layer (FastAPI endpoints)
├── core/          # Core configuration
├── domain/        # Business logic and interfaces
│   ├── models/    # Domain models
│   └── ports/     # Abstract interfaces (ports)
└── infrastructure/# External implementations
    └── adapters/  # Concrete implementations of ports
```

### Ports & Adapters Pattern

The service uses a ports and adapters pattern for VQA functionality:

- **Port (`VqaPort`)**: Defines the interface for VQA operations:
  - `process_captioning()`: Generates captions for images
  - `process_question()`: Answers questions about images

- **Adapters**: Concrete implementations of the `VqaPort` interface
  - Currently supports VLM (Vision Language Model) adapter
  - New adapters can be easily added by implementing the `VqaPort` interface

### Adapter Registry Pattern

The project uses a registry pattern (`registry.py`) for managing VQA adapters:

```python
@register_adapter("adapter_name")
class NewVqaAdapter(VqaPort):
    # Implement the VqaPort interface
    pass
```

This makes it easy to:
- Register new VQA model implementations
- Switch between different VQA models
- Maintain multiple implementations simultaneously

## 🚀 API Endpoints

### Authentication

Some endpoints require an API key for access. You must provide your API key in the `X-API-Key` header for protected endpoints. If the API key is missing or invalid, the service will return a 401 Unauthorized error.

**Example header:**

```
X-API-Key: your_api_key_here
```

---

### Health Check

**GET `/health`**
- Description: Health check endpoint to verify service status
- Authentication: ❌ No API key required
- Response:
  ```json
  {
    "status": "ok"
  }
  ```

### Image Captioning

**POST `/vqa/captioning`**
- Description: Generate an image caption, optionally taking a history of previous Q&A.
- Authentication: ✅ Requires API key (`X-API-Key` header)
- Request Headers:
  - `X-API-Key: your_api_key_here`
- Request Body:
  ```json
  {
    "image": {
      "bytes": [ /* image bytes as list<int> */ ],
      "metadata": { /* optional metadata */ }
    },
    "history": [
      {
        "question": "What is in the glass?",
        "answer": "MATE 🧉"
      },
      {
        "question": "What is the color of the laptop?",
        "answer": "Black."
      }
    ]
  }

* `history` (optional): array of prior Q\&A pairs.

- Response:
  ```json
  {
    "output": "Generated caption text",
    "details": {
      // Optional additional details about the captioning process
    }
  }
  ```

### Question Answering

**POST `/vqa/question`**
- Description: Ask a question about the image, with optional history of earlier interactions.
- Authentication: ✅ Requires API key (`X-API-Key` header)
- Request Headers:
  - `X-API-Key: your_api_key_here`
- Request Body:
  ```json
  {
    "image": {
      "bytes": [ /* image bytes as list<int> */ ],
      "metadata": { /* optional metadata */ }
    },
    "question": "What color are the bananas?",
    "history": [
      {
        "question": "What is in the glass?",
        "answer": "MATE 🧉"
      },
      {
        "question": "What is the color of the laptop?",
        "answer": "Black."
      }
    ]
  }

* `question`: the current question to ask.
* `history` (optional): array of prior Q\&A pairs.

- Response:
  ```json
  {
    "output": "Blue",
    "details": {
      // Optional additional details about the question answering process
    }
  }
  ```

## 🛠️ Setup & Configuration

### 1. Clone the repository
```bash
git clone https://github.com/Almouhannad/SightMate-VQA-Service.git
cd SightMate-VQA-Service
```

### 2. Create a `.env` file

Create a `.env` file in the project root with the following variables (see [src/core/config.py](src/core/config.py) for details):

```env
# VQA model to use:
VQA_ADAPTER=smsa # Or vlm (must register api)
# API Key repository to use (e.g. mongo_db, in-memory, ...)
API_KEY_REPOSITORY=mongo_db
LMS_API_BASE_URI_FOR_CONTAINER=your_gemma_api_base_uri  # Only needed if vlm

# MongoDB configuration
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_ROOT_USERNAME=your_mongo_root_username
MONGO_ROOT_PASSWORD=your_mongo_root_password
MONGO_DATABASE=your_database_name
# Application database and user
MONGO_DATABASE=vqa_service_database
MONGO_APP_USERNAME=vqa_service
MONGO_APP_PASSWORD=admin
MONGODB_URI=mongodb://${MONGO_APP_USERNAME}:${MONGO_APP_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DATABASE}

# Mongo Express credentials
ME_USERNAME=admin
ME_PASSWORD=admin
```

### 3. Build and run with Docker Compose

Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

Build and start all services (API, MongoDB, Mongo Express):

```bash
docker-compose up --build
```

- The API will be available at [http://localhost:9902](http://localhost:9902)
- Mongo Express UI will be available at [http://localhost:9802](http://localhost:9802)

## 🔌 Adding New VQA Models

To add a new VQA model adapter:

1. Create a new adapter class in `src/infrastructure/adapters/vqa/`:
```python
from src.domain.ports.vqa_port import VqaPort
from src.infrastructure.adapters.vqa.registry import register_adapter

@register_adapter("new_model")
class NewModelAdapter(VqaPort):
    def process_captioning(self, captioning_input):
        # Implement captioning logic
        pass

    def process_question(self, question_input):
        # Implement question answering logic
        pass
```

2. Update the `.env` file to use your new adapter:
```env
VQA_ADAPTER=new_model
```

## 🔑 API Key Management & Repository Pattern

The service uses a flexible, pluggable repository pattern for API key management, following the same clean architecture principles as the rest of the project. This allows you to easily swap out the backend for API key storage (e.g., MongoDB, in-memory, etc.).

**How it works:**

- The repository interface (`ApiKeyRepository`) defines async methods for getting, creating, and updating API keys.
  - Api keys must be stored in DB/other backend using their hash values **(not plain-text)**, with usage of `key_prefix` for fast, indexed search
- The MongoDB implementation (`MongoDbApiKeyRepository`) is registered using a decorator and selected via configuration.
- The API key is validated for each request using a FastAPI dependency (see [`src/api/dependencies/authentication.py`](src/api/dependencies/authentication.py)).
- You can add new repository backends by implementing the interface, they'll be automatically registered, make sure to specify your backend name in `.env` (`API_KEY_REPOSITORY` field).



## 📸 More Screenshots
<div align="center">
  <img src="screenshots/1.png" width="600" alt="VQA Demo 2">
  <br><br>
  <img src="screenshots/2.png" width="600" alt="VQA Demo 3">
</div>


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- ChatGPT
- FastAPI for the fast API
- My brother who bought me a new laptop so I can run VLM locally :)
- My friends because they are supportive