import { useState, useCallback } from "react";

const API_URL = "http://localhost:8000";

export default function useChessGame() {
  const [moves, setMoves] = useState([]);
  const [index, setIndex] = useState(0);
  const [level, setLevel] = useState(1);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadGame = useCallback((lvl) => {
    const targetLevel = lvl !== undefined ? lvl : level;
    setLoading(true);
    setError(null);
    fetch(`${API_URL}/generate-game?level=${targetLevel}`)
      .then((res) => {
        if (!res.ok) throw new Error("Erreur serveur");
        return res.json();
      })
      .then((data) => {
        setMoves(data.moves);
        setIndex(0);
        setResult(data.result);
        setLevel(data.level);
        setLoading(false);
      })
      .catch((err) => {
        setError("Impossible de contacter le serveur. Verifiez que le backend tourne sur le port 8000.");
        setLoading(false);
      });
  }, [level]);

  const next = () => {
    if (index < moves.length - 1) setIndex((i) => i + 1);
  };

  const prev = () => {
    if (index > 0) setIndex((i) => i - 1);
  };

  const goTo = (i) => {
    if (i >= 0 && i < moves.length) setIndex(i);
  };

  const currentMove = moves[index] || null;

  return {
    moves,
    currentMove,
    fen: currentMove?.fen || null,
    index,
    total: moves.length,
    level,
    result,
    loading,
    error,
    next,
    prev,
    goTo,
    loadGame,
  };
}
