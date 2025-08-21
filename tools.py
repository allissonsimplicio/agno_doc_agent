# tools.py
import os
import glob
import json
from typing import List
from agno.tools import tool

# ========================================
# TOOLS PARA AGENTES (usando decorator @tool)
# ========================================

@tool
def find_files_in_project(project_path: str, patterns: List[str]) -> str:
    """
    Encontra arquivos em um projeto baseado em padrões glob.
    
    Args:
        project_path: Caminho para o diretório do projeto
        patterns: Lista de padrões glob (ex: ['**/*.py', '**/*.md'])
    
    Returns:
        JSON string com lista de caminhos de arquivos encontrados
    """
    found_files = []
    
    # Converte para caminho absoluto
    project_path = os.path.abspath(project_path)
    
    # Para cada padrão fornecido
    for pattern in patterns:
        # Combina o caminho do projeto com o padrão
        full_pattern = os.path.join(project_path, pattern)
        
        # Encontra arquivos que correspondem ao padrão
        matching_files = glob.glob(full_pattern, recursive=True)
        
        # Adiciona à lista (evita duplicatas)
        for file_path in matching_files:
            if os.path.isfile(file_path) and file_path not in found_files:
                found_files.append(file_path)
    
    # Ordena e remove duplicatas
    found_files = sorted(list(set([os.path.abspath(f) for f in found_files])))
    
    # Retorna como JSON
    return json.dumps(found_files, indent=2)


@tool 
def read_file_content(file_path: str) -> str:
    """
    Lê o conteúdo de um arquivo de texto.
    
    Args:
        file_path: Caminho para o arquivo
        
    Returns:
        Conteúdo do arquivo como string
    """
    try:
        # Tenta diferentes codificações
        encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                return content
            except UnicodeDecodeError:
                continue
        
        # Se todas as codificações falharem, lê como binário e converte
        with open(file_path, 'rb') as f:
            content = f.read()
            return content.decode('utf-8', errors='replace')
            
    except FileNotFoundError:
        return f"Erro: Arquivo '{file_path}' não encontrado."
    except Exception as e:
        return f"Erro ao ler arquivo '{file_path}': {str(e)}"


# ========================================
# FUNÇÕES AUXILIARES (não são tools)
# ========================================

def get_project_documentation(project_path):
    """
    Lê todos os arquivos .md e .txt do diretório de um projeto e retorna seu conteúdo.
    Isso fornece a base de conhecimento para o agente.
    """
    docs_content = ""
    search_pattern = os.path.join(project_path, "**", "*")
    
    # Encontra todos os arquivos .md e .txt recursivamente
    doc_files = [f for f in glob.glob(search_pattern, recursive=True) 
                 if f.endswith((".md", ".txt")) and os.path.isfile(f)]
    
    for file_path in doc_files:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                docs_content += f"--- Início de {filename} ---\n"
                docs_content += f.read()
                docs_content += f"\n--- Fim de {filename} ---\n\n"
        except Exception as e:
            docs_content += f"--- Erro ao ler {filename}: {e}---\n\n"
            
    return docs_content


def list_doc_files(project_path):
    """Lista todos os arquivos de documentação em um diretório de projeto."""
    search_pattern = os.path.join(project_path, "**", "*")
    doc_files = [f for f in glob.glob(search_pattern, recursive=True) 
                 if f.endswith((".md", ".txt")) and os.path.isfile(f)]
    return [os.path.abspath(f) for f in doc_files]


def list_files_debug(directory: str) -> None:
    """
    Função auxiliar para debug - lista arquivos em um diretório
    """
    print(f"Arquivos em {directory}:")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"  {os.path.join(root, file)}")


# ========================================
# VERSÕES LEGACY (mantidas para compatibilidade)
# ========================================

def find_files_in_project_legacy(base_path, patterns):
    """
    VERSÃO LEGACY: Encontra todos os arquivos em um diretório base que correspondem a uma lista de padrões glob.
    Use find_files_in_project() com @tool em vez desta.
    """
    found_files = []
    for pattern in patterns:
        search_pattern = os.path.join(base_path, pattern)
        found_files.extend(glob.glob(search_pattern, recursive=True))
    
    return sorted(list(set([os.path.abspath(f) for f in found_files])))


def read_file_content_legacy(file_path):
    """
    VERSÃO LEGACY: Lê e retorna o conteúdo de um único arquivo de texto.
    Use read_file_content() com @tool em vez desta.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo não encontrado em '{file_path}'."
    except Exception as e:
        return f"Erro ao ler o arquivo '{file_path}': {e}"