import streamlit as st
import os
from groq import Groq
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Mental Health Support Chatbot",
    page_icon="🧠",
    layout="centered"
)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY not found. Please check your .env file.")
        st.markdown("""
        **To fix this:**
        1. Create a `.env` file in your project directory
        2. Add your API key: `GROQ_API_KEY=your-api-key-here`
        3. Restart the application
        """)
        st.stop()
    return Groq(api_key=api_key)

# System prompt for mental health support
MENTAL_HEALTH_PROMPT = """You are a compassionate and empathetic mental health support chatbot. Your role is to:

1. Listen actively and validate the user's emotions
2. Provide emotional support and encouragement
3. Offer practical coping strategies and techniques
4. Recognize emotional states from user input
5. Respond with warmth, understanding, and professionalism
6. Suggest breathing exercises, mindfulness techniques, or grounding exercises when appropriate
7. Encourage seeking professional help when needed
8. Give brief, positive responses

Guidelines:
- Always be supportive and non-judgmental
- Use empathetic language and acknowledge feelings
- Provide helpful suggestions without being prescriptive
- Recognize signs of distress and respond appropriately
- Never provide medical advice or diagnosis
- Encourage professional help for serious concerns

Remember: You are a supportive companion, not a replacement for professional mental health care."""

# THIS IS THE KEY FIX - Parser function for Groq streaming response
def parse_groq_stream(stream):
    """Parse Groq streaming response to extract content"""
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

def analyze_emotion_and_respond(client, user_message, conversation_history):
    """Generate empathetic response based on emotional analysis"""
    
    # Create messages for the API call
    messages = [{"role": "system", "content": MENTAL_HEALTH_PROMPT}]
    
    # Add conversation history
    messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Create chat completion with streaming
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Using LLaMA model as requested
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True 
        )
        
        return stream
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def main():
    # App header
    st.title("🧠 Mental Health Support Chatbot")
    st.markdown("*A compassionate AI companion for emotional support and mental wellness*")
    
    # Sidebar with information
    with st.sidebar:
        st.header("💡 About This Chatbot")
        st.markdown("""
        This chatbot is designed to:
        - Provide emotional support
        - Understand your feelings
        - Offer coping strategies
        - Practice active listening
        
        **Important:** This is not a replacement for professional mental health care.
        """)
        
        st.header("🚨 Crisis Resources")
        st.markdown("""
        **If you're in crisis:**
        - Emergency: Call your local emergency number
        - Crisis Text Line: Text HOME to 741741
        - National Suicide Prevention Lifeline: 988
        """)
        
        # Show API key status
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            st.success("✅ API Key loaded successfully")
        else:
            st.error("❌ API Key not found in .env file")
        
        # Clear chat button
        if st.button("🔄 Clear Conversation"):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.rerun()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation_history = []
        
        # Add welcome message
        welcome_msg = """Hello! I'm here to listen and support you. I understand that everyone goes through difficult times, and I want you to know that your feelings are valid. 

How are you feeling today? You can share anything that's on your mind - I'm here to listen without judgment. 💙"""
        
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Initialize Groq client
    try:
        client = init_groq_client()
    except:
        st.stop()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Share what's on your mind..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Understanding your feelings..."):
                response_stream = analyze_emotion_and_respond(
                    client, 
                    prompt, 
                    st.session_state.conversation_history[-10:]  # Keep last 10 messages for context
                )
                
                if response_stream:
                    # FIXED: Use the parser function with st.write_stream
                    response = st.write_stream(parse_groq_stream(response_stream))
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.conversation_history.append({"role": "assistant", "content": response})
                else:
                    error_msg = "I'm sorry, I'm having trouble responding right now. Please try again."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Add helpful suggestions at the bottom
    st.markdown("---")
    st.markdown("### 🌟 Quick Self-Care Suggestions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🫁 Breathing Exercise"):
            breathing_msg = """Let's try a simple breathing exercise together:

1. **Inhale** slowly through your nose for 4 counts
2. **Hold** your breath for 4 counts  
3. **Exhale** slowly through your mouth for 6 counts
4. **Repeat** this cycle 4-5 times

Focus on the sensation of your breath. You're doing great! 🌸"""
            
            st.session_state.messages.append({"role": "assistant", "content": breathing_msg})
            st.rerun()
    
    with col2:
        if st.button("🧘 Mindfulness Tip"):
            mindfulness_msg = """Here's a quick mindfulness exercise:

**5-4-3-2-1 Grounding Technique:**
- **5** things you can see
- **4** things you can touch  
- **3** things you can hear
- **2** things you can smell
- **1** thing you can taste

This helps bring you back to the present moment. Take your time with each step. 🍃"""
            
            st.session_state.messages.append({"role": "assistant", "content": mindfulness_msg})
            st.rerun()
    
    with col3:
        if st.button("💝 Positive Affirmation"):
            affirmations = [
                "You are stronger than you know and braver than you feel. 💪",
                "Your feelings are valid, and you deserve compassion and understanding. 🤗",
                "Every day is a new opportunity for growth and healing. 🌱",
                "You have overcome challenges before, and you can do it again. ⭐",
                "It's okay to not be okay. Healing takes time, and that's perfectly normal. 💙"
            ]
            
            import random
            affirmation_msg = random.choice(affirmations)
            
            st.session_state.messages.append({"role": "assistant", "content": affirmation_msg})
            st.rerun()

if __name__ == "__main__":
    main()
