import streamlit as st
import asyncio
from .agent import OllamaAgent

def create_chat_app(agent: OllamaAgent):
    """Create a Streamlit chat interface using the provided OllamaAgent.
    
    Args:
        agent: An initialized OllamaAgent instance
    """
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What's on your mind?"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            async def get_response():
                full_response = ""
                async for chunk in agent.stream_response(
                    prompt,
                    conversation_history=st.session_state.messages[:-1]  # Exclude current prompt
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                return full_response
                
            # Run the async function
            full_response = asyncio.run(get_response())
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response}) 