Review LLM arch and function

Review tests (MonkeyPatch, MagicMock, etc)

Review Docker logs vs python logger

What does this do?
    - Dockerfile
    - CMD ["poetry", "run", "uvicorn", "app.main:app_fastapi", "--host", "0.0.0.0", "--port", "8000"]
    - ENV PYTHONDONTWRITEBYTECODE=1
    - ENV PYTHONUNBUFFERED=1

Why cant you use poetry bundle with llama-cpp-python (requires cmake, c build stuffs)?

What is kubectl? What is minikube?