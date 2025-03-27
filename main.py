from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI()
load_dotenv()
client.api_base = os.getenv("OPENAI_API_BASE")
client.api_key = os.getenv("OPENAI_API_KEY")
if client.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

def geracao_texto(message, model='auto', temperature=0.4, max_tokens=50, n=1):
    mensagens = [{"role": "user", "content": message}]
    resposta = client.chat.completions.create(
        model=model,
        messages=mensagens,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n
    )
    mensagens.append(resposta.choices[0].message.model_dump(exclude_none=True))
    return mensagens

mensagens = [{"role": "user", "content": "O que é uma maçã em 5 palavras?"}]
resposta = geracao_texto(mensagens[0]['content'])
print(resposta.choices[0].message.content)