import httpx
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HF_TOKEN", "")


async def generate_chat_response(
    messages: List[Dict[str, str]],
    max_tokens: int = 500,
    temperature: float = 0.7
) -> Optional[str]:
    """
    Generate a response from Hugging Face Mistral model.
    
    Args:
        messages: List of messages with role and content
        max_tokens: Maximum tokens in response
        temperature: Randomness of response (0-1)
    
    Returns:
        Generated response text or None if request fails
    """
    if not HF_TOKEN:
        return "Error: HF_TOKEN no está configurada. Por favor, configura la variable de entorno HF_TOKEN."
    
    try:
        # Format messages for the model
        formatted_prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted_prompt += f"[INST] {content} [/INST]"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                HUGGING_FACE_API_URL,
                headers={
                    "Authorization": f"Bearer {HF_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": 0.9,
                        "do_sample": True,
                    }
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                result = data[0]
                if "generated_text" in result:
                    # Extract just the assistant response
                    generated = result["generated_text"]
                    # Remove the prompt from the response
                    if "[/INST]" in generated:
                        response_text = generated.split("[/INST]")[-1].strip()
                        return response_text
                    return generated
            
            return None
    except Exception as e:
        print(f"Error generating chat response: {e}")
        return None


system_prompt = """Eres un asistente de viajes amable y experto. Ayudas a los usuarios a planificar sus viajes, 
responder preguntas sobre destinos, actividades, presupuestos, seguridad de viajes y recomendaciones de viaje.
Sé conciso pero informativo en tus respuestas. Usa emojis ocasionalmente para hacer las conversaciones más amenas.
Siempre ofrece información práctica y útil."""


async def chat_with_travel_assistant(
    user_message: str,
    conversation_history: List[Dict[str, str]] = None
) -> str:
    """
    Chat with travel planning assistant.
    
    Args:
        user_message: User's message
        conversation_history: List of previous messages for context
    
    Returns:
        Assistant's response
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add system instruction and user message
    messages = [
        {"role": "system", "content": system_prompt},
        *conversation_history,
        {"role": "user", "content": user_message}
    ]
    
    response = await generate_chat_response(messages)
    
    if response is None:
        return "Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo."
    
    return response


async def get_travel_recommendation(destination: str, preferences: str = "") -> str:
    """
    Get AI-powered travel recommendations for a destination.
    
    Args:
        destination: Travel destination
        preferences: User preferences
    
    Returns:
        Travel recommendation text
    """
    prompt = f"Dame recomendaciones de viaje para {destination}"
    if preferences:
        prompt += f" considerando estas preferencias: {preferences}"
    
    response = await chat_with_travel_assistant(prompt)
    return response


async def get_budget_advice(destination: str, budget: float, duration: int) -> str:
    """
    Get AI-powered budget advice for a trip.
    
    Args:
        destination: Travel destination
        budget: Total budget in euros
        duration: Trip duration in days
    
    Returns:
        Budget advice text
    """
    prompt = f"""Dime cómo distribuir un presupuesto de €{budget} para un viaje de {duration} días a {destination}.
    Incluye estimaciones para alojamiento, comida, transporte y actividades."""
    
    response = await chat_with_travel_assistant(prompt)
    return response
