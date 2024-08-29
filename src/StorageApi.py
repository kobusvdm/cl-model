__all__ = ["StorageApi", "LocalStorageBlob", "CloudStorageBlob", "AzureStorageBlob"]

from abc import ABC, abstractmethod
from typing import Optional

from prefect.blocks.core import Block
from prefect.filesystems import LocalFileSystem
from pydantic import SecretStr


class StorageApi(Block, ABC):
    """Defines the abstract base class for the storage provider."""    
    @abstractmethod
    def save(self, path: str, data: bytes) -> str:
        """Saves an object to Azure Blob storage."""
        pass
        
    @abstractmethod
    def read(self, path: str) -> bytes:
        """Reads a text file from Azure Blob storage."""
        pass
    
class LocalStorageBlob(StorageApi):
    """Defines a generic local Blob storage provider class."""

    
    def save(self, path: str, data: bytes):
        """Saves an object to Azure Blob storage."""
        local_file_system_block = LocalFileSystem().write_path(path=path, content=data)
        
    def read(self, path: str) -> bytes:
        """Reads a text file from Azure Blob storage."""
        local_file_system_block = LocalFileSystem.read_path(path)
        
class CloudStorageBlob(StorageApi, ABC):
    """Abstract base class for cloud storage providers."""
    ...        
    

__all__ = ["AzureStorageBlob"]