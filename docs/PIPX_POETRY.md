# pipx e Poetry — Guia Completo

## O problema que tudo isso resolve

O Linux usa o Python internamente para várias tarefas do sistema. Se você instalar pacotes livremente via `pip` no Python global, pode sobrescrever uma biblioteca que o sistema depende e quebrar coisas.

Por isso, em versões recentes do Python (3.12+) no Debian/Ubuntu, o `pip install` direto é bloqueado com o erro `externally-managed-environment`.

A solução é nunca tocar no Python do sistema e usar ferramentas de isolamento.

---

## pip vs pipx — qual a diferença?

| | pip | pipx |
|---|---|---|
| Para quê | bibliotecas que seu código importa | ferramentas de linha de comando |
| Isolamento | não (por padrão) | sim (cada ferramenta tem seu próprio venv) |
| Exemplo de uso | `import requests` no código | `poetry install` no terminal |

**Regra de ouro:**
- Vai fazer `import` no código? → `pip` dentro de um venv
- Vai rodar como comando no terminal? → `pipx`

---

## O que é pipx?

O pipx instala ferramentas CLI (comandos de terminal) em ambientes virtuais isolados, mas deixa os comandos disponíveis globalmente no terminal.

**Onde as coisas ficam:**

```
~/.local/pipx/venvs/
├── poetry/        → venv isolado do Poetry
├── black/         → venv isolado do Black
└── httpie/        → venv isolado do HTTPie

~/.local/bin/
├── poetry         → comando disponível no terminal
├── black
└── httpie
```

O pipx cria um venv real para cada ferramenta (igual ao `python -m venv`), usando o Python do sistema como base — mas sem instalar nada dentro do Python do sistema.

**Instalando o pipx:**

```bash
sudo apt install pipx
pipx ensurepath
```

O `ensurepath` adiciona `~/.local/bin` ao PATH, para o terminal conseguir achar os comandos instalados pelo pipx. Depois disso, abra um novo terminal.

> **PATH** é uma variável do sistema que diz ao terminal onde procurar os comandos. Sem isso, você digita `poetry` e o terminal não sabe onde está esse comando.

---

## O que é Poetry?

O Poetry é um gerenciador de projetos e dependências Python. Ele substitui o uso manual de `venv` + `pip`, automatizando tudo.

**Instalando via pipx:**

```bash
pipx install poetry
```

---

## Como o Poetry funciona

### O arquivo pyproject.toml

Toda vez que você inicia um projeto com Poetry, ele cria um arquivo chamado `pyproject.toml`. Esse arquivo é o coração do projeto — ele registra:

- O nome e versão do projeto
- Qual versão do Python é necessária
- Todas as dependências instaladas

**Sem esse arquivo, o Poetry não sabe que a pasta é um projeto.** Por isso você sempre precisa iniciar antes de instalar qualquer coisa.

### Criando um projeto

```bash
# opção 1 — cria uma pasta nova com estrutura pronta
poetry new meu-projeto

# opção 2 — inicializa um projeto numa pasta que já existe
cd meu-projeto
poetry init
```

### Gerenciando versões do Python

O Poetry tem um gerenciador de versões do Python embutido:

```bash
# instala o Python 3.14 gerenciado pelo Poetry
poetry python install 3.14

# define qual Python o projeto atual vai usar
poetry env use 3.14
```

O `env use` só define a configuração. O ambiente virtual é criado de fato quando você instala dependências.

Você pode usar tanto o Python do sistema quanto os instalados pelo Poetry:

```bash
poetry env use 3.12   # usa qualquer Python 3.12 encontrado
poetry env use /usr/bin/python3.12   # força um caminho específico
```

### Instalando dependências

```bash
# instala uma lib e registra no pyproject.toml
poetry add fastapi

# instala com extras opcionais
poetry add 'fastapi[standard]'

# instala dependência só para desenvolvimento (testes, linters etc)
poetry add --group dev pytest
```

### O venv do projeto

O Poetry cria um venv isolado para cada projeto. Por padrão fica em:

```
~/.cache/pypoetry/virtualenvs/
```

