import sys
from pathlib import Path

import pandas as pd

# Diretórios de entrada e saída de dados
INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "RNC2026_consolidado.xlsx"

def validate_output():
    print("")
    print("VALIDAÇÃO".center(30, "="))
    print("\nLendo arquivo consolidado de referência...")
    # dtype=str para garantir o dígito 0 à esquerda dos CPFs
    df_referencia = pd.read_excel(OUTPUT_FILE, dtype=str)
    
    print(f"{len(df_referencia)} linhas encontradas.")

    # Busca por todos os arquivos .xlsx no diretório de entrada
    arquivos = sorted(INPUT_DIR.glob("*.xlsx"))
    
    print("\nComparando a referência aos arquivos gerados:")
    # Se você quiser verificar se todas as linhas de cada arquivo constam na referência:
    for arq in arquivos:
        df_atual = pd.read_excel(arq, dtype=str)
        
        # Verificação se todo dado do DataFrame atual existe no DataFrame de referência
        merged = pd.merge(df_atual, df_referencia, how='inner')
        if len(merged) < len(df_atual):
            sys.exit(f"Erro: Há dados no arquivo {arq.name} que não foram encontrados na referência.")
        else:
            print(f"- [OK] {arq.name}")
            
    print("\nValidação concluída com sucesso!")



def main(generate=True, validate=False):
    # Busca por todos os arquivos .xlsx no diretório de entrada
    arquivos = sorted(INPUT_DIR.glob("*.xlsx"))
    
    if not arquivos:
        sys.exit(f"Nenhum arquivo .xlsx encontrado em {INPUT_DIR}")

    # informação sobre os arquivos encontrados
    print(f"{len(arquivos)} arquivo(s) encontrado(s).\n")

    # DataFrame que irá reunir as informações de cada linha
    dfs = []
    # Colunas de referência. Todos os arquivos devem ter exatamente as mesmas colunas
    colunas_ref = None
    # Total de linhas dos arquivos de entrada, para comparação com a planilha de saída
    total_linhas = 0

    for arq in arquivos:
        df = pd.read_excel(arq, dtype=str)
        colunas = list(df.columns)

        if colunas_ref is None:
            # Utiliza as colunas do primeiro arquivo como referência
            colunas_ref = colunas
            print(f"[OK] {arq.name}  —  {len(df)} linhas, {len(colunas)} colunas (referência)")

            # Atualiza o total de linhas encontrado
            total_linhas += len(df)

        # verifica se as colunas do arquivo difere da referência e prepara mensagem de erro
        elif colunas != colunas_ref:
            extras = set(colunas) - set(colunas_ref)
            faltando = set(colunas_ref) - set(colunas)
            sys.exit(
                f"[ERRO] {arq.name}: colunas divergem.\n"
                f"       Extras   : {extras or '—'}\n"
                f"       Faltando : {faltando or '—'}"
            )
        else:
            # Informação sobre o arquivo válido
            print(f"[OK] {arq.name}  —  {len(df)} linhas")
            
            # Atualiza o total de linhas encontrado
            total_linhas += len(df)

        # concatena o DataFrame do arquivo atual à lista de DataFrames
        dfs.append(df)

    print(f"\nTotal de linhas/colunas processadas nos arquivos: {total_linhas} linhas x {len(colunas)} colunas")

    # Concatena todos os DataFrames em um único DataFrame consolidado
    consolidado = pd.concat(dfs, ignore_index=True)
    print(f"Total de linhas/colunas no arquivo consolidado: {len(consolidado)} linhas × {len(consolidado.columns)} colunas")

    if total_linhas == len(consolidado):
        print("Total de linhas OK.")
    else:
        sys.exit("Número de linhas não confere.")

    if len(colunas) == len(consolidado.columns):
        print("Total de colunas OK.")
    else:
        sys.exit("Número de colunas não confere.")

    # Salva o arquivo consolidado em formato Excel no diretório de saída
    if generate:
        OUTPUT_DIR.mkdir(exist_ok=True)
        print("\nCriando arquivo consolidado...")
        consolidado.to_excel(OUTPUT_FILE, index=False)
        print(f"Arquivo salvo em: {OUTPUT_FILE}")

    # Função para validação do arquivo de saída
    if validate:
        validate_output()

if __name__ == "__main__":
    main(generate=True, validate=True)
