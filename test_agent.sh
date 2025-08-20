
#!/bin/bash
# Script para testar o Agente de Documentação
# NOTA: Este script deve ser executado em um ambiente bash (como Git Bash no Windows).

echo "--- Iniciando Teste Automatizado do Agente de Documentação ---"

# Etapa 1: Instalar dependências
echo "Verificando e instalando dependências (agno, python-dotenv)..."
pip install agno python-dotenv --quiet --user

if [ $? -ne 0 ]; then
    echo "Erro: Falha ao instalar as dependências com pip. Abortando teste."
    exit 1
fi

echo "Dependências instaladas."
echo ""

# Etapa 2: Executar o agente com uma série de inputs de teste
# Usamos um "here document" (<<EOF) para passar múltiplos comandos para o script python.
echo "Iniciando o agente e enviando comandos..."

python run.py <<EOF
Qual é o objetivo principal do projeto?
Lembre-se que a versão atual do projeto é 1.2.3.
Quais são os arquivos de documentação disponíveis?
Qual é a versão atual do projeto?
sair
EOF

echo ""
echo "--- Teste Automatizado Concluído ---"
echo "Por favor, verifique a saída acima para confirmar se o agente respondeu corretamente."

