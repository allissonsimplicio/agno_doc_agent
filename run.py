import argparse
import os
import database

# No futuro, importaremos e chamaremos o agente orquestrador daqui
# from agents.orchestrator import run_orchestration

from agents.orchestrator import run_orchestration

def analyze_project(project_path):
    """
    Função que dispara o processo de análise de documentação.
    Delega todo o trabalho para o Agente Orquestrador.
    """
    run_orchestration(project_path)


def main():
    """
    Ponto de entrada principal da CLI.
    Configura o parser de argumentos e direciona para a função apropriada.
    """
    # Garante que o banco de dados e as tabelas existam antes de qualquer operação
    database.initialize_database()
    print("-" * 50)

    parser = argparse.ArgumentParser(
        prog="doc-analyzer",
        description="Uma ferramenta de IA para analisar e comparar documentação e código-fonte.",
        epilog="Para ajuda em um comando específico, use: doc-analyzer <comando> --help"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis", required=True)

    # Define o comando 'analyze'
    analyze_parser = subparsers.add_parser("analyze", help="Executa a análise completa de um projeto.")
    analyze_parser.add_argument("project_path", type=str, help="O caminho para o diretório do projeto a ser analisado.")

    args = parser.parse_args()

    if args.command == "analyze":
        project_path = args.project_path
        # Se o caminho não for fornecido via argumento, solicita interativamente
        if not project_path:
            try:
                project_path = input("Por favor, insira o caminho para o diretório do projeto: ")
            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário.")
                return

        # Valida se o caminho fornecido é um diretório válido
        if not os.path.isdir(project_path):
            print(f"Erro: O caminho fornecido '{project_path}' não é um diretório válido.")
            return
        
        project_path = os.path.abspath(project_path)
        print(f"Iniciando análise no projeto: {project_path}")
        analyze_project(project_path)

if __name__ == "__main__":
    main()