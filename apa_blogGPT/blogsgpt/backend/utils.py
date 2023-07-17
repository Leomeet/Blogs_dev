import streamlit as st
import os
import requests
import pickle
import functools
from requests_auth_aws_sigv4 import AWSSigV4
from langchain.callbacks import get_openai_callback
from .models_config import MODELS_JSON
from langchain_utils.utils import LangchainUtils
from exceptions.exceptions import (
    LlmModelSelectionException,
    EmptyModelSelectionException,
    MissingKeysException,
)


class General:
    """
    General Utility functions for application
    """

    def __init__(self):
        self.MODELS = MODELS_JSON["models"]
        self.open_ai_key = os.environ.get("OPENAI_API_KEYS", None)
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", None)
        self.aws_secret_secret_kes = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
        self.aws_session_token = os.environ.get("AWS_SESSION_TOKEN", None)

    def __call__(self):
        """
        setting on selection values
        """
        if st.session_state["selected_model"] == "":
            raise EmptyModelSelectionException("No Model Selected")
        else:
            models_data = self.MODELS.get(st.session_state["selected_model"], None)
            for i, key in enumerate(models_data.get("keys")):
                if not os.environ.get(key):
                    raise MissingKeysException(f"Missing required keys: {key} ")

    def initialize_session(self):
        """
        initializing session variables
        """
        # Initialise session state variables
        if "dataset" not in st.session_state:
            st.session_state["dataset"] = []
        if "generated" not in st.session_state:
            st.session_state["generated"] = []
        if "past" not in st.session_state:
            st.session_state["past"] = []
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        if "cost" not in st.session_state:
            st.session_state["cost"] = [
                0.0,
            ]
        if "tokens" not in st.session_state:
            st.session_state["tokens"] = [
                0,
            ]
        if "chat_summary" not in st.session_state:
            st.session_state["chat_summary"] = []
        if "selected_model" not in st.session_state:
            st.session_state["selected_model"] = ""
        if "query" not in st.session_state:
            st.session_state.query = ""

    def generate_from_custom_api(self, query):
        """call custom api mapped with custom llm endpoint

        Args:
            query: user input

        Returns:
            : answer response from custom llm
        """
        info = [
            x for x in self.MODELS if x["name"] == st.session_state["selected_model"]
        ]
        pre_set_url = info[0].get("conn", None) if info else ""

        st.session_state["messages"].append({"role": "user", "content": query})
        payload = {
            "inputs": query,
        }

        aws_auth = AWSSigV4(
            "sagemaker",
            region="us-east-1",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=os.environ["AWS_SESSION_TOKEN"],
        )

        try:
            ans = requests.request(
                "POST", pre_set_url, auth=aws_auth, json=payload, timeout=5
            )
            if str(ans.status_code)[0] == "4":
                st.warning("Unable to process Request check endpoint")
        except ConnectionError as error:
            print(error)

        ans = ans.json()[0].get("generated_text")
        st.session_state["messages"].append({"role": "ai", "content": ans})

        return (ans,)

    def generate_conversational_response(self, query):
        """
        Generates Answer for given query by calling OpenAI API
        """
        utils = LangchainUtils()
        store = utils.conversational_summary()
        st.session_state["messages"].append({"role": "user", "content": query})
        sources = ""
        if st.session_state["dataset"] != "none":
            with open("custom_embeddings/apa_data_with_source.pkl", "rb") as file:
                index = pickle.load(file)
            sources = utils.doc_search_vecstore(st.session_state["dataset"], query)

        chat_history = st.session_state.get("chat_summary")
        chat_summary = ""
        if chat_history:
            chat_summary = " ".join(x.get("history") for x in chat_history)
        with get_openai_callback() as openai_callback:
            answer = utils.get_answer(sources, query, chat_summary, True)
            st.session_state["tokens"].append(openai_callback.total_tokens)
            st.session_state["cost"].append(openai_callback.total_cost)

            st.session_state["messages"].append(
                {"role": "ai", "content": answer.get("output_text", None)}
            )

        store.save_context(
            inputs={"input": query},
            outputs={"output": answer.get("output_text", None)},
        )
        st.session_state.get("chat_summary").append(store.load_memory_variables({}))

        return answer.get("output_text")

    def generate_static_response(self, query):
        """
        Generating Response based on the query given
        with a similarity search to given doc / dataset

        Args:
            query (str): Question by user

        Returns:
            str: answer from LLM
        """
        utils = LangchainUtils()
        st.session_state["messages"].append({"role": "user", "content": query})
        with open("custom_embaddings/apa_data_with_source.pkl", "rb") as f:
            index = pickle.load(f)
        sources = utils.search_docs(index, query)
        with get_openai_callback() as openai_callback:
            answer = utils.get_answer(sources, query, True)
            st.session_state["tokens"].append(openai_callback.total_tokens)
            st.session_state["cost"].append(openai_callback.total_cost)
            st.session_state["messages"].append(
                {"role": "ai", "content": answer.get("output_text", None)}
            )

        return answer.get("output_text")

    def get_chat_current_info():
        cost = st.session_state["cost"]
        tokens = st.session_state["tokens"]
        return cost[-1], tokens[-1]

    def get_chat_total_info():
        cost = functools.reduce(lambda a, b: a + b, st.session_state["cost"])
        tokens = functools.reduce(lambda a, b: a + b, st.session_state["tokens"])
        return cost, tokens
