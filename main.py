from extrair_ticker import extrair_ticker
from extrair_dados_finance import resumo_empresa
from noticias import buscar_noticias
from processamento_final import gerar_relatorio_final
from terminal import console, processar_e_carregar, input_de_dados, imprimir_relatorio, limpar_console, Text
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from operator import itemgetter

chain_pipeline_completa = (
      RunnablePassthrough.assign(
            ticker=itemgetter("empresa") | RunnableLambda(extrair_ticker)
      )
      | RunnableParallel({
            "dados_financeiros": itemgetter("ticker") | RunnableLambda(resumo_empresa),
            "noticias": itemgetter("empresa") | RunnableLambda(buscar_noticias)
      })
      | RunnableLambda(lambda x: gerar_relatorio_final(x["dados_financeiros"], x["noticias"]))
)

if __name__ == "__main__":
    
    try:
        nome_da_empresa = input_de_dados()
        if not nome_da_empresa:
            console.print(Text("\nAnálise abortada pelo usuário.", style="bold red"))
            exit()

        relatorio = processar_e_carregar(nome_da_empresa, chain_pipeline_completa)

        imprimir_relatorio(relatorio=relatorio)

    except Exception as e:
        limpar_console()
        console.print(f"[bold red]Erro no pipeline:[/bold red] {e}")
