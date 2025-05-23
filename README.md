# LLM Microservice with LLAMA.CPP

# TODO
CHECK if README is needed in docker when setting up poetry

## Features

*   **Direct GGUF Model Integration:** Leverages `llama-cpp-python` for direct, efficient loading and inference with GGUF-formatted Large Language Models.
*   **High-Performance API:** Built with FastAPI for asynchronous request handling, enabling efficient concurrent processing of chat completion requests.
*   **Optimized Local Inference:**
    *   Utilizes `llama-cpp-python` for CPU-optimized inference.
    *   Supports GPU offloading (`N_GPU_LAYERS`) for accelerated performance if compatible hardware is available.
*   **OpenAI-Compatible Chat API:** Exposes a `/v1/chat/completions` endpoint with a request/response structure similar to the OpenAI API, facilitating easier integration with existing tools and SDKs.
*   **Robust Model Management:**
    *   Model loading and resource management handled within FastAPI's `lifespan` events for clean startup and shutdown.
    *   Clear logging for model loading status and inference process.
*   **Containerization Ready:** Designed for containerization (e.g., using Docker) with environment variable-based configuration for model path, GPU layers, and other parameters.
*   **Comprehensive Testing:**
    *   Includes **unit tests** for individual components and logic.
    *   Includes **integration tests** to verify the end-to-end API workflow.
*   **Automatic API Documentation:** FastAPI provides interactive API documentation (Swagger UI at `/docs` and ReDoc at `/redoc`) out-of-the-box.
*   **Configurable Inference:** Allows runtime configuration of model path, context size (`N_CTX`), GPU layers, and threading via environment variables.
*   **Health Check Endpoint:** Provides a `/health` endpoint to monitor the service status and model loading state.


## Prerequisites/Setup (Ubuntu)

### Docker
https://docs.docker.com/engine/install/ubuntu/

### Docker Compose
https://docs.docker.com/desktop/setup/install/linux/

### NVIDIA Container Toolkit (For GPU version)
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

### Kubectl and Minikube
Get latest kubectl
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
Make executable
```
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
Verify
```
kubectl version --client
```

Get latest minikube
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```
Make executable
```
sudo install minikube /usr/local/bin/
```
Verify
```
minikube version
```
Add metrics-server addon
```
minikube addons enable metrics-server
minikube addons enable dashboard
```
Switch to using minikube docker daemon
```
# use minikube
eval $(minikube -p minikube docker-env)
# switch back to docker
eval $(minikube -p minikube docker-env -u)
```

### Poetry
If you have poetry, navigate to the project root directory
```
poetry install
```

If you don't have poetry, setup the project locally with
```
curl -sSL https://install.python-poetry.org | python3 -
```
Add it to your path (either run in current terminal or add permanently to your bashrc)
```
export PATH="$HOME/.local/bin:$PATH"
```
If you added it to your bashrc with your facourite text editor then run the following to reload it
```
source ~/.bashrc
```
Verify with
```
poetry --version
```
If installing for local GPU usage in your poetry venv, run the following. Else, skip to the last step
```
CMAKE_ARGS="-DGGML_CUDA=on" poetry add llama-cpp-python==0.3.9
```
Install dependencies with
```
poetry install
```


#### Note!
You can activate the environment using $ poetry shell (if shell installed), with $ source .venv/bin/activate, or run scripts using $ poetry run python <my_file.py>


## Project Structure

MS_LLM/   REDO ME


## Testing

Testing accomplished with PyTest and PyTest-Cov
```
pytest --cov=app --cov-report=term-missing tests/
```

### UNIT
```
poetry run pytest tests/unit
```

### INTEGRATION

Start the app (main.py) using uvicorn or by running the app with python

#### Option 1. UVICORN
```
cd app/
poetry run uvicorn main:app_fastapi --reload --host 0.0.0.0 --port 8000

# In a new terminal navigate to the project root
poetry run pytest tests/integration
```

#### Option 2. PYTHON
```
cd app/
poetry run python3 main.py

# In a new terminal navigate to the project root
poetry run pytest tests/integration
```

#### Option 3. DOCKER
Note you can do this with the CPU or GPU builds
```
# CPU
docker compose up --build

# GPU
docker compose -f docker-compose_GPU.yml up --build
```

In a new terminal
```
poetry run pytest tests/integration
```

Or using docker build + run method
```
docker build -t ms_llm_app:<tag> .
docker run --env-file .env ms_llm_app:<tag>
```

## Usage

### Talking to the LLM
Samples with curl or using a tool like postman
```
curl -X GET http://localhost:8000/v1/health
    
curl -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d \
'{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 150
}'
```

With the main.py application running either through docker-compose, with python, or with uvicorn run:
```
cd app/
poetry run python3 client_chat.py
```
This enables chat demo with history

### Scaling
After having the docker image built
```
docker build -t ms_llm_app:k8 .
```

Assuming kubectl and minikube (with driver=docker, and addons: metrics-server, dashboard) and are setup on your system in terminal run:
```
minikube start
eval $(minikube -p minikube docker-env)
kubectl apply -f llm-k8-configmap.yaml
kubectl apply -f llm-k8-deploy.yaml
kubectl apply -f llm-k8-service.yaml
kubectl apply -f llm-k8-hpa.yaml
```

View running status
```
watch kubectl get pods -l app=llm-app
```

Interact
```
minikube service llm-app-service --url
# ex/ 192.168.49.2:31720
curl -X POST http://192.168.49.2:30554/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 50
}'
# Response
```

Monitor
```
kubectl top pods -l app=llm-app
kubectl get hpa llm-app-hpa -w
kubectl get pods -l app=llm-app -w
```

To test load, navigate to tests/load/

```
cd tests/load/
# IP => minikube service llm-app-service --url
poetry run locust --host="<IP>"
```

To stop
```
kubectl delete -f llm-k8-hpa.yaml
kubectl delete -f llm-k8-service.yaml
kubectl delete -f llm-k8-deploy.yaml
kubectl delete -f llm-k8-configmap.yaml
```

## Model Zoo

From llama.cpp github
```
https://github.com/ggml-org/llama.cpp?tab=readme-ov-file#text-only
```
Add model .gguf to app/models/ directory

