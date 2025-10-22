import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, TrendingUp, AlertCircle, Target, BarChart3 } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const DetalhesPartidaV2 = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analise, setAnalise] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarAnalise();
  }, [id]);

  const carregarAnalise = async () => {
    try {
      const response = await axios.get(`${API}/partidas/${id}/analise-v2`);
      setAnalise(response.data);
    } catch (error) {
      console.error("Erro ao carregar análise:", error);
      toast.error("Erro ao carregar análise");
    } finally {
      setLoading(false);
    }
  };

  const getConfiancaCor = (confianca) => {
    if (confianca === "Sem recomendação segura") {
      return "bg-red-100 text-red-800 border-red-300";
    }
    switch (confianca) {
      case "Alta":
        return "bg-emerald-100 text-emerald-800 border-emerald-300";
      case "Média":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "Baixa":
        return "bg-orange-100 text-orange-800 border-orange-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const getConfiancaPercentual = (confianca) => {
    if (confianca === "Sem recomendação segura") return 0;
    if (confianca === "Baixa") return 35;
    if (confianca === "Média") return 65;
    if (confianca === "Alta") return 90;
    return 50;
  };

  const formatarDataHora = (dataHora) => {
    if (!dataHora) return null;
    try {
      const date = new Date(dataHora);
      return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dataHora;
    }
  };

  const formatarDataHoraCompacta = (dataHora) => {
    if (!dataHora) return null;
    try {
      const date = new Date(dataHora);
      const dia = date.getDate().toString().padStart(2, '0');
      const mes = (date.getMonth() + 1).toString().padStart(2, '0');
      const hora = date.getHours().toString().padStart(2, '0');
      const minuto = date.getMinutes().toString().padStart(2, '0');
      return `${dia}/${mes} ${hora}:${minuto}`;
    } catch {
      return dataHora;
    }
  };

  const gerarCabecalhoPartida = () => {
    const partes = [];
    if (partida.campeonato) partes.push(partida.campeonato);
    if (partida.rodada) partes.push(`Rodada ${partida.rodada}`);
    partes.push(`${partida.time_casa} vs ${partida.time_visitante}`);
    if (partida.data_hora) partes.push(formatarDataHoraCompacta(partida.data_hora));
    if (partida.local_estadio) partes.push(partida.local_estadio);
    return partes.join(' – ');
  };

  const getResultadoCor = (resultado) => {
    switch (resultado) {
      case "Casa":
        return "text-blue-700";
      case "Empate":
        return "text-gray-700";
      case "Fora":
        return "text-purple-700";
      default:
        return "text-gray-700";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mb-4"></div>
          <p className="text-gray-600">Gerando análise versão 2.0...</p>
        </div>
      </div>
    );
  }

  if (!analise) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Análise não encontrada</h3>
          <Button onClick={() => navigate("/")} className="mt-4">
            Voltar ao Dashboard
          </Button>
        </div>
      </div>
    );
  }

  const { partida, analise_1x2 } = analise;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b-2 border-emerald-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-4">
            <Button
              onClick={() => navigate("/")}
              variant="outline"
              className="border-gray-300 hover:bg-gray-100"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="outline" className="text-purple-700 border-purple-300 font-semibold">
                  ⚡ Análise 2.0
                </Badge>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold text-gray-900 leading-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                {gerarCabecalhoPartida()}
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Probabilidades Normalizadas - Card Principal */}
          <Card className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 border-2 border-emerald-300 shadow-xl">
            <CardHeader className="border-b-2 border-emerald-100">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div className="flex-1 min-w-[250px]">
                  <CardDescription className="text-emerald-700 font-semibold mb-1 flex items-center gap-2">
                    <Target className="h-4 w-4" />
                    Previsão 1X2 (Probabilidades Coerentes)
                  </CardDescription>
                  <CardTitle className={`text-3xl font-bold ${getResultadoCor(analise_1x2.resultado_previsto)}`}>
                    {analise_1x2.resultado_previsto}
                  </CardTitle>
                  <div className="mt-2">
                    <Badge className={`${getConfiancaCor(analise_1x2.confianca)} text-base px-3 py-1 font-bold`}>
                      {analise_1x2.confianca}
                    </Badge>
                  </div>
                  <div className="text-xs text-gray-600 mt-2">
                    Diferença entre 1º e 2º: {analise_1x2.diferenca_probabilidade}%
                  </div>
                </div>
                
                {/* Gauge de Confiança */}
                <div className="flex flex-col items-center">
                  <div className="relative w-32 h-32">
                    <svg className="transform -rotate-90 w-32 h-32">
                      {/* Círculo de fundo */}
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        stroke="#e5e7eb"
                        strokeWidth="12"
                        fill="none"
                      />
                      {/* Círculo de progresso */}
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        stroke={
                          analise_1x2.confianca === "Alta" ? "#10b981" :
                          analise_1x2.confianca === "Média" ? "#f59e0b" :
                          analise_1x2.confianca === "Baixa" ? "#f97316" :
                          "#ef4444"
                        }
                        strokeWidth="12"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 56}`}
                        strokeDashoffset={`${2 * Math.PI * 56 * (1 - getConfiancaPercentual(analise_1x2.confianca) / 100)}`}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out"
                      />
                    </svg>
                    {/* Texto central */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-2xl font-bold text-gray-900">
                        {getConfiancaPercentual(analise_1x2.confianca)}%
                      </span>
                      <span className="text-xs text-gray-600">Confiança</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-6">
              {/* Gráfico de Barras de Probabilidades */}
              <div className="space-y-4 mb-6">
                <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-emerald-600" />
                  Probabilidades (soma = 100%)
                </h3>
                
                {/* Casa */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">
                      🏠 Vitória {partida.time_casa}
                    </span>
                    <span className="text-lg font-bold text-blue-700">
                      {analise_1x2.probabilidade_casa}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-blue-600 h-8 rounded-full flex items-center justify-end pr-3 transition-all duration-500"
                      style={{ width: `${analise_1x2.probabilidade_casa}%` }}
                    >
                      {analise_1x2.probabilidade_casa > 15 && (
                        <span className="text-white text-xs font-bold">
                          {analise_1x2.probabilidade_casa}%
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Empate */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">
                      🤝 Empate
                    </span>
                    <span className="text-lg font-bold text-gray-700">
                      {analise_1x2.probabilidade_empate}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-gray-400 to-gray-500 h-8 rounded-full flex items-center justify-end pr-3 transition-all duration-500"
                      style={{ width: `${analise_1x2.probabilidade_empate}%` }}
                    >
                      {analise_1x2.probabilidade_empate > 15 && (
                        <span className="text-white text-xs font-bold">
                          {analise_1x2.probabilidade_empate}%
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Fora */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">
                      ✈️ Vitória {partida.time_visitante}
                    </span>
                    <span className="text-lg font-bold text-purple-700">
                      {analise_1x2.probabilidade_fora}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-purple-500 to-purple-600 h-8 rounded-full flex items-center justify-end pr-3 transition-all duration-500"
                      style={{ width: `${analise_1x2.probabilidade_fora}%` }}
                    >
                      {analise_1x2.probabilidade_fora > 15 && (
                        <span className="text-white text-xs font-bold">
                          {analise_1x2.probabilidade_fora}%
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Análise de Valor (EV) */}
              <div className="bg-white rounded-lg p-4 border-2 border-gray-200 mb-4">
                <h4 className="font-semibold text-gray-900 mb-3">💰 Análise de Valor Esperado (EV)</h4>
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-xs text-gray-600 mb-1">Casa (Odd {partida.odd_casa}x)</div>
                    <div className={`text-lg font-bold ${analise_1x2.ev_casa > 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                      {(analise_1x2.ev_casa * 100).toFixed(2)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-600 mb-1">Empate (Odd {partida.odd_empate}x)</div>
                    <div className={`text-lg font-bold ${analise_1x2.ev_empate > 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                      {(analise_1x2.ev_empate * 100).toFixed(2)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-600 mb-1">Fora (Odd {partida.odd_fora}x)</div>
                    <div className={`text-lg font-bold ${analise_1x2.ev_fora > 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                      {(analise_1x2.ev_fora * 100).toFixed(2)}%
                    </div>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">Melhor Aposta:</span>
                    <span className="text-base font-bold text-emerald-700">{analise_1x2.melhor_aposta}</span>
                  </div>
                </div>
              </div>

              {/* Justificativa */}
              <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-5 border-2 border-blue-200">
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-blue-600" />
                  Justificativa da Análise
                </h4>
                <div className="text-sm text-gray-800 whitespace-pre-line leading-relaxed">
                  {analise_1x2.justificativa}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tabs */}
          <Tabs defaultValue="fatores" className="w-full">
            <TabsList className="grid w-full grid-cols-2 bg-white border-2 border-gray-200">
              <TabsTrigger value="fatores">Fatores de Análise</TabsTrigger>
              <TabsTrigger value="dados">Dados da Partida</TabsTrigger>
            </TabsList>

            {/* Fatores de Análise */}
            <TabsContent value="fatores" className="space-y-4">
              <Card className="bg-white">
                <CardHeader>
                  <CardTitle className="text-emerald-700">Detalhes dos Fatores (Time da Casa)</CardTitle>
                  <CardDescription>Scores individuais (0-10) que influenciaram a previsão</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(analise_1x2.detalhes_casa).map(([fator, score]) => {
                      const percentage = (score / 10) * 100;
                      let cor = "bg-red-500";
                      if (score >= 7) cor = "bg-emerald-500";
                      else if (score >= 5) cor = "bg-yellow-500";
                      
                      return (
                        <div key={fator} className="flex items-center gap-4">
                          <div className="flex-1">
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium text-gray-700 capitalize">
                                {fator.replace(/_/g, " ")}
                              </span>
                              <span className="text-sm font-bold text-gray-900">{score}/10</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3">
                              <div
                                className={`${cor} h-3 rounded-full transition-all`}
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white">
                <CardHeader>
                  <CardTitle className="text-purple-700">Detalhes dos Fatores (Time Visitante)</CardTitle>
                  <CardDescription>Scores individuais (0-10) que influenciaram a previsão</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(analise_1x2.detalhes_fora).map(([fator, score]) => {
                      const percentage = (score / 10) * 100;
                      let cor = "bg-red-500";
                      if (score >= 7) cor = "bg-purple-500";
                      else if (score >= 5) cor = "bg-yellow-500";
                      
                      return (
                        <div key={fator} className="flex items-center gap-4">
                          <div className="flex-1">
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium text-gray-700 capitalize">
                                {fator.replace(/_/g, " ")}
                              </span>
                              <span className="text-sm font-bold text-gray-900">{score}/10</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3">
                              <div
                                className={`${cor} h-3 rounded-full transition-all`}
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>

              {/* Scores Brutos */}
              <Card className="bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-300">
                <CardHeader>
                  <CardTitle className="text-gray-700">Scores Brutos (antes da normalização)</CardTitle>
                  <CardDescription>Valores absolutos calculados pelo sistema</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="bg-white rounded-lg p-4 border-2 border-blue-200">
                      <div className="text-xs text-gray-600 mb-1">Casa</div>
                      <div className="text-2xl font-bold text-blue-700">{analise_1x2.scores_brutos.casa}</div>
                    </div>
                    <div className="bg-white rounded-lg p-4 border-2 border-gray-200">
                      <div className="text-xs text-gray-600 mb-1">Empate</div>
                      <div className="text-2xl font-bold text-gray-700">{analise_1x2.scores_brutos.empate}</div>
                    </div>
                    <div className="bg-white rounded-lg p-4 border-2 border-purple-200">
                      <div className="text-xs text-gray-600 mb-1">Fora</div>
                      <div className="text-2xl font-bold text-purple-700">{analise_1x2.scores_brutos.fora}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Dados da Partida */}
            <TabsContent value="dados" className="space-y-4">
              <Card className="bg-white">
                <CardHeader>
                  <CardTitle className="text-emerald-700">Desempenho e Estatísticas</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">🏠 {partida.time_casa}</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Forma:</span>
                          <span className="font-semibold">{partida.forma_casa}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Média Gols Marcados:</span>
                          <span className="font-semibold">{partida.media_gols_marcados_casa}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Média Gols Sofridos:</span>
                          <span className="font-semibold">{partida.media_gols_sofridos_casa}</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">✈️ {partida.time_visitante}</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Forma:</span>
                          <span className="font-semibold">{partida.forma_fora}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Média Gols Marcados:</span>
                          <span className="font-semibold">{partida.media_gols_marcados_fora}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Média Gols Sofridos:</span>
                          <span className="font-semibold">{partida.media_gols_sofridos_fora}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">H2H:</span>
                        <span className="ml-2 font-semibold">{partida.historico_h2h || "Não informado"}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Artilheiro:</span>
                        <span className="ml-2 font-semibold">{partida.artilheiro_disponivel ? "✅ Sim" : "❌ Não"}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Lesões/Suspensões:</span>
                        <span className="ml-2 font-semibold">{partida.lesoes_suspensoes || "Nenhuma"}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Árbitro:</span>
                        <span className="ml-2 font-semibold">{partida.arbitro || "Não informado"}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Média Cartões Árbitro:</span>
                        <span className="ml-2 font-semibold">{partida.media_cartoes_arbitro}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Escalação Definida:</span>
                        <span className="ml-2 font-semibold">{partida.escalacao_definida ? "✅ Sim" : "❌ Não"}</span>
                      </div>
                      <div className="md:col-span-2">
                        <span className="text-gray-600">Condições:</span>
                        <span className="ml-2 font-semibold">{partida.condicoes_externas || "Normais"}</span>
                      </div>
                      <div className="md:col-span-2">
                        <span className="text-gray-600">Notícias:</span>
                        <span className="ml-2 font-semibold">{partida.noticias_relevantes || "Nenhuma"}</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
};

export default DetalhesPartidaV2;
