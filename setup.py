from setuptools import setup, find_packages

setup(
    name="omnicare-ai",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "langgraph",
        "langchain-openai",
        "langchain-core",
        "httpx",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "pydantic",
    ],
)
