import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, Save } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const NovaPartida = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    campeonato: "",
    rodada: "",
    time_casa: "",
    time_visitante: "",
    forma_casa: "",
    forma_fora: "",
    media_gols_marcados_casa: "",
    media_gols_sofridos_casa: "",
    media_gols_marcados_fora: "",
    media_gols_sofridos_fora: "",
    historico_h2h: "",
    artilheiro_disponivel: true,
    lesoes_suspensoes: "",
    escalacao_definida: true,
    arbitro: "",
    media_cartoes_arbitro: "",
    condicoes_externas: "",
    noticias_relevantes: "",
    odd_casa: "",
    odd_empate: "",
    odd_fora: ""
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        ...formData,
        rodada: parseInt(formData.rodada),
        media_gols_marcados_casa: parseFloat(formData.media_gols_marcados_casa),
        media_gols_sofridos_casa: parseFloat(formData.media_gols_sofridos_casa),
        media_gols_marcados_fora: parseFloat(formData.media_gols_marcados_fora),
        media_gols_sofridos_fora: parseFloat(formData.media_gols_sofridos_fora),
        media_cartoes_arbitro: parseFloat(formData.media_cartoes_arbitro),
        odd_casa: parseFloat(formData.odd_casa),
        odd_empate: parseFloat(formData.odd_empate),
        odd_fora: parseFloat(formData.odd_fora)
      };

      const response = await axios.post(`${API}/partidas`, payload);
      toast.success("Partida cadastrada com sucesso!");
      navigate(`/partida/${response.data.id}`);
    } catch (error) {
      console.error("Erro ao cadastrar partida:", error);
      toast.error("Erro ao cadastrar partida. Verifique os dados.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-4">
            <Button
              onClick={() => navigate("/")}
              variant="outline"
              className="border-gray-300"
              data-testid="voltar-btn"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                Nova Partida
              </h1>
              <p className="text-gray-600 text-sm mt-1">Preencha os dados para análise automática</p>
            </div>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit}>
          <div className="space-y-6">
            {/* Identificação */}
            <Card className="bg-white">
              <CardHeader>
                <CardTitle className="text-emerald-700">Identificação da Partida</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="campeonato">Campeonato</Label>
                    <Input
                      id="campeonato"
                      placeholder="Ex: Série B"
                      value={formData.campeonato}
                      onChange={(e) => handleChange("campeonato", e.target.value)}
                      required
                      data-testid="campeonato-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="rodada">Rodada</Label>
                    <Input
                      id="rodada"
                      type="number"
                      placeholder="34"
                      value={formData.rodada}
                      onChange={(e) => handleChange("rodada", e.target.value)}
                      required
                      data-testid="rodada-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="time_casa">Time da Casa</Label>
                    <Input
                      id="time_casa"
                      placeholder="Sport"
                      value={formData.time_casa}
                      onChange={(e) => handleChange("time_casa", e.target.value)}
                      required
                      data-testid="time-casa-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="time_visitante">Time Visitante</Label>
                    <Input
                      id="time_visitante"
                      placeholder="Avaí"
                      value={formData.time_visitante}
                      onChange={(e) => handleChange("time_visitante", e.target.value)}
                      required
                      data-testid="time-visitante-input"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Desempenho */}
            <Card className="bg-white">
              <CardHeader>
                <CardTitle className="text-emerald-700">Desempenho Recente</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="forma_casa">Forma Casa (últimos 5)</Label>
                    <Input
                      id="forma_casa"
                      placeholder="V-E-V-D-V"
                      value={formData.forma_casa}
                      onChange={(e) => handleChange("forma_casa", e.target.value)}
                      required
                      data-testid="forma-casa-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="forma_fora">Forma Fora (últimos 5)</Label>
                    <Input
                      id="forma_fora"
                      placeholder="D-V-E-D-E"
                      value={formData.forma_fora}
                      onChange={(e) => handleChange("forma_fora", e.target.value)}
                      required
                      data-testid="forma-fora-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="media_gols_marcados_casa">Média Gols Marcados Casa</Label>
                    <Input
                      id="media_gols_marcados_casa"
                      type="number"
                      step="0.1"
                      placeholder="1.8"
                      value={formData.media_gols_marcados_casa}
                      onChange={(e) => handleChange("media_gols_marcados_casa", e.target.value)}
                      required
                      data-testid="media-gols-marcados-casa-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="media_gols_sofridos_casa">Média Gols Sofridos Casa</Label>
                    <Input
                      id="media_gols_sofridos_casa"
                      type="number"
                      step="0.1"
                      placeholder="0.9"
                      value={formData.media_gols_sofridos_casa}
                      onChange={(e) => handleChange("media_gols_sofridos_casa", e.target.value)}
                      required
                      data-testid="media-gols-sofridos-casa-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="media_gols_marcados_fora">Média Gols Marcados Fora</Label>
                    <Input
                      id="media_gols_marcados_fora"
                      type="number"
                      step="0.1"
                      placeholder="1.1"
                      value={formData.media_gols_marcados_fora}
                      onChange={(e) => handleChange("media_gols_marcados_fora", e.target.value)}
                      required
                      data-testid="media-gols-marcados-fora-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="media_gols_sofridos_fora">Média Gols Sofridos Fora</Label>
                    <Input
                      id="media_gols_sofridos_fora"
                      type="number"
                      step="0.1"
                      placeholder="1.7"
                      value={formData.media_gols_sofridos_fora}
                      onChange={(e) => handleChange("media_gols_sofridos_fora", e.target.value)}
                      required
                      data-testid="media-gols-sofridos-fora-input"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <Label htmlFor="historico_h2h">Histórico H2H</Label>
                    <Input
                      id="historico_h2h"
                      placeholder="3V 2E 1D nos últimos 6"
                      value={formData.historico_h2h}
                      onChange={(e) => handleChange("historico_h2h", e.target.value)}
                      data-testid="historico-h2h-input"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Elenco / Tática */}
            <Card className="bg-white">
              <CardHeader>
                <CardTitle className="text-emerald-700">Elenco e Tática</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="artilheiro_disponivel">Artilheiro Disponível</Label>
                    <Select
                      value={formData.artilheiro_disponivel ? "sim" : "nao"}
                      onValueChange={(value) => handleChange("artilheiro_disponivel", value === "sim")}
                    >
                      <SelectTrigger data-testid="artilheiro-disponivel-select">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="sim">Sim</SelectItem>
                        <SelectItem value="nao">Não</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="escalacao_definida">Escalação Definida</Label>
                    <Select
                      value={formData.escalacao_definida ? "sim" : "nao"}
                      onValueChange={(value) => handleChange("escalacao_definida", value === "sim")}
                    >
                      <SelectTrigger data-testid="escalacao-definida-select">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="sim">Sim</SelectItem>
                        <SelectItem value="nao">Não</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="md:col-span-2">
                    <Label htmlFor="lesoes_suspensoes">Lesões / Suspensões</Label>
                    <Textarea
                      id="lesoes_suspensoes"
                      placeholder="2 defensores fora"
                      value={formData.lesoes_suspensoes}
                      onChange={(e) => handleChange("lesoes_suspensoes", e.target.value)}
                      data-testid="lesoes-suspensoes-input"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Contexto */}
            <Card className="bg-white">
              <CardHeader>
                <CardTitle className="text-emerald-700">Contexto e Condições</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="arbitro">Árbitro</Label>
                    <Input
                      id="arbitro"
                      placeholder="Raphael Claus"
                      value={formData.arbitro}
                      onChange={(e) => handleChange("arbitro", e.target.value)}
                      data-testid="arbitro-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="media_cartoes_arbitro">Média de Cartões do Árbitro</Label>
                    <Input
                      id="media_cartoes_arbitro"
                      type="number"
                      step="0.1"
                      placeholder="5.4"
                      value={formData.media_cartoes_arbitro}
                      onChange={(e) => handleChange("media_cartoes_arbitro", e.target.value)}
                      data-testid="media-cartoes-arbitro-input"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <Label htmlFor="condicoes_externas">Condições Externas</Label>
                    <Textarea
                      id="condicoes_externas"
                      placeholder="Chuva leve, gramado pesado"
                      value={formData.condicoes_externas}
                      onChange={(e) => handleChange("condicoes_externas", e.target.value)}
                      data-testid="condicoes-externas-input"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <Label htmlFor="noticias_relevantes">Notícias Relevantes</Label>
                    <Textarea
                      id="noticias_relevantes"
                      placeholder="Técnico pressionado após 3 derrotas"
                      value={formData.noticias_relevantes}
                      onChange={(e) => handleChange("noticias_relevantes", e.target.value)}
                      data-testid="noticias-relevantes-input"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Odds */}
            <Card className="bg-white">
              <CardHeader>
                <CardTitle className="text-emerald-700">Odds (Pré-Live)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="odd_casa">Odd Casa</Label>
                    <Input
                      id="odd_casa"
                      type="number"
                      step="0.01"
                      placeholder="2.10"
                      value={formData.odd_casa}
                      onChange={(e) => handleChange("odd_casa", e.target.value)}
                      required
                      data-testid="odd-casa-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="odd_empate">Odd Empate</Label>
                    <Input
                      id="odd_empate"
                      type="number"
                      step="0.01"
                      placeholder="3.25"
                      value={formData.odd_empate}
                      onChange={(e) => handleChange("odd_empate", e.target.value)}
                      required
                      data-testid="odd-empate-input"
                    />
                  </div>
                  <div>
                    <Label htmlFor="odd_fora">Odd Fora</Label>
                    <Input
                      id="odd_fora"
                      type="number"
                      step="0.01"
                      placeholder="3.40"
                      value={formData.odd_fora}
                      onChange={(e) => handleChange("odd_fora", e.target.value)}
                      required
                      data-testid="odd-fora-input"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Submit */}
            <div className="flex justify-end gap-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/")}
                data-testid="cancelar-btn"
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-8"
                data-testid="salvar-btn"
              >
                {loading ? (
                  "Salvando..."
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Salvar e Analisar
                  </>
                )}
              </Button>
            </div>
          </div>
        </form>
      </main>
    </div>
  );
};

export default NovaPartida;