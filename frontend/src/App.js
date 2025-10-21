import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "@/pages/Dashboard";
import NovaPartida from "@/pages/NovaPartida";
import DetalhesPartida from "@/pages/DetalhesPartida";
import DetalhesPartidaV2 from "@/pages/DetalhesPartidaV2";
import { Toaster } from "@/components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/nova-partida" element={<NovaPartida />} />
          <Route path="/partida/:id" element={<DetalhesPartida />} />
          <Route path="/partida-v2/:id" element={<DetalhesPartidaV2 />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;