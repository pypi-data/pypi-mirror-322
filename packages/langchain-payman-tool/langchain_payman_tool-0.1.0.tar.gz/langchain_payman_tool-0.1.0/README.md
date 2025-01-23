# langchain-payman-tool

This package contains the LangChain integration with PaymanAI

## Installation

```bash
pip install -U langchain-payman-tool
```

And you should configure credentials by setting the following environment variables:

* TODO: fill this out

## Chat Models

`ChatPaymanAI` class exposes chat models from PaymanAI.

```python
from langchain_payman_tool import ChatPaymanAI

llm = ChatPaymanAI()
llm.invoke("Sing a ballad of LangChain.")
```

## Embeddings

`PaymanAIEmbeddings` class exposes embeddings from PaymanAI.

```python
from langchain_payman_tool import PaymanAIEmbeddings

embeddings = PaymanAIEmbeddings()
embeddings.embed_query("What is the meaning of life?")
```

## LLMs
`PaymanAILLM` class exposes LLMs from PaymanAI.

```python
from langchain_payman_tool import PaymanAILLM

llm = PaymanAILLM()
llm.invoke("The meaning of life is")
```
