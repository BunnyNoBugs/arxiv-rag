## **ArxivRAG**

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

🚀 Deployment Instructions
**Telegram Bot Integration**
This project includes a Telegram bot that utilizes the RAG class to respond intelligently to user queries. Follow these steps to deploy and run the bot:

🛠 Setup and Configuration
Ensure you have all required dependencies installed:

```
pip install -r requirements.txt
```

Create a .env file. Example .env:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GPTUNNEL_API_KEY=your_gptunnel_api_key
```

Set Up the Bot
The bot is configured to respond to /start and /help commands and handle free-text user messages via rag_reply.

▶️ Run the Bot
Start the bot by running the following command:

```
python bot.py
```
The bot will connect to Telegram and begin listening for messages.
