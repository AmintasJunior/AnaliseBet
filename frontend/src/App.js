import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "@/pages/Dashboard";
import NovaPartidaV2 from "@/pages/NovaPartidaV2";
import DetalhesPartidaV2 from "@/pages/DetalhesPartidaV2";
import { Toaster } from "@/components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          {/* Versão 2.0 como única opção */}
          <Route path="/nova-partida" element={<NovaPartidaV2 />} />
          <Route path="/partida/:id" element={<DetalhesPartidaV2 />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;