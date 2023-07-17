

import streamlit as st

from streamlit_chat import message
from streamlit_toggle import st_toggle_switch
from streamlit.runtime.scriptrunner import add_script_run_ctx
from concurrent.futures import ThreadPoolExecutor

from backend.models_config import MODELS_JSON
from db.vecstore import Vecstore
from backend.utils import General

class UiElements(object):
    """
    User interface components and supporting functions
    """

    def __init__(self):
        self.counter = 0

    def select_llm_model(self):
        """
        Function to add llm selection panel in sidebar
        """
        # LLM model selection section
        model_name = st.sidebar.selectbox(
            "Models",
            options=self.MODELS.keys(),
        )
        if model_name:
            st.session_state["selected_model"] = model_name

        # publishing information about the chosen LLM model
        expander = st.sidebar.expander("model info")
        info = self.MODELS.get(st.session_state["selected_model"], "")
        expander.write(info.get("info", ""))
        if info:
            if info["name"] not in ["GPT-3", "GPT-4"] and info.get("conn") == "":
                st.sidebar.warning("Please Enable EndPoint")

    def select_documents(self):
        """
        select documents wrapper
        """
        # Document Selection
        st.sidebar.divider()

        vecstore = Vecstore()
        data_collection = vecstore.list_all_collections()
        data_collection.append("none")
        st.sidebar.subheader("Data Collection")
        selected_dataset = st.sidebar.selectbox(
            "select a dataset",
            options=data_collection,
            on_change=vecstore.release_all(),
        )
        if selected_dataset:
            st.session_state["dataset"] = selected_dataset
            # vecstore.load_collection(selected_dataset)

        document_upload_toggle = st_toggle_switch(
            active_color="grey",
            label="upload document",
        )
        if document_upload_toggle:
            # Document Upload
            self.upload_files()

    def upload_files(self):
        """
        performing file upload for data collection

        Returns:
            file_name: name of the file being uploaded
        """
        uploaded_files = st.sidebar.file_uploader(
            "dataset file",
            accept_multiple_files=True,
        )
        for uploaded_file in uploaded_files:
            data = uploaded_file.getvalue().decode('utf-8')
            file_name = (uploaded_file.name).split(".")[0]
            self.background_db_upload(file_name, data)
            st.write("filename:", file_name)

    def upload_callback(self, future):
        """
        a callback function for file upload thread to notify when the task is complete

        Args:
            future: Threadpoolexecutor instance
        """
        st.sidebar.success("Uploaded your data")

    def background_db_upload(self, file_name, data):
        """
        data upload to database with vector embeddings using Threading

        Args:
            file_name: name of the file
            data: content of the file
        """
        vecstore = Vecstore()
        if file_name not in vecstore.list_all_collections():
            with ThreadPoolExecutor() as executor:
                future = executor.submit(vecstore.setup_new_collection, file_name, data)
                future.add_done_callback(self.upload_callback)
                for task in executor._threads:
                    add_script_run_ctx(task)

    def clear_conversation(self):
        """
        flushing the session memory with clear button press
        """
        # clear conversation section
        clear_button = st.sidebar.button("Clear Conversation", key="clear")
        if clear_button:
            st.session_state["dataset"] = ""
            st.session_state["generated"] = []
            st.session_state["past"] = []
            st.session_state["messages"] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
            st.session_state["number_tokens"] = []
            st.session_state["cost"] = []
            st.session_state["total_cost"] = 0.0
            st.session_state["tokens"] = []

    def submit_query(self):
        """function to set input box empty after hitting enter"""
        st.session_state.query = st.session_state.widget
        st.session_state.widget = ""


class UiWrappers(UiElements):
    """
    contains individual sections of application
    sidebar and chat
    """

    def __init__(self):
        self.MODELS = MODELS_JSON["models"]

    def sidebar(self):
        """
        Base sidebar Container
        """
        st.sidebar.image("images/simform-logo.png", width=60)
        st.sidebar.title("BlogsGPT ✨ (vecstore)")
        self.select_llm_model()
        self.clear_conversation()
        self.select_documents()

    def chat(self):
        """
        Base chat Container
        """
        # container for chat history
        response_container = st.container()
        # container for text box
        container = st.container()
        with container:
            st.text_input("You:", key="widget", on_change=self.submit_query)
            functions = General()
            if st.session_state.query:
                output = (
                    functions.generate_conversational_response(st.session_state.query)
                    if st.session_state["selected_model"].lower() in ["gpt-3", "gpt-4"]
                    else functions.generate_from_custom_api(st.session_state.query)
                )
                st.session_state["past"].append(st.session_state.query)
                st.session_state["generated"].append(output)

        if st.session_state["generated"]:
            with response_container:
                for i in range(len(st.session_state["generated"])):
                    message(
                        st.session_state["past"][i], is_user=True, key=str(i) + "_user"
                    )
                    message(st.session_state["generated"][i], key=str(i))

    def dev_stats(self):
        '''
        Will Display cost of each conversation with each message and reply as current info
        and total conversation as the info of whole conversation up-till the end
        '''
        functions = General()
        curr_cost, curr_token = functions.get_chat_current_info()
        total_cost, total_tokens = functions.get_chat_total_info()
        st.sidebar.code(
            f"""
                # Total cost
                No_of_tokens = {total_tokens}
                Total_cost = ${total_cost}
            """,
            language="python",
        )
        st.sidebar.markdown(
            f"""
            >  current cost  
            ```No. of tokens: {curr_token}```  
            ```Total Cost: ${curr_cost}```
            """
        )
