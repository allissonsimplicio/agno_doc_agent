# Agno Doc Agent

Este é um sistema multi-agente inteligente projetado para analisar, refatorar e atualizar a documentação de projetos de software.

O sistema utiliza uma arquitetura de múltiplos agentes para dividir as tarefas de pesquisa, análise e escrita, garantindo um processo robusto e modular.

---

## Funcionalidades

- **Análise de Projetos Externos:** Pode analisar qualquer projeto de software local fornecendo o caminho para o diretório.
- **Priorização Inteligente:** Identifica e prioriza arquivos `README.md` e arquivos modificados recentemente como as fontes de verdade mais prováveis.
- **Detecção de Inconsistências:** O Agente Analista compara o código-fonte com a documentação para encontrar funcionalidades não documentadas ou documentação obsoleta.
- **Geração de Documentação:** O Agente Escritor reescreve a documentação do zero em Português-BR, criando um `README` unificado e coeso.
- **Limpeza Automática:** Após gerar a nova documentação, o sistema oferece a opção de arquivar os arquivos de documentação antigos em um diretório `docs.old`.

## Arquitetura dos Agentes

1.  **Agente Pesquisador (Researcher):** Vasculha o diretório do projeto em busca de arquivos de código e documentação, extraindo metadados como data de modificação.
2.  **Agente Analista (Analyzer):** Recebe todos os arquivos e utiliza um modelo de linguagem para identificar discrepâncias, lacunas e inconsistências.
3.  **Agente Escritor (Writer):** Recebe as discrepâncias e o conteúdo original para gerar uma documentação nova, completa e em Português-BR.
4.  **Agente Orquestrador (Orchestrator):** Gerencia todo o fluxo de trabalho, desde a entrada do usuário até a chamada de cada agente na ordem correta e a finalização do processo.

---

## Como Usar

### 1. Pré-requisitos

- Python 3.8+
- Uma chave de API da Anthropic (para o modelo Claude 3 Sonnet)

### 2. Configuração

1.  **Clone o repositório (se aplicável):**
    ```bash
    git clone <url_do_repositorio>
    cd agno_doc_agent
    ```

2.  **Crie o arquivo de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave da API:
    ```
    ANTHROPIC_API_KEY="sua_chave_aqui"
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Execução

Para iniciar a análise, execute o `run.py` com o comando `analyze`.

```bash
python run.py analyze
```

O sistema irá solicitar interativamente que você insira o caminho para o diretório do projeto que deseja analisar.

Alternativamente, você pode fornecer o caminho como um argumento:

```bash
python run.py analyze "C:\caminho\para\seu\projeto"
```
