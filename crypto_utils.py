"""
Advanced cryptographic utilities for Zencrypt v6
Includes ECC, Argon2, and concurrent processing capabilities
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import argon2
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import queue
import os
from typing import List, Tuple, Generator
import threading
from dataclasses import dataclass
from merklelib import MerkleTree
from io import BytesIO, IOBase

# Constants
CHUNK_SIZE = 2 * 1024 * 1024  # 2MB chunks for parallel processing

@dataclass
class ChunkMetadata:
    """Metadata for file chunks during parallel processing"""
    index: int
    hash: str
    size: int

class CryptoQueue:
    """Thread-safe queue for crypto operations"""
    def __init__(self):
        self.queue = queue.Queue()
        self.results = {}
        self._lock = threading.Lock()

    def put(self, item: Tuple[int, bytes]):
        self.queue.put(item)

    def get(self) -> Tuple[int, bytes]:
        return self.queue.get()

    def store_result(self, chunk_index: int, result: bytes):
        with self._lock:
            self.results[chunk_index] = result

    def get_ordered_results(self) -> List[bytes]:
        return [self.results[i] for i in sorted(self.results.keys())]

class ECCHandler:
    """Handles Elliptic Curve Cryptography operations"""
    def __init__(self):
        self.curve = ec.SECP384R1()
        self.backend = default_backend()

    def generate_keypair(self) -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
        private_key = ec.generate_private_key(self.curve, self.backend)
        public_key = private_key.public_key()
        return private_key, public_key

    def derive_key(self, private_key: ec.EllipticCurvePrivateKey, 
                  peer_public_key: ec.EllipticCurvePublicKey) -> bytes:
        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=self.backend
        ).derive(shared_key)
        return derived_key

class Argon2Handler:
    """Handles Argon2 password hashing"""
    def __init__(self):
        self.ph = argon2.PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32
        )

    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)

    def verify_password(self, hash: str, password: str) -> bool:
        try:
            self.ph.verify(hash, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False

class ParallelFileProcessor:
    """Handles parallel processing of large files"""
    CHUNK_SIZE = 2 * 1024 * 1024  # 2MB chunks
    
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or os.cpu_count()
        self.chunk_queue = CryptoQueue()
        self.merkle_tree = None

    def process_file_parallel(self, file_obj, processor_func, use_processes: bool = False) -> bytes:
        """Process a file in parallel chunks
        
        Args:
            file_obj: A file-like object (can be Flask FileStorage or path string)
            processor_func: Function to process each chunk
            use_processes: Whether to use multiprocessing
        """
        chunk_metadata = []
        
        # Split file into chunks and process
        with ThreadPoolExecutor(max_workers=self.num_workers) if not use_processes \
             else ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            
            # Submit chunks for processing
            futures = []
            for chunk_index, chunk in enumerate(self._read_chunks(file_obj)):
                future = executor.submit(processor_func, chunk)
                futures.append((chunk_index, future))
            
            # Collect results
            for chunk_index, future in futures:
                result = future.result()
                self.chunk_queue.store_result(chunk_index, result)
                
                metadata = ChunkMetadata(
                    index=chunk_index,
                    hash=hash(result),
                    size=len(result)
                )
                chunk_metadata.append(metadata)

        # Build Merkle tree from chunk metadata
        self.merkle_tree = MerkleTree([
            f"{meta.index}:{meta.hash}:{meta.size}" 
            for meta in chunk_metadata
        ])
        
        return b''.join(self.chunk_queue.get_ordered_results())

    def _read_chunks(self, file_obj) -> Generator[bytes, None, None]:
        """Read file in chunks
        
        Args:
            file_obj: File-like object (BytesIO, FileStorage, or path string)
        """
        if isinstance(file_obj, str):
            with open(file_obj, 'rb') as f:
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk
        elif isinstance(file_obj, (BytesIO, IOBase)):
            while True:
                chunk = file_obj.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
            file_obj.seek(0)

    def verify_chunk_integrity(self, chunk_metadata: ChunkMetadata) -> bool:
        """Verify a chunk's integrity using the Merkle tree"""
        if not self.merkle_tree:
            raise ValueError("No Merkle tree available. Process a file first.")
        
        leaf_value = f"{chunk_metadata.index}:{chunk_metadata.hash}:{chunk_metadata.size}"
        return self.merkle_tree.verify_leaf(leaf_value)
