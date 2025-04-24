import json
import yfinance
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
client = openai.Client()

def retorna_cotacao_acao_historica(ticker, periodo='1mo'):
    ticker = ticker.replace('.SA', '')
    ticker_obj = yfinance.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period=periodo)['Close']
    hist.index = hist.index.strftime('%Y-%m-%d')
    hist = round(hist, 2)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    return hist.to_json()

tools = [
  {
    'type': 'function',
    'function': {
      'name': 'retorna_cotacao_acao_historica',
      'description': 'Retorna a cotação diária histórica para uma ação da bovespa',
      'parameters': {
        'type': 'object',
        'properties': {
          'ticker': {
            'type':'string',
            'description': 'O ticker da ação. Exemplo: "ABEV3" para ambev, "PETR4" para petrobras, etc'
          },
          'periodo': {
            'type': 'string',
            'description': 'O período desejado. Pode ser 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max',
            'enum': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
          }
        }
      }
    }
  }
]

funcoes_disponiveis = {
    'retorna_cotacao_acao_historica': retorna_cotacao_acao_historica
}

def gera_texto(mensagens):
    resposta = client.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=mensagens,
        tools=tools,
        tool_choice='auto'
    )
    tool_calls = resposta.choices[0].message.tool_calls
    if tool_calls:
        mensagens.append(resposta.choices[0].message)
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            function_to_call = funcoes_disponiveis[func_name]
            func_args = json.loads(tool_call.function.arguments)
            func_return = function_to_call(**func_args)
            mensagens.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': func_name,
                'content': func_return
            })
        segunda_resposta = client.chat.completions.create(
            model='gpt-3.5-turbo-1106',
            messages=mensagens
        )
        mensagens.append(segunda_resposta.choices[0].message)
        print(f'Assistent: {mensagens[-1].content}')
        return mensagens

if __name__ == '__main__':
  print('Bem vindo ao GPT Financeiro!')
  while True:
    input_usuario = input('Você: ')
    mensagens = [{'role': 'user', 'content': input_usuario}]
    mensagens = gera_texto(mensagens)
    if input_usuario == 'sair':
      break