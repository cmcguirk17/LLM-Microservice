from typing import Annotated
from fastapi import Request, HTTPException, Depends
from llama_cpp import Llama
import logging

logger = logging.getLogger(__name__)

async def get_llm_instance(request: Request) -> Llama:
    """
    Dependency to get the LLM instance stored in app.state.
    Raises HTTPException 503 if the LLM is not available.
    """
    # Check if 'llm' attribute exists on app.state and is not None
    if not hasattr(request.app.state, "llm") or request.app.state.llm is None:
        logger.error(
            "LLM instance not found in application state. It might not have loaded correctly."
        )
        # If not available, raise an HTTP 503 error
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail="LLM model is not loaded or unavailable. Check /health endpoint.",
        )
    # If found return the LLM instance
    return request.app.state.llm

LLMDependency = Annotated[Llama, Depends(get_llm_instance)]