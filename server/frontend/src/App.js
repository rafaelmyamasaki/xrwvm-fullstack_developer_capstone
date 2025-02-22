import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register"; // Importe o componente Register
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      {/* Rota para a página de login */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Rota para a página de registro */}
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
