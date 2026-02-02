import React from "react";

export default function ExplanationPanel({ move }) {
  if (!move || move.move_san === "--") return null;

  return (
    <div className="explanation">
      <div className="explanation-header">
        <span className="explanation-turn">{move.turn}</span>
        <span className="explanation-san">{move.move_san}</span>
        <span className="explanation-num">Coup {move.move_number}</span>
      </div>
      <p className="explanation-comment">{move.comment}</p>
      {move.incident && (
        <p className="explanation-incident">{move.incident}</p>
      )}
      {move.alternative && (
        <p className="explanation-alt">{move.alternative}</p>
      )}
    </div>
  );
}
