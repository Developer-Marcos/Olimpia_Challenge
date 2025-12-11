from config import LLM_TICKET
from parsers import TickerOutput
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

ticker_parser = PydanticOutputParser(pydantic_object=TickerOutput)

template_ticker = PromptTemplate(template="""
Você é um especialista em mercado financeiro brasileiro (B3).
Sua tarefa é encontrar o Ticker (código) da empresa solicitada e retornar um JSON.

Regras de Decisão:
1. Empresas Brasileiras: Retorne o código mais líquido (final 3 ou 4).
2. Empresas Estrangeiras: Retorne o código do BDR (geralmente final 34).
3. Formato: O código DEVE terminar em ".SA".

INSTRUÇÕES DE FORMATO:
{format_instructions}

EXEMPLOS (Siga estritamente este padrão):
- Entrada: "Petrobras"
  Saída: {{"ticker": "PETR4.SA"}}

- Entrada: "Apple"
  Saída: {{"ticker": "AAPL34.SA"}}

- Entrada: "Nvidia"
  Saída: {{"ticker": "NVDC34.SA"}}
                                 
- Entrada: "Magazine Luiza" / "Magalu"
  Saída: {{"ticker": "MGLU3.SA"}}
                                 
- Entrada: "Meta" / "Facebook"
  Saída: {{"ticker": "M1TA34.SA"}}

- Entrada: "Padaria do Zé"
  Saída: {{"ticker": "NAO_ENCONTRADO"}}

IMPORTANTE: 
- NÃO use blocos de código markdown (como ```json). 
- Retorne APENAS o JSON bruto.

Empresa solicitada: {empresa}
Saída:
""",
input_variables=["empresa"],
partial_variables={"format_instructions": ticker_parser.get_format_instructions()})

chain_extrair_ticker = template_ticker | LLM_TICKET | ticker_parser

def extrair_ticker(empresa: str) -> str:
      resposta = chain_extrair_ticker.invoke({"empresa": empresa})
      return resposta.ticker
