from langchain_core.prompts import PromptTemplate
from parsers import SaidaFinalParser
from langchain_core.output_parsers import PydanticOutputParser
from config import LLM

parser_final = PydanticOutputParser(pydantic_object=SaidaFinalParser)

template_final = PromptTemplate(template="""
Você é um Analista de Investment Banking Sênior.
Sua tarefa é compilar um relatório executivo em PORTUGUÊS DO BRASIL com base nos dados brutos abaixo.

DADOS FINANCEIROS:
{dados_financeiros}

NOTÍCIAS RECENTES:
{noticias}
                                
INSTRUÇÕES DE FORMATO:
{format_instructions}

REQUISITOS DO RELATÓRIO:
1. titulo: Nome da Empresa + Ticker
2. preco acao: Extraia o valor numérico dos dados financeiros e formate com o símbolo da moeda.
3. Resumo Corporativo: Em UM parágrafo conciso (máximo 50 palavras), cite o setor, o que a empresa faz e seus principais produtos. Seja direto.
4. Destaques Recentes: Analise o bloco NOTÍCIAS RECENTES e você deve obrigatoriamente resumir de 2 a 3 notícias RELEVANTES. Se houver menos de 3 relevantes, use todas as notícias que você considera pertinentes, mas tente alcançar o mínimo de 2 resumos. Resuma em bullet points com no máximo 3 linhas cada.
5. fontes da noticia: Para cada resumo de notícia gerado no Destaques Recentes (ponto 4), você deve retornar na mesma ordem a URL COMPLETA que você encontrou junto à notícia bruta. É obrigatório que a lista de fontes tenha o mesmo número de itens que a lista de destaques recentes.
                                
NÃO invente informações. Se o dado não estiver acima, diga "Não informado".
Gere o relatório com formatação limpa e profissional.

RELATÓRIO FINAL:
""", input_variables=["dados_financeiros", "noticias"], partial_variables={"format_instructions": parser_final.get_format_instructions()})

chain_final = template_final | LLM | parser_final

def gerar_relatorio_final(dados, noticias):
      if not dados or "Erro" in dados:
        return None
      
      return chain_final.invoke({"dados_financeiros": dados, "noticias": noticias})