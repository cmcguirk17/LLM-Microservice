# 🦙 LLM Microservice with LLAMA.CPP 🚀

A high-performance FastAPI microservice for running GGUF-formatted Large Language Models using `llama-cpp-python`. It offers an OpenAI-compatible chat API, efficient local inference with CPU/GPU support, and is ready for containerization and Kubernetes deployment.

---

## ✨ Features

*   🧠 **Direct GGUF Model Integration:** Leverages `llama-cpp-python` for efficient loading and inference with GGUF models.
*   ⚡ **High-Performance API:** Built with FastAPI for asynchronous request handling and efficient concurrent processing.
*   💻 **Optimized Local Inference:**
    *   CPU-optimized inference via `llama-cpp-python`.
    *   GPU offloading support (`N_GPU_LAYERS`) for accelerated performance on compatible hardware.
*   🤖 **OpenAI-Compatible Chat API:** Exposes a `/v1/chat/completions` endpoint mimicking the OpenAI API structure for easy integration.
*   🛠️ **Robust Model Management:** Clean startup/shutdown model loading within FastAPI's `lifespan` events, with clear logging.
*   📦 **Containerization Ready:** Designed for Docker, with environment variable-based configuration.
*   🧪 **Comprehensive Testing:** Includes unit and integration tests using PyTest.
*   📖 **Automatic API Documentation:** Interactive API docs (Swagger UI at `/docs` and ReDoc at `/redoc`) via FastAPI. Docs also available via sphinx in docs/_build/html/index.html!
*   ⚙️ **Configurable Inference:** Runtime configuration for model path, context size (`N_CTX`), GPU layers, and threading.
*   ❤️ **Health Check Endpoint:** `/v1/health` endpoint for service status and model loading state.

---

## 🛠️ Prerequisites & Setup (Ubuntu Linux)

This guide assumes an Ubuntu-based environment.

### 1. Core Tools

*   **Docker:** For containerizing the application.
    *   Installation: [Docker for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
*   **Docker Compose:** For managing multi-container Docker applications locally.
    *   Installation: [Docker Compose for Linux](https://docs.docker.com/compose/install/linux/) (*Note: Docker Desktop for Linux includes Compose*)

### 2. Poetry (Python Dependency Management)

*   **Installation:**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
*   **Add to PATH** (run in current terminal or add to `~/.bashrc`):
    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```
    If added to shell config, reload it: `source ~/.bashrc`
*   **Verify:**
    ```bash
    poetry --version
    ```
*   **Install Project Dependencies:** Navigate to the project root directory:
    ```bash
    poetry install
    ```
    *   **For Local GPU Usage (Optional):** If you intend to run locally with GPU acceleration and have the CUDA toolkit installed, use this command *instead* of the plain `poetry add llama-cpp-python` (if it was added before) or if installing `llama-cpp-python` for the first time for GPU:
        ```bash
        # Ensure CUDA toolkit is installed on your system first
        CMAKE_ARGS="-DGGML_CUDA=on poetry add llama-cpp-python
        # Then run poetry install if you haven't already or to update
        poetry install
        ```

    > 📝 **Note:** Activate the Poetry environment using `poetry shell`, `source .venv/bin/activate`, or run commands with `poetry run ...`.

### 3. NVIDIA Container Toolkit (For GPU Support in Docker)

*   Required if you want to use the GPU version of the Docker image.
*   Installation: [NVIDIA Container Toolkit Install Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### 4. Kubernetes Tools (For Minikube Deployment)

*   **kubectl (Kubernetes Command-Line Tool):**
    ```bash
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    kubectl version --client
    ```
*   **Minikube (Local Kubernetes):**
    ```bash
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube /usr/local/bin/
    minikube version
    ```
*   **Minikube Addons:**
    ```bash
    minikube addons enable metrics-server
    minikube addons enable dashboard
    ```
*   **Minikube Docker Environment:** To build images directly into Minikube's Docker daemon:
    ```bash
    # Switch to Minikube's Docker daemon
    eval $(minikube -p minikube docker-env)

    # To switch back to your system's Docker daemon later
    # eval $(minikube -p minikube docker-env -u)
    ```

---

## 📂 Project Structure

ms_llm/
├── .env # Environment variables for local Docker runs (gitignored)
├── .gitignore
├── app/ # Main application source code
│ ├── api/ # API endpoint definitions
│ │ └── v1/
│ │ └── endpoints.py
│ ├── core/ # Core logic, config, dependencies
│ │ ├── config.py
│ │ └── dependencies.py
│ ├── models/ # Directory for GGUF model files
│ │ └── YOUR_MODEL.gguf # Placeholder for your actual model file
│ ├── schemas.py # Pydantic schemas
│ ├── client_chat.py # Example CLI chat client
│ └── main.py # FastAPI application entrypoint
├── docs/ # Sphinx documentation source files
├── k8s_deploy/ # Kubernetes manifest files
├── tests/ # Test suite
│ ├── init.py
│ ├── integration/ # Integration tests (run against a running app)
│ │ └── ...
│ ├── load/ # Load testing scripts
│ │ └── locustfile.py
│ └── unit/ # Unit tests
│ └── ...
├── Dockerfile # Dockerfile for CPU build
├── Dockerfile_GPU # Dockerfile for GPU build
├── docker-compose.yml # Docker Compose for CPU
├── docker-compose_GPU.yml # Docker Compose for GPU
├── poetry.lock
├── pyproject.toml # Poetry project configuration
└── README.md

---

## 🚀 Usage

### 1. Running Locally (without Docker)

Ensure you have installed dependencies using Poetry (see Prerequisites).

*   **Option 1: Uvicorn (Recommended for development)**
    ```bash
    cd app/
    poetry run uvicorn main:app_fastapi --reload --host 0.0.0.0 --port 8000
    ```
*   **Option 2: Python**
    ```bash
    cd app/
    poetry run python main.py
    ```

### 2. Running with Docker Compose

*   **CPU Version:**
    ```bash
    # Make sure your .env file is configured
    docker compose up --build
    ```
*   **GPU Version:**
    ```bash
    # Make sure your .env file is configured
    docker compose -f docker-compose.gpu.yml up --build
    ```

### 3. Building & Running Docker Image Manually

*   Build the image:
    ```bash
    # For CPU
    docker build -t ms_llm_app:latest .
    # For GPU (using Dockerfile_GPU)
    # docker build -f Dockerfile_GPU -t ms_llm_app_gpu:latest .
    ```
*   Run the container:
    ```bash
    docker run -p 8000:8000 --env-file .env ms_llm_app:latest
    # For GPU
    docker run --gpus all -p 8000:8000 --env-file .env ms_llm_app_gpu:latest
    ```

### 4. Interacting with the API

The service will typically be available at `http://localhost:8000`.

*   **Health Check:**
    ```bash
    curl http://localhost:8000/v1/health
    ```
*   **Chat Completions:**
    ```bash
    curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {"role": "system", "content": "You are a witty AI assistant."},
            {"role": "user", "content": "Why is the sky blue?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }'
    ```
*   **Interactive CLI Client:**
    Once the service is running (locally or via Docker):
    ```bash
    cd app/
    poetry run python client_chat.py
    ```
    Follow the prompts to interact with the LLM.

### 5. Deploying & Scaling with Minikube (Kubernetes)

1.  **Start Minikube:**
    ```bash
    minikube start --driver=docker
    ```
2.  **Set Docker Environment to Minikube:**
    ```bash
    eval $(minikube -p minikube docker-env)
    ```
3.  **Build Docker Image:**
    Make sure `imagePullPolicy: Never` is set in `llm-k8-deploy.yaml`
    ```bash
    docker build -t ms_llm_app:k8 .
    ```
4.  **Apply Kubernetes Manifests:**
    (Ensure you are in the project root where YAML files are)
    ```bash
    kubectl apply -f llm-k8-configmap.yaml
    kubectl apply -f llm-k8-deploy.yaml
    kubectl apply -f llm-k8-service.yaml
    kubectl apply -f llm-k8-hpa.yaml
    ```
5.  **Monitor Deployment:**
    *   Watch pod status: `watch kubectl get pods -l app=llm-app`
    *   Check service URL: `minikube service llm-app-service --url` (replace `llm-app-service` with your actual service name)
    *   View dashboard: `minikube dashboard`

6.  **Interact with Deployed Service:**
    Use the URL from `minikube service ... --url`. Let's say it's `http://192.168.49.2:30554`.
    ```bash
    curl -X POST http://192.168.49.2:30554/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [{"role": "user", "content": "Who won the Stanley Cup in 2020?"}],
        "temperature": 0.7,
        "max_tokens": 50
    }'
    ```
7.  **Monitor HPA and Resource Usage:**
    ```bash
    kubectl get hpa llm-app-hpa -w
    kubectl top pods -l app=llm-app
    ```
8.  **Load Testing with Locust:**
    *   Navigate to your Locust test directory (e.g., `tests/load/` or project root if `locustfile.py` is there).
    *   Get the service URL: `minikube service llm-app-service --url`
    *   Run Locust:
        ```bash
        poetry run locust --host="<SERVICE_URL_FROM_MINIKUBE>"
        ```
        Open `http://localhost:8089` in your browser.

9.  **Teardown Minikube Deployment:**
    ```bash
    kubectl delete -f llm-k8-hpa.yaml
    kubectl delete -f llm-k8-service.yaml
    kubectl delete -f llm-k8-deploy.yaml
    kubectl delete -f llm-k8-configmap.yaml
    # Optionally, stop Minikube:
    # minikube stop
    ```

---

## 🧪 Testing

Tests are run using PyTest. Coverage reports are generated using `pytest-cov`.

*   **Run all tests with coverage:**
    (From project root)
    ```bash
    poetry run pytest --cov=app --cov-report=term-missing tests/
    ```
*   **Run only Unit Tests:**
    ```bash
    poetry run pytest tests/unit/
    ```
*   **Run only Integration Tests:**
    *   The application must be running for integration tests. Start it using one of the methods in the "Usage" section (e.g., Uvicorn, Docker).
    *   Then, in a new terminal:
        ```bash
        poetry run pytest tests/integration/
        ```

---

## 📚 Model Zoo

You can find a variety of GGUF-formatted models compatible with `llama.cpp`. A good starting point is TheBloke on Hugging Face, or the official `llama.cpp` resources.

*   **`llama.cpp` Model Suggestions:** [llama.cpp Model List](https://github.com/ggerganov/llama.cpp#models)
*   **TheBloke on Hugging Face:** [Search for GGUF models](https://huggingface.co/TheBloke)

Place your downloaded `.gguf` model files into the `app/models/` directory. Update the `MODEL_PATH` environment variable (in `.env`, Docker Compose, or Kubernetes ConfigMap) to point to your chosen model file (e.g., `app/models/your-chosen-model.Q4_K_M.gguf`).

---
