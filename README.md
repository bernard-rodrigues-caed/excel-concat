# Excel Concat

Uma aplicação para concatenação e validação dos dados concatenados.

## Instalação direta

Para quem só tem o Python instalado (sem precisar criar o ambiente virtual ou instalar dependências na mão), basta dar duplo clique em `build.bat` — ele cria o `.venv`, instala as dependências e gera o executável.

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

## Interface gráfica

Também é possível rodar a aplicação com uma interface gráfica (Tkinter, já incluso no Python):

```bash
python ./gui.py
```

Escolha a origem dos arquivos `.xlsx`:
- **Pasta `input/`** (padrão) — mesmo comportamento da linha de comando;
- **Selecionar arquivos manualmente** — escolha arquivos de qualquer pasta pelo diálogo do sistema.

Depois clique em "Executar". O andamento e eventuais erros aparecem na área de log da janela.

## Gerando o executável (PyInstaller)

Com o ambiente virtual já ativado:

```bash
python -m PyInstaller --onedir --windowed --noconfirm --name RNC_Concat gui.py
```

O executável e seus arquivos de suporte são gerados em `dist/RNC_Concat/`. Para distribuir, copie a pasta inteira (não só o `.exe`) e crie as pastas `input/` e `output/` ao lado dele.