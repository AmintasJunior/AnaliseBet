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
    # Identificação
    campeonato: str
    rodada: int
    time_casa: str
    time_visitante: str
    
    # Desempenho
    forma_casa: str  # Ex: "V-E-V-D-V"
    forma_fora: str  # Ex: "D-V-E-D-E"
    media_gols_marcados_casa: float
    media_gols_sofridos_casa: float
    media_gols_marcados_fora: float
    media_gols_sofridos_fora: float
    
    # H2H
    historico_h2h: str  # Ex: "3V 2E 1D nos últimos 6"
    
    # Elenco / Tática
    artilheiro_disponivel: bool
    lesoes_suspensoes: str
    escalacao_definida: bool
    
    # Contexto e Condições
    arbitro: str
    media_cartoes_arbitro: float
    condicoes_externas: str
    noticias_relevantes: str
    
    # Odds
    odd_casa: float
    odd_empate: float
    odd_fora: float


class Partida(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    campeonato: str
    rodada: int
    time_casa: str
    time_visitante: str
    forma_casa: str
    forma_fora: str
    media_gols_marcados_casa: float
    media_gols_sofridos_casa: float
    media_gols_marcados_fora: float
    media_gols_sofridos_fora: float
    historico_h2h: str
    artilheiro_disponivel: bool
    lesoes_suspensoes: str
    escalacao_definida: bool
    arbitro: str
    media_cartoes_arbitro: float
    condicoes_externas: str
    noticias_relevantes: str
    odd_casa: float
    odd_empate: float
    odd_fora: float
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


class AnaliseCompleta(BaseModel):
    partida: Partida
    melhor_recomendacao: Analise
    todas_analises: List[Analise]


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


def calcular_score_total_mercado(partida: Partida, mercado: str) -> Dict[str, Any]:
    """Calcula o score total ponderado para um mercado específico"""
    
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
        odd_ref = partida.odd_casa
    elif mercado == "Fora":
        score_forma = score_forma_fora
        score_h2h = 10 - score_h2h_casa
        score_xg = score_xg_fora
        odd_ref = partida.odd_fora
    elif mercado == "Empate":
        score_forma = (score_forma_casa + score_forma_fora) / 2
        score_h2h = 5.0
        score_xg = 5.0
        odd_ref = partida.odd_empate
    elif mercado in ["Casa ou Empate", "Fora ou Empate", "Casa ou Fora"]:
        score_forma = max(score_forma_casa, score_forma_fora)
        score_h2h = 6.0
        score_xg = (score_xg_casa + score_xg_fora) / 2
        odd_ref = 1.5  # Estimativa
    elif mercado == "Ambos Marcam":
        # Para ambos marcarem, queremos ataque forte dos dois lados
        score_forma = (score_forma_casa + score_forma_fora) / 2
        score_h2h = 6.0
        score_xg = min(partida.media_gols_marcados_casa, partida.media_gols_marcados_fora) * 3
        score_xg = min(10, score_xg)
        odd_ref = 2.0
    elif "Acima" in mercado or "Abaixo" in mercado:
        # Para gols, considera o ataque e defesa de ambos
        media_total = partida.media_gols_marcados_casa + partida.media_gols_marcados_fora
        score_forma = (score_forma_casa + score_forma_fora) / 2
        score_h2h = 5.0
        score_xg = min(10, media_total * 2)
        odd_ref = 1.8
    else:
        score_forma = (score_forma_casa + score_forma_fora) / 2
        score_h2h = 5.0
        score_xg = (score_xg_casa + score_xg_fora) / 2
        odd_ref = 2.0
    
    score_odds = calcular_score_odds_implicitas(odd_ref, 2.0)
    
    # Pesos conforme tabela
    pesos = {
        "forma_recente": 0.20,
        "historico_h2h": 0.10,
        "escalacao_artilheiro": 0.15,
        "lesoes_suspensoes": 0.10,
        "arbitro": 0.05,
        "motivacao": 0.05,
        "condicoes_externas": 0.05,
        "noticias": 0.10,
        "odds_implicitas": 0.10,
        "xg_xga": 0.10
    }
    
    # Calcula score total ponderado (0-100)
    score_total = (
        score_forma * pesos["forma_recente"] * 10 +
        score_h2h * pesos["historico_h2h"] * 10 +
        score_artilheiro * pesos["escalacao_artilheiro"] * 10 +
        score_lesoes * pesos["lesoes_suspensoes"] * 10 +
        score_arbitro * pesos["arbitro"] * 10 +
        score_motivacao * pesos["motivacao"] * 10 +
        score_condicoes * pesos["condicoes_externas"] * 10 +
        score_motivacao * pesos["noticias"] * 10 +
        score_odds * pesos["odds_implicitas"] * 10 +
        score_xg * pesos["xg_xga"] * 10
    )
    
    detalhes = {
        "forma_recente": score_forma,
        "historico_h2h": score_h2h,
        "escalacao_artilheiro": score_artilheiro,
        "lesoes_suspensoes": score_lesoes,
        "arbitro": score_arbitro,
        "motivacao": score_motivacao,
        "condicoes_externas": score_condicoes,
        "noticias": score_motivacao,
        "odds_implicitas": score_odds,
        "xg_xga": score_xg
    }
    
    return {"score_total": round(score_total, 2), "detalhes": detalhes}


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


def gerar_justificativa(partida: Partida, mercado: str, analise_data: Dict) -> str:
    """Gera justificativa textual automática"""
    justificativa = []
    
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


def analisar_partida_completa(partida: Partida) -> AnaliseCompleta:
    """Analisa todos os mercados e retorna a melhor recomendação"""
    
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


@api_router.get("/partidas/{partida_id}/analise", response_model=AnaliseCompleta)
async def analisar_partida(partida_id: str):
    """Gera análise completa de uma partida"""
    partida_dict = await db.partidas.find_one({"id": partida_id}, {"_id": 0})
    
    if not partida_dict:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    if isinstance(partida_dict['criado_em'], str):
        partida_dict['criado_em'] = datetime.fromisoformat(partida_dict['criado_em'])
    
    partida = Partida(**partida_dict)
    analise = analisar_partida_completa(partida)
    
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