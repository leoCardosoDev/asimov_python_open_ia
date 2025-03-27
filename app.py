import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Carregar variáveis de ambiente do .env
load_dotenv()

# Inicializar o cliente OpenAI
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
if client.api_key is None:
    st.error("Variável de ambiente OPENAI_API_KEY não está definida.")
    st.stop()

def geracao_texto(message, model='auto', temperature=0.4, max_tokens=50):
    """Simula streaming da resposta da API da OpenAI."""
    # Realiza a requisição para a API
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Simulação de streaming de texto
    content = response.choices[0].message.content
    for char in content:
        yield char
        time.sleep(0.05)  # Delay para simular streaming

# Título do aplicativo Streamlit
st.title("Gerador de Texto com OpenAI")

# Área de texto para input do usuário
user_input = st.text_area("Digite uma mensagem para o gerador de texto:")

# Botão para gerar a resposta
if st.button("Gerar Resposta"):
    if user_input:
        response_placeholder = st.empty()
        response_text = ""
        
        # Receber texto simulado em partes
        for char in geracao_texto(user_input):
            response_text += char
            response_placeholder.markdown(response_text, unsafe_allow_html=True)

        st.success("Resposta obtida com sucesso!")
    else:
        st.warning("Por favor, insira uma mensagem.")