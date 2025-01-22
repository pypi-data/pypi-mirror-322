import logging
import os
import json
import sys
from collections.abc import AsyncGenerator
from typing import Annotated, Optional, Union
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob.aio import ContainerClient
from azure.storage.filedatalake.aio import FileSystemClient
import azure.identity
import azure.identity.aio
from azure.identity import DefaultAzureCredential as SyncDefaultAzureCredential
from fastapi import Depends, Request
from pydantic import BaseModel,ConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from fastapi_app.authentication import AuthenticationHelper
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from azure.keyvault.secrets.aio import SecretClient
from openai import AsyncAzureOpenAI, AsyncOpenAI


logger = logging.getLogger("webapp")


class OpenAIClient(BaseModel):
    """
    OpenAI client
    """

    client: AsyncOpenAI | AsyncAzureOpenAI
    model_config = {"arbitrary_types_allowed": True}


class FastAPIAppContext(BaseModel):
    """
    Context for the FastAPI app
    """
    auth_helper: AuthenticationHelper
    model_config = ConfigDict(arbitrary_types_allowed=True)

   
    blob_storage_connection_string: str
    azure_storage_account: str
    azure_storage_container: str
    azure_userstorage_account: str
    azure_userstorage_container: str
    azure_client_app_id: str
    azure_client_app_secret: str
    config_user_upload_enabled: bool
    config_user_blob_container_client: Optional[str] 
    config_blob_container_client: str
    openai_chat_model: str
    openai_embed_model: str
    openai_embed_dimensions: Optional[int]
    openai_chat_deployment: Optional[str]
    openai_embed_deployment: Optional[str]
    embedding_column: str
   
    

async def common_parameters():
    """
    Get the common parameters for the FastAPI app
    Use the pattern of `os.getenv("VAR_NAME") or "default_value"` to avoid empty string values
    """
    OPENAI_EMBED_HOST = os.getenv("OPENAI_EMBED_HOST")
    OPENAI_CHAT_HOST = os.getenv("OPENAI_CHAT_HOST")
    if OPENAI_EMBED_HOST == "azure":
        openai_embed_deployment = os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT") or "text-embedding-ada-002"
        openai_embed_model = os.getenv("AZURE_OPENAI_EMBED_MODEL") or "text-embedding-ada-002"
        openai_embed_dimensions = int(os.getenv("AZURE_OPENAI_EMBED_DIMENSIONS") or 1536)
        embedding_column = os.getenv("AZURE_OPENAI_EMBEDDING_COLUMN") or "embedding_ada002"
    elif OPENAI_EMBED_HOST == "ollama":
        openai_embed_deployment = None
        openai_embed_model = os.getenv("OLLAMA_EMBED_MODEL") or "nomic-embed-text"
        openai_embed_dimensions = None
        embedding_column = os.getenv("OLLAMA_EMBEDDING_COLUMN") or "embedding_nomic"
    else:
        openai_embed_deployment = None
        openai_embed_model = os.getenv("OPENAICOM_EMBED_MODEL") or "text-embedding-ada-002"
        openai_embed_dimensions = int(os.getenv("OPENAICOM_EMBED_DIMENSIONS", 1536))
        embedding_column = os.getenv("OPENAICOM_EMBEDDING_COLUMN") or "embedding_ada002"
    if OPENAI_CHAT_HOST == "azure":
        openai_chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT") or "gpt-4o-mini"
        openai_chat_model = os.getenv("AZURE_OPENAI_CHAT_MODEL") or "gpt-4o-mini"
    elif OPENAI_CHAT_HOST == "ollama":
        openai_chat_deployment = None
        openai_chat_model = os.getenv("OLLAMA_CHAT_MODEL") or "phi3:3.8b"
        openai_embed_model = os.getenv("OLLAMA_EMBED_MODEL") or "nomic-embed-text"
    else:
        openai_chat_deployment = None
        openai_chat_model = os.getenv("OPENAICOM_CHAT_MODEL") or "gpt-3.5-turbo"
   
    AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
    AZURE_USERSTORAGE_ACCOUNT = os.getenv("AZURE_USERSTORAGE_ACCOUNT")
    AZURE_USERSTORAGE_CONTAINER = os.getenv("AZURE_USERSTORAGE_CONTAINER")
    BLOB_STORAGE_CONNECTION_STRING = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
    AZURE_USE_AUTHENTICATION = os.getenv("AZURE_USE_AUTHENTICATION", "").lower() == "true"
    AZURE_ENFORCE_ACCESS_CONTROL = os.getenv("AZURE_ENFORCE_ACCESS_CONTROL", "").lower() == "true"
    AZURE_ENABLE_GLOBAL_DOCUMENT_ACCESS = os.getenv("AZURE_ENABLE_GLOBAL_DOCUMENT_ACCESS", "").lower() == "true"
    AZURE_ENABLE_UNAUTHENTICATED_ACCESS = os.getenv("AZURE_ENABLE_UNAUTHENTICATED_ACCESS", "").lower() == "true"
    AZURE_CLIENT_APP_ID = os.getenv("AZURE_AUTH_CLIENT_ID")
    AZURE_KEY_VAULT_NAME = os.getenv("AZURE_KEY_VAULT_NAME") 
    #AZURE_AUTH_TENANT_ID = os.getenv("AZURE_AUTH_TENANT_ID")
    try:
        customer_tenants_json = os.getenv('CUSTOMER_TENANTS_JSON', '[]')
        # Attempt to parse as-is
        try:
            customer_tenants = json.loads(customer_tenants_json)
        except json.JSONDecodeError:
            # Possibly double-escaped (like in .env)
            customer_tenants_json = customer_tenants_json.replace('\\\"', '"')
            customer_tenants = json.loads(customer_tenants_json)
        
        if not customer_tenants:
            logger.error("Error: No valid tenant IDs found in CUSTOMER_TENANTS_JSON.")
            sys.exit(1)
            
        # Extract tenant IDs
        tenant_ids = [tenant.get('tenantId') for tenant in customer_tenants]
        
        if not any(tenant_ids):
            logger.error("Error: No valid tenant IDs found in CUSTOMER_TENANTS_JSON.")
            sys.exit(1)
            
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse CUSTOMER_TENANTS_JSON: {str(e)}")
        sys.exit(1)

    

    USE_USER_UPLOAD = os.getenv("USE_USER_UPLOAD", "").lower() == "true"
    CONFIG_USER_BLOB_CONTAINER_CLIENT = os.getenv("CONFIG_USER_BLOB_CONTAINER_CLIENT", None)
    CONFIG_BLOB_CONTAINER_CLIENT = os.getenv("CONFIG_BLOB_CONTAINER_CLIENT", "blob_container_client")
    AZURE_SERVER_APP_ID = os.getenv("AZURE_SERVER_APP_ID")
    
    # Fetch the secret name from environment variables or use default
    AZURE_AUTH_CLIENT_SECRET_NAME = os.getenv("AZURE_AUTH_CLIENT_SECRET_NAME")
    AZURE_SERVER_APP_SECRET_NAME = os.getenv("AZURE_SERVER_APP_SECRET_NAME")

    if not BLOB_STORAGE_CONNECTION_STRING:
        raise ValueError("BLOB_STORAGE_CONNECTION_STRING environment variable is not set.")

    if not AZURE_KEY_VAULT_NAME:
        raise ValueError("AZURE_KEY_VAULT_NAME environment variable is not set.")

    AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
    if not AZURE_STORAGE_CONTAINER:
        raise ValueError("AZURE_STORAGE_CONTAINER environment variable is not set.")

    # Handle user storage account and container being empty
    AZURE_USERSTORAGE_ACCOUNT = AZURE_USERSTORAGE_ACCOUNT or "None"
    AZURE_USERSTORAGE_CONTAINER = AZURE_USERSTORAGE_CONTAINER or "None"

    

    # Create a Key Vault client to retrieve secrets
   
    async with SecretClient(
        vault_url=f"https://{AZURE_KEY_VAULT_NAME}.vault.azure.net", credential=get_azure_blob_kv_credential()
    ) as key_vault_client:
        auth_client_secret = (await key_vault_client.get_secret(AZURE_AUTH_CLIENT_SECRET_NAME)).value
        server_app_secret = (await key_vault_client.get_secret(AZURE_SERVER_APP_SECRET_NAME)).value
    

     # Creating FileSystemClient if user upload is enabled
    if USE_USER_UPLOAD:
        logger.info("USE_USER_UPLOAD is true, setting up user upload feature")
        if not AZURE_USERSTORAGE_ACCOUNT or not AZURE_USERSTORAGE_CONTAINER:
            raise ValueError("AZURE_USERSTORAGE_ACCOUNT and AZURE_USERSTORAGE_CONTAINER must be set when USE_USER_UPLOAD is true")
        user_blob_container_client = FileSystemClient(
            f"https://{AZURE_USERSTORAGE_ACCOUNT}.dfs.core.windows.net",
            AZURE_USERSTORAGE_CONTAINER,
            credential=azure.identity.DefaultAzureCredential()
        )
    else:
        user_blob_container_client = None

    auth_helper = AuthenticationHelper(
        use_authentication=AZURE_USE_AUTHENTICATION,
        client_app_id=AZURE_CLIENT_APP_ID,
        tenant_ids=tenant_ids,
        require_access_control=AZURE_ENFORCE_ACCESS_CONTROL,
        enable_global_documents=AZURE_ENABLE_GLOBAL_DOCUMENT_ACCESS,
        enable_unauthenticated_access=AZURE_ENABLE_UNAUTHENTICATED_ACCESS,
        server_app_id=AZURE_SERVER_APP_ID,
        server_app_secret=server_app_secret,
    )

    return FastAPIAppContext(
        azure_storage_container=AZURE_STORAGE_CONTAINER,
        blob_storage_connection_string=BLOB_STORAGE_CONNECTION_STRING,
        azure_client_app_id=AZURE_CLIENT_APP_ID,
        azure_client_app_secret=auth_client_secret,
        azure_storage_account=AZURE_STORAGE_ACCOUNT,
        azure_userstorage_account=AZURE_USERSTORAGE_ACCOUNT,
        azure_userstorage_container=AZURE_USERSTORAGE_CONTAINER,
        auth_helper = auth_helper,
        config_user_upload_enabled=USE_USER_UPLOAD,
        config_user_blob_container_client=CONFIG_USER_BLOB_CONTAINER_CLIENT,
        config_blob_container_client=CONFIG_BLOB_CONTAINER_CLIENT,
        user_blob_container_client=user_blob_container_client,
        openai_chat_model=openai_chat_model,
        openai_embed_model=openai_embed_model,
        openai_embed_dimensions=openai_embed_dimensions,
        openai_chat_deployment=openai_chat_deployment,
        openai_embed_deployment=openai_embed_deployment,
        embedding_column=embedding_column,
    )

azure_blob_kv_credential = None  # Initialize globally
def get_azure_blob_kv_credential():
    global azure_blob_kv_credential  # Refer to the global variable
    if azure_blob_kv_credential is None:
        azure_blob_kv_credential = azure.identity.aio.DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    return azure_blob_kv_credential


async def get_azure_credential() -> Union[azure.identity.AzureDeveloperCliCredential, azure.identity.ManagedIdentityCredential, azure.identity.DefaultAzureCredential]:
    try:
        if client_id := os.getenv("APP_IDENTITY_ID"):
            # Use managed identity if client_id is provided
            logger.info(
                "Using managed identity for client ID %s",
                client_id,
            )
            return azure.identity.ManagedIdentityCredential(client_id=client_id)
        else:
            # Try AzureDeveloperCliCredential first
            if tenant_id := os.getenv("AZURE_TENANT_ID"):
                return azure.identity.AzureDeveloperCliCredential(tenant_id=tenant_id)
            else:
                # Fallback to DefaultAzureCredential
                return azure.identity.DefaultAzureCredential()
    except Exception as e:
        logger.warning("Failed to authenticate using Azure Developer CLI: %s", e)
        raise e


sync_azure_credential = None
def get_sync_azure_credential():
    global sync_azure_credential
    if sync_azure_credential is None:
        sync_azure_credential = SyncDefaultAzureCredential(exclude_shared_token_cache_credential=True)
    return sync_azure_credential

async def create_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Get the agent database"""
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        autoflush=False,
    )


async def get_async_sessionmaker(
    request: Request,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    yield request.state.sessionmaker


async def get_context(
    request: Request,
) -> FastAPIAppContext:
    return request.state.context

async def get_auth_setup(request: Request):
    # Access auth_helper from the request state
    auth_helper = request.state.auth_helper
    if auth_helper:
        return JSONResponse(content=auth_helper.get_auth_setup_for_client())
    else:
        return JSONResponse(content={"error": "auth_helper not set"}, status_code=500)


async def get_async_db_session(
    sessionmaker: Annotated[async_sessionmaker[AsyncSession], Depends(get_async_sessionmaker)],
) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session


async def create_file_system_client(credential) -> FileSystemClient:
    # Create FileSystemClient using the user's storage account and container
    file_system_client = FileSystemClient(
        account_url=f"https://{os.getenv('AZURE_USERSTORAGE_ACCOUNT')}.dfs.core.windows.net",
        file_system=os.getenv("AZURE_USERSTORAGE_CONTAINER"),
        credential=credential
    )
    return file_system_client

async def get_user_file_system_client(
    request: Request
) -> FileSystemClient:
    # Getting user-specific file system client from request state
    return request.state.user_blob_container_client



async def create_blob_service_client(credential) -> BlobServiceClient:
    # Create BlobServiceClient using connection string or account URL
    blob_service_client = BlobServiceClient(
        account_url=f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net",
        credential=credential
    )
    return blob_service_client

async def create_blob_container_client(credential) -> ContainerClient:
    # Using BlobServiceClient to create a ContainerClient for a specific container
    blob_service_client = await create_blob_service_client(credential)
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

async def get_user_blob_container_client(
    request: Request
) -> ContainerClient:
    # Check if the client exists in the request state
    if not hasattr(request.state, "user_blob_container_client") or request.state.user_blob_container_client is None:
        raise HTTPException(status_code=500, detail="Blob container client not found in request state")
    
    return request.state.user_blob_container_client


async def get_openai_chat_client(
    request: Request,
) -> OpenAIClient:
    """Get the OpenAI chat client"""
    return OpenAIClient(client=request.state.chat_client)


async def get_openai_embed_client(
    request: Request,
) -> OpenAIClient:
    """Get the OpenAI embed client"""
    return OpenAIClient(client=request.state.embed_client)




CommonDeps = Annotated[FastAPIAppContext, Depends(get_context)]
AuthSetup=Annotated[JSONResponse, Depends(get_auth_setup)]
DBSession = Annotated[AsyncSession, Depends(get_async_db_session)]
BlobContainerClient = Annotated[ContainerClient, Depends(get_user_blob_container_client)]
UserBlobServiceClient = Annotated[FileSystemClient, Depends(get_user_blob_container_client)]
ChatClient = Annotated[OpenAIClient, Depends(get_openai_chat_client)]
EmbeddingsClient = Annotated[OpenAIClient, Depends(get_openai_embed_client)]

