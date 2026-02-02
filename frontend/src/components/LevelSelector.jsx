import React from "react";

const LEVELS = [
  { value: 1, label: "Niveau 1", desc: "Pedagogique" },
  { value: 2, label: "Niveau 2", desc: "Solide" },
  { value: 3, label: "Niveau 3", desc: "Difficile" },
];

export default function LevelSelector({ level, onSelect, disabled }) {
  return (
    <div className="level-selector">
      {LEVELS.map((l) => (
        <button
          key={l.value}
          className={`level-btn ${level === l.value ? "level-active" : ""}`}
          onClick={() => onSelect(l.value)}
          disabled={disabled}
        >
          <span className="level-label">{l.label}</span>
          <span className="level-desc">{l.desc}</span>
        </button>
      ))}
    </div>
  );
}
