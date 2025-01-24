from typing import Dict, Any, Optional
import threading
import redis
import json
from abc import ABC, abstractmethod
from enum import Enum
from collections import OrderedDict
from google.cloud import firestore
from google.cloud.firestore import Client, DocumentReference


# Method 1: Set environment variable
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firebase-credentials.json"

class Memory:
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __str__(self) -> str:
        return str(self.data)

class AbstractMemoryStore(ABC):
    @abstractmethod
    def save_memory(self, key: str, data: Any, participant_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def load_memory(self, key: str, participant_id: Optional[str] = None) -> Optional[Any]:
        pass

    @abstractmethod
    def load_all_memory(self, participant_id: Optional[str] = None) -> Memory:
        pass

    @abstractmethod
    def flush_all_memory(self, participant_id: Optional[str] = None) -> None:
        pass

class StandardMemory(AbstractMemoryStore):
    def __init__(self, max_size: int = 1000, participant_id: Optional[str] = None):
        self._memory = OrderedDict()
        self._lock = threading.RLock()
        self._max_size = max_size
        self._participant_id = participant_id

    def _get_key(self, key: str, participant_id: Optional[str] = None) -> str:
        pid = participant_id or self._participant_id
        return f"{pid}:{key}" if pid else key

    def save_memory(self, key: str, data: Any, participant_id: Optional[str] = None) -> None:
        full_key = self._get_key(key, participant_id)
        with self._lock:
            if full_key in self._memory:
                del self._memory[full_key]
            elif len(self._memory) >= self._max_size:
                self._memory.popitem(last=False)
            self._memory[full_key] = data

    def load_memory(self, key: str, participant_id: Optional[str] = None) -> Optional[Any]:
        full_key = self._get_key(key, participant_id)
        with self._lock:
            if full_key not in self._memory:
                return None
            value = self._memory.pop(full_key)
            self._memory[full_key] = value
            return value

    def load_all_memory(self, participant_id: Optional[str] = None) -> Memory:
        memory = Memory()
        prefix = f"{participant_id or self._participant_id}:" if participant_id or self._participant_id else ""
        with self._lock:
            for key, value in self._memory.items():
                if key.startswith(prefix):
                    base_key = key[len(prefix):] if prefix else key
                    memory.data[base_key] = value
        return memory

    def flush_all_memory(self, participant_id: Optional[str] = None) -> None:
        prefix = f"{participant_id or self._participant_id}:" if participant_id or self._participant_id else ""
        with self._lock:
            keys_to_remove = [k for k in self._memory.keys() if k.startswith(prefix)]
            for key in keys_to_remove:
                del self._memory[key]

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return self.load_memory(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self.save_memory(name, value)

class RedisMemory(AbstractMemoryStore):
    def __init__(self, host='localhost', port=6379, db=0, participant_id: Optional[str] = None):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self._participant_id = participant_id

    def _get_key(self, key: str, participant_id: Optional[str] = None) -> str:
        pid = participant_id or self._participant_id
        return f"{pid}:{key}" if pid else key

    def save_memory(self, key: str, data: Any, participant_id: Optional[str] = None) -> None:
        full_key = self._get_key(key, participant_id)
        serialized = json.dumps(data)
        self._redis.set(full_key, serialized)

    def load_memory(self, key: str, participant_id: Optional[str] = None) -> Optional[Any]:
        full_key = self._get_key(key, participant_id)
        data = self._redis.get(full_key)
        return json.loads(data) if data else None

    def load_all_memory(self, participant_id: Optional[str] = None) -> Memory:
        memory = Memory()
        prefix = f"{participant_id or self._participant_id}:" if participant_id or self._participant_id else ""
        pattern = f"{prefix}*" if prefix else "*"
        
        for key in self._redis.scan_iter(pattern):
            base_key = key[len(prefix):] if prefix else key
            memory.data[base_key] = self.load_memory(base_key, participant_id)
        return memory

    def flush_all_memory(self, participant_id: Optional[str] = None) -> None:
        prefix = f"{participant_id or self._participant_id}:" if participant_id or self._participant_id else ""
        pattern = f"{prefix}*" if prefix else "*"
        
        for key in self._redis.scan_iter(pattern):
            self._redis.delete(key)

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return self.load_memory(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self.save_memory(name, value)


class FirestoreMemory(AbstractMemoryStore):
    def __init__(self, document_path: str, client: Optional[Client] = None):
        """Initialize Firestore memory store
        
        Args:
            document_path: Full path to the Firestore document (e.g. 'memories/user1')
            client: Optional Firestore client. If not provided, creates a new one
        """
        # Use object.__setattr__ to bypass our custom __setattr__ for initialization
        object.__setattr__(self, 'db', client or firestore.Client())
        
        # Split path into collection/document parts and create document reference
        path_parts = document_path.split('/')
        if len(path_parts) % 2 != 0:
            raise ValueError("Document path must have an even number of segments (collection/document pairs)")
        object.__setattr__(self, 'doc_ref', self.db.document(document_path))

    def save_memory(self, key: str, data: Any) -> None:
        """Save data as a field in the Firestore document"""
        # Serialize data to JSON-compatible format
        serialized_data = json.dumps(data, default=self._serialize_object)
        # Only use json.loads if the data was actually serialized to a string
        if isinstance(data, (list, dict)):
            self.doc_ref.set({key: data}, merge=True)
        else:
            self.doc_ref.set({key: json.loads(serialized_data)}, merge=True)

    def load_memory(self, key: str) -> Optional[Any]:
        """Load specific field from the Firestore document"""
        doc = self.doc_ref.get()
        if not doc.exists:
            return None
        value = doc.get(key)
        return json.loads(json.dumps(value)) if value is not None else None

    def _serialize_object(self, obj):
        """Helper method to serialize special objects"""
        if isinstance(obj, Enum):
            return {"__enum__": str(obj)}
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def load_all_memory(self) -> Memory:
        """Load all fields from the Firestore document"""
        memory = Memory()
        doc = self.doc_ref.get()
        if doc.exists:
            memory.data = doc.to_dict() or {}
        return memory

    def flush_all_memory(self, participant_id: Optional[str] = None) -> None:
        self.doc_ref.delete()

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return self.load_memory(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ('db', 'doc_ref') or name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            self.save_memory(name, value)