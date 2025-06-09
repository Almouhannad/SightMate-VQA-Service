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

The service exposes the following REST endpoints:

### Health Check

**GET `/health`**
- Description: Health check endpoint to verify service status
- Response:
  ```json
  {
    "status": "ok"
  }
  ```

### Image Captioning

**POST `/vqa/captioning`**
- Description: Generates captions for uploaded images
- Request Body:
  ```json
  {
    "image": {
      "bytes": [/* array of image bytes */],
      "metadata": {
        // Optional metadata about the image
      }
    },
    "options": {
      // Optional configuration for the captioning process
    }
  }
  ```
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
- Description: Answers questions about uploaded images
- Request Body:
  ```json
  {
    "image": {
      "bytes": [/* array of image bytes */],
      "metadata": {
        // Optional metadata about the image
      }
    },
    "question": "What color is the car?",
    "options": {
      // Optional configuration for the question answering process
    }
  }
  ```
- Response:
  ```json
  {
    "output": "Answer to the question",
    "details": {
      // Optional additional details about the question answering process
    }
  }
  ```

## 🛠️ Setup & Configuration

1. Clone the repository:
```bash
git clone https://github.com/Almouhannad/SightMate-VQA-Service.git
cd SightMate-VQA-Service
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```env
VQA_ADAPTER=vlm  # The VQA adapter to use
LMS_API=http://your_vlm_api_endpoint  # VLM API endpoint
```

4. Run the service:
```bash
uvicorn src.api.main:app --reload
```

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