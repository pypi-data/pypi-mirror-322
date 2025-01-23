from django.urls import path
from django.conf import settings
import djp
from django.urls import include
import os
from typing import Literal
from django.core.exceptions import ImproperlyConfigured
from kitchenai.core.schema.rag import RAGConfigSchema
from pydantic import ValidationError
from kitchenai.core.schema.base import validate_bento_config
from kitchenai.core.types import ModelType, ModelName, VectorStore
from kitchenai_starter_agent.__version__ import __version__
from enum import Enum

class EnvVars(str, Enum):
    MODEL_TYPE = "SIMPLE_RAG_MODEL_TYPE"
    MODEL_NAME = "SIMPLE_RAG_MODEL_NAME"
    TEMPERATURE = "SIMPLE_RAG_TEMPERATURE"
    VECTOR_STORE = "SIMPLE_RAG_VECTOR_STORE"
    VECTOR_STORE_ENDPOINT = "SIMPLE_RAG_VECTOR_STORE_ENDPOINT"
    CHUNK_SIZE = "SIMPLE_RAG_CHUNK_SIZE"



def get_available_env_vars():
    """
    Returns information about all available environment variables and their configurations.
    
    Returns:
        dict: A dictionary describing each environment variable, its purpose, default value, and allowed values
    """
    try:
        return RAGConfigSchema(
            llm_type=os.environ.get(EnvVars.MODEL_TYPE, ModelType.LITELLM),
            llm_name=os.environ.get(EnvVars.MODEL_NAME, ModelName.GPT4O),
            temperature=float(os.environ.get(EnvVars.TEMPERATURE, "0.7")),
            vector_store=os.environ.get(EnvVars.VECTOR_STORE, VectorStore.CHROMA),
            vector_store_endpoint=os.environ.get(EnvVars.VECTOR_STORE_ENDPOINT, "chroma_db"),
            chunk_size=int(os.environ.get(EnvVars.CHUNK_SIZE, "1024"))
        )
    except Exception as e:
        raise ImproperlyConfigured(f"Invalid RAG configuration: {str(e)}")


@djp.hookimpl
def installed_apps():
    return ["kitchenai_starter_agent"]


# @djp.hookimpl
# def urlpatterns():
#     # A list of URL patterns to add to urlpatterns:
#     return [
#         path("starter-agent/", include("kitchenai_starter_agent.urls", namespace="starter_agent")),
#     ]

@djp.hookimpl
def settings(current_settings):
    # Make changes to the Django settings.py globals here

    # Validate RAG settings
    rag_config = get_available_env_vars()
    
    # Use the validated config
    settings = rag_config.model_dump()
    config = {
        "name": "kitchenai_starter_agent",
        "description": "a simple starter agent that covers majority of cases",
        "namespace": "starter_agent",
        "home": "home",
        "version": __version__,
        "tags": ["starter-agent", "bento", "kitchenai_starter_agent", "kitchenai-bento-starter-agent"],
    }

    try:
        validate_bento_config(config)
    except ValidationError as e:
        raise ImproperlyConfigured(f"Invalid bento configuration: {str(e)}") from e

    config["settings"] = settings
    current_settings["KITCHENAI"]["bento"].append(config)
    current_settings["kitchenai_starter_agent"] = settings
    


@djp.hookimpl
def middleware():
    # A list of middleware class strings to add to MIDDLEWARE:
    # Wrap strings in djp.Before("middleware_class_name") or
    # djp.After("middleware_class_name") to specify before or after
    return []

