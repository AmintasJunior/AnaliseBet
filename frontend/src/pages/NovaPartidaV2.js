import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { ArrowLeft, Save, Info } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const NovaPartidaV2 = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("geral");
  const [formData, setFormData] = useState({
    // Geral
    campeonato: "",
    rodada: "",
    data_hora: "",
    local_estadio: "",
    arbitro: "",
    media_cartoes_arbitro: "",
    condicoes_externas: "",
    historico_h2h: "",
    odd_casa: "",
    odd_empate: "",
    odd_fora: "",
    noticia_1: "",
    noticia_2: "",
    noticia_3: "",
    observacoes_adicionais: "",
    observacoes_contextuais: "",
    
    // Casa
    time_casa: "",
    forma_casa: "",
    media_gols_marcados_casa: "",
    media_gols_sofridos_casa: "",
    desempenho_especifico_casa: "",
    lesoes_suspensoes_casa: "",
    artilheiro_disponivel_casa: true,
    
    // Fora
    time_visitante: "",
    forma_fora: "",
    media_gols_marcados_fora: "",
    media_gols_sofridos_fora: "",
    desempenho_especifico_fora: "",
    lesoes_suspensoes_fora: "",
    artilheiro_disponivel_fora: true
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
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
                Nova Partida - Análise 2.0
              </h1>
              <p className="text-gray-600 text-sm mt-1">
                Preencha os dados organizados por abas para análise inteligente
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit}>
          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="text-emerald-700 flex items-center gap-2">
                <Info className="h-5 w-5" />
                Dados da Partida
              </CardTitle>
              <CardDescription>
                Organize as informações em abas: Geral, Casa e Fora
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-3 mb-6">
                  <TabsTrigger value="geral" className="data-[state=active]:bg-emerald-600 data-[state=active]:text-white">
                    📋 Geral
                  </TabsTrigger>
                  <TabsTrigger value="casa" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
                    🏠 Casa
                  </TabsTrigger>
                  <TabsTrigger value="fora" className="data-[state=active]:bg-orange-600 data-[state=active]:text-white">
                    ✈️ Fora
                  </TabsTrigger>
                </TabsList>

                {/* ABA GERAL */}
                <TabsContent value="geral" className="space-y-6">
                  {/* Identificação */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Identificação da Partida
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="campeonato">Campeonato *</Label>
                        <Input
                          id="campeonato"
                          placeholder="Ex: Liga dos Campeões"
                          value={formData.campeonato}
                          onChange={(e) => handleChange("campeonato", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="rodada">Rodada *</Label>
                        <Input
                          id="rodada"
                          type="number"
                          placeholder="Ex: 3"
                          value={formData.rodada}
                          onChange={(e) => handleChange("rodada", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="data_hora">Data e Hora</Label>
                        <Input
                          id="data_hora"
                          type="datetime-local"
                          value={formData.data_hora}
                          onChange={(e) => handleChange("data_hora", e.target.value)}
                        />
                      </div>
                      <div>
                        <Label htmlFor="local_estadio">Local (Estádio)</Label>
                        <Input
                          id="local_estadio"
                          placeholder="Ex: BayArena"
                          value={formData.local_estadio}
                          onChange={(e) => handleChange("local_estadio", e.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Árbitro e Condições */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Árbitro e Condições
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="arbitro">Árbitro *</Label>
                        <Input
                          id="arbitro"
                          placeholder="Nome do árbitro"
                          value={formData.arbitro}
                          onChange={(e) => handleChange("arbitro", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="media_cartoes_arbitro">Média de Cartões do Árbitro *</Label>
                        <Input
                          id="media_cartoes_arbitro"
                          type="number"
                          step="0.1"
                          placeholder="Ex: 4.2"
                          value={formData.media_cartoes_arbitro}
                          onChange={(e) => handleChange("media_cartoes_arbitro", e.target.value)}
                          required
                        />
                      </div>
                      <div className="md:col-span-2">
                        <Label htmlFor="condicoes_externas">Condições Externas *</Label>
                        <Textarea
                          id="condicoes_externas"
                          placeholder="Ex: Clima bom, gramado em perfeitas condições"
                          value={formData.condicoes_externas}
                          onChange={(e) => handleChange("condicoes_externas", e.target.value)}
                          required
                          rows={2}
                        />
                      </div>
                    </div>
                  </div>

                  {/* H2H */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Histórico de Confrontos (H2H)
                    </h3>
                    <div>
                      <Label htmlFor="historico_h2h">Histórico H2H *</Label>
                      <Input
                        id="historico_h2h"
                        placeholder="Ex: 3V 2E 1D nos últimos 6 jogos (perspectiva do time da casa)"
                        value={formData.historico_h2h}
                        onChange={(e) => handleChange("historico_h2h", e.target.value)}
                        required
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Informe o histórico do ponto de vista do time da casa
                      </p>
                    </div>
                  </div>

                  {/* Odds */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Odds (Cotações)
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <Label htmlFor="odd_casa">Odd Casa *</Label>
                        <Input
                          id="odd_casa"
                          type="number"
                          step="0.01"
                          placeholder="Ex: 2.10"
                          value={formData.odd_casa}
                          onChange={(e) => handleChange("odd_casa", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="odd_empate">Odd Empate *</Label>
                        <Input
                          id="odd_empate"
                          type="number"
                          step="0.01"
                          placeholder="Ex: 3.50"
                          value={formData.odd_empate}
                          onChange={(e) => handleChange("odd_empate", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="odd_fora">Odd Fora *</Label>
                        <Input
                          id="odd_fora"
                          type="number"
                          step="0.01"
                          placeholder="Ex: 3.20"
                          value={formData.odd_fora}
                          onChange={(e) => handleChange("odd_fora", e.target.value)}
                          required
                        />
                      </div>
                    </div>
                  </div>

                  {/* Notícias */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Notícias e Observações
                    </h3>
                    <div className="space-y-3">
                      <div>
                        <Label htmlFor="noticia_1">Notícia 1</Label>
                        <Textarea
                          id="noticia_1"
                          placeholder="Primeira notícia relevante sobre a partida"
                          value={formData.noticia_1}
                          onChange={(e) => handleChange("noticia_1", e.target.value)}
                          rows={2}
                        />
                      </div>
                      <div>
                        <Label htmlFor="noticia_2">Notícia 2</Label>
                        <Textarea
                          id="noticia_2"
                          placeholder="Segunda notícia relevante sobre a partida"
                          value={formData.noticia_2}
                          onChange={(e) => handleChange("noticia_2", e.target.value)}
                          rows={2}
                        />
                      </div>
                      <div>
                        <Label htmlFor="noticia_3">Notícia 3</Label>
                        <Textarea
                          id="noticia_3"
                          placeholder="Terceira notícia relevante sobre a partida"
                          value={formData.noticia_3}
                          onChange={(e) => handleChange("noticia_3", e.target.value)}
                          rows={2}
                        />
                      </div>
                      <div>
                        <Label htmlFor="observacoes_adicionais">Observações Adicionais</Label>
                        <Textarea
                          id="observacoes_adicionais"
                          placeholder="Qualquer informação adicional relevante"
                          value={formData.observacoes_adicionais}
                          onChange={(e) => handleChange("observacoes_adicionais", e.target.value)}
                          rows={3}
                        />
                      </div>
                    </div>
                  </div>
                </TabsContent>

                {/* ABA CASA */}
                <TabsContent value="casa" className="space-y-6">
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 mb-4">
                    <p className="text-sm text-blue-800 font-medium">
                      🏠 Dados específicos do time que joga em casa
                    </p>
                  </div>

                  {/* Time Casa */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Identificação
                    </h3>
                    <div>
                      <Label htmlFor="time_casa">Nome do Time da Casa *</Label>
                      <Input
                        id="time_casa"
                        placeholder="Ex: Leverkusen"
                        value={formData.time_casa}
                        onChange={(e) => handleChange("time_casa", e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  {/* Forma e Desempenho */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Forma e Desempenho Recente
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="forma_casa">Forma Casa (últimos 5) *</Label>
                        <Input
                          id="forma_casa"
                          placeholder="Ex: V-V-E-V-D"
                          value={formData.forma_casa}
                          onChange={(e) => handleChange("forma_casa", e.target.value)}
                          required
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          V = Vitória, E = Empate, D = Derrota
                        </p>
                      </div>
                      <div>
                        <Label htmlFor="desempenho_especifico_casa">Desempenho em Casa</Label>
                        <Input
                          id="desempenho_especifico_casa"
                          placeholder="Ex: 8 vitórias em 10 jogos em casa"
                          value={formData.desempenho_especifico_casa}
                          onChange={(e) => handleChange("desempenho_especifico_casa", e.target.value)}
                        />
                      </div>
                      <div>
                        <Label htmlFor="media_gols_marcados_casa">Média Gols Marcados (Casa) *</Label>
                        <Input
                          id="media_gols_marcados_casa"
                          type="number"
                          step="0.1"
                          placeholder="Ex: 2.3"
                          value={formData.media_gols_marcados_casa}
                          onChange={(e) => handleChange("media_gols_marcados_casa", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="media_gols_sofridos_casa">Média Gols Sofridos (Casa) *</Label>
                        <Input
                          id="media_gols_sofridos_casa"
                          type="number"
                          step="0.1"
                          placeholder="Ex: 0.8"
                          value={formData.media_gols_sofridos_casa}
                          onChange={(e) => handleChange("media_gols_sofridos_casa", e.target.value)}
                          required
                        />
                      </div>
                    </div>
                  </div>

                  {/* Elenco Casa */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Elenco e Disponibilidade
                    </h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div>
                          <Label htmlFor="artilheiro_disponivel_casa" className="text-base">
                            Artilheiro Disponível
                          </Label>
                          <p className="text-sm text-gray-600">
                            O principal artilheiro está confirmado?
                          </p>
                        </div>
                        <Switch
                          id="artilheiro_disponivel_casa"
                          checked={formData.artilheiro_disponivel_casa}
                          onCheckedChange={(checked) => handleChange("artilheiro_disponivel_casa", checked)}
                        />
                      </div>
                      <div>
                        <Label htmlFor="lesoes_suspensoes_casa">Lesões e Suspensões</Label>
                        <Textarea
                          id="lesoes_suspensoes_casa"
                          placeholder="Ex: Zagueiro titular suspenso, meio-campista lesionado"
                          value={formData.lesoes_suspensoes_casa}
                          onChange={(e) => handleChange("lesoes_suspensoes_casa", e.target.value)}
                          rows={3}
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Deixe em branco se não houver desfalques
                        </p>
                      </div>
                    </div>
                  </div>
                </TabsContent>

                {/* ABA FORA */}
                <TabsContent value="fora" className="space-y-6">
                  <div className="bg-orange-50 p-4 rounded-lg border border-orange-200 mb-4">
                    <p className="text-sm text-orange-800 font-medium">
                      ✈️ Dados específicos do time visitante
                    </p>
                  </div>

                  {/* Time Fora */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Identificação
                    </h3>
                    <div>
                      <Label htmlFor="time_visitante">Nome do Time Visitante *</Label>
                      <Input
                        id="time_visitante"
                        placeholder="Ex: PSG"
                        value={formData.time_visitante}
                        onChange={(e) => handleChange("time_visitante", e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  {/* Forma e Desempenho */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Forma e Desempenho Recente
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="forma_fora">Forma Fora (últimos 5) *</Label>
                        <Input
                          id="forma_fora"
                          placeholder="Ex: V-D-V-V-E"
                          value={formData.forma_fora}
                          onChange={(e) => handleChange("forma_fora", e.target.value)}
                          required
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          V = Vitória, E = Empate, D = Derrota
                        </p>
                      </div>
                      <div>
                        <Label htmlFor="desempenho_especifico_fora">Desempenho Fora</Label>
                        <Input
                          id="desempenho_especifico_fora"
                          placeholder="Ex: 6 vitórias em 10 jogos fora"
                          value={formData.desempenho_especifico_fora}
                          onChange={(e) => handleChange("desempenho_especifico_fora", e.target.value)}
                        />
                      </div>
                      <div>
                        <Label htmlFor="media_gols_marcados_fora">Média Gols Marcados (Fora) *</Label>
                        <Input
                          id="media_gols_marcados_fora"
                          type="number"
                          step="0.1"
                          placeholder="Ex: 1.9"
                          value={formData.media_gols_marcados_fora}
                          onChange={(e) => handleChange("media_gols_marcados_fora", e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="media_gols_sofridos_fora">Média Gols Sofridos (Fora) *</Label>
                        <Input
                          id="media_gols_sofridos_fora"
                          type="number"
                          step="0.1"
                          placeholder="Ex: 1.2"
                          value={formData.media_gols_sofridos_fora}
                          onChange={(e) => handleChange("media_gols_sofridos_fora", e.target.value)}
                          required
                        />
                      </div>
                    </div>
                  </div>

                  {/* Elenco Fora */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                      Elenco e Disponibilidade
                    </h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div>
                          <Label htmlFor="artilheiro_disponivel_fora" className="text-base">
                            Artilheiro Disponível
                          </Label>
                          <p className="text-sm text-gray-600">
                            O principal artilheiro está confirmado?
                          </p>
                        </div>
                        <Switch
                          id="artilheiro_disponivel_fora"
                          checked={formData.artilheiro_disponivel_fora}
                          onCheckedChange={(checked) => handleChange("artilheiro_disponivel_fora", checked)}
                        />
                      </div>
                      <div>
                        <Label htmlFor="lesoes_suspensoes_fora">Lesões e Suspensões</Label>
                        <Textarea
                          id="lesoes_suspensoes_fora"
                          placeholder="Ex: Atacante principal lesionado, lateral suspenso"
                          value={formData.lesoes_suspensoes_fora}
                          onChange={(e) => handleChange("lesoes_suspensoes_fora", e.target.value)}
                          rows={3}
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Deixe em branco se não houver desfalques
                        </p>
                      </div>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>

              {/* Botões de Ação */}
              <div className="flex items-center justify-between mt-8 pt-6 border-t">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate("/")}
                  className="border-gray-300"
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  disabled={loading}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white"
                >
                  {loading ? (
                    <>Salvando...</>
                  ) : (
                    <>
                      <Save className="h-4 w-4 mr-2" />
                      Salvar e Analisar
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </form>
      </main>
    </div>
  );
};

export default NovaPartidaV2;
