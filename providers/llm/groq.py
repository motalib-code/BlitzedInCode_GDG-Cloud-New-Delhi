"""
Groq LLM provider.
https://groq.com/
"""
import asyncio
import warnings
from typing import Optional, Dict, Any, List

from .base import BaseLLMProvider
from .config import get_config


class GroqProvider(BaseLLMProvider):
    """
    Groq API-based LLM provider.
    Supports Llama 3 and other Groq-hosted models with fast inference.
    """
    
    provider_name = "groq"
    is_local = False
    max_concurrent = 10
    supports_streaming = True
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Groq provider.
        
        Args:
            config: Optional configuration dictionary. Supported keys:
                - api_key: Groq API key (overrides env.config)
                - model: Model to use (default: 'llama-3.1-8b-instant')
                - temperature: Temperature for sampling (default: 0)
                - max_tokens: Maximum tokens to generate (default: 1000)
                - top_p: Top-p sampling parameter (default: 0.95)
                - max_concurrent: Max concurrent requests (default: 10)
        """
        super().__init__(config)
        
        # Set defaults
        self.config.setdefault('model', 'llama-3.1-8b-instant')
        self.config.setdefault('temperature', 0)
        self.config.setdefault('max_tokens', 1000)
        self.config.setdefault('top_p', 0.95)
        
        if 'max_concurrent' in self.config:
            self.max_concurrent = self.config['max_concurrent']
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
    
    def _validate_config(self) -> None:
        """Validate Groq configuration and API key."""
        llm_config = get_config()
        
        # Check for API key in config or global config
        api_key = self.config.get('api_key') or llm_config.get_api_key('groq')
        
        if not api_key:
            warnings.warn(
                "Groq API key not found. Please set GROQ_API_KEY in env.config "
                "or provide 'api_key' in provider config.",
                UserWarning
            )
        else:
            self.config['api_key'] = api_key
    
    async def generate_async(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate text using Groq API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt (prepended to user prompt)
            **kwargs: Additional Groq parameters
            
        Returns:
            Generated text
            
        Raises:
            ValueError: If API key is missing or generation fails
        """
        api_key = self.config.get('api_key')
        if not api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY in env.config "
                "or provide 'api_key' in config."
            )
        
        try:
            # Import LangChain Groq
            from langchain_groq import ChatGroq
            
            # Initialize ChatGroq
            llm = ChatGroq(
                model_name=self.config.get('model', 'llama-3.1-8b-instant'),
                groq_api_key=api_key,
                temperature=kwargs.get('temperature', self.config.get('temperature', 0)),
                max_tokens=kwargs.get('max_tokens', self.config.get('max_tokens', 1000)),
                top_p=kwargs.get('top_p', self.config.get('top_p', 0.95)),
            )
            
            # Combine system prompt with user prompt if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Run generation in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: llm.invoke(full_prompt)
            )
            
            return response.content
            
        except ImportError:
            raise ImportError(
                "LangChain Groq not installed. Install with: pip install langchain-groq"
            )
        except Exception as e:
            raise ValueError(f"Groq generation failed: {str(e)}")
    
    async def chat_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        Generate chat completion using Groq API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional Groq parameters
            
        Returns:
            Generated response
        """
        api_key = self.config.get('api_key')
        if not api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY in env.config "
                "or provide 'api_key' in config."
            )
        
        try:
            from langchain_groq import ChatGroq
            from langchain.schema import HumanMessage, AIMessage, SystemMessage
            
            # Initialize ChatGroq
            llm = ChatGroq(
                model_name=self.config.get('model', 'llama-3.1-8b-instant'),
                groq_api_key=api_key,
                temperature=kwargs.get('temperature', self.config.get('temperature', 0)),
                max_tokens=kwargs.get('max_tokens', self.config.get('max_tokens', 1000)),
                top_p=kwargs.get('top_p', self.config.get('top_p', 0.95)),
            )
            
            # Convert messages to LangChain format
            langchain_messages = []
            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                
                if role == 'system':
                    langchain_messages.append(SystemMessage(content=content))
                elif role == 'user':
                    langchain_messages.append(HumanMessage(content=content))
                elif role == 'assistant':
                    langchain_messages.append(AIMessage(content=content))
            
            # Run chat in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: llm.invoke(langchain_messages)
            )
            
            return response.content
            
        except ImportError:
            raise ImportError(
                "LangChain Groq not installed. Install with: pip install langchain-groq"
            )
        except Exception as e:
            raise ValueError(f"Groq chat generation failed: {str(e)}")
