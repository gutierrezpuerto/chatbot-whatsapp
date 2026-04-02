""" originalmente creado por Enrique Martínez, 2024-06-17
    actualizado por Enrique Martínez, 2024-06-17 verificar esta info
from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class Message(BaseModel):
    texto: str


@app.get("/")
def home():
    return {"mensaje": "Chatbot activo"}


@app.post("/chat")
def chat(message: Message):
    user_text = message.texto

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "Sos un vendedor experto en desarrollo web, IA, chatbot y soluciones informáticas."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.output[0].content[0].text

    except Exception as e:
        print("ERROR:", e)
        reply = "Error en el sistema. Intentalo más tarde."

    return {
        "usuario": user_text,
        "respuesta": reply
    }


@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    user_text = data.get("Body")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "Sos un vendedor experto en desarrollo web e IA."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.output[0].content[0].text

    except Exception as e:
        print("ERROR:", e)
        reply = "Estoy en mantenimiento ahora mismo, por favor intenta más tarde."

    twilio_response = f"""
"""<Response>
    <Message>{reply}</Message>
</Response>


    return Response(content=twilio_response, media_type="application/xml")"""

from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()


@app.get("/")
def home():
    return {"mensaje": "Chatbot activo"}


@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.form()

    # Mensaje que envía el usuario
    user_text = data.get("Body") or ""

    print("Mensaje recibido:", user_text)

    # Respuesta simple (sin IA)
    if "hola" in user_text.lower():
        reply = "¡Hola! ¿Que tál? ¿En qué puedo ayudarte hoy? Soy tu asistente virtual, un chatbot desarrollado por Nosotros."
    elif "precio" in user_text.lower():
        reply = "Nuestros precios varían según el proyecto. ¿Buscas web o chatbot?"
    elif "web" in user_text.lower():
        reply = "Desarrollamos páginas web modernas que agilizan tus ventas y mejoran tu presencia online. Estas son landing pages, tiendas onlines, etc.    "
    elif "chatbot" in user_text.lower():
         reply = "Creamos chatbots personalizados que mejoran la atención del cliente y aumentan tus ventas. Pueden ser con IA o sin IA, dime y te explico un poco más."
    elif "con ia" in user_text.lower():
        reply = "Nuestros chatbots con IA utilizan tecnología avanzada para ofrecer respuestas inteligentes y personalizadas, mejorando la experiencia del cliente y aumentando la eficiencia de tus ventas."
    elif "sin ia" in user_text.lower():
        reply = "Nuestros chatbots sin IA son soluciones simples y efectivas para responder preguntas frecuentes, guiar a los clientes y mejorar del atención al cliente sin necesidad de inteligencia artificial."     
    elif "gracias" in user_text.lower():
        reply = "¡De nada! Si tienes más preguntas, no dudes en preguntar."
    else:
        reply = "Lo siento, no entendí tu mensaje. ¿Podrías reformularlo incorpotando palabras clave como 'precio', 'web' o 'chatbot'?"
        
    # Respuesta en formato Twilio (XML)
    twilio_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>
"""

    return Response(content=twilio_response, media_type="application/xml")