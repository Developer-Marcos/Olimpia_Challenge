import yfinance as yf

def resumo_empresa(ticker: str) -> dict:
      if not ticker or "NAO_ENCONTRADO" in ticker:
            return None
      
      try:
            acao = yf.Ticker(ticker).info

            if 'longName' not in acao or acao['longName'] is None:
                  print(f"Aviso: Ticker '{ticker}' não retornou dados válidos no Yahoo Finance.")
                  return None
            
            preco = acao.get('currentPrice') or acao.get('regularMarketPrice') or "N/A"

            dados = {
                  "Ticker": ticker,
                  "Nome": acao.get('longName', "Nome Indisponível"),
                  "Setor": acao.get('sector', "Não informado"),
                  "Industria": acao.get('industry', "Não informado"),
                  "Resumo": acao.get('longBusinessSummary', "Sem resumo"),
                  "Site": acao.get('website', "Site não encontrado"),
                  "Preco_Atual": preco,
                  "Moeda": acao.get('currency', "BRL")
            }
            return dados
      
      except Exception as e:
            print(f"Erro ao buscar dados para {ticker}: {e}")
            return None