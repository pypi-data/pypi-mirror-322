from setuptools import setup, find_packages

setup(
    name="streamlit-ollama-agent",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.24.0",
        "openai>=1.0.0",
        "pydantic-ai>=0.0.1",
        "httpx>=0.24.0",
    ],
    author="Shenakiii",
    author_email="re@dac.ted",
    description="A reusable Streamlit-based chat interface for Ollama models using PydanticAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/streamlit-ollama-agent",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 