import os
import zipfile

import panel as pn
import param
from dotenv import find_dotenv, load_dotenv
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

_ = load_dotenv(find_dotenv())  # read local .env file

llm_name = "gpt-4"
chunk_size = 126
chunk_overlap = 12


def unzip_file(zip_file, destination):
    with zipfile.ZipFile(zip_file, "r") as ref:
        ref.extractall(destination)
    return os.path.join(destination, "resume.pdf")


def load_db(file, chain_type, k):
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings(api_key=openai.api_key)
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa


class cbfs(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query = param.String("")
    db_response = param.List([])

    def __init__(self, pdf_doc, **params):
        super(cbfs, self).__init__(**params)
        self.panels = []
        self.loaded_file = pdf_doc
        self.qa = load_db(self.loaded_file, "stuff", 10)

    def call_load_db(self, count):
        if count == 0 or file_input.value is None:
            return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
        else:
            file_input.save("temp.pdf")
            self.loaded_file = file_input.filename
            button_load.button_style = "outline"
            self.qa = load_db("temp.pdf", "stuff", 4)
            button_load.button_style = "solid"
        self.clr_history()
        return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")

    def convchain(self, query):
        if not query:
            return pn.WidgetBox(
                pn.Row("User:", pn.pane.Markdown("", width=600)), scroll=True
            )
        result = self.qa.invoke({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result["answer"]
        self.panels.extend(
            [
                pn.Row("User:", pn.pane.Markdown(query, width=600)),
                pn.Row(
                    "ChatBot:",
                    pn.pane.Markdown(
                        self.answer, width=600, styles={"background-color": "#F6F6F6"}
                    ),
                ),
            ]
        )
        # inp.value = ''  #clears loading indicator when cleared
        return pn.WidgetBox(*self.panels, scroll=True)

    @param.depends(
        "db_query ",
    )
    def get_lquest(self):
        if not self.db_query:
            return pn.Column(
                pn.Row(
                    pn.pane.Markdown(
                        "Last question to DB:", styles={"background-color": "#F6F6F6"}
                    )
                ),
                pn.Row(pn.pane.Str("no DB accesses so far")),
            )
        return pn.Column(
            pn.Row(
                pn.pane.Markdown("DB query:", styles={"background-color": "#F6F6F6"})
            ),
            pn.pane.Str(self.db_query),
        )

    @param.depends(
        "db_response",
    )
    def get_sources(self):
        if not self.db_response:
            return
        rlist = [
            pn.Row(
                pn.pane.Markdown(
                    "Result of DB lookup:", styles={"background-color": "#F6F6F6"}
                )
            )
        ]
        for doc in self.db_response:
            rlist.append(pn.Row(pn.pane.Str(doc)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    @param.depends("convchain", "clr_history")
    def get_chats(self):
        if not self.chat_history:
            return pn.WidgetBox(
                pn.Row(pn.pane.Str("No History Yet")), width=600, scroll=True
            )
        rlist = [
            pn.Row(
                pn.pane.Markdown(
                    "Current Chat History variable",
                    styles={"background-color": "#F6F6F6"},
                )
            )
        ]
        for exchange in self.chat_history:
            rlist.append(pn.Row(pn.pane.Str(exchange)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    def clr_history(self, count=0):
        self.chat_history = []
        return
