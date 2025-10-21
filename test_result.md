#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: |
  Sistema de Análise de Apostas Esportivas - VERSÃO 2.0
  
  Melhorias Implementadas:
  1. Sistema de probabilidades coerentes (Casa + Empate + Fora = 100%)
  2. Novo cálculo com 7 fatores ponderados:
     - Forma recente (25%)
     - Força do elenco (15%)
     - Desempenho casa/fora (15%)
     - Confrontos diretos H2H (15%)
     - Motivação/contexto (10%)
     - Notas do analista (10%)
     - Notícias/contexto externo (10%)
  3. Sistema de confiança (Alta >20pts, Média 10-20pts, Baixa <10pts)
  4. Justificativa automática detalhada
  5. Análise de valor esperado (EV) para cada mercado

backend:
  - task: "Novo sistema de cálculo de probabilidades normalizadas"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: |
          Implementado calcular_scores_independentes() que:
          - Calcula scores separados para Casa, Empate e Fora
          - Normaliza automaticamente para somar 100%
          - Usa 7 fatores com pesos definidos
          - Calcula confiança baseado na diferença de probabilidades
  
  - task: "Endpoint /api/partidas/{id}/analise-v2"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: |
          Novo endpoint que retorna:
          - Probabilidades normalizadas (Casa, Empate, Fora = 100%)
          - Resultado previsto e confiança
          - EV para cada mercado
          - Justificativa detalhada
          - Detalhes dos fatores para ambos os times

  - task: "Função gerar_justificativa_1x2"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: |
          Gera justificativa automática mostrando:
          - Top 3 fatores que mais influenciaram
          - Observações específicas do resultado
          - Alertas sobre desfalques e contexto

frontend:
  - task: "Nova página DetalhesPartidaV2"
    implemented: true
    working: true
    file: "/app/frontend/src/pages/DetalhesPartidaV2.js"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: |
          Página completa com:
          - Gráfico de barras para probabilidades normalizadas
          - Display de confiança visual
          - Análise de valor esperado (EV)
          - Justificativa detalhada
          - Detalhes dos fatores para ambos os times
          - Scores brutos antes da normalização

  - task: "Atualização do Dashboard com botão v2.0"
    implemented: true
    working: true
    file: "/app/frontend/src/pages/Dashboard.js"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: |
          Adicionado botão principal "Análise v2.0" para cada partida
          Mantido botão secundário para versão antiga
          Header atualizado com informação sobre v2.0

  - task: "Rota /partida-v2/:id"
    implemented: true
    working: true
    file: "/app/frontend/src/App.js"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Nova rota configurada para página v2.0"

metadata:
  created_by: "main_agent"
  version: "2.0"
  test_sequence: 0
  run_ui: false

test_plan:
  current_focus:
    - "Teste de cálculo de probabilidades normalizadas"
    - "Verificação de soma = 100%"
    - "Teste de sistema de confiança"
    - "Teste de geração de justificativa"
    - "Teste da interface v2.0"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
  - agent: "main"
    message: |
      VERSÃO 2.0 IMPLEMENTADA COM SUCESSO!
      
      Principais mudanças:
      1. Backend: Novo sistema de cálculo com normalização garantida
      2. Frontend: Interface moderna com gráficos de barras e visualização clara
      3. API: Novo endpoint /analise-v2 com dados coerentes
      
      Próximos passos:
      - Testar backend para garantir probabilidades somam 100%
      - Testar frontend v2.0
      - Validar com partida de exemplo