import streamlit as st


class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.employee_information = assistant.employee_information

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    def render_messages(self):
        messages = st.session_state.messages

        for message in messages:
            if message["role"] == "user":
                st.chat_message("human").markdown(message["content"])
            elif message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def render_user_input(self):
        user_input = st.chat_input("Type here...")
        if user_input and user_input != "":
            st.chat_message("human").markdown(user_input)

            response_generator = self.get_response(user_input)

            with st.chat_message("ai"):
                response = st.write_stream(response_generator)

            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "ai", "content": response})

    def render(self):
        st.title("PoliSense AI - Intelligent Employee Policy Assistant")
        st.caption("RAG-based assistant using company policy PDF")

        with st.sidebar:
            st.title("PoliSense AI Assistant")

            # ----------------------------------
            # PDF Upload Section
            # ----------------------------------
            st.subheader("📄 Upload Policy Document")
            uploaded_pdf = st.file_uploader(
                "Upload a PDF file",
                type="pdf",
                help="Upload your policy document to analyze",
                key="pdf_uploader",
            )

            # Track successful uploads in session state
            if "last_uploaded_pdf" not in st.session_state:
                st.session_state.last_uploaded_pdf = None

            if uploaded_pdf is not None:
                import tempfile
                import os
                from langchain_community.document_loaders import PyPDFLoader
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                from langchain_community.embeddings import HuggingFaceEmbeddings
                from langchain_community.vectorstores import FAISS

                st.info(f"📁 Processing: {uploaded_pdf.name}")

                # Process the uploaded PDF
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as tmp_file:
                    tmp_file.write(uploaded_pdf.read())
                    tmp_file_path = tmp_file.name

                try:
                    loader = PyPDFLoader(tmp_file_path)
                    documents = loader.load()

                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=800,
                        chunk_overlap=150,
                    )
                    chunks = splitter.split_documents(documents)

                    embeddings = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/all-MiniLM-L6-v2"
                    )

                    new_vectorstore = FAISS.from_documents(chunks, embeddings)
                    st.session_state.vectorstore = new_vectorstore

                    # Clear message history to start fresh with new PDF
                    st.session_state.messages = []

                    # Reinitialize the assistant with new vectorstore
                    from assistant import Assistant
                    from prompts import SYSTEM_PROMPT

                    st.session_state.assistant = Assistant(
                        system_prompt=SYSTEM_PROMPT,
                        llm=st.session_state.assistant.llm,
                        message_history=st.session_state.messages,
                        vector_store=st.session_state.vectorstore,
                        employee_information=st.session_state.employee_data,
                    )

                    # Update self to reflect changes
                    self.assistant = st.session_state.assistant

                    # Store the uploaded filename
                    st.session_state.last_uploaded_pdf = uploaded_pdf.name

                    st.success(f"✅ Successfully loaded: {uploaded_pdf.name}")
                    st.info("You can now ask questions about the uploaded document!")
                finally:
                    os.unlink(tmp_file_path)
            elif st.session_state.last_uploaded_pdf:
                # Show success message if PDF was recently uploaded
                st.success(f"✅ Using: {st.session_state.last_uploaded_pdf}")
                st.info("You can ask questions about the loaded document!")

        self.render_messages()
        self.render_user_input()
