# agents/orchestrator.py
import os
import shutil
from .researcher import run_researcher
from .analyzer import run_analyzer
from .writer import run_writer

def run_orchestration(project_path):
    """
    Orquestra todo o fluxo de trabalho de análise e reescrita de documentação.
    """
    print("--- Iniciando Orquestração da Análise de Documentação ---")
    print(f"Projeto Alvo: {os.path.abspath(project_path)}")
    print("-" * 60)
    
    # ETAPA 1: PESQUISA
    search_patterns = [
        '**/*.py', '**/*.js', '**/*.ts',  # Código
        '**/*.md', '**/*.txt'  # Documentação
    ]
    knowledge_base = run_researcher(project_path, search_patterns)
    
    if not knowledge_base:
        print("\n[Orquestrador] O Agente Pesquisador não encontrou arquivos relevantes. Encerrando.")
        return
    
    # ETAPA 2: ORGANIZAÇÃO
    print(f"\n[Orquestrador] O Pesquisador encontrou {len(knowledge_base)} arquivos.")
    knowledge_base.sort(key=lambda x: (x['is_readme'], x['last_modified']), reverse=True)
    print("Ordem de prioridade para análise definida (READMEs e arquivos recentes primeiro).")
    
    file_paths_for_analyzer = [item['path'] for item in knowledge_base]
    print(f"\n[Orquestrador] Enviando {len(file_paths_for_analyzer)} arquivos para o Analista.")
    print("-" * 60)
    
    # ETAPA 3: ANÁLISE
    discrepancies = run_analyzer(file_paths_for_analyzer)
    
    if not discrepancies or (isinstance(discrepancies, list) and discrepancies and "Erro" in discrepancies[0]):
        print("\n[Orquestrador] Nenhuma discrepância encontrada ou ocorreu um erro na análise. Processo finalizado.")
        if discrepancies and "Erro" in discrepancies[0]:
            print(f"   Detalhe do erro: {discrepancies[0]}")
        return
    
    print(f"\n[Orquestrador] O Analista encontrou {len(discrepancies)} pontos para melhorar.")
    print("-" * 60)
    
    # ETAPA 4: ESCRITA (NOVO)
    new_readme_content = run_writer(discrepancies, knowledge_base)
    
    # ETAPA 5: FINALIZAÇÃO (NOVO)
    print("\n[Orquestrador] Processo de escrita finalizado. Salvando e organizando arquivos...")
    
    # Salva o novo README
    new_readme_path = os.path.join(project_path, 'README_gerado.md')
    try:
        with open(new_readme_path, 'w', encoding='utf-8') as f:
            f.write(new_readme_content)
        print(f"✅ Novo README salvo em: {new_readme_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar o novo README: {e}")
        return
    
    # Prepara para mover os arquivos antigos
    old_docs_path = os.path.join(project_path, 'docs.old')
    doc_files_to_move = [item['path'] for item in knowledge_base if item['type'] == 'documentacao']
    
    if not doc_files_to_move:
        print("\n[Orquestrador] Nenhum arquivo de documentação antigo para mover.")
    else:
        print("\nOs seguintes arquivos de documentação foram usados e podem ser arquivados:")
        for f_path in doc_files_to_move:
            print(f"  - {os.path.basename(f_path)}")
        
        try:
            # Solicita confirmação do usuário
            confirm = input(f"\nDeseja mover esses {len(doc_files_to_move)} arquivos para '{old_docs_path}'? (s/n): ").lower()
            if confirm == 's':
                if not os.path.exists(old_docs_path):
                    os.makedirs(old_docs_path)
                
                for f_path in doc_files_to_move:
                    base_name = os.path.basename(f_path)
                    destination = os.path.join(old_docs_path, base_name)
                    shutil.move(f_path, destination)
                    print(f"  -> Movido: {base_name}")
                print(f"✅ Arquivos antigos arquivados em: {old_docs_path}")
            else:
                print("\nOperação de arquivamento cancelada pelo usuário.")
        except Exception as e:
            print(f"❌ Erro ao mover arquivos antigos: {e}")
    
    print("\n" + "-" * 60)
    print("--- Orquestração Concluída --- ")