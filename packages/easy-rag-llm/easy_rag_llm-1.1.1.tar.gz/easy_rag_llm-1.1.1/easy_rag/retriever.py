import os
import numpy as np
import faiss
from tqdm import tqdm
from pypdf import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed
from .embedding import Embedding


class Retriever:
    def __init__(self, embedding):
        self.embedding = embedding

    def load_resources(self, resource_path, chunk_size=512, chunk_overlap=50, max_workers=10):
        if not os.path.isdir(resource_path):
            raise ValueError(f"Invalid resource path: {resource_path}")

        nodes = []
        pdf_files = [
            os.path.join(resource_path, file_name)
            for file_name in os.listdir(resource_path)
            if file_name.endswith(".pdf")
        ]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._extract_text_from_pdf, pdf, os.path.basename(pdf)): pdf
                for pdf in pdf_files
            }
            for future in tqdm(as_completed(futures), desc="Extracting Text from PDFs", total=len(futures)):
                try:
                    nodes.extend(future.result())
                except Exception as e:
                    print(f"Error processing {futures[future]}: {e}")

        chunks = self._split_text_into_chunks(nodes, chunk_size, chunk_overlap)

        embeddings = []
        metadata = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._create_embedding_with_metadata, chunk): chunk for chunk in chunks
            }
            for future in tqdm(as_completed(futures), desc="Generating Embeddings", total=len(futures)):
                try:
                    embedding, meta = future.result()
                    embeddings.append(embedding)
                    metadata.append(meta)
                except Exception as e:
                    print(f"Error generating embedding: {e}")

        if embeddings:
            index = self._create_faiss_index(np.array(embeddings, dtype=np.float32))
        else:
            raise ValueError("No embeddings generated.")

        return index, metadata



    def _extract_text_from_pdf(self, pdf_path, file_name):
        nodes = []
        file_name = os.path.basename(pdf_path)
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text().strip()
                if text:
                    nodes.append({"page_number": i + 1, "text": text, "file_name": file_name})
                else:
                    print(f"Warning: Empty text on page {i + 1} in {pdf_path}")
            except Exception as e:
                print(f"Error extracting text from page {i + 1} in {pdf_path}: {e}")
        return nodes

    def _split_text_into_chunks(self, nodes, chunk_size, chunk_overlap):
        chunks = []
        for node in nodes:
            text = node["text"]
            page_number = node["page_number"]
            file_name = node["file_name"]
            for i in range(0, len(text), chunk_size - chunk_overlap):
                chunk_text = text[i:i + chunk_size]
                chunks.append({"text": chunk_text, "page_number": page_number, "file_name": file_name})
        return chunks

    def _create_embedding_with_metadata(self, chunk):
        embedding = self.embedding.create_embedding(chunk["text"])
        return embedding, chunk
    
    """
    indexFlatL2에 대한 메모:
    브루트포스 알고리즘이며 유를리디안 거리 이용.
    코사인 유사도 지원.
    다른 인덱스사용도 고민할 것. HNSF를 적용해보려함. (efSearch=50-200 테스트)
    """

    def _create_faiss_index(self, embeddings):
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index
