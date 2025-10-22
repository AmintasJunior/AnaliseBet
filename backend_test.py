#!/usr/bin/env python3
"""
Teste Completo do Backend - AnaliseBet 2.0
Sistema de análise de apostas esportivas com probabilidades normalizadas
"""

import requests
import json
import sys
from typing import Dict, Any

# Configuração da URL base
BASE_URL = "https://apostas-inteligentes.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.created_matches = []  # Para limpeza posterior
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Registra resultado do teste"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        
    def test_create_match_complete(self) -> str:
        """Testa criação de partida com todos os campos novos"""
        print("\n=== TESTE 1: POST /api/partidas - Criar partida completa ===")
        
        payload = {
            "campeonato": "Liga dos Campeões",
            "rodada": 3,
            "data_hora": "2024-10-22T16:00:00",
            "local_estadio": "BayArena",
            "time_casa": "Leverkusen",
            "forma_casa": "V-V-E-V-D",
            "media_gols_marcados_casa": 2.5,
            "media_gols_sofridos_casa": 1.0,
            "desempenho_especifico_casa": "Forte em casa com 80% aproveitamento",
            "lesoes_suspensoes_casa": "Nenhuma",
            "artilheiro_disponivel_casa": True,
            "time_visitante": "PSG",
            "forma_fora": "V-D-V-V-E",
            "media_gols_marcados_fora": 2.8,
            "media_gols_sofridos_fora": 1.2,
            "desempenho_especifico_fora": "Bom fora de casa",
            "lesoes_suspensoes_fora": "2 desfalques importantes",
            "artilheiro_disponivel_fora": False,
            "historico_h2h": "3V 2E 1D nos últimos 6 jogos",
            "arbitro": "Michael Oliver",
            "media_cartoes_arbitro": 4.5,
            "condicoes_externas": "Boas condições",
            "noticia_1": "Leverkusen confiante após sequência positiva",
            "noticia_2": "PSG com desfalques no ataque",
            "noticia_3": "Decisivo para classificação",
            "observacoes_adicionais": "Jogo importante para ambos",
            "odd_casa": 2.10,
            "odd_empate": 3.50,
            "odd_fora": 3.20
        }
        
        try:
            response = requests.post(f"{self.base_url}/partidas", json=payload)
            
            if response.status_code == 200:
                match_data = response.json()
                match_id = match_data.get("id")
                self.created_matches.append(match_id)
                
                # Verifica se todos os campos foram salvos
                required_fields = ["campeonato", "time_casa", "time_visitante", "forma_casa", "forma_fora", 
                                 "noticia_1", "noticia_2", "noticia_3", "desempenho_especifico_casa"]
                
                missing_fields = [field for field in required_fields if not match_data.get(field)]
                
                if missing_fields:
                    self.log_test("Criar partida completa", False, f"Campos ausentes: {missing_fields}")
                else:
                    self.log_test("Criar partida completa", True, f"Partida criada com ID: {match_id}")
                
                return match_id
            else:
                self.log_test("Criar partida completa", False, f"Status: {response.status_code}, Erro: {response.text}")
                return None
                
        except Exception as e:
            self.log_test("Criar partida completa", False, f"Exceção: {str(e)}")
            return None
    
    def test_create_balanced_teams(self) -> str:
        """Cenário 1: Times equilibrados (diferença < 5%)"""
        print("\n=== CENÁRIO 1: Times equilibrados ===")
        
        payload = {
            "campeonato": "Premier League",
            "rodada": 15,
            "data_hora": "2024-10-23T15:00:00",
            "local_estadio": "Stamford Bridge",
            "time_casa": "Chelsea",
            "forma_casa": "V-E-V-E-D",
            "media_gols_marcados_casa": 1.8,
            "media_gols_sofridos_casa": 1.2,
            "desempenho_especifico_casa": "Equilibrado em casa",
            "lesoes_suspensoes_casa": "1 desfalque menor",
            "artilheiro_disponivel_casa": True,
            "time_visitante": "Arsenal",
            "forma_fora": "E-V-D-V-E",
            "media_gols_marcados_fora": 1.9,
            "media_gols_sofridos_fora": 1.1,
            "desempenho_especifico_fora": "Equilibrado fora",
            "lesoes_suspensoes_fora": "1 desfalque menor",
            "artilheiro_disponivel_fora": True,
            "historico_h2h": "2V 3E 1D nos últimos 6",
            "arbitro": "Anthony Taylor",
            "media_cartoes_arbitro": 4.0,
            "condicoes_externas": "Condições normais",
            "noticia_1": "Clássico equilibrado",
            "noticia_2": "Ambos em boa fase",
            "noticia_3": "Disputa acirrada esperada",
            "observacoes_adicionais": "Derby londrino",
            "odd_casa": 2.80,
            "odd_empate": 3.20,
            "odd_fora": 2.90
        }
        
        try:
            response = requests.post(f"{self.base_url}/partidas", json=payload)
            
            if response.status_code == 200:
                match_data = response.json()
                match_id = match_data.get("id")
                self.created_matches.append(match_id)
                self.log_test("Criar partida equilibrada", True, f"ID: {match_id}")
                return match_id
            else:
                self.log_test("Criar partida equilibrada", False, f"Status: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Criar partida equilibrada", False, f"Exceção: {str(e)}")
            return None
    
    def test_create_dominant_home(self) -> str:
        """Cenário 2: Time casa dominante"""
        print("\n=== CENÁRIO 2: Time casa dominante ===")
        
        payload = {
            "campeonato": "La Liga",
            "rodada": 8,
            "data_hora": "2024-10-24T20:00:00",
            "local_estadio": "Camp Nou",
            "time_casa": "Barcelona",
            "forma_casa": "V-V-V-V-V",
            "media_gols_marcados_casa": 3.2,
            "media_gols_sofridos_casa": 0.8,
            "desempenho_especifico_casa": "Invencível em casa esta temporada",
            "lesoes_suspensoes_casa": "Nenhuma",
            "artilheiro_disponivel_casa": True,
            "time_visitante": "Getafe",
            "forma_fora": "D-D-E-D-V",
            "media_gols_marcados_fora": 1.1,
            "media_gols_sofridos_fora": 2.3,
            "desempenho_especifico_fora": "Dificuldades fora de casa",
            "lesoes_suspensoes_fora": "3 titulares desfalcados",
            "artilheiro_disponivel_fora": False,
            "historico_h2h": "5V 1E 0D nos últimos 6",
            "arbitro": "Mateu Lahoz",
            "media_cartoes_arbitro": 3.8,
            "condicoes_externas": "Excelentes condições",
            "noticia_1": "Barcelona em grande fase",
            "noticia_2": "Getafe com muitos desfalques",
            "noticia_3": "Favorito absoluto em casa",
            "observacoes_adicionais": "Diferença técnica evidente",
            "odd_casa": 1.25,
            "odd_empate": 5.50,
            "odd_fora": 8.00
        }
        
        try:
            response = requests.post(f"{self.base_url}/partidas", json=payload)
            
            if response.status_code == 200:
                match_data = response.json()
                match_id = match_data.get("id")
                self.created_matches.append(match_id)
                self.log_test("Criar partida casa dominante", True, f"ID: {match_id}")
                return match_id
            else:
                self.log_test("Criar partida casa dominante", False, f"Status: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Criar partida casa dominante", False, f"Exceção: {str(e)}")
            return None
    
    def test_create_strong_away(self) -> str:
        """Cenário 3: Time fora forte"""
        print("\n=== CENÁRIO 3: Time fora forte ===")
        
        payload = {
            "campeonato": "Serie A",
            "rodada": 12,
            "data_hora": "2024-10-25T18:30:00",
            "local_estadio": "Stadio Olimpico",
            "time_casa": "Roma",
            "forma_casa": "D-E-D-V-D",
            "media_gols_marcados_casa": 1.3,
            "media_gols_sofridos_casa": 1.8,
            "desempenho_especifico_casa": "Instável em casa",
            "lesoes_suspensoes_casa": "2 jogadores importantes fora",
            "artilheiro_disponivel_casa": False,
            "time_visitante": "Inter Milan",
            "forma_fora": "V-V-V-E-V",
            "media_gols_marcados_fora": 2.6,
            "media_gols_sofridos_fora": 0.9,
            "desempenho_especifico_fora": "Excelente fora de casa",
            "lesoes_suspensoes_fora": "Nenhuma",
            "artilheiro_disponivel_fora": True,
            "historico_h2h": "1V 1E 4D nos últimos 6",
            "arbitro": "Daniele Orsato",
            "media_cartoes_arbitro": 4.2,
            "condicoes_externas": "Boas condições",
            "noticia_1": "Inter em excelente momento",
            "noticia_2": "Roma com problemas internos",
            "noticia_3": "Visitante favorito",
            "observacoes_adicionais": "Inter busca liderança",
            "odd_casa": 3.80,
            "odd_empate": 3.40,
            "odd_fora": 1.95
        }
        
        try:
            response = requests.post(f"{self.base_url}/partidas", json=payload)
            
            if response.status_code == 200:
                match_data = response.json()
                match_id = match_data.get("id")
                self.created_matches.append(match_id)
                self.log_test("Criar partida fora forte", True, f"ID: {match_id}")
                return match_id
            else:
                self.log_test("Criar partida fora forte", False, f"Status: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Criar partida fora forte", False, f"Exceção: {str(e)}")
            return None
    
    def test_list_matches(self):
        """Testa listagem de partidas"""
        print("\n=== TESTE 2: GET /api/partidas - Listar partidas ===")
        
        try:
            response = requests.get(f"{self.base_url}/partidas")
            
            if response.status_code == 200:
                matches = response.json()
                if isinstance(matches, list):
                    self.log_test("Listar partidas", True, f"Retornou {len(matches)} partidas")
                else:
                    self.log_test("Listar partidas", False, "Resposta não é uma lista")
            else:
                self.log_test("Listar partidas", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Listar partidas", False, f"Exceção: {str(e)}")
    
    def test_get_match(self, match_id: str):
        """Testa busca de partida específica"""
        print(f"\n=== TESTE 3: GET /api/partidas/{match_id} - Buscar partida ===")
        
        try:
            response = requests.get(f"{self.base_url}/partidas/{match_id}")
            
            if response.status_code == 200:
                match_data = response.json()
                required_fields = ["id", "campeonato", "time_casa", "time_visitante"]
                
                missing_fields = [field for field in required_fields if not match_data.get(field)]
                
                if missing_fields:
                    self.log_test("Buscar partida específica", False, f"Campos ausentes: {missing_fields}")
                else:
                    self.log_test("Buscar partida específica", True, f"Partida encontrada: {match_data.get('time_casa')} vs {match_data.get('time_visitante')}")
            else:
                self.log_test("Buscar partida específica", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Buscar partida específica", False, f"Exceção: {str(e)}")
    
    def test_analysis_v2_critical_validations(self, match_id: str, scenario_name: str):
        """TESTE PRINCIPAL: Validações críticas da análise v2.0"""
        print(f"\n=== TESTE 4: GET /api/partidas/{match_id}/analise-v2 - {scenario_name} ===")
        
        try:
            response = requests.get(f"{self.base_url}/partidas/{match_id}/analise-v2")
            
            if response.status_code != 200:
                self.log_test(f"Análise v2.0 - {scenario_name}", False, f"Status: {response.status_code}")
                return
            
            data = response.json()
            analise = data.get("analise_1x2", {})
            
            # VALIDAÇÃO 1: Probabilidades somam 100%
            prob_casa = analise.get("probabilidade_casa", 0)
            prob_empate = analise.get("probabilidade_empate", 0)
            prob_fora = analise.get("probabilidade_fora", 0)
            soma_prob = prob_casa + prob_empate + prob_fora
            
            if abs(soma_prob - 100) <= 0.1:  # Tolerância para arredondamento
                self.log_test(f"✅ Probabilidades somam 100% - {scenario_name}", True, f"Soma: {soma_prob}%")
            else:
                self.log_test(f"❌ Probabilidades somam 100% - {scenario_name}", False, f"Soma: {soma_prob}% (Casa: {prob_casa}%, Empate: {prob_empate}%, Fora: {prob_fora}%)")
            
            # VALIDAÇÃO 2: Resultado previsto válido
            resultado_previsto = analise.get("resultado_previsto", "")
            resultados_validos = ["Casa", "Empate", "Fora", "Sem recomendação"]
            
            if resultado_previsto in resultados_validos:
                self.log_test(f"✅ Resultado previsto válido - {scenario_name}", True, f"Resultado: {resultado_previsto}")
            else:
                self.log_test(f"❌ Resultado previsto válido - {scenario_name}", False, f"Resultado inválido: {resultado_previsto}")
            
            # VALIDAÇÃO 3: Confiança válida
            confianca = analise.get("confianca", "")
            confiancas_validas = ["Alta", "Média", "Baixa", "Sem recomendação segura"]
            
            if confianca in confiancas_validas:
                self.log_test(f"✅ Confiança válida - {scenario_name}", True, f"Confiança: {confianca}")
            else:
                self.log_test(f"❌ Confiança válida - {scenario_name}", False, f"Confiança inválida: {confianca}")
            
            # VALIDAÇÃO 4: Sistema de confiança (diferença < 5% = Sem recomendação segura)
            diferenca_prob = analise.get("diferenca_probabilidade", 0)
            
            if diferenca_prob < 5 and confianca == "Sem recomendação segura":
                self.log_test(f"✅ Sistema confiança (< 5%) - {scenario_name}", True, f"Diferença: {diferenca_prob}%, Confiança: {confianca}")
            elif diferenca_prob >= 5 and confianca != "Sem recomendação segura":
                self.log_test(f"✅ Sistema confiança (>= 5%) - {scenario_name}", True, f"Diferença: {diferenca_prob}%, Confiança: {confianca}")
            else:
                self.log_test(f"❌ Sistema confiança - {scenario_name}", False, f"Diferença: {diferenca_prob}%, Confiança: {confianca}")
            
            # VALIDAÇÃO 5: EV calculados
            ev_casa = analise.get("ev_casa")
            ev_empate = analise.get("ev_empate")
            ev_fora = analise.get("ev_fora")
            
            if all(isinstance(ev, (int, float)) for ev in [ev_casa, ev_empate, ev_fora]):
                self.log_test(f"✅ EV calculados - {scenario_name}", True, f"EV Casa: {ev_casa}, Empate: {ev_empate}, Fora: {ev_fora}")
            else:
                self.log_test(f"❌ EV calculados - {scenario_name}", False, f"EVs inválidos: {ev_casa}, {ev_empate}, {ev_fora}")
            
            # VALIDAÇÃO 6: Melhor aposta
            melhor_aposta = analise.get("melhor_aposta", "")
            
            if melhor_aposta:
                self.log_test(f"✅ Melhor aposta definida - {scenario_name}", True, f"Melhor aposta: {melhor_aposta}")
            else:
                self.log_test(f"❌ Melhor aposta definida - {scenario_name}", False, "Melhor aposta não definida")
            
            # VALIDAÇÃO 7: Detalhes dos times (7 fatores cada)
            detalhes_casa = analise.get("detalhes_casa", {})
            detalhes_fora = analise.get("detalhes_fora", {})
            
            fatores_esperados = [
                "forma_recente", "forca_elenco", "desempenho_casa_fora", 
                "historico_h2h", "motivacao_contexto", "notas_analista", "contexto_externo"
            ]
            
            fatores_casa_ok = all(fator in detalhes_casa for fator in fatores_esperados)
            fatores_fora_ok = all(fator in detalhes_fora for fator in fatores_esperados)
            
            if fatores_casa_ok and fatores_fora_ok:
                self.log_test(f"✅ Detalhes 7 fatores - {scenario_name}", True, "Todos os 7 fatores presentes")
            else:
                missing_casa = [f for f in fatores_esperados if f not in detalhes_casa]
                missing_fora = [f for f in fatores_esperados if f not in detalhes_fora]
                self.log_test(f"❌ Detalhes 7 fatores - {scenario_name}", False, f"Faltam - Casa: {missing_casa}, Fora: {missing_fora}")
            
            # VALIDAÇÃO 8: Scores brutos
            scores_brutos = analise.get("scores_brutos", {})
            
            if all(key in scores_brutos for key in ["casa", "empate", "fora"]):
                self.log_test(f"✅ Scores brutos - {scenario_name}", True, f"Scores: Casa {scores_brutos['casa']}, Empate {scores_brutos['empate']}, Fora {scores_brutos['fora']}")
            else:
                self.log_test(f"❌ Scores brutos - {scenario_name}", False, f"Scores incompletos: {scores_brutos}")
            
            # VALIDAÇÃO 9: Justificativa detalhada
            justificativa = analise.get("justificativa", "")
            
            if len(justificativa) > 100:  # Deve ser texto detalhado
                self.log_test(f"✅ Justificativa detalhada - {scenario_name}", True, f"Justificativa com {len(justificativa)} caracteres")
            else:
                self.log_test(f"❌ Justificativa detalhada - {scenario_name}", False, f"Justificativa muito curta: {len(justificativa)} caracteres")
            
            # Mostra resumo da análise
            print(f"    📊 RESUMO - {scenario_name}:")
            print(f"    Probabilidades: Casa {prob_casa}% | Empate {prob_empate}% | Fora {prob_fora}%")
            print(f"    Resultado: {resultado_previsto} | Confiança: {confianca}")
            print(f"    Diferença: {diferenca_prob}% | Melhor aposta: {melhor_aposta}")
            
        except Exception as e:
            self.log_test(f"Análise v2.0 - {scenario_name}", False, f"Exceção: {str(e)}")
    
    def test_delete_match(self, match_id: str):
        """Testa exclusão de partida"""
        print(f"\n=== TESTE 5: DELETE /api/partidas/{match_id} - Deletar partida ===")
        
        try:
            response = requests.delete(f"{self.base_url}/partidas/{match_id}")
            
            if response.status_code == 200:
                # Verifica se realmente foi deletada
                check_response = requests.get(f"{self.base_url}/partidas/{match_id}")
                
                if check_response.status_code == 404:
                    self.log_test("Deletar partida", True, "Partida deletada com sucesso")
                else:
                    self.log_test("Deletar partida", False, "Partida ainda existe após deleção")
            else:
                self.log_test("Deletar partida", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Deletar partida", False, f"Exceção: {str(e)}")
    
    def cleanup_matches(self):
        """Limpa partidas criadas durante os testes"""
        print("\n=== LIMPEZA: Removendo partidas de teste ===")
        
        for match_id in self.created_matches:
            try:
                requests.delete(f"{self.base_url}/partidas/{match_id}")
                print(f"    Removida partida: {match_id}")
            except:
                pass
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTE COMPLETO DO BACKEND - AnaliseBet 2.0")
        print(f"URL Base: {self.base_url}")
        print("=" * 80)
        
        # Criar partidas de teste
        match_complete = self.test_create_match_complete()
        match_balanced = self.test_create_balanced_teams()
        match_home_dominant = self.test_create_dominant_home()
        match_away_strong = self.test_create_strong_away()
        
        # Testes básicos
        self.test_list_matches()
        
        if match_complete:
            self.test_get_match(match_complete)
        
        # TESTES PRINCIPAIS - Análise v2.0
        if match_complete:
            self.test_analysis_v2_critical_validations(match_complete, "PARTIDA COMPLETA")
        
        if match_balanced:
            self.test_analysis_v2_critical_validations(match_balanced, "TIMES EQUILIBRADOS")
        
        if match_home_dominant:
            self.test_analysis_v2_critical_validations(match_home_dominant, "CASA DOMINANTE")
        
        if match_away_strong:
            self.test_analysis_v2_critical_validations(match_away_strong, "FORA FORTE")
        
        # Teste de deleção (apenas uma partida)
        if match_complete:
            self.test_delete_match(match_complete)
            self.created_matches.remove(match_complete)  # Remove da lista para não tentar deletar novamente
        
        # Limpeza
        self.cleanup_matches()
        
        # Relatório final
        self.print_final_report()
    
    def print_final_report(self):
        """Imprime relatório final dos testes"""
        print("\n" + "=" * 80)
        print("📋 RELATÓRIO FINAL DOS TESTES")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de testes: {total_tests}")
        print(f"✅ Passou: {passed_tests}")
        print(f"❌ Falhou: {failed_tests}")
        print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 TESTES QUE FALHARAM:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  ❌ {result['test']}: {result['message']}")
        
        print("\n" + "=" * 80)
        
        return failed_tests == 0


def main():
    """Função principal"""
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("⚠️  ALGUNS TESTES FALHARAM!")
        sys.exit(1)


if __name__ == "__main__":
    main()