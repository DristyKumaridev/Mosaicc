# Mental Health Support Chatbot 🧠

A compassionate AI companion built with Streamlit and Groq to provide emotional support, active listening, and mental wellness strategies. This chatbot leverages the power of the Llama 3 model to offer empathetic and fast responses in a safe and non-judgmental environment.



---

## ✨ Core Features

* **Empathetic Conversations**: The AI is guided by a detailed system prompt to be supportive, validating, and understanding.
* **Real-time Streaming**: Responses are streamed token-by-token, creating a smooth and natural conversational experience.
* **Conversation Memory**: The chatbot remembers the last 10 messages to maintain context throughout the conversation.
* **Quick Self-Care Suggestions**: Interactive buttons provide instant access to guided breathing exercises, mindfulness tips, and positive affirmations.
* **Crisis Resources**: Important contact information for crisis support is readily available in the sidebar.
* **Clean & Simple UI**: Built with Streamlit for an intuitive and user-friendly interface.

---

## 🛠️ Technology Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **LLM & Backend**: [Groq API](https://groq.com/) (using the `llama-3.3-70b-versatile` model)
* **Language**: Python
* **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

* Python 3.8 or newer
* An API key from [GroqCloud](https://console.groq.com/keys)

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/mental-health-chatbot.git](https://github.com/your-username/mental-health-chatbot.git)
    cd mental-health-chatbot
    ```

2.  **Create a virtual environment:**
    * On macOS / Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    Create a file named `requirements.txt` and add the following lines:
    ```
    streamlit
    groq
    python-dotenv
    ```
    Then, run the installation command:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

1.  **Create a `.env` file** in the root directory of your project. This file will securely store your API key.

2.  **Add your Groq API key** to the `.env` file in the following format:
    ```
    GROQ_API_KEY="Your_Api_Key"
    ```

### 4. Running the Application

Launch the Streamlit app with the following command:
```bash
streamlit run app.py
