from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from typing import Optional
from parsers import SaidaFinalParser
from itertools import cycle
import threading
import os, sys, time

console = Console()

def limpar_console():
      if os.name == 'nt':
            os.system('cls')
      else:
            os.system('clear')

def processar_e_carregar(empresa: str, chain):
      mensagem = f"Buscando dados para {empresa}. Isso pode levar alguns segundos..."

      with console.status(Text(mensagem, style="bold cyan")):
            relatorio = chain.invoke({"empresa": empresa})
      
      return relatorio

def carregamento(empresa: str, parar_carregamento: threading.Event):
      mensagem = Text(f"Buscando dados para {empresa}. Isso pode levar alguns segundos...", style="italic cyan")

      indicator_progresso = cycle([
            Text(".  ", style="bold yellow"),
            Text(".. ", style="bold yellow"),
            Text("...", style="bold yellow"),
            Text("   ", style="bold yellow")
      ])

      sys.stdout.write(f"\r{mensagem.plain}  ")
      sys.stdout.flush()

      while not parar_carregamento.is_set():
            texto_completo = Text.assemble(
                  mensagem,
                  " ",
                  next(indicator_progresso)
            )

            sys.stdout.write(f"\r{texto_completo.markup}")
            sys.stdout.flush()
            time.sleep(0.2)
            
      
      sys.stdout.write(f"\r{' ' * (len(mensagem.plain) + 10)}\r") 
      sys.stdout.flush()

def input_de_dados() -> str:
      limpar_console()
      console.print(
            Panel(
                  "Digite o nome de uma empresa de capital aberto brasileira (Ex: Petrobras, Vale, Embraer).",
                  title=Text("INSTRUÇÕES", style="bold yellow"),
                  border_style="green"
            )
      )
      
      entrada_bruta = str(input("Nome da empresa: "))

      if not entrada_bruta:
            return ""
      
      limpar_console()
      return entrada_bruta.strip().title()

def imprimir_relatorio(relatorio: Optional[SaidaFinalParser]):
      limpar_console()
      if not relatorio:
            console.print(
                  Panel("[Bold red] Erro: Falha na Geração do Relatório ou Ticker Não Encontrado."),
                  border_style="red"
            )
            return
      
      if ' - ' in relatorio.titulo:
            partes = relatorio.titulo.split(' - ')
            nome_empresa = ' - '.join(partes[:-1])
            ticker_completo = partes[-1]
      else:
            nome_empresa = relatorio.titulo
            ticker_completo = ""

      titulo = Text.assemble(
            ("RELATÓRIO: ", "bold cyan"),
            (nome_empresa, "bold white"),
            (" - ", "bold white"),
            (ticker_completo, "bold yellow")
    )

      preco_texto = Text.assemble(
            ("PREÇO ATUAL DA AÇÃO: ", "bold yellow"),
            (relatorio.preco_acao, "bold green")
      )

      resumo_empresa = Panel(
            Markdown(relatorio.resumo_empresa),
            title=Text("RESUMO: ", style="bold blue"),
            border_style="cyan"
      )

      noticias = relatorio.resumo_noticias
      noticias_fontes = relatorio.fontes_da_noticia

      noticias_tabela = Table(title="ÚLTIMAS NOTÍCIAS RELEVANTES", border_style="magenta", show_header=False, show_lines=True)
      noticias_tabela.add_column("Índice", style="dim", width=3)
      noticias_tabela.add_column("Noticía e Fonte", style="white")

      if isinstance(noticias, list) and len(noticias) > 0:
            fontes_validas = isinstance(noticias_fontes, list) and len(noticias_fontes) == len(noticias)
            
            for i, noticia in enumerate(noticias, 1):
                  fonte_link = noticias_fontes[i-1] if fontes_validas else "Não Informado"

                  noticia_formatada = Text.assemble(
                        (f"{noticia}\n", "italic"),
                        ("Fonte: ", "bold magenta"),
                        (fonte_link, "link " + fonte_link)
                  )
                  noticias_tabela.add_row(str(i), noticia_formatada)
            
      else:
            noticias_tabela.add_row(
                  "Aviso!",
                  Text("Nenhuma notícia de mercado recente encontrada.", style="yellow")
            )
      
      console.rule(titulo)
      console.print(preco_texto, justify="center")
      console.print(resumo_empresa)
      console.print(noticias_tabela)
      console.rule(style="cyan")