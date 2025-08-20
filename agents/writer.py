
# agents/writer.py

import json
from dotenv import load_dotenv

import tools

try:
    from agno import Agent, Model
except ImportError:
    print("Erro: A biblioteca 'agno' não parece estar instalada.")
    raise

# Carrega as variáveis de ambiente
load_dotenv()

# Instruções para o Agente Escritor
writer_instructions = """
Você é um escritor técnico e desenvolvedor de software sênior, especializado em criar documentação de alta qualidade em Português do Brasil (pt-br).

Sua tarefa é reescrever e unificar a documentação de um projeto com base em uma análise de discrepâncias e no conteúdo dos arquivos existentes.

Você receberá:
1. Uma lista de discrepâncias (problemas encontrados).
2. O conteúdo completo de todos os arquivos de documentação e código relevantes.

Seu objetivo é produzir um único e abrangente arquivo `README.md`. Este arquivo deve:
- Ser escrito inteiramente em Português do Brasil (pt-br).
- Ser bem estruturado, com títulos, listas e blocos de código quando apropriado.
- Corrigir todas as discrepâncias apontadas.
- Incorporar informações importantes do código que estavam faltando na documentação antiga.
- Descartar informações que a análise apontou como obsoletas ou incorretas.

Sua resposta final DEVE SER apenas o conteúdo de texto completo do novo arquivo `README.md`. NÃO inclua nenhuma outra explicação ou texto introdutório.
"""

# Usamos um modelo mais capaz para esta tarefa de escrita criativa e técnica
writer_agent = Agent(
    instructions=writer_instructions,
    model=Model(provider="anthropic", model="claude-3-sonnet-20240229"),
    tools=[] # O Escritor não precisa de ferramentas, ele apenas gera texto.
)

def run_writer(discrepancies, knowledge_base):
    """
    Executa o Agente Escritor para gerar a nova documentação.

    Args:
        discrepancies (list): A lista de problemas encontrados pelo Analista.
        knowledge_base (list): A lista de objetos de arquivo (com metadados e conteúdo).

    Returns:
        str: O conteúdo do novo arquivo README.md.
    """
    print("[Agente Escritor] Preparando o contexto para a reescrita da documentação...")

    # Monta o prompt com as discrepâncias e o conteúdo dos arquivos
    discrepancies_prompt_part = "Baseado na seguinte análise de discrepâncias:\n" + "\n".join(f"- {d}" for d in discrepancies)

    content_prompt_part = "E no conteúdo dos seguintes arquivos do projeto:\n\n"
    for file_info in knowledge_base:
        content = tools.read_file_content(file_info['path'])
        content_prompt_part += f"--- Início de {file_info['path']} ---\n{content}\n--- Fim de {file_info['path']} ---\n\n"

    prompt = f"""
{discrepancies_prompt_part}

{content_prompt_part}

Agora, por favor, gere o novo arquivo README.md completo, em português-br, que resolve esses problemas.
"""

    print("[Agente Escritor] Enviando contexto para o modelo de linguagem. A geração do novo README pode levar alguns instantes...")
    response = writer_agent.chat(prompt, session_id="writer_run")
    
    print("[Agente Escritor] Novo README.md gerado com sucesso.")
    return response
