import React, { useEffect } from "react";
import useChessGame from "./hooks/useChessGame";
import ChessBoard from "./components/ChessBoard";
import GameControls from "./components/GameControls";
import ExplanationPanel from "./components/ExplanationPanel";
import LevelSelector from "./components/LevelSelector";
import MoveList from "./components/MoveList";
import "./style.css";

export default function App() {
  const {
    moves, currentMove, fen, index, total,
    level, result, loading, error,
    next, prev, goTo, loadGame,
  } = useChessGame();

  useEffect(() => {
    loadGame(1);
  }, []);

  const handleLevel = (lvl) => {
    loadGame(lvl);
  };

  // Parse last move UCI for highlight
  let lastMove = null;
  if (currentMove && currentMove.move_uci && currentMove.move_uci !== "--") {
    const uci = currentMove.move_uci;
    lastMove = { from: uci.slice(0, 2), to: uci.slice(2, 4) };
  }

  // Keyboard navigation
  useEffect(() => {
    const handler = (e) => {
      if (e.key === "ArrowRight") next();
      if (e.key === "ArrowLeft") prev();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [index, total]);

  return (
    <div className="app">
      <header className="header">
        <h1>Chess Tutor Engine</h1>
        <p className="subtitle">Laboratoire d'analyse</p>
      </header>

      <LevelSelector level={level} onSelect={handleLevel} disabled={loading} />

      {error && <div className="error-msg">{error}</div>}

      {loading && <div className="loading">Generation de la partie...</div>}

      {!loading && !error && fen && (
        <div className="main-layout">
          <div className="left-panel">
            <MoveList moves={moves} index={index} goTo={goTo} />
          </div>

          <div className="center-panel">
            <ChessBoard fen={fen} lastMove={lastMove} />
            <GameControls
              prev={prev}
              next={next}
              reload={() => loadGame(level)}
              index={index}
              total={total}
              loading={loading}
            />
          </div>

          <div className="right-panel">
            <ExplanationPanel move={currentMove} />
            {result && result !== "*" && index === total - 1 && (
              <div className="result-box">
                Resultat : {result}
              </div>
            )}
          </div>
        </div>
      )}

      {!loading && !error && !fen && (
        <div className="welcome">
          Selectionnez un niveau et lancez une partie.
        </div>
      )}
    </div>
  );
}
