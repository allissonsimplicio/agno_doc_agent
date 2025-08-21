# Agente Analista: Compara código e documentação para encontrar discrepâncias.
# agents/analyzer.py
import json
from dotenv import load_dotenv
import tools

# Carrega as variáveis de ambiente (ex: ANTHROPIC_API_KEY)
load_dotenv()

try:
    from agno.agent import Agent
    from agno.models.anthropic import Claude
except ImportError:
    print("Erro: A biblioteca 'agno' não parece estar instalada.")
    raise

# Carrega as variáveis de ambiente
load_dotenv()

# Instruções para o Agente Analista
analyzer_instructions = """
Você é um assistente de IA e desenvolvedor de software sênior, extremamente meticuloso com a qualidade da documentação. Sua especialidade é encontrar lacunas e inconsistências entre o código-fonte e a documentação técnica.

Você receberá o conteúdo de vários arquivos de um projeto. Sua tarefa é analisá-los e identificar:

1.  Funções, classes ou métodos importantes no código que não são mencionados na documentação.
2.  Funcionalidades descritas na documentação que não parecem ter uma implementação correspondente no código.
3.  Endpoints de API, variáveis de ambiente ou passos de configuração que estão no código mas não documentados.

Concentre-se em fornecer um relatório claro e acionável. Sua resposta final DEVE SER um objeto JSON com uma única chave `discrepancies`, que contém uma lista de strings. Cada string deve ser uma discrepância clara e concisa que você encontrou.

Exemplo de Resposta Válida:
{"discrepancies": ["A função `getUser` em `user_controller.py` não está documentada no `README.md`.", "O `README.md` menciona um sistema de cache, mas não há código de cache visível."]}
"""

# Instância do Agente Analista
# Usamos um modelo mais capaz (Sonnet) para esta tarefa de raciocínio complexo.
analyzer_agent = Agent(
    instructions=analyzer_instructions,
    model=Claude(id="claude-3-5-sonnet-20241022"),
    tools=[]  # O Analista não precisa de ferramentas, ele apenas raciocina sobre o conteúdo.
)

def run_analyzer(all_file_paths):
    """
    Executa o Agente Analista para comparar todos os arquivos fornecidos.
    Args:
        all_file_paths (list): Uma lista com os caminhos de todos os arquivos a serem analisados.
    Returns:
        list: Uma lista de strings contendo as discrepâncias encontradas.
    """
    print(f"[Agente Analista] Lendo e preparando o conteúdo de {len(all_file_paths)} arquivos...")
    
    # Constrói um grande prompt com todo o conteúdo dos arquivos
    content_prompt_part = ""
    for file_path in all_file_paths:
        # Usamos nossa ferramenta para ler o conteúdo de cada arquivo
        content = tools.read_file_content(file_path)
        content_prompt_part += f"--- Início do conteúdo de: {file_path} ---\n{content}\n--- Fim do conteúdo de: {file_path}---\n\n"
    
    prompt = f"""
Analise o conteúdo de todos os arquivos do projeto fornecidos abaixo e gere seu relatório de discrepâncias em formato JSON.

{content_prompt_part}
"""
    
    print("[Agente Analista] Enviando o conteúdo para análise do modelo. Isso pode levar um momento...")
    response = analyzer_agent.run(prompt)
    print(f"[Agente Analista] Resposta bruta do modelo: {response}")
    
    try:
        # Se a resposta for um objeto RunResponse, extraia o conteúdo
        if hasattr(response, 'content'):
            response_content = response.content
        else:
            response_content = str(response)
            
        report = json.loads(response_content)
        if isinstance(report, dict) and 'discrepancies' in report:
            discrepancies = report['discrepancies']
            print(f"[Agente Analista] Sucesso: {len(discrepancies)} discrepâncias encontradas.")
            return discrepancies
        else:
            error_msg = f"Erro de formato na resposta do Analista: {response_content}"
            print(f"[Agente Analista] {error_msg}")
            return [error_msg]
    except json.JSONDecodeError:
        error_msg = f"Erro de decodificação na resposta do Analista: {response}"
        print(f"[Agente Analista] {error_msg}")
        return [error_msg]