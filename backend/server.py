from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import math

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class PartidaCreate(BaseModel):
    # Identificação Geral
    campeonato: str
    rodada: int
    data_hora: Optional[str] = None  # Ex: "2024-10-22T16:00:00"
    local_estadio: Optional[str] = None  # Ex: "BayArena"
    
    # Time Casa
    time_casa: str
    forma_casa: str  # Ex: "V-E-V-D-V"
    media_gols_marcados_casa: float
    media_gols_sofridos_casa: float
    desempenho_especifico_casa: Optional[str] = None  # Desempenho jogando em casa
    lesoes_suspensoes_casa: Optional[str] = None
    artilheiro_disponivel_casa: bool = True
    
    # Time Fora
    time_visitante: str
    forma_fora: str  # Ex: "D-V-E-D-E"
    media_gols_marcados_fora: float
    media_gols_sofridos_fora: float
    desempenho_especifico_fora: Optional[str] = None  # Desempenho jogando fora
    lesoes_suspensoes_fora: Optional[str] = None
    artilheiro_disponivel_fora: bool = True
    
    # H2H
    historico_h2h: str  # Ex: "3V 2E 1D nos últimos 6"
    
    # Contexto Geral
    arbitro: str
    media_cartoes_arbitro: float
    condicoes_externas: str
    
    # Notícias (3 campos separados com impacto)
    noticia_1: Optional[str] = None
    noticia_1_impacto: Optional[int] = 0  # 0-10
    noticia_2: Optional[str] = None
    noticia_2_impacto: Optional[int] = 0  # 0-10
    noticia_3: Optional[str] = None
    noticia_3_impacto: Optional[int] = 0  # 0-10
    observacoes_adicionais: Optional[str] = None
    
    # Observações Contextuais (lista de observações manuais com impacto)
    observacoes_contextuais: Optional[List[Dict[str, Any]]] = None  # [{"texto": str, "impacto": int}]
    
    # Odds
    odd_casa: float
    odd_empate: float
    odd_fora: float
    
    # Campos legados (para compatibilidade)
    artilheiro_disponivel: Optional[bool] = None
    lesoes_suspensoes: Optional[str] = None
    escalacao_definida: Optional[bool] = None
    noticias_relevantes: Optional[str] = None


class Partida(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Identificação Geral
    campeonato: str
    rodada: int
    data_hora: Optional[str] = None
    local_estadio: Optional[str] = None
    
    # Time Casa
    time_casa: str
    forma_casa: str
    media_gols_marcados_casa: float
    media_gols_sofridos_casa: float
    desempenho_especifico_casa: Optional[str] = None
    lesoes_suspensoes_casa: Optional[str] = None
    artilheiro_disponivel_casa: bool = True
    
    # Time Fora
    time_visitante: str
    forma_fora: str
    media_gols_marcados_fora: float
    media_gols_sofridos_fora: float
    desempenho_especifico_fora: Optional[str] = None
    lesoes_suspensoes_fora: Optional[str] = None
    artilheiro_disponivel_fora: bool = True
    
    # H2H
    historico_h2h: str
    
    # Contexto Geral
    arbitro: str
    media_cartoes_arbitro: float
    condicoes_externas: str
    
    # Notícias (com impacto)
    noticia_1: Optional[str] = None
    noticia_1_impacto: Optional[int] = 0  # 0-10
    noticia_2: Optional[str] = None
    noticia_2_impacto: Optional[int] = 0  # 0-10
    noticia_3: Optional[str] = None
    noticia_3_impacto: Optional[int] = 0  # 0-10
    observacoes_adicionais: Optional[str] = None
    
    # Observações Contextuais (lista de observações manuais com impacto)
    observacoes_contextuais: Optional[List[Dict[str, Any]]] = None  # [{"texto": str, "impacto": int}]
    
    # Odds
    odd_casa: float
    odd_empate: float
    odd_fora: float
    
    # Campos legados (para compatibilidade)
    artilheiro_disponivel: Optional[bool] = None
    lesoes_suspensoes: Optional[str] = None
    escalacao_definida: Optional[bool] = None
    noticias_relevantes: Optional[str] = None
    
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Analise(BaseModel):
    mercado: str
    probabilidade: float
    classificacao_prob: str
    odd: float
    ev: float
    classificacao_ev: str
    recomendacao: str
    justificativa: str
    score_total: float
    detalhes_scores: Dict[str, Any]


class ObservacaoContextual(BaseModel):
    """Observação contextual com impacto numérico"""
    texto: str
    impacto: int  # -10 a +10

class Analise1X2(BaseModel):
    """Modelo para análise 1X2 com probabilidades normalizadas (Versão 2.0)"""
    probabilidade_casa: float
    probabilidade_empate: float
    probabilidade_fora: float
    resultado_previsto: str
    confianca: str
    diferenca_probabilidade: float
    justificativa: str
    detalhes_casa: Dict[str, float]
    detalhes_fora: Dict[str, float]
    detalhes_casa_ponderados: Dict[str, Dict[str, float]]  # {fator: {nota, peso, ponderado}}
    detalhes_fora_ponderados: Dict[str, Dict[str, float]]  # {fator: {nota, peso, ponderado}}
    scores_brutos: Dict[str, float]
    # Análise de valor (EV) para cada mercado
    ev_casa: float
    ev_empate: float
    ev_fora: float
    # Observações contextuais
    observacoes_contextuais: List[ObservacaoContextual]


class AnaliseCompleta(BaseModel):
    partida: Partida
    melhor_recomendacao: Analise
    todas_analises: List[Analise]


class AnaliseCompletaV2(BaseModel):
    """Versão 2.0 com análise 1X2 coerente"""
    partida: Partida
    analise_1x2: Analise1X2
    outras_analises: Optional[List[Analise]] = None


# ================ LÓGICA DE CÁLCULO - VERSÃO 2.0 ================
# Sistema de cálculo coerente com probabilidades normalizadas

def calcular_score_forma(forma: str) -> float:
    """Calcula score baseado na forma recente (V-E-D)"""
    if not forma:
        return 5.0
    
    pontos = 0
    jogos = forma.upper().split('-')
    for jogo in jogos:
        if 'V' in jogo:
            pontos += 3
        elif 'E' in jogo:
            pontos += 1
    
    max_pontos = len(jogos) * 3
    if max_pontos == 0:
        return 5.0
    
    # Normaliza para 0-10
    score = (pontos / max_pontos) * 10
    return round(score, 2)


def calcular_score_h2h(h2h: str, perspectiva: str = "casa") -> float:
    """Calcula score do histórico H2H"""
    if not h2h:
        return 5.0
    
    # Tenta extrair V, E, D do texto
    h2h_upper = h2h.upper()
    vitorias = h2h_upper.count('V')
    empates = h2h_upper.count('E')
    derrotas = h2h_upper.count('D')
    
    total = vitorias + empates + derrotas
    if total == 0:
        return 5.0
    
    if perspectiva == "casa":
        pontos = vitorias * 3 + empates * 1
    else:
        pontos = derrotas * 3 + empates * 1
    
    max_pontos = total * 3
    score = (pontos / max_pontos) * 10
    return round(score, 2)


def calcular_score_artilheiro(disponivel: bool) -> float:
    """Score da escalação e artilheiro"""
    return 8.0 if disponivel else 4.0


def calcular_score_lesoes(texto_lesoes: str) -> float:
    """Score baseado em lesões/suspensões"""
    if not texto_lesoes or texto_lesoes.lower() in ["nenhuma", "sem desfalques", "-"]:
        return 9.0
    
    texto_lower = texto_lesoes.lower()
    if "grave" in texto_lower or "titular" in texto_lower or "3" in texto_lower or "4" in texto_lower:
        return 3.0
    elif "2" in texto_lower:
        return 5.0
    else:
        return 7.0


def calcular_score_arbitro(media_cartoes: float) -> float:
    """Score do árbitro - quanto mais cartões, menor o score para jogo travado"""
    if media_cartoes < 3:
        return 7.0
    elif media_cartoes < 5:
        return 5.0
    else:
        return 3.0


def calcular_score_motivacao(noticias: str) -> float:
    """Score baseado em notícias e motivação"""
    if not noticias:
        return 5.0
    
    noticias_lower = noticias.lower()
    positivos = ["confiante", "motivado", "decisivo", "acesso", "título", "classificação"]
    negativos = ["pressão", "crise", "derrotas", "demissão", "rebaixamento"]
    
    score = 5.0
    for palavra in positivos:
        if palavra in noticias_lower:
            score += 1.5
    for palavra in negativos:
        if palavra in noticias_lower:
            score -= 1.5
    
    return max(0, min(10, round(score, 2)))


def calcular_score_condicoes(condicoes: str) -> float:
    """Score de condições externas"""
    if not condicoes:
        return 7.0
    
    condicoes_lower = condicoes.lower()
    if "chuva" in condicoes_lower or "pesado" in condicoes_lower:
        return 4.0
    elif "boas" in condicoes_lower or "ótimo" in condicoes_lower:
        return 9.0
    else:
        return 7.0


def calcular_score_xg(media_gols_marcados: float, media_gols_sofridos: float) -> float:
    """Score baseado em média de gols"""
    saldo = media_gols_marcados - media_gols_sofridos
    
    if saldo >= 1.5:
        return 9.0
    elif saldo >= 0.8:
        return 7.5
    elif saldo >= 0:
        return 6.0
    elif saldo >= -0.8:
        return 4.0
    else:
        return 2.0


def calcular_score_odds_implicitas(odd: float, odd_referencia: float) -> float:
    """Score baseado na diferença entre odd e odd de referência"""
    prob_implicita = 1 / odd
    prob_ref = 1 / odd_referencia
    
    diferenca = prob_implicita - prob_ref
    
    if diferenca > 0.1:
        return 7.0
    elif diferenca > 0:
        return 6.0
    elif diferenca > -0.1:
        return 5.0
    else:
        return 4.0


def gerar_observacoes_contextuais(partida: Partida, analise_data: Dict) -> List[Dict[str, Any]]:
    """
    Gera observações contextuais automáticas com impacto numérico (-10 a +10)
    """
    observacoes = []
    
    # Observações do time casa
    detalhes_casa = analise_data["detalhes_casa"]
    detalhes_fora = analise_data["detalhes_fora"]
    
    # 1. Forma recente - Casa
    vitorias_casa = partida.forma_casa.upper().count('V')
    jogos_casa = len(partida.forma_casa.split('-'))
    if vitorias_casa >= 4 and jogos_casa >= 5:
        observacoes.append({
            "texto": f"✓ {partida.time_casa} não perde há {vitorias_casa} vitórias em {jogos_casa} jogos",
            "impacto": min(3 + vitorias_casa - 4, 5)
        })
    elif partida.forma_casa.upper().count('D') >= 3:
        derrotas = partida.forma_casa.upper().count('D')
        observacoes.append({
            "texto": f"⚠ {partida.time_casa} acumula {derrotas} derrotas recentes",
            "impacto": max(-3 - (derrotas - 3), -5)
        })
    
    # 2. Forma recente - Fora
    vitorias_fora = partida.forma_fora.upper().count('V')
    jogos_fora = len(partida.forma_fora.split('-'))
    if vitorias_fora >= 4 and jogos_fora >= 5:
        observacoes.append({
            "texto": f"✓ {partida.time_visitante} em ótima sequência com {vitorias_fora} vitórias",
            "impacto": min(3 + vitorias_fora - 4, 5)
        })
    elif partida.forma_fora.upper().count('D') >= 3:
        derrotas = partida.forma_fora.upper().count('D')
        observacoes.append({
            "texto": f"⚠ {partida.time_visitante} sem vitórias há {derrotas} partidas",
            "impacto": max(-3 - (derrotas - 3), -5)
        })
    
    # 3. Lesões/Suspensões - Casa
    lesoes_casa = partida.lesoes_suspensoes_casa if partida.lesoes_suspensoes_casa else partida.lesoes_suspensoes
    if lesoes_casa and lesoes_casa.lower() not in ["nenhuma", "sem desfalques", "-", ""]:
        impacto = -2
        if "titular" in lesoes_casa.lower() or "grave" in lesoes_casa.lower():
            impacto = -4
        observacoes.append({
            "texto": f"⚠ {partida.time_casa} - Desfalques: {lesoes_casa}",
            "impacto": impacto
        })
    
    # 4. Lesões/Suspensões - Fora
    lesoes_fora = partida.lesoes_suspensoes_fora
    if lesoes_fora and lesoes_fora.lower() not in ["nenhuma", "sem desfalques", "-", ""]:
        impacto = -2
        if "titular" in lesoes_fora.lower() or "grave" in lesoes_fora.lower():
            impacto = -4
        observacoes.append({
            "texto": f"⚠ {partida.time_visitante} - Desfalques: {lesoes_fora}",
            "impacto": impacto
        })
    
    # 5. Artilheiro disponível
    if not partida.artilheiro_disponivel_casa:
        observacoes.append({
            "texto": f"⚠ {partida.time_casa} sem artilheiro principal",
            "impacto": -3
        })
    if not partida.artilheiro_disponivel_fora:
        observacoes.append({
            "texto": f"⚠ {partida.time_visitante} sem artilheiro principal",
            "impacto": -3
        })
    
    # 6. Desempenho em casa
    if detalhes_casa["desempenho_casa_fora"] >= 8.0:
        observacoes.append({
            "texto": f"✓ {partida.time_casa} com forte desempenho em casa (média {partida.media_gols_marcados_casa:.1f} gols)",
            "impacto": 3
        })
    
    # 7. Desempenho fora
    if detalhes_fora["desempenho_casa_fora"] >= 8.0:
        observacoes.append({
            "texto": f"✓ {partida.time_visitante} com forte desempenho fora (média {partida.media_gols_marcados_fora:.1f} gols)",
            "impacto": 3
        })
    elif detalhes_fora["desempenho_casa_fora"] <= 3.0:
        observacoes.append({
            "texto": f"⚠ {partida.time_visitante} com dificuldades jogando fora de casa",
            "impacto": -3
        })
    
    # 8. Árbitro rigoroso
    if partida.media_cartoes_arbitro >= 5:
        observacoes.append({
            "texto": f"ℹ️ Árbitro {partida.arbitro} conhecido por ser rigoroso (média {partida.media_cartoes_arbitro:.1f} cartões)",
            "impacto": 0
        })
    
    # 9. Condições adversas
    if partida.condicoes_externas and "chuva" in partida.condicoes_externas.lower():
        observacoes.append({
            "texto": f"⚠ Condições climáticas adversas: {partida.condicoes_externas}",
            "impacto": -2
        })
    
    # 10. Notícias com impacto numérico (inseridas manualmente)
    if partida.noticia_1 and partida.noticia_1.strip():
        impacto = partida.noticia_1_impacto if partida.noticia_1_impacto else 0
        observacoes.append({
            "texto": f"🗞️ {partida.noticia_1}",
            "impacto": impacto
        })
    
    if partida.noticia_2 and partida.noticia_2.strip():
        impacto = partida.noticia_2_impacto if partida.noticia_2_impacto else 0
        observacoes.append({
            "texto": f"🗞️ {partida.noticia_2}",
            "impacto": impacto
        })
    
    if partida.noticia_3 and partida.noticia_3.strip():
        impacto = partida.noticia_3_impacto if partida.noticia_3_impacto else 0
        observacoes.append({
            "texto": f"🗞️ {partida.noticia_3}",
            "impacto": impacto
        })
    
    # 11. Adicionar observações contextuais manuais do usuário (se existirem)
    if partida.observacoes_contextuais:
        for obs in partida.observacoes_contextuais:
            # Se for dict com texto e impacto
            if isinstance(obs, dict):
                texto = obs.get("texto", "")
                impacto = obs.get("impacto", 0)
                if texto.strip():
                    observacoes.append({
                        "texto": f"ℹ️ {texto}",
                        "impacto": impacto
                    })
            # Se for string (compatibilidade com versão antiga)
            elif isinstance(obs, str) and obs.strip():
                observacoes.append({
                    "texto": f"ℹ️ {obs}",
                    "impacto": 0
                })
    
    return observacoes


def calcular_scores_independentes(partida: Partida) -> Dict[str, Any]:
    """
    VERSÃO 2.0: Calcula scores independentes para Casa, Empate e Fora
    Usa os 7 fatores com pesos ajustados que somam 100%
    """
    
    # ====== CÁLCULO DOS SCORES BASE (0-10) ======
    
    # 1. Forma recente (25%)
    score_forma_casa = calcular_score_forma(partida.forma_casa)
    score_forma_fora = calcular_score_forma(partida.forma_fora)
    
    # 2. Força do elenco (15%) - combinação de artilheiro + lesões (separado para casa e fora)
    # Casa
    artilheiro_casa = partida.artilheiro_disponivel_casa if partida.artilheiro_disponivel_casa is not None else partida.artilheiro_disponivel if partida.artilheiro_disponivel is not None else True
    lesoes_casa = partida.lesoes_suspensoes_casa if partida.lesoes_suspensoes_casa else partida.lesoes_suspensoes if partida.lesoes_suspensoes else "Nenhuma"
    score_artilheiro_casa = calcular_score_artilheiro(artilheiro_casa)
    score_lesoes_casa = calcular_score_lesoes(lesoes_casa)
    score_forca_elenco_casa = (score_artilheiro_casa + score_lesoes_casa) / 2
    
    # Fora
    artilheiro_fora = partida.artilheiro_disponivel_fora if partida.artilheiro_disponivel_fora is not None else partida.artilheiro_disponivel if partida.artilheiro_disponivel is not None else True
    lesoes_fora = partida.lesoes_suspensoes_fora if partida.lesoes_suspensoes_fora else partida.lesoes_suspensoes if partida.lesoes_suspensoes else "Nenhuma"
    score_artilheiro_fora = calcular_score_artilheiro(artilheiro_fora)
    score_lesoes_fora = calcular_score_lesoes(lesoes_fora)
    score_forca_elenco_fora = (score_artilheiro_fora + score_lesoes_fora) / 2
    
    # 3. Desempenho casa/fora (15%) - baseado em média de gols
    score_desempenho_casa = calcular_score_xg(partida.media_gols_marcados_casa, partida.media_gols_sofridos_casa)
    score_desempenho_fora = calcular_score_xg(partida.media_gols_marcados_fora, partida.media_gols_sofridos_fora)
    
    # 4. Histórico H2H (15%)
    score_h2h_casa = calcular_score_h2h(partida.historico_h2h, "casa")
    score_h2h_fora = 10 - score_h2h_casa
    
    # 5. Motivação/contexto (10%) - combinar notícias
    noticias_combinadas = ""
    if partida.noticia_1:
        noticias_combinadas += partida.noticia_1 + " "
    if partida.noticia_2:
        noticias_combinadas += partida.noticia_2 + " "
    if partida.noticia_3:
        noticias_combinadas += partida.noticia_3 + " "
    if partida.noticias_relevantes:
        noticias_combinadas += partida.noticias_relevantes
    
    score_motivacao = calcular_score_motivacao(noticias_combinadas.strip())
    
    # 6. Notas do analista (10%) - baseado em múltiplos fatores
    score_arbitro = calcular_score_arbitro(partida.media_cartoes_arbitro)
    
    # 7. Notícias/contexto externo (10%)
    score_contexto = calcular_score_condicoes(partida.condicoes_externas)
    
    # ====== PESOS VERSÃO 2.0 (somam 100%) ======
    PESO_FORMA = 0.25
    PESO_FORCA_ELENCO = 0.15
    PESO_DESEMPENHO = 0.15
    PESO_H2H = 0.15
    PESO_MOTIVACAO = 0.10
    PESO_ANALISTA = 0.10
    PESO_CONTEXTO = 0.10
    
    # ====== CÁLCULO SCORE CASA (0-100) ======
    score_casa = (
        score_forma_casa * PESO_FORMA * 10 +
        score_forca_elenco_casa * PESO_FORCA_ELENCO * 10 +
        score_desempenho_casa * PESO_DESEMPENHO * 10 +
        score_h2h_casa * PESO_H2H * 10 +
        score_motivacao * PESO_MOTIVACAO * 10 +
        score_arbitro * PESO_ANALISTA * 10 +
        score_contexto * PESO_CONTEXTO * 10
    )
    
    # ====== CÁLCULO SCORE FORA (0-100) ======
    score_fora = (
        score_forma_fora * PESO_FORMA * 10 +
        score_forca_elenco_fora * PESO_FORCA_ELENCO * 10 +
        score_desempenho_fora * PESO_DESEMPENHO * 10 +
        score_h2h_fora * PESO_H2H * 10 +
        score_motivacao * PESO_MOTIVACAO * 10 +
        score_arbitro * PESO_ANALISTA * 10 +
        score_contexto * PESO_CONTEXTO * 10
    )
    
    # ====== CÁLCULO SCORE EMPATE (0-100) ======
    # Empate favorecido quando times estão equilibrados
    diferenca_forma = abs(score_forma_casa - score_forma_fora)
    diferenca_desempenho = abs(score_desempenho_casa - score_desempenho_fora)
    
    # Quanto menor a diferença, maior o score do empate
    score_forma_empate = 10 - diferenca_forma
    score_desempenho_empate = 10 - diferenca_desempenho
    score_h2h_empate = 5.0  # Neutro
    
    # Média da força do elenco para empate
    score_forca_elenco_empate = (score_forca_elenco_casa + score_forca_elenco_fora) / 2
    
    score_empate = (
        score_forma_empate * PESO_FORMA * 10 +
        score_forca_elenco_empate * PESO_FORCA_ELENCO * 10 +
        score_desempenho_empate * PESO_DESEMPENHO * 10 +
        score_h2h_empate * PESO_H2H * 10 +
        score_motivacao * PESO_MOTIVACAO * 10 +
        score_arbitro * PESO_ANALISTA * 10 +
        score_contexto * PESO_CONTEXTO * 10
    )
    
    # ====== NORMALIZAÇÃO PARA SOMAR 100% ======
    total_scores = score_casa + score_empate + score_fora
    
    if total_scores > 0:
        prob_casa = (score_casa / total_scores) * 100
        prob_empate = (score_empate / total_scores) * 100
        prob_fora = (score_fora / total_scores) * 100
    else:
        # Fallback para caso extremo
        prob_casa = prob_empate = prob_fora = 33.33
    
    # Arredonda e garante soma exata de 100%
    prob_casa = round(prob_casa, 2)
    prob_empate = round(prob_empate, 2)
    prob_fora = round(100 - prob_casa - prob_empate, 2)
    
    # ====== CÁLCULO DA CONFIANÇA (VERSÃO 2.0 - Limite 5%) ======
    probabilidades = [prob_casa, prob_empate, prob_fora]
    prob_max = max(probabilidades)
    prob_segunda = sorted(probabilidades, reverse=True)[1]
    diferenca = prob_max - prob_segunda
    
    # Novo sistema: diferença < 5% = Sem recomendação segura
    if diferenca < 5:
        confianca = "Sem recomendação segura"
        resultado_previsto = "Sem recomendação"
    else:
        if diferenca >= 20:
            confianca = "Alta"
        elif diferenca >= 10:
            confianca = "Média"
        else:
            confianca = "Baixa"
        
        # ====== IDENTIFICAR RESULTADO PREVISTO ======
        if prob_casa > prob_empate and prob_casa > prob_fora:
            resultado_previsto = "Casa"
        elif prob_fora > prob_casa and prob_fora > prob_empate:
            resultado_previsto = "Fora"
        else:
            resultado_previsto = "Empate"
    
    # ====== DETALHES DOS FATORES ======
    detalhes_casa = {
        "forma_recente": round(score_forma_casa, 2),
        "forca_elenco": round(score_forca_elenco_casa, 2),
        "desempenho_casa_fora": round(score_desempenho_casa, 2),
        "historico_h2h": round(score_h2h_casa, 2),
        "motivacao_contexto": round(score_motivacao, 2),
        "notas_analista": round(score_arbitro, 2),
        "contexto_externo": round(score_contexto, 2)
    }
    
    detalhes_fora = {
        "forma_recente": round(score_forma_fora, 2),
        "forca_elenco": round(score_forca_elenco_fora, 2),
        "desempenho_casa_fora": round(score_desempenho_fora, 2),
        "historico_h2h": round(score_h2h_fora, 2),
        "motivacao_contexto": round(score_motivacao, 2),
        "notas_analista": round(score_arbitro, 2),
        "contexto_externo": round(score_contexto, 2)
    }
    
    # ====== DETALHES PONDERADOS (com peso e valor ponderado) ======
    pesos_dict = {
        "forma_recente": PESO_FORMA * 100,  # 25%
        "forca_elenco": PESO_FORCA_ELENCO * 100,  # 15%
        "desempenho_casa_fora": PESO_DESEMPENHO * 100,  # 15%
        "historico_h2h": PESO_H2H * 100,  # 15%
        "motivacao_contexto": PESO_MOTIVACAO * 100,  # 10%
        "notas_analista": PESO_ANALISTA * 100,  # 10%
        "contexto_externo": PESO_CONTEXTO * 100  # 10%
    }
    
    detalhes_casa_ponderados = {}
    for fator, nota in detalhes_casa.items():
        peso = pesos_dict[fator]
        ponderado = round((nota * peso) / 10, 2)  # Valor ponderado
        detalhes_casa_ponderados[fator] = {
            "nota": nota,
            "peso": peso,
            "ponderado": ponderado
        }
    
    detalhes_fora_ponderados = {}
    for fator, nota in detalhes_fora.items():
        peso = pesos_dict[fator]
        ponderado = round((nota * peso) / 10, 2)  # Valor ponderado
        detalhes_fora_ponderados[fator] = {
            "nota": nota,
            "peso": peso,
            "ponderado": ponderado
        }
    
    return {
        "probabilidade_casa": prob_casa,
        "probabilidade_empate": prob_empate,
        "probabilidade_fora": prob_fora,
        "resultado_previsto": resultado_previsto,
        "confianca": confianca,
        "diferenca_probabilidade": round(diferenca, 2),
        "detalhes_casa": detalhes_casa,
        "detalhes_fora": detalhes_fora,
        "detalhes_casa_ponderados": detalhes_casa_ponderados,
        "detalhes_fora_ponderados": detalhes_fora_ponderados,
        "scores_brutos": {
            "casa": round(score_casa, 2),
            "empate": round(score_empate, 2),
            "fora": round(score_fora, 2)
        }
    }


def calcular_score_total_mercado(partida: Partida, mercado: str) -> Dict[str, Any]:
    """
    Mantido para compatibilidade com versão antiga
    Calcula o score total ponderado para um mercado específico
    """
    # Scores base (0-10)
    score_forma_casa = calcular_score_forma(partida.forma_casa)
    score_forma_fora = calcular_score_forma(partida.forma_fora)
    score_h2h_casa = calcular_score_h2h(partida.historico_h2h, "casa")
    score_artilheiro = calcular_score_artilheiro(partida.artilheiro_disponivel)
    score_lesoes = calcular_score_lesoes(partida.lesoes_suspensoes)
    score_arbitro = calcular_score_arbitro(partida.media_cartoes_arbitro)
    score_motivacao = calcular_score_motivacao(partida.noticias_relevantes)
    score_condicoes = calcular_score_condicoes(partida.condicoes_externas)
    score_xg_casa = calcular_score_xg(partida.media_gols_marcados_casa, partida.media_gols_sofridos_casa)
    score_xg_fora = calcular_score_xg(partida.media_gols_marcados_fora, partida.media_gols_sofridos_fora)
    
    # Ajusta scores conforme o mercado
    if mercado == "Casa":
        score_forma = score_forma_casa
        score_h2h = score_h2h_casa
        score_xg = score_xg_casa
    elif mercado == "Fora":
        score_forma = score_forma_fora
        score_h2h = 10 - score_h2h_casa
        score_xg = score_xg_fora
    elif mercado == "Empate":
        score_forma = (score_forma_casa + score_forma_fora) / 2
        score_h2h = 5.0
        score_xg = 5.0
    else:
        score_forma = (score_forma_casa + score_forma_fora) / 2
        score_h2h = 5.0
        score_xg = (score_xg_casa + score_xg_fora) / 2
    
    # Pesos
    pesos = {
        "forma_recente": 0.25,
        "historico_h2h": 0.15,
        "escalacao_artilheiro": 0.15,
        "lesoes_suspensoes": 0.15,
        "motivacao": 0.10,
        "arbitro": 0.10,
        "condicoes_externas": 0.10,
    }
    
    # Calcula score total ponderado (0-100)
    score_total = (
        score_forma * pesos["forma_recente"] * 10 +
        score_h2h * pesos["historico_h2h"] * 10 +
        score_artilheiro * pesos["escalacao_artilheiro"] * 10 +
        score_lesoes * pesos["lesoes_suspensoes"] * 10 +
        score_motivacao * pesos["motivacao"] * 10 +
        score_arbitro * pesos["arbitro"] * 10 +
        score_condicoes * pesos["condicoes_externas"] * 10
    )
    
    detalhes = {
        "forma_recente": score_forma,
        "historico_h2h": score_h2h,
        "escalacao_artilheiro": score_artilheiro,
        "lesoes_suspensoes": score_lesoes,
        "arbitro": score_arbitro,
        "motivacao": score_motivacao,
        "condicoes_externas": score_condicoes,
        "xg_xga": score_xg
    }
    
    return {"score_total": round(score_total, 2), "detalhes": detalhes}


def gerar_justificativa(partida: Partida, mercado: str, analise_data: Dict) -> str:
    """Gera justificativa textual automática (versão antiga mantida para compatibilidade)"""
    # Fatores positivos
    detalhes = analise_data["detalhes"]
    positivos = []
    negativos = []
    
    if detalhes["forma_recente"] >= 7:
        if "Casa" in mercado:
            positivos.append(f"✓ {partida.time_casa} em boa forma recente ({partida.forma_casa})")
        elif "Fora" in mercado:
            positivos.append(f"✓ {partida.time_visitante} em boa forma fora de casa ({partida.forma_fora})")
    
    if detalhes["escalacao_artilheiro"] >= 7:
        positivos.append("✓ Artilheiro confirmado na escalação")
    else:
        negativos.append("⚠ Artilheiro indisponível")
    
    if detalhes["lesoes_suspensoes"] >= 7:
        positivos.append("✓ Elenco praticamente completo")
    else:
        negativos.append(f"⚠ Desfalques importantes: {partida.lesoes_suspensoes}")
    
    if detalhes["condicoes_externas"] >= 7:
        positivos.append(f"✓ Boas condições externas: {partida.condicoes_externas}")
    elif detalhes["condicoes_externas"] < 5:
        negativos.append(f"⚠ Condições adversas: {partida.condicoes_externas}")
    
    if partida.noticias_relevantes:
        if detalhes["motivacao"] >= 6:
            positivos.append(f"✓ Contexto favorável: {partida.noticias_relevantes}")
        else:
            negativos.append(f"⚠ Contexto desfavorável: {partida.noticias_relevantes}")
    
    justificativa_texto = "\n".join(positivos)
    if negativos:
        justificativa_texto += "\n\n" + "\n".join(negativos)
    
    return justificativa_texto


def calcular_probabilidade(score_total: float) -> float:
    """Converte score em probabilidade usando função sigmoid"""
    prob = 100 / (1 + math.exp(-(score_total - 50) / 10))
    return round(prob, 2)


def classificar_probabilidade(prob: float) -> str:
    """Classifica a probabilidade"""
    if prob < 50:
        return "Baixa"
    elif prob < 65:
        return "Média"
    elif prob < 80:
        return "Alta"
    else:
        return "Muito Alta"


def calcular_ev(prob: float, odd: float) -> float:
    """Calcula o valor esperado"""
    ev = (prob / 100 * odd) - 1
    return round(ev, 4)


def classificar_ev(ev: float) -> str:
    """Classifica o EV"""
    if ev <= 0:
        return "Sem valor"
    elif ev <= 0.10:
        return "Valor Moderado"
    else:
        return "Alto Valor"


def gerar_justificativa_1x2(partida: Partida, analise_data: Dict) -> str:
    """
    VERSÃO 2.0 APRIMORADA: Gera justificativa natural e descritiva
    Foca na explicação qualitativa sem repetir números excessivamente
    """
    resultado = analise_data["resultado_previsto"]
    confianca = analise_data["confianca"]
    diferenca = analise_data["diferenca_probabilidade"]
    
    # Caso sem recomendação segura
    if confianca == "Sem recomendação segura":
        return (
            f"Os times estão extremamente equilibrados estatisticamente. "
            f"A diferença entre os resultados mais prováveis é de apenas {diferenca:.2f}%, "
            f"o que torna qualquer previsão insegura. "
            f"Não há vantagem clara para nenhum dos lados nesta partida."
        )
    
    # Seleciona detalhes do time correto
    if resultado == "Casa":
        detalhes = analise_data["detalhes_casa"]
        detalhes_oponente = analise_data["detalhes_fora"]
        time_favorito = partida.time_casa
        time_oponente = partida.time_visitante
        local = "em casa"
    elif resultado == "Fora":
        detalhes = analise_data["detalhes_fora"]
        detalhes_oponente = analise_data["detalhes_casa"]
        time_favorito = partida.time_visitante
        time_oponente = partida.time_casa
        local = "fora de casa"
    else:
        # Empate
        justificativa = (
            f"A análise estatística indica grande equilíbrio entre {partida.time_casa} e {partida.time_visitante}. "
            f"Ambos os times apresentam características similares nos principais fatores analisados. "
        )
        
        # Verifica histórico
        if "empate" in partida.historico_h2h.lower() or "e" in partida.historico_h2h.upper():
            justificativa += f"O histórico de confrontos diretos reforça a tendência de igualdade. "
        
        # Confiança
        if confianca == "Baixa":
            justificativa += f"No entanto, a confiança é baixa ({diferenca:.2f}%), indicando que o resultado ainda é incerto."
        else:
            justificativa += f"A confiança na previsão de empate é {confianca.lower()} ({diferenca:.2f}%)."
        
        return justificativa
    
    # Monta justificativa natural para vitória
    justificativa = f"O {time_favorito} apresenta "
    
    # Analisa forma recente
    if detalhes["forma_recente"] >= 7:
        vitorias = partida.forma_casa.upper().count('V') if resultado == "Casa" else partida.forma_fora.upper().count('V')
        justificativa += f"excelente momento com forma recente superior"
        if vitorias >= 3:
            justificativa += f" (sequência invicta)"
        justificativa += ", "
    elif detalhes["forma_recente"] >= 5:
        justificativa += "forma recente estável, "
    
    # Analisa desempenho específico
    if detalhes["desempenho_casa_fora"] >= 7:
        justificativa += f"forte desempenho jogando {local} "
        if resultado == "Casa":
            justificativa += f"com média de {partida.media_gols_marcados_casa:.1f} gols marcados"
        else:
            justificativa += f"com média de {partida.media_gols_marcados_fora:.1f} gols marcados"
        justificativa += ", "
    
    # Analisa força do elenco
    if detalhes["forca_elenco"] >= 7:
        justificativa += "e elenco bem estruturado. "
    else:
        justificativa += "mas enfrenta problemas no elenco. "
    
    # Compara com oponente
    diferenca_forma = detalhes["forma_recente"] - detalhes_oponente["forma_recente"]
    diferenca_desempenho = detalhes["desempenho_casa_fora"] - detalhes_oponente["desempenho_casa_fora"]
    
    if diferenca_forma >= 2 or diferenca_desempenho >= 2:
        justificativa += f"Em contraste, o {time_oponente} "
        
        if detalhes_oponente["forma_recente"] < 5:
            justificativa += "passa por momento irregular "
        
        if detalhes_oponente["desempenho_casa_fora"] < 5:
            local_oponente = "fora de casa" if resultado == "Casa" else "em casa"
            justificativa += f"e apresenta dificuldades jogando {local_oponente}. "
        else:
            justificativa += "mas mantém desempenho razoável. "
    else:
        justificativa += f"O {time_oponente} também apresenta bom desempenho, "
        justificativa += f"o que reduz a margem de vantagem do favorito. "
    
    # Adiciona contexto de confiança
    if confianca == "Alta":
        justificativa += f"A diferença de {diferenca:.2f}% entre as probabilidades indica alta confiança na previsão."
    elif confianca == "Média":
        justificativa += f"A diferença de {diferenca:.2f}% sugere vantagem moderada, com confiança média na previsão."
    else:
        justificativa += f"Apesar da leve vantagem estatística, a diferença de apenas {diferenca:.2f}% indica baixa confiança no resultado."
    
    return justificativa
    if partida.noticia_2:
        noticias.append(partida.noticia_2)
    if partida.noticia_3:
        noticias.append(partida.noticia_3)
    if partida.noticias_relevantes:
        noticias.append(partida.noticias_relevantes)
    
    if noticias:
        justificativa += "\n**Contexto e Notícias:**\n"
        for i, noticia in enumerate(noticias[:3], 1):
            justificativa += f"ℹ️ {i}. {noticia}\n"
    
    return justificativa


def analisar_mercado(partida: Partida, mercado: str, odd: float) -> Analise:
    """Analisa um mercado específico"""
    analise_data = calcular_score_total_mercado(partida, mercado)
    score_total = analise_data["score_total"]
    
    prob = calcular_probabilidade(score_total)
    class_prob = classificar_probabilidade(prob)
    ev = calcular_ev(prob, odd)
    class_ev = classificar_ev(ev)
    
    if ev > 0.10:
        recomendacao = "✅ Aposta de alto valor"
    elif ev > 0:
        recomendacao = "⚡ Aposta de valor moderado"
    else:
        recomendacao = "❌ Não recomendada"
    
    justificativa = gerar_justificativa(partida, mercado, analise_data)
    
    return Analise(
        mercado=mercado,
        probabilidade=prob,
        classificacao_prob=class_prob,
        odd=odd,
        ev=ev,
        classificacao_ev=class_ev,
        recomendacao=recomendacao,
        justificativa=justificativa,
        score_total=score_total,
        detalhes_scores=analise_data["detalhes"]
    )


def analisar_1x2_v2(partida: Partida) -> Analise1X2:
    """
    VERSÃO 2.0: Analisa mercado 1X2 com probabilidades normalizadas
    """
    # Calcula probabilidades coerentes
    analise_data = calcular_scores_independentes(partida)
    
    # Calcula EV (Expected Value) para cada mercado
    prob_casa = analise_data["probabilidade_casa"]
    prob_empate = analise_data["probabilidade_empate"]
    prob_fora = analise_data["probabilidade_fora"]
    
    ev_casa = calcular_ev(prob_casa, partida.odd_casa)
    ev_empate = calcular_ev(prob_empate, partida.odd_empate)
    ev_fora = calcular_ev(prob_fora, partida.odd_fora)
    
    # Gera justificativa
    justificativa = gerar_justificativa_1x2(partida, analise_data)
    
    # Gera observações contextuais automáticas
    observacoes = gerar_observacoes_contextuais(partida, analise_data)
    observacoes_formatadas = [
        ObservacaoContextual(texto=obs["texto"], impacto=obs["impacto"])
        for obs in observacoes
    ]
    
    return Analise1X2(
        probabilidade_casa=prob_casa,
        probabilidade_empate=prob_empate,
        probabilidade_fora=prob_fora,
        resultado_previsto=analise_data["resultado_previsto"],
        confianca=analise_data["confianca"],
        diferenca_probabilidade=analise_data["diferenca_probabilidade"],
        justificativa=justificativa,
        detalhes_casa=analise_data["detalhes_casa"],
        detalhes_fora=analise_data["detalhes_fora"],
        detalhes_casa_ponderados=analise_data["detalhes_casa_ponderados"],
        detalhes_fora_ponderados=analise_data["detalhes_fora_ponderados"],
        scores_brutos=analise_data["scores_brutos"],
        ev_casa=ev_casa,
        ev_empate=ev_empate,
        ev_fora=ev_fora,
        observacoes_contextuais=observacoes_formatadas
    )


def analisar_partida_completa(partida: Partida) -> AnaliseCompleta:
    """Analisa todos os mercados e retorna a melhor recomendação (mantido para compatibilidade)"""
    
    # Define mercados e odds
    mercados = [
        ("Casa", partida.odd_casa),
        ("Empate", partida.odd_empate),
        ("Fora", partida.odd_fora),
        ("Casa ou Empate", 1.30),  # Odds estimadas
        ("Fora ou Empate", 1.50),
        ("Casa ou Fora", 1.25),
        ("Ambos Marcam", 1.85),
        ("Acima 1.5 gols", 1.50),
        ("Acima 2.5 gols", 2.00),
        ("Abaixo 2.5 gols", 1.70)
    ]
    
    analises = []
    for mercado, odd in mercados:
        analise = analisar_mercado(partida, mercado, odd)
        analises.append(analise)
    
    # Ordena por EV (maior primeiro)
    analises_ordenadas = sorted(analises, key=lambda x: x.ev, reverse=True)
    melhor = analises_ordenadas[0]
    
    return AnaliseCompleta(
        partida=partida,
        melhor_recomendacao=melhor,
        todas_analises=analises_ordenadas
    )


def analisar_partida_v2(partida: Partida) -> AnaliseCompletaV2:
    """
    VERSÃO 2.0: Análise completa com foco em 1X2 coerente
    """
    analise_1x2 = analisar_1x2_v2(partida)
    
    return AnaliseCompletaV2(
        partida=partida,
        analise_1x2=analise_1x2,
        outras_analises=None  # Será expandido futuramente
    )


# ================ ROUTES ================

@api_router.get("/")
async def root():
    return {"message": "API de Análise de Apostas Esportivas"}


@api_router.post("/partidas", response_model=Partida)
async def criar_partida(input: PartidaCreate):
    """Cria uma nova partida"""
    partida = Partida(**input.model_dump())
    doc = partida.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    
    await db.partidas.insert_one(doc)
    return partida


@api_router.get("/partidas", response_model=List[Partida])
async def listar_partidas():
    """Lista todas as partidas"""
    partidas = await db.partidas.find({}, {"_id": 0}).to_list(1000)
    
    for partida in partidas:
        if isinstance(partida['criado_em'], str):
            partida['criado_em'] = datetime.fromisoformat(partida['criado_em'])
    
    return partidas


@api_router.get("/partidas/{partida_id}", response_model=Partida)
async def buscar_partida(partida_id: str):
    """Busca uma partida por ID"""
    partida = await db.partidas.find_one({"id": partida_id}, {"_id": 0})
    
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    if isinstance(partida['criado_em'], str):
        partida['criado_em'] = datetime.fromisoformat(partida['criado_em'])
    
    return partida


@api_router.put("/partidas/{partida_id}", response_model=Partida)
async def atualizar_partida(partida_id: str, input: PartidaCreate):
    """Atualiza uma partida existente"""
    partida_existente = await db.partidas.find_one({"id": partida_id})
    
    if not partida_existente:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    partida_atualizada = Partida(id=partida_id, **input.model_dump())
    doc = partida_atualizada.model_dump()
    doc['criado_em'] = doc['criado_em'].isoformat()
    
    await db.partidas.update_one({"id": partida_id}, {"$set": doc})
    return partida_atualizada


@api_router.delete("/partidas/{partida_id}")
async def deletar_partida(partida_id: str):
    """Deleta uma partida"""
    result = await db.partidas.delete_one({"id": partida_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    return {"message": "Partida deletada com sucesso"}


# Endpoint antigo removido - usar /analise-v2


@api_router.get("/partidas/{partida_id}/analise-v2", response_model=AnaliseCompletaV2)
async def analisar_partida_v2_endpoint(partida_id: str):
    """
    VERSÃO 2.0: Análise com probabilidades normalizadas e coerentes
    - Probabilidades Casa + Empate + Fora = 100%
    - Sistema de confiança (Alta/Média/Baixa)
    - Justificativa automática detalhada
    - Análise de valor esperado (EV)
    """
    partida_dict = await db.partidas.find_one({"id": partida_id}, {"_id": 0})
    
    if not partida_dict:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    if isinstance(partida_dict['criado_em'], str):
        partida_dict['criado_em'] = datetime.fromisoformat(partida_dict['criado_em'])
    
    partida = Partida(**partida_dict)
    analise = analisar_partida_v2(partida)
    
    return analise


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()