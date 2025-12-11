from pydantic import BaseModel, Field
from typing import List

class TickerOutput(BaseModel):
      ticker: str = Field(description="O código da ação na B3, estritamente no formato TICKER.SA (ex: PETR4.SA)")

class SaidaFinalParser(BaseModel):
      titulo: str = Field(
            description="Nome da empresa e Ticker (ex: Petrobras - PETR4.SA)"
      )
      preco_acao: str = Field(
            description="Preço atual da ação formatado com a moeda (ex: R$ 35,50 ou US$ 120.00)"
      )
      resumo_empresa: str = Field(
            description="Texto contendo setor, breve histórico e principais produtos/serviços"
      )
      resumo_noticias: List[str] = Field( 
            description="Lista com os resumos das notícias em formato de texto"
      )
      fontes_da_noticia: List[str] = Field( 
            description="Lista com as respectivas fontes presentes nas noticias."
      )