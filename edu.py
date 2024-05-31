import streamlit as st
import openai

# Set up the OpenAI API client
api_key = st.secrets["openai"]["api_key"]
openai.api_key = api_key

# Streamlit application
st.title("🤖EduMinds")
st.title("Your personal assistant")

def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content'].strip()

def chat_interface():
    # Initialize session state if not already done
    if 'conversations' not in st.session_state:
        st.session_state.conversations = []

    # Display conversation history
    for user_input, response in st.session_state.conversations:
        st.write(f"🔣 User: {user_input}")
        st.write(f"⚙️ EduMinds: {response}")
        st.markdown('---')

    # User input and Send button
    user_input_key = st.session_state.user_input_count if 'user_input_count' in st.session_state else 0
    user_input = st.text_area(f"🔣 Your message to EduMinds:", key=f"user_input_{user_input_key}")
    send_button = st.button("Send")

    if send_button and user_input:
        # Prepare the message history for the API
        messages = [{"role": "system", "content": "You are EduMinds, a helpful assistant."}]
        for user_msg, bot_msg in st.session_state.conversations:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        
        # Add the new user input to the messages
        messages.append({"role": "user", "content": user_input})

        # Get response from GPT-3.5 Turbo
        response = chat_with_gpt(messages)

        # Update conversation history
        st.session_state.conversations.append((user_input, response))

        # Clear the input field
        st.session_state.user_input_count = user_input_key + 1

        # Rerun the app to update the interface
        st.experimental_rerun()

if __name__ == "__main__":
    chat_interface()
