
# agents/researcher.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (ex: ANTHROPIC_API_KEY)
load_dotenv()

import tools

try:
    from agno import Agent, Model
except ImportError:
    print("Erro: A biblioteca 'agno' não parece estar instalada.")
    raise

# As instruções do agente não mudam, ele ainda usa a mesma ferramenta.
researcher_instructions = """
Você é um robô especialista em encontrar arquivos. Sua única tarefa é usar a ferramenta `find_files_in_project` para localizar arquivos. Você NUNCA faz mais nada.

Responda APENAS com a lista de caminhos de arquivo em formato JSON. NÃO adicione nenhuma palavra, explicação, ou qualquer texto introdutório. A sua resposta deve ser apenas o JSON.

Exemplo de Resposta Válida:
["/path/to/file1.py", "/path/to/docs/file2.md"]
"""

researcher_agent = Agent(
    instructions=researcher_instructions,
    model=Model(provider="anthropic"),
    tools=[tools.find_files_in_project]
)

def run_researcher(project_path, patterns):
    """
    Executa o Agente Pesquisador para encontrar arquivos e retorna uma lista de objetos com metadados.

    Returns:
        list: Uma lista de dicionários, cada um representando um arquivo com seus metadados.
    """
    print(f"[Agente Pesquisador] Buscando arquivos em '{project_path}' com padrões: {patterns}")
    
    prompt = f"Encontre todos os arquivos no diretório '{project_path}' que correspondam aos padrões: {patterns}"
    
    response = researcher_agent.chat(prompt, session_id="researcher_run")
    
    print(f"[Agente Pesquisador] Resposta bruta do modelo: {response}")

    try:
        file_paths = json.loads(response)
        if not isinstance(file_paths, list):
            print(f"[Agente Pesquisador] Erro: A resposta JSON não é uma lista: {response}")
            return []

        print(f"[Agente Pesquisador] Encontrados {len(file_paths)} arquivos. Extraindo metadados...")
        
        knowledge_base = []
        for path in file_paths:
            try:
                stat = os.stat(path)
                file_info = {
                    "path": path,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": 'documentacao' if path.endswith(('.md', '.txt')) else 'codigo',
                    "is_readme": os.path.basename(path).lower() == 'readme.md'
                }
                knowledge_base.append(file_info)
            except FileNotFoundError:
                print(f"[Agente Pesquisador] Aviso: Arquivo '{path}' não encontrado durante extração de metadados.")
            except Exception as e:
                print(f"[Agente Pesquisador] Erro ao processar metadados para '{path}': {e}")

        print(f"[Agente Pesquisador] Metadados extraídos para {len(knowledge_base)} arquivos.")
        return knowledge_base

    except json.JSONDecodeError:
        print(f"[Agente Pesquisador] Erro: A resposta não é um JSON válido: {response}")
        return []
