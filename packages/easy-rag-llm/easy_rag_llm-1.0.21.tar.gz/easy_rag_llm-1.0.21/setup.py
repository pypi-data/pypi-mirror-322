from setuptools import setup, find_packages

setup(
    name="easy-rag-llm",
    version="1.0.21",
    author="Aiden-Kwak",
    author_email="duckracoon@gist.ac.kr",
    description="Easily implement RAG workflows with pre-built modules.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Aiden-Kwak/easy_rag",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "faiss-cpu",
        "numpy",
        "tqdm",
        "pypdf",
        "openai",
        "requests",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
