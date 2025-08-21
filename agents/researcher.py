# agents/researcher.py
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (ex: ANTHROPIC_API_KEY)
load_dotenv()

import tools

try:
    from agno.agent import Agent
    from agno.models.anthropic import Claude
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
    model=Claude(id="claude-3-5-sonnet-20241022"),
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
    
    response = researcher_agent.run(prompt)

    content = response.get_content_as_string()
    print(f"[Agente Pesquisador] Resposta bruta do modelo: {content}")
    # Corrige as barras invertidas para garantir que o JSON seja válido em Windows
    corrected_content = content.replace('\\', '\\\\')
    try:
        file_paths = json.loads(corrected_content)
        if not isinstance(file_paths, list):
            print(f"[Agente Pesquisador] Erro: A resposta JSON não é uma lista: {corrected_content}")
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