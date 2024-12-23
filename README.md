The RAG class provides a straightforward implementation of a Retrieval-Augmented Generation (RAG) system, combining document retrieval with advanced text generation capabilities. It leverages LLM via the GPTunnel API and a langchain-community built-in ArxivRetriever, to answer complex scientific questions effectively.

✨ Key Features
🔍 Retrieval with Augmented Generation
Retrieves relevant scientific articles to provide context for generating detailed and accurate answers.

⚙️ Customizable LLM
Uses the GPTunnelLLM class, seamlessly integrated with the GPTunnel API, offering configurable model settings.

💬 Conversation History
Keeps track of past interactions to:

- Ensure coherent and contextually aware responses.
- Enhance conversational continuity over multiple exchanges.

📜 Flexible Prompt Design
Utilizes a structured prompt template that dynamically integrates:

- Context from retrieved documents.
- Conversation history for continuity.
- The current user question to tailor responses precisely.
