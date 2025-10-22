import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Plus, TrendingUp, Trash2, Edit, Eye } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [partidas, setPartidas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarPartidas();
  }, []);

  const carregarPartidas = async () => {
    try {
      const response = await axios.get(`${API}/partidas`);
      setPartidas(response.data);
    } catch (error) {
      console.error("Erro ao carregar partidas:", error);
      toast.error("Erro ao carregar partidas");
    } finally {
      setLoading(false);
    }
  };

  const deletarPartida = async (id, e) => {
    e.stopPropagation();
    if (window.confirm("Tem certeza que deseja deletar esta partida?")) {
      try {
        await axios.delete(`${API}/partidas/${id}`);
        toast.success("Partida deletada com sucesso");
        carregarPartidas();
      } catch (error) {
        console.error("Erro ao deletar partida:", error);
        toast.error("Erro ao deletar partida");
      }
    }
  };

  return (
    <div className="min-h-screen" style={{ background: "linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%)" }}>
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                ⚽ Análise Inteligente de Apostas
              </h1>
              <p className="text-gray-600 mt-1">
                Sistema de recomendação baseado em dados • 
                <span className="ml-2 text-emerald-600 font-semibold">Versão 2.0 com Probabilidades Coerentes</span>
              </p>
            </div>
            <Button
              onClick={() => navigate("/nova-partida")}
              className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-6 py-6 rounded-xl shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
              data-testid="nova-partida-btn"
            >
              <Plus className="mr-2 h-5 w-5" />
              Nova Partida
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
            <p className="mt-4 text-gray-600">Carregando partidas...</p>
          </div>
        ) : partidas.length === 0 ? (
          <div className="text-center py-20">
            <TrendingUp className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">Nenhuma partida cadastrada</h3>
            <p className="text-gray-600 mb-6">Comece adicionando sua primeira análise de partida</p>
            <Button
              onClick={() => navigate("/nova-partida")}
              className="bg-emerald-600 hover:bg-emerald-700"
              data-testid="nova-partida-empty-btn"
            >
              <Plus className="mr-2 h-4 w-4" />
              Adicionar Partida
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {partidas.map((partida) => (
              <Card
                key={partida.id}
                className="bg-white hover:shadow-xl transition-all duration-300 cursor-pointer border-gray-200 overflow-hidden group"
                data-testid={`partida-card-${partida.id}`}
              >
                <CardHeader className="bg-gradient-to-r from-emerald-50 to-teal-50 pb-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardDescription className="text-xs font-semibold text-emerald-700 uppercase tracking-wide mb-1">
                        {partida.campeonato} • Rodada {partida.rodada}
                      </CardDescription>
                      <CardTitle className="text-lg font-bold text-gray-900 leading-tight">
                        {partida.time_casa} <span className="text-gray-500">vs</span> {partida.time_visitante}
                      </CardTitle>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-4">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Forma Casa:</span>
                      <span className="font-semibold text-gray-900">{partida.forma_casa}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Forma Fora:</span>
                      <span className="font-semibold text-gray-900">{partida.forma_fora}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm pt-2 border-t border-gray-100">
                      <span className="text-gray-600">Odds:</span>
                      <div className="flex gap-2 font-semibold text-sm">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">{partida.odd_casa}</span>
                        <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded">{partida.odd_empate}</span>
                        <span className="bg-red-100 text-red-800 px-2 py-1 rounded">{partida.odd_fora}</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 flex gap-2">
                    <Button
                      onClick={() => navigate(`/partida/${partida.id}`)}
                      className="flex-1 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-semibold rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
                      data-testid={`ver-analise-btn-${partida.id}`}
                    >
                      <Eye className="mr-2 h-4 w-4" />
                      Ver Análise
                    </Button>
                    <Button
                      onClick={(e) => deletarPartida(partida.id, e)}
                      variant="outline"
                      className="border-red-200 text-red-600 hover:bg-red-50 hover:border-red-300"
                      data-testid={`deletar-btn-${partida.id}`}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;