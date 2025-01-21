import numpy as np
import json
import os
from attogradDB.embedding import BertEmbedding
from attogradDB.indexing import HNSW
import uuid

## Add support for custom tokenization and tiktoken
## Log perfomance for both brute force and hnsw indexing

class VectorStore:
    def __init__(self, indexing="hnsw", embedding_model="bert", save_index=False):
        self.vector = {}  
        self.index = {}
        self.idx = 0
        if embedding_model == "bert":   
            self.embedding_model = BertEmbedding()
        if indexing == "hnsw":
            self.indexing = "hnsw"
            self.index = HNSW()
        elif indexing == "brute-force":
            self.indexing = "brute-force"

    def get_key_by_value(self, value):
        for key, val in self.vector.items():
            # Use np.array_equal for array comparison
            if np.array_equal(val, value):
                return key
        return None
    
    @staticmethod
    def similarity(vector_a, vector_b, method="cosine"):
        """Calculate similarity between two vectors."""
        if method == "cosine":
            return np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
        else:
            raise ValueError("Invalid similarity method")
    
    def add_text(self, vector_id, input_data):
        """
        Add a tokenized vector to the store.
        
        Args:
            vector_id (str): Identifier for the vector.
            input_data (str): Text input to be tokenized and stored.
            tokenizer (str): Tokenizer model to be used (default is "gpt-4").
        """

        tokenized_vector = np.array(self.embedding_model.embed(input_data))
        
        if self.indexing == "hnsw":
            self.vector[vector_id] = tokenized_vector
            self.index.add_node(tokenized_vector)
        else:
            self.vector[vector_id] = tokenized_vector
            self.update_index(vector_id, tokenized_vector)

    def add_documents(self, docs):
        """
        Create id's for each of the document
        Add the document to the store

        Args:
            docs (List[str]): List of documents to be added to the store.
        """
        for doc in docs:
            self.add_text(f"doc_{self.idx}", doc)
            self.idx += 1
    
    def get_vector(self, vector_id, decode_results=False):
        """Retrieve vector by its ID."""
        if decode_results:
            # Return the n similar results decoded back to text
            decoded_text = self.embedding_model.reverse_embedding(self.vector.get(vector_id))
            return decoded_text
        else:
            return self.vector.get(vector_id)
    
    def update_index(self, vector_id, vector):
        """Update the similarity index with new vectors."""
        for existing_id, existing_vector in self.vector.items():
            if existing_id == vector_id:
                continue  # Skip if same vector
            cosine_similarity = self.similarity(vector, existing_vector)
            if existing_id not in self.index:
                self.index[existing_id] = {}
            self.index[existing_id][vector_id] = cosine_similarity
            if vector_id not in self.index:
                self.index[vector_id] = {}
            self.index[vector_id][existing_id] = cosine_similarity

    def get_similar(self, query_text, top_n=5, decode_results=True):
        """
        Get top N similar vectors to the query text.

        Args:
            query_text (str): Text input for the query to find similar vectors.
            top_n (int): Number of top similar vectors to return (default is 5).
            decode_results (bool): Whether to decode the results back to text (default is True).

        Returns:
            List[Tuple[str, float]]: List of vector IDs and their similarity scores.
        """
        query_vector = np.array(self.embedding_model.embed(query_text))
        
        results = []

        if self.indexing == "hnsw":
            nearest_vectors = self.index.search(query_vector, top_n)
            for vector in nearest_vectors:
                cosine_similarity = self.similarity(query_vector, vector)
                results.append((self.get_key_by_value(value=vector), cosine_similarity))
        
        else:
            for existing_id, existing_vector in self.vector.items():
                cosine_similarity = self.similarity(query_vector, existing_vector)
                results.append((existing_id, cosine_similarity))
        
            results.sort(key=lambda x: x[1], reverse=True)
                
        if decode_results:
            # Return the n similar results decoded back to text
            decoded_results = []
            for result in results[:top_n]:
                decoded_text = self.embedding_model.reverse_embedding(self.vector[result[0]])
                decoded_results.append((result[0], result[1], decoded_text))
            return decoded_results
        
        return results[:top_n]
    
    
class keyValueStore:
    def __init__(self, json_path="data.json"):
        '''
        Initialize key-value store with master and default collections.
        Creates directory structure if it doesn't exist.
        '''
        self.base_path = json_path.rsplit('.', 1)[0]
        os.makedirs(self.base_path, exist_ok=True)
        
        # Initialize master collection structure
        self.master_collections = {}
        self.current_master = "default"
        self.current_collection = "default"
        
        # Create default master collection and collection
        master_path = os.path.join(self.base_path, "default")
        os.makedirs(master_path, exist_ok=True)
        collection_path = os.path.join(master_path, "default.json")
        
        if not os.path.exists(collection_path):
            with open(collection_path, "w") as f:
                json.dump({"documents": []}, f)

    def create_master_collection(self, name):
        '''Create a new master collection'''
        path = os.path.join(self.base_path, name)
        os.makedirs(path, exist_ok=True)
        self.master_collections[name] = {}
        
    def create_collection(self, name, master_collection="default"):
        '''Create a new collection within a master collection'''
        master_path = os.path.join(self.base_path, master_collection)
        collection_path = os.path.join(master_path, f"{name}.json")
        
        if not os.path.exists(collection_path):
            with open(collection_path, "w") as f:
                json.dump({"documents": []}, f)

    def use_collection(self, collection, master_collection="default"):
        '''Switch to a specific collection'''
        self.current_master = master_collection
        self.current_collection = collection

    def add(self, data, doc_id=None):
        '''
        Add document(s) to current collection
        '''
        collection_path = os.path.join(self.base_path, self.current_master, 
                                     f"{self.current_collection}.json")
        
        with open(collection_path, "r") as f:
            try:
                collection_data = json.load(f)
            except json.JSONDecodeError:
                collection_data = {"documents": []}

        if isinstance(data, list):
            for idx, doc in enumerate(data):
                doc_with_id = doc.copy()
                if doc_id is None:
                    doc_with_id["_id"] = str(uuid.uuid4())
                else:
                    doc_with_id["_id"] = f"{doc_id}_{idx}"
                collection_data["documents"].append(doc_with_id)
        else:
            doc_with_id = data.copy()
            doc_with_id["_id"] = doc_id or str(uuid.uuid4())
            collection_data["documents"].append(doc_with_id)

        with open(collection_path, "w") as f:
            json.dump(collection_data, f, indent=4)

    def add_json(self, json_file):
        '''
        Add documents from a JSON file to current collection
        
        Args:
            json_file (str): Path to JSON file containing documents
        '''
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            # Handle both single document and list of documents
            if isinstance(data, dict):
                self.add(data)
            elif isinstance(data, list):
                self.add(data)
            else:
                raise ValueError("JSON file must contain either a single document or list of documents")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {json_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {json_file}")

    def __getitem__(self, key):
        '''Retrieve document by index'''
        collection_path = os.path.join(self.base_path, self.current_master,
                                     f"{self.current_collection}.json")
        with open(collection_path, "r") as f:
            collection_data = json.load(f)
        return collection_data["documents"][key]

    def search(self, key, value):
        '''Search documents by key-value pair'''
        collection_path = os.path.join(self.base_path, self.current_master,
                                     f"{self.current_collection}.json")
        with open(collection_path, "r") as f:
            collection_data = json.load(f)
        
        return [doc for doc in collection_data["documents"] if doc.get(key) == value]

    def toVector(self, indexing="brute-force", embedding_model="bert", collection=None, master_collection=None):
        '''
        Convert collection documents to vector store
        '''
        if collection:
            self.use_collection(collection, master_collection or self.current_master)
            
        collection_path = os.path.join(self.base_path, self.current_master,
                                     f"{self.current_collection}.json")
        
        with open(collection_path, "r") as f:
            collection_data = json.load(f)

        docs = [json.dumps(doc, separators=(',', ':')) for doc in collection_data["documents"]]
        
        vectorStore = VectorStore(indexing=indexing, embedding_model=embedding_model)
        vectorStore.add_documents(docs)
        
        return vectorStore
