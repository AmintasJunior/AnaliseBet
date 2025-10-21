import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, TrendingUp, AlertCircle } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const DetalhesPartida = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analise, setAnalise] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarAnalise();
  }, [id]);

  const carregarAnalise = async () => {
    try {
      const response = await axios.get(`${API}/partidas/${id}/analise`);
      setAnalise(response.data);
    } catch (error) {
      console.error("Erro ao carregar análise:", error);
      toast.error("Erro ao carregar análise");
    } finally {
      setLoading(false);
    }
  };

  const getClassificacaoCor = (classificacao) => {
    switch (classificacao) {
      case "Muito Alta":
        return "bg-emerald-100 text-emerald-800 border-emerald-200";
      case "Alta":
        return "bg-green-100 text-green-800 border-green-200";
      case "Média":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "Baixa":
        return "bg-orange-100 text-orange-800 border-orange-200";
      case "Alto Valor":
        return "bg-emerald-100 text-emerald-800 border-emerald-200";
      case "Valor Moderado":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "Sem valor":
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mb-4"></div>
          <p className="text-gray-600">Gerando análise...</p>
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

  const { partida, melhor_recomendacao, todas_analises } = analise;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-4">
            <Button
              onClick={() => navigate("/")}
              variant="outline"
              className="border-gray-300"
              data-testid="voltar-dashboard-btn"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div className="flex-1">
              <div className="text-xs font-semibold text-emerald-700 uppercase tracking-wide mb-1">
                {partida.campeonato} • Rodada {partida.rodada}
              </div>
              <h1 className="text-3xl font-bold text-gray-900" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                {partida.time_casa} <span className="text-gray-400">vs</span> {partida.time_visitante}
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Melhor Recomendação */}
          <Card className="bg-gradient-to-br from-emerald-50 to-teal-50 border-2 border-emerald-200 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardDescription className="text-emerald-700 font-semibold mb-1">
                    Melhor Recomendação
                  </CardDescription>
                  <CardTitle className="text-2xl font-bold text-gray-900">
                    {melhor_recomendacao.mercado}
                  </CardTitle>
                </div>
                <div className="text-right">
                  <div className="text-4xl font-bold text-emerald-700">
                    {melhor_recomendacao.odd}x
                  </div>
                  <div className="text-sm text-gray-600 mt-1">
                    EV: {(melhor_recomendacao.ev * 100).toFixed(2)}%
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  <Badge className={getClassificacaoCor(melhor_recomendacao.classificacao_prob)}>
                    Probabilidade {melhor_recomendacao.classificacao_prob}: {melhor_recomendacao.probabilidade}%
                  </Badge>
                  <Badge className={getClassificacaoCor(melhor_recomendacao.classificacao_ev)}>
                    {melhor_recomendacao.classificacao_ev}
                  </Badge>
                  <Badge className="bg-purple-100 text-purple-800 border-purple-200">
                    Score: {melhor_recomendacao.score_total}/100
                  </Badge>
                </div>
                <div className="bg-white rounded-lg p-4 border border-emerald-100">
                  <h4 className="font-semibold text-gray-900 mb-2">{melhor_recomendacao.recomendacao}</h4>
                  <div className="text-sm text-gray-700 whitespace-pre-line">
                    {melhor_recomendacao.justificativa}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tabs */}
          <Tabs defaultValue="dados" className="w-full">
            <TabsList className="grid w-full grid-cols-3 bg-white border border-gray-200">
              <TabsTrigger value="dados" data-testid="tab-dados">Dados da Partida</TabsTrigger>
              <TabsTrigger value="mercados" data-testid="tab-mercados">Todos os Mercados</TabsTrigger>
              <TabsTrigger value="scores" data-testid="tab-scores">Detalhes dos Scores</TabsTrigger>
            </TabsList>

            {/* Dados da Partida */}
            <TabsContent value="dados" className="space-y-4">
              <Card className="bg-white">
                <CardHeader>
                  <CardTitle className="text-emerald-700">Desempenho e Estatísticas</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">Time da Casa</h4>
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
                      <h4 className="font-semibold text-gray-900 mb-3">Time Visitante</h4>
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
                        <span className="ml-2 font-semibold">{partida.artilheiro_disponivel ? "Sim" : "Não"}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Lesões/Suspensões:</span>
                        <span className="ml-2 font-semibold">{partida.lesoes_suspensoes || "Nenhuma"}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Árbitro:</span>
                        <span className="ml-2 font-semibold">{partida.arbitro || "Não informado"}</span>
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

            {/* Todos os Mercados */}
            <TabsContent value="mercados" className="space-y-4">
              {todas_analises.map((mercado, index) => (
                <Card key={index} className="bg-white hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg">{mercado.mercado}</CardTitle>
                        <CardDescription className="mt-1">
                          Score: {mercado.score_total}/100 • Probabilidade: {mercado.probabilidade}%
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-emerald-700">{mercado.odd}x</div>
                        <div className="text-xs text-gray-600 mt-1">EV: {(mercado.ev * 100).toFixed(2)}%</div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2 mb-3">
                      <Badge className={getClassificacaoCor(mercado.classificacao_prob)}>
                        {mercado.classificacao_prob}
                      </Badge>
                      <Badge className={getClassificacaoCor(mercado.classificacao_ev)}>
                        {mercado.classificacao_ev}
                      </Badge>
                    </div>
                    <div className="text-sm text-gray-700">
                      <strong>{mercado.recomendacao}</strong>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>

            {/* Detalhes dos Scores */}
            <TabsContent value="scores">
              <Card className="bg-white">
                <CardHeader>
                  <CardTitle className="text-emerald-700">Breakdown dos Fatores de Pontuação</CardTitle>
                  <CardDescription>Scores individuais (0-10) do mercado recomendado</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(melhor_recomendacao.detalhes_scores).map(([fator, score]) => (
                      <div key={fator} className="flex items-center gap-4">
                        <div className="flex-1">
                          <div className="flex justify-between mb-1">
                            <span className="text-sm font-medium text-gray-700 capitalize">
                              {fator.replace(/_/g, " ")}
                            </span>
                            <span className="text-sm font-bold text-gray-900">{score}/10</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                              className="bg-emerald-600 h-2.5 rounded-full transition-all"
                              style={{ width: `${(score / 10) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    ))}
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

export default DetalhesPartida;