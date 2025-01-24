import inspect
import os
import shutil

import pytest
from langchain.prompts import ChatPromptTemplate
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

from ..kwwutils import (
    clock,
    count_tokens,
    create_vectordb,
    get_documents_by_path,
    get_embeddings,
    get_llm,
    printit,
)


@clock
def test_basic(options, model):
    printit("options", options)
    printit("model", model)
    llm_type = "llm"
    options["llm_type"] = llm_type
    model = "llama3:latest"
    options["model"] = model
    temperature = 0.1
    options["temperature"] = temperature
    printit("2 options", options)
    llm = get_llm(options)
    printit("llm", llm)
    prompt = "What is 1 + 1?"
    output = llm.invoke(prompt)
    print(f"output {output}")
    assert llm.temperature == temperature
    assert llm.model == model
    assert "2" in output
    output = count_tokens(output)
    print(f"token output {output}")


@clock
def test_get_llm(options, model):
    printit("options", options)
    printit("model", model)
    llm = get_llm(options)
    printit("llm", llm)
    prompt = "What is 1 + 1?"
    output = llm.invoke(prompt)
    print(f"output {output}")
    assert "2" in output


@clock
def test_get_chat_llm(options, model):
    printit("options", options)
    printit("model", model)
    llm_type = "chat"
    options["llm_type"] = llm_type
    options["model"] = model
    llm = get_llm(options)
    template1 = "What is the best name to describe a company that makes {product}?"
    prompt1 = ChatPromptTemplate.from_template(template=template1)
    chain = prompt1 | llm
    output = chain.invoke({"product": "car"})
    printit("output", output)


@clock
def test_get_documents_by_path_file(options, model):
    printit("options", options)
    printit("model", model)
    dirname = os.path.dirname(os.path.abspath(__file__))
    printit("dirname", dirname)
    testfile = os.path.abspath(os.path.join(dirname, "../pytest.ini"))
    printit("testfile", testfile)
    docs = get_documents_by_path(testfile)
    printit("docs", docs)
    assert docs[0].metadata["source"] == testfile


@clock
def test_get_documents_by_path_dir(options, model):
    printit("options", options)
    printit("model", model)
    dirname = os.path.dirname(os.path.abspath(__file__))
    printit("dirname", dirname)
    dirpath = os.path.abspath(os.path.join(dirname, "../data"))
    printit("dirpath", dirpath)
    docs = get_documents_by_path(dirpath)
    printit("docs", docs)
    assert docs[0].metadata["source"].startswith(dirpath)


@clock
def test_get_documents_by_path_web(options, model):
    printit("options", options)
    printit("model", model)
    testfile = "https://www.langchain.com/"
    printit("testfile", testfile)
    docs = get_documents_by_path(testfile)
    printit("docs", docs)
    assert docs[0].metadata["source"] == testfile


@pytest.mark.parametrize(
    "vectorstore, vectordb_type",
    [
        # ("Chroma", "disk"),
        # ("Chroma", "memory"),
        ("FAISS", "disk"),
        # ("FAISS", "memory"),
    ],
)
@clock
def test_create_vectordb(options, model, vectorstore, vectordb_type):
    name_ = f"{inspect.currentframe().f_code.co_name}"
    printit("options", options)
    printit("model", model)
    options["vectorstore"] = vectorstore
    options["vectordb_type"] = vectordb_type
    printit("options", options)
    vectordb = create_vectordb(options)
    printit("vectordb", vectordb)
    print(f"{name_} vectorestore {vectorstore} vectordb_type {vectordb_type}")
    if vectorstore == "Chroma":
        documents = vectordb.get(ids=None, include=["documents"])
        for doc in documents:
            print(f"{name_} doc", doc)
    elif vectorstore == "FAISS":
        num_vectors = vectordb.index.ntotal
        printit(f"{name_} num_vectors", num_vectors)


@pytest.mark.testme
@pytest.mark.parametrize(
    "vectorstore, vectordb_type",
    [
        ("Chroma", "disk"),
        ("Chroma", "memory"),
        ("FAISS", "disk"),
        ("FAISS", "memory"),
    ],
)
@clock
def test_create_vectordb_documents(options, model, vectorstore, vectordb_type):
    name_ = f"{inspect.currentframe().f_code.co_name}"
    printit("options", options)
    printit("model", model)
    options["vectorstore"] = vectorstore
    options["vectordb_type"] = vectordb_type
    printit("options", options)
    all_docs = []
    if os.path.isdir(options["persist_directory"]):
        shutil.rmtree(options["persist_directory"])
    PYTHON_CODE = """
    def hello_world():
        print("Hello, World!")
    # Call the function
    hello_world()
    # class AnswerWithJustification(BaseModel):
    #     '''An answer to the user question along with justification for the answer.'''
    #     answer: str
    #     '''The answer to the user's question'''
    #     justification: str
    #     '''Justification for the answer'''
    # structured_llm = llm.with_structured_output(AnswerWithJustification)
    # output = structured_llm.invoke("What weighs more, a pound of bricks or a pound of feathers")

    # parser = CommaSeparatedListOutputParser()
    # items = parser.invoke("apple, banana, cherry")
    # print(f"items {items}\n")
    """
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=50, chunk_overlap=0
    )
    python_docs = python_splitter.create_documents([PYTHON_CODE])
    all_docs.extend(python_docs)
    printit(f"{name_} 5 all_docs len:", len(all_docs))
    printit(f"{name_} 5B all_docs:", all_docs)

    markdown_text = """
    # LangChain
    Building applications with LLMs through composability
    ## Quick Install
    ```bash
    pip install langchain
    ```
    As an open-source project in a rapidly developing field, we are extremely open to contributions.
    """
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=60, chunk_overlap=0
    )
    md_docs = md_splitter.create_documents(
        [markdown_text], [{"source": "https://www.langchain.com"}]
    )
    all_docs.extend(md_docs)
    printit(f"{name_} all_docs len:", len(all_docs))
    options["documents"] = all_docs
    vectordb = create_vectordb(options)
    printit("vectordb", vectordb)
    print(f"{name_} vectorestore {vectorstore} vectordb_type {vectordb_type}")
    if vectorstore == "Chroma":
        vectordata = vectordb.get(ids=None, include=["documents"])
        printit("vectordata documents len:", len(vectordata["documents"]))
        ndocuments = len(vectordata["documents"])
    elif vectorstore == "FAISS":
        ndocuments = vectordb.index.ntotal
        printit(f"{name_} ndocuments", ndocuments)
    assert ndocuments == 25


@pytest.mark.parametrize("embedding", ["chroma", "gpt4all", "huggingface"])
@clock
def test_get_embeddings(options, model, embedding):
    printit("options", options)
    printit("model", model)
    options["embedding"] = embedding
    embedding = get_embeddings(options)
    printit("embedding", embedding)