Mas é recomendado configurar para ficar dentro do projeto:

```bash
poetry config virtualenvs.in-project true
```

Assim o venv fica em `.venv/` dentro da pasta do projeto, mais fácil de visualizar.

### Ativando o ambiente virtual

```bash
# Poetry 1.x (pode estar desatualizado)
poetry shell

# Poetry 2.x em diante
source $(poetry env info --path)/bin/activate
```

Quando ativado, o terminal mostra o nome do ambiente:

```
(meu-projeto-py3.12) davi@notebook:~/estudos/meu-projeto$
```

Para sair:

```bash
deactivate
```

### Rodando comandos sem ativar o ambiente

Você não precisa ativar o venv para rodar comandos do projeto:

```bash
poetry run python arquivo.py
poetry run uvicorn main:app --reload
poetry run pytest
```

O `poetry run` executa o comando dentro do venv automaticamente.

---

## Dois venvs — entendendo a relação pipx + Poetry

Quando você usa Poetry instalado via pipx, existem dois venvs separados:

```
~/.local/pipx/venvs/poetry/          → venv do pipx, só para rodar o Poetry em si
~/estudos/meu-projeto/.venv/          → venv do Poetry, para o seu projeto
```

O primeiro é transparente — você nunca mexe nele. O segundo é onde ficam o FastAPI, uvicorn e tudo que o projeto precisa.

---

## O arquivo poetry.lock

Quando você instala dependências, o Poetry cria também um `poetry.lock`. Esse arquivo registra as versões **exatas** de tudo que foi instalado, incluindo dependências das dependências.

**Para projetos de aplicação (APIs, sistemas):** commite o `poetry.lock` no git. Assim todo mundo que clonar o projeto instala exatamente as mesmas versões.

**Para bibliotecas:** ignore o `poetry.lock` no git, pois quem usar sua lib vai resolver as versões no próprio projeto.

Para instalar exatamente o que está no lock:

```bash
poetry install
```

---

## Fluxo completo de um projeto novo

```bash
# 1. instalar pipx (uma vez só na máquina)
sudo apt install pipx
pipx ensurepath
# abrir novo terminal

# 2. instalar Poetry (uma vez só na máquina)
pipx install poetry

# 3. configurar venv dentro do projeto (uma vez só na máquina)
poetry config virtualenvs.in-project true

# 4. instalar a versão do Python desejada (se necessário)
poetry python install 3.12

# 5. criar o projeto
poetry new meu-projeto
cd meu-projeto

# 6. definir o Python do projeto
poetry env use 3.12

# 7. instalar dependências
poetry add fastapi
poetry add --group dev pytest

# 8. ativar o ambiente e rodar
source $(poetry env info --path)/bin/activate
uvicorn main:app --reload
```

---

## .gitignore recomendado

```gitignore
# Ambiente virtual
.venv/

# Python
__pycache__/
*.py[cod]
*.pyo

# Testes
.pytest_cache/
htmlcov/
.coverage

# Variáveis de ambiente
.env
.env.*

# IDEs
.vscode/
.idea/

# SO
.DS_Store
Thumbs.db
```

> Lembre: **não ignore o `poetry.lock`** em projetos de aplicação.

---

## Dúvidas comuns

**Posso ter duas versões do Poetry instaladas?**
Não via pipx. Mas raramente é necessário — o Poetry é compatível com projetos de diferentes versões do Python e diferentes dependências.

**O pipx consome muita memória?**
Não. Os venvs ficam parados em disco e só consomem recursos quando você executa a ferramenta.

**Posso importar libs instaladas via pipx no meu código?**
Não. O pipx é só para ferramentas CLI. Libs que você vai importar no código precisam ser instaladas via `poetry add` dentro do projeto.

**O que é `poetry install` sem nenhum argumento?**
Instala todas as dependências listadas no `pyproject.toml` e `poetry.lock`. Útil quando você clona um projeto existente.

**Diferença entre `poetry add` e `poetry install`?**
- `poetry add` → adiciona uma nova dependência ao projeto
- `poetry install` → instala o que já está registrado no `pyproject.toml`