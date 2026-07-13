import faiss
import numpy as np
import os
import json
import logging
from typing import List, Dict, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

class FaissStore:
    """Manages the FAISS vector database for image similarity search."""
    
    def __init__(self, dimension: int = 768):
        # 768 is the dim for DINOv2 Base
        self.dimension = dimension
        self.index_file = os.path.join(settings.INDEX_DIR, "omniscene.faiss")
        self.meta_file = os.path.join(settings.INDEX_DIR, "omniscene_meta.json")
        
        # IndexFlatIP with normalized vectors = Cosine Similarity
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Mapping from FAISS internal ID (int) to our UUID (str)
        # We use IndexIDMap to assign arbitrary integer IDs, but it requires IndexFlatIP to be wrapped.
        self.index = faiss.IndexIDMap(self.index)
        
        # Map our string UUIDs to integers for FAISS, and store metadata
        self.uuid_to_int: Dict[str, int] = {}
        self.int_to_uuid: Dict[int, str] = {}
        self.metadata: Dict[str, dict] = {}
        self.next_id = 0
        
        self._ensure_dir()
        self.load()
        
    def _ensure_dir(self):
        os.makedirs(settings.INDEX_DIR, exist_ok=True)
        
    def load(self):
        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            logger.info(f"Loading FAISS index from {self.index_file}")
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, 'r') as f:
                data = json.load(f)
                self.uuid_to_int = data.get("uuid_to_int", {})
                # Convert string keys back to int
                self.int_to_uuid = {int(k): v for k, v in data.get("int_to_uuid", {}).items()}
                self.metadata = data.get("metadata", {})
                self.next_id = data.get("next_id", 0)
        else:
            logger.info("No existing FAISS index found. Creating new one.")

    def save(self):
        logger.info(f"Saving FAISS index to {self.index_file}")
        faiss.write_index(self.index, self.index_file)
        
        data = {
            "uuid_to_int": self.uuid_to_int,
            "int_to_uuid": self.int_to_uuid,
            "metadata": self.metadata,
            "next_id": self.next_id
        }
        with open(self.meta_file, 'w') as f:
            json.dump(data, f)
            
    def add_embedding(self, item_id: str, embedding: np.ndarray, meta: dict = None):
        """Add a single normalized embedding to the index."""
        if embedding.shape[0] != self.dimension:
            raise ValueError(f"Expected embedding of dimension {self.dimension}, got {embedding.shape[0]}")
            
        if item_id in self.uuid_to_int:
            logger.warning(f"Item {item_id} already exists in index. Updating metadata only.")
            if meta:
                self.metadata[item_id] = meta
            return
            
        # Ensure correct shape (1, d)
        if len(embedding.shape) == 1:
            embedding = np.expand_dims(embedding, axis=0)
            
        # Ensure float32
        embedding = embedding.astype('float32')
        
        internal_id = self.next_id
        self.next_id += 1
        
        self.uuid_to_int[item_id] = internal_id
        self.int_to_uuid[internal_id] = item_id
        self.metadata[item_id] = meta or {}
        
        # Add to FAISS (requires IDs array to be int64)
        ids_array = np.array([internal_id], dtype=np.int64)
        self.index.add_with_ids(embedding, ids_array)
        
        # Save after every addition for safety in V1
        self.save()
        
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Search for top k similar embeddings."""
        if self.index.ntotal == 0:
            return []
            
        # Ensure shape and type
        if len(query_embedding.shape) == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        query_embedding = query_embedding.astype('float32')
        
        # Search
        # D is distances (inner product = cosine similarity for normalized vectors)
        # I is the array of internal IDs
        D, I = self.index.search(query_embedding, k)
        
        results = []
        for i in range(len(I[0])):
            internal_id = I[0][i]
            if internal_id == -1:  # -1 means no neighbor found
                continue
                
            similarity = float(D[0][i])
            item_id = self.int_to_uuid.get(internal_id)
            meta = self.metadata.get(item_id, {})
            
            results.append({
                "id": item_id,
                "similarity": similarity,
                "metadata": meta
            })
            
        return results

# Global instance
faiss_store = FaissStore()
