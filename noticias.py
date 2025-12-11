from langchain_tavily import TavilySearch
from config import TAVILY_API_KEY

def buscar_noticias(empresa: str):
      pesquisa = TavilySearch(
            tavily_api_key = TAVILY_API_KEY,
            max_results = 3,
            topic="news"
      )

      try:
            query = f"notícias corporativas financeiras '{empresa}' resultados ações -oferta -promoção"
            resultados = pesquisa.invoke({"query": query})

            if not resultados:
                  return "Nenhuma noticia recente encontrada."
            
            lista_noticias = list()
        
            if isinstance(resultados, dict) and 'results' in resultados:
                  lista_noticias = resultados['results']
            elif isinstance(resultados, list):
                  lista_noticias = resultados
            
            if not lista_noticias:
                  return "Nenhuma notícia relevante encontrada."

            texto_final = list()
        
            for i, noticia in enumerate(lista_noticias, 1):
                  titulo = noticia.get('title', 'Sem título')
                  data = noticia.get('published_date', '')
                  link = noticia.get('url', '#')
                  conteudo = noticia.get('content', '').replace('\n', ' ')

                  texto_formatado = (
                  f"{i}. {titulo}\n"
                  f"Data: {data}\n"
                  f"Resumo: {conteudo}\n"
                  f" Link: {link}"
                  )

                  texto_final.append(texto_formatado)

            return "\n\n".join(texto_final)


      except Exception as e:
            return f"Erro na busca de noticias: {e}"
      
