from typing import AsyncIterator, Optional
import httpx
import json
from pydantic_ai.models.ollama import OllamaModel
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

class StreamingOllamaModel(OllamaModel):
    """Custom OllamaModel that adds direct streaming support."""
    
    async def stream_chat(
        self,
        prompt: str,
        message_history: Optional[list[dict]] = None,
    ) -> AsyncIterator[str]:
        """Stream chat responses directly from Ollama."""
        # Format conversation history
        conversation = ""
        if message_history:
            for message in message_history:
                role = message["role"]
                content = message["content"]
                conversation += f"{role}: {content}\n"
        
        # Add current prompt
        conversation += f"user: {prompt}\nassistant: "
        
        # Prepare request
        url = "http://localhost:11434/api/generate"
        data = {
            "model": self.model_name,
            "prompt": conversation,
            "stream": True
        }
        
        # Stream the response
        async with httpx.AsyncClient() as client:
            async with client.stream('POST', url, json=data, timeout=None) as r:
                async for line in r.aiter_lines():
                    if line:
                        response_data = json.loads(line)
                        if "response" in response_data:
                            yield response_data["response"]

class OllamaAgent:
    def __init__(
        self,
        model_name: str = "llama2",
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
        use_direct_streaming: bool = False
    ):
        """Initialize an Ollama agent with custom configuration.
        
        Args:
            model_name: Name of the Ollama model to use
            base_url: Base URL for the Ollama API
            api_key: API key (not required for Ollama, defaults to "ollama")
            use_direct_streaming: If True, uses direct Ollama streaming instead of OpenAI compatibility
        """
        if use_direct_streaming:
            self.model = StreamingOllamaModel(model_name)
            self.agent = Agent(self.model)
            self._use_direct = True
        else:
            self.client = AsyncOpenAI(
                base_url=base_url,
                api_key=api_key
            )
            self.model = OpenAIModel(model_name, openai_client=self.client)
            self.agent = Agent(self.model)
            self._use_direct = False
        
    async def stream_response(
        self,
        prompt: str,
        conversation_history: Optional[list[dict[str, str]]] = None
    ) -> AsyncIterator[str]:
        """Stream a response from the agent with optional conversation history.
        
        Args:
            prompt: The current user prompt
            conversation_history: Optional list of previous messages in the format
                                [{"role": "user"|"assistant", "content": str}]
        
        Yields:
            Chunks of the response as they become available
        """
        if self._use_direct:
            async for chunk in self.model.stream_chat(prompt, conversation_history):
                yield chunk
        else:
            # Build conversation context if history is provided
            if conversation_history:
                conversation = ""
                for msg in conversation_history:
                    role_prefix = "User: " if msg["role"] == "user" else "Assistant: "
                    conversation += f"{role_prefix}{msg['content']}\n"
                conversation += f"User: {prompt}\nAssistant: "
            else:
                conversation = f"User: {prompt}\nAssistant: "
                
            async with self.agent.run_stream(conversation) as result:
                full_response = ""
                async for chunk in result.stream():
                    if chunk and len(chunk) > len(full_response):
                        new_content = chunk[len(full_response):]
                        full_response += new_content
                        yield new_content 