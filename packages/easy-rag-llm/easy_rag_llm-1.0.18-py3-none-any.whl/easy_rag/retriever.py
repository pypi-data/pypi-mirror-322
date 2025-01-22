import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from pypdf import PdfReader
import numpy as np
import faiss

class Retriever:
    def __init__(self, embedding):
        self.embedding = embedding

    def load_resources(self, resource_path, chunk_size=512, chunk_overlap=50, max_workers=10):
        if not os.path.isdir(resource_path):
            raise ValueError(f"Invalid resource path: {resource_path}")

        nodes = self._extract_text_from_pdfs(resource_path, max_workers)
        chunks = self._split_text_into_chunks(nodes, chunk_size, chunk_overlap)

        # Async embedding generation
        embeddings, metadata = asyncio.run(self._generate_embeddings_async(chunks))

        if embeddings:
            index = self._create_faiss_index(np.array(embeddings, dtype=np.float32))
        else:
            raise ValueError("No embeddings generated.")

        return index, metadata

    def _extract_text_from_pdfs(self, resource_path, max_workers):
        pdf_files = [
            os.path.join(resource_path, file_name)
            for file_name in os.listdir(resource_path)
            if file_name.endswith(".pdf")
        ]

        nodes = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._extract_text_from_pdf, pdf): pdf for pdf in pdf_files
            }
            for future in tqdm(asyncio.as_completed(futures), desc="Extracting PDFs", total=len(futures)):
                try:
                    nodes.extend(future.result())
                except Exception as e:
                    print(f"Error processing {futures[future]}: {e}")
        return nodes

    def _extract_text_from_pdf(self, pdf_path):
        nodes = []
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text().strip()
                if text:
                    nodes.append({"page_number": i + 1, "text": text, "file_name": os.path.basename(pdf_path)})
                else:
                    print(f"Warning: Empty text on page {i + 1} in {pdf_path}")
            except Exception as e:
                print(f"Error extracting text from page {i + 1} in {pdf_path}: {e}")
        return nodes

    def _split_text_into_chunks(self, nodes, chunk_size, chunk_overlap):
        chunks = []
        for node in nodes:
            text = node["text"]
            for i in range(0, len(text), chunk_size - chunk_overlap):
                chunk_text = text[i:i + chunk_size]
                chunks.append({"text": chunk_text, "page_number": node["page_number"], "file_name": node["file_name"]})
        return chunks

    async def _generate_embeddings_async(self, chunks):
        semaphore = asyncio.Semaphore(10)

        async def process_chunk(chunk):
            async with semaphore:
                return await asyncio.to_thread(self._create_embedding_with_metadata, chunk)

        tasks = [process_chunk(chunk) for chunk in chunks]
        embeddings, metadata = [], []
        for task in tqdm(asyncio.as_completed(tasks), desc="Generating Embeddings", total=len(tasks)):
            try:
                embedding, meta = await task
                embeddings.append(embedding)
                metadata.append(meta)
            except Exception as e:
                print(f"Error generating embedding: {e}")
        return embeddings, metadata

    def _create_embedding_with_metadata(self, chunk):
        embedding = self.embedding.create_embedding(chunk["text"])
        return embedding, chunk

    def _create_faiss_index(self, embeddings):
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index
