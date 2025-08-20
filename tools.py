import os
import glob

# Diretório onde a documentação do projeto está armazenada.
DOCS_DIR = r"C:\Users\allis\Documents\agno_doc_agent\project_docs"

def get_project_documentation():
    """
    Lê todos os arquivos .md e .txt do diretório project_docs e retorna seu conteúdo.
    Isso fornece a base de conhecimento para o agente.
    """
    docs_content = ""
    try:
        for filename in os.listdir(DOCS_DIR):
            if filename.endswith((".md", ".txt")):
                file_path = os.path.join(DOCS_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    import os
import glob

def get_project_documentation(project_path):
    """
    Lê todos os arquivos .md e .txt do diretório de um projeto e retorna seu conteúdo.
    Isso fornece a base de conhecimento para o agente.
    """
    docs_content = ""
    search_pattern = os.path.join(project_path, "**", "*")
    
    # Encontra todos os arquivos .md e .txt recursivamente
    doc_files = [f for f in glob.glob(search_pattern, recursive=True) if f.endswith((".md", ".txt")) and os.path.isfile(f)]

    for file_path in doc_files:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                docs_content += f"--- Início de {filename} ---
"
                docs_content += f.read()
                docs_content += f"
--- Fim de {filename} ---

"
        except Exception as e:
            docs_content += f"--- Erro ao ler {filename}: {e} ---

"
            
    return docs_content

def list_doc_files(project_path):
    "Lista todos os arquivos de documentação em um diretório de projeto."
    search_pattern = os.path.join(project_path, "**", "*")
    doc_files = [f for f in glob.glob(search_pattern, recursive=True) if f.endswith((".md", ".txt")) and os.path.isfile(f)]
    return [os.path.abspath(f) for f in doc_files]
    except FileNotFoundError:
        return "Erro: O diretório de documentação 'project_docs' não foi encontrado."
    return docs_content

def list_doc_files():
    "Lista todos os arquivos de documentação no diretório project_docs."
    try:
        files = [f for f in os.listdir(DOCS_DIR) if f.endswith((".md", ".txt")])]
        return files
    except FileNotFoundError:
        return "Erro: O diretório de documentação 'project_docs' não foi encontrado."

# --- Ferramenta para o Agente Pesquisador ---
def find_files_in_project(base_path, patterns):
    """
    Encontra todos os arquivos em um diretório base que correspondem a uma lista de padrões glob.
    """
    found_files = []
    for pattern in patterns:
        search_pattern = os.path.join(base_path, pattern)
        found_files.extend(glob.glob(search_pattern, recursive=True))
    
    return sorted(list(set([os.path.abspath(f) for f in found_files])))

# --- Nova Ferramenta para o Agente Analista ---
def read_file_content(file_path):
    """
    Lê e retorna o conteúdo de um único arquivo de texto.
    
    Args:
        file_path (str): O caminho absoluto para o arquivo.

    Returns:
        str: O conteúdo do arquivo, ou uma mensagem de erro se não for encontrado/decodificado.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo não encontrado em '{file_path}'."
    except Exception as e:
        return f"Erro ao ler o arquivo '{file_path}': {e}"
