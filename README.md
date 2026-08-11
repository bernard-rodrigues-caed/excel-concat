# Excel Concat

Uma aplicação para concatenação e validação dos dados concatenados.

## Ambiente virtual


```bash
python -m venv .venv
```

- Windows

```bash
.venv\Scripts\activate
```

- Linux/Mac

```bash
source .venv/bin/activate
```

## Instalação das dependências

```bash
pip install -r requirements.txt
```

## Rodando a aplicação

Para sucesso da aplicação é fundamental que os arquivos Excel de entrada (em `input/`) possuam cabeçalhos de mesmo tamanho e nomes.

- Insira todos os arquivos `.xlsx` na pasta `input/`;
- Rode o script:
```bash
python ./excel_concat.py
```

## Output e Validações

O arquivo consolidado será gerado dentro da pasta `output/` e as validações irão garantir que todos os dados encontrados nos arquivos de entrada estão no arquivo de saída.