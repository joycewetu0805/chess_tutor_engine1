from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import chess
import random

app = FastAPI(title="Chess Tutor Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# MODELS
# =====================

class MoveData(BaseModel):
    move_san: str
    move_uci: str
    fen: str
    turn: str
    move_number: int
    comment: str
    incident: Optional[str] = None
    alternative: Optional[str] = None

class GameResponse(BaseModel):
    moves: List[MoveData]
    level: int
    result: str

# =====================
# OPENINGS
# =====================

OPENINGS = {
    "italienne": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"],
    "espagnole": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
    "sicilienne": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4"],
    "francaise": ["e2e4", "e7e6", "d2d4", "d7d5"],
    "caro_kann": ["e2e4", "c7c6", "d2d4", "d7d5"],
    "dame": ["d2d4", "d7d5", "c2c4", "e7e6", "b1c3", "g8f6"],
    "anglaise": ["c2c4", "e7e5", "b1c3", "g8f6"],
    "pirc": ["e2e4", "d7d6", "d2d4", "g8f6", "b1c3"],
}

PIECE_FR = {
    chess.PAWN: "pion", chess.KNIGHT: "cavalier", chess.BISHOP: "fou",
    chess.ROOK: "tour", chess.QUEEN: "dame", chess.KING: "roi",
}

PIECE_VALUES = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
}

CENTER = [chess.D4, chess.D5, chess.E4, chess.E5]
EXTENDED_CENTER = CENTER + [chess.C3, chess.C4, chess.C5, chess.C6,
                             chess.F3, chess.F4, chess.F5, chess.F6]

# =====================
# MOVE DESCRIPTION
# =====================

def describe_move(board, move, level):
    piece = board.piece_at(move.from_square)
    is_capture = board.is_capture(move)
    is_check = board.gives_check(move)
    piece_name = PIECE_FR.get(piece.piece_type, "piece") if piece else "piece"
    to_name = chess.SQUARE_NAMES[move.to_square]

    parts = []
    incident = None
    alternative = None

    if board.is_castling(move):
        side = "petit" if move.to_square > move.from_square else "grand"
        parts.append(f"{side.capitalize()} roque. Le roi se met en securite et la tour entre en jeu.")
    elif is_capture:
        captured = board.piece_at(move.to_square)
        cap_name = PIECE_FR.get(captured.piece_type, "piece") if captured else "piece"
        parts.append(f"Le {piece_name} capture le {cap_name} en {to_name}.")
        if captured and piece:
            att_val = PIECE_VALUES.get(piece.piece_type, 0)
            cap_val = PIECE_VALUES.get(captured.piece_type, 0)
            if cap_val > att_val:
                parts.append("Echange favorable : gain de materiel.")
            elif cap_val < att_val:
                incident = "Echange defavorable : perte de materiel."
            else:
                parts.append("Echange egal.")
    elif piece and piece.piece_type == chess.PAWN:
        if move.to_square in CENTER:
            parts.append(f"Le pion avance en {to_name}, occupant le centre.")
        elif move.promotion:
            parts.append("Promotion du pion en dame ! Coup decisif.")
        else:
            parts.append(f"Le pion avance en {to_name}.")
    elif piece and piece.piece_type in (chess.KNIGHT, chess.BISHOP):
        if move.to_square in EXTENDED_CENTER:
            parts.append(f"Le {piece_name} se developpe en {to_name}, controlant des cases centrales.")
        else:
            parts.append(f"Le {piece_name} se deplace en {to_name}.")
    elif piece and piece.piece_type == chess.QUEEN:
        parts.append(f"La dame se place en {to_name}.")
        if board.fullmove_number < 8:
            incident = "Sortie precoce de la dame. Elle risque d'etre harcelee."
    elif piece and piece.piece_type == chess.ROOK:
        file_idx = chess.square_file(move.to_square)
        has_pawns = any(
            board.piece_at(chess.square(file_idx, r))
            and board.piece_at(chess.square(file_idx, r)).piece_type == chess.PAWN
            for r in range(8)
        )
        if not has_pawns:
            parts.append(f"La tour s'installe sur la colonne ouverte {chr(ord('a') + file_idx)}.")
        else:
            parts.append(f"La tour se deplace en {to_name}.")
    else:
        parts.append(f"Le {piece_name} se deplace en {to_name}.")

    if is_check:
        parts.append("Echec au roi !")

    # Alternatives selon le niveau
    if level <= 2:
        prob = 0.35 if level == 1 else 0.2
        legal = list(board.legal_moves)
        others = [m for m in legal if m != move]
        if others and random.random() < prob:
            alt = random.choice(others[:3])
            alt_san = board.san(alt)
            prefix = "Alternative possible" if level == 1 else "A considerer"
            alternative = f"{prefix} : {alt_san}"

    return {"comment": " ".join(parts), "incident": incident, "alternative": alternative}

# =====================
# MOVE PICKER
# =====================

def pick_move(board, level):
    legal = list(board.legal_moves)
    if not legal:
        return None

    if level == 1:
        return random.choice(legal)

    scored = []
    for m in legal:
        score = 0
        piece = board.piece_at(m.from_square)
        if board.is_capture(m):
            captured = board.piece_at(m.to_square)
            if captured and piece:
                score += PIECE_VALUES.get(captured.piece_type, 0) - PIECE_VALUES.get(piece.piece_type, 0) + 5
            else:
                score += 3
        if board.gives_check(m):
            score += 3 if level == 3 else 2
        if m.to_square in CENTER:
            score += 2
        if piece and piece.piece_type in (chess.KNIGHT, chess.BISHOP) and board.fullmove_number < 12:
            score += 2 if level == 3 else 1
        if piece and piece.piece_type == chess.QUEEN and board.fullmove_number < 8:
            score -= 3
        if board.is_castling(m):
            score += 5
        scored.append((m, score))

    scored.sort(key=lambda x: -x[1])
    top_n = max(2, len(scored) // (5 if level == 3 else 3))
    return random.choice(scored[:top_n])[0]

# =====================
# GAME GENERATION
# =====================

def generate_game(level=1, max_moves=30):
    board = chess.Board()
    moves_data = []

    opening_name = random.choice(list(OPENINGS.keys()))
    opening_uci = OPENINGS[opening_name]

    # Position initiale
    moves_data.append(MoveData(
        move_san="--", move_uci="--", fen=board.fen(),
        turn="Blancs", move_number=0,
        comment=f"Position de depart. Ouverture : {opening_name.replace('_', ' ').title()}.",
    ))

    # Ouverture
    for uci_str in opening_uci:
        move = chess.Move.from_uci(uci_str)
        if move not in board.legal_moves:
            break
        info = describe_move(board, move, level)
        turn = "Blancs" if board.turn == chess.WHITE else "Noirs"
        san = board.san(move)
        board.push(move)
        moves_data.append(MoveData(
            move_san=san, move_uci=uci_str, fen=board.fen(),
            turn=turn, move_number=board.fullmove_number, **info,
        ))

    # Suite generee
    while len(moves_data) < max_moves + 1 and not board.is_game_over():
        move = pick_move(board, level)
        if not move:
            break
        info = describe_move(board, move, level)
        turn = "Blancs" if board.turn == chess.WHITE else "Noirs"
        san = board.san(move)
        board.push(move)
        moves_data.append(MoveData(
            move_san=san, move_uci=move.uci(), fen=board.fen(),
            turn=turn, move_number=board.fullmove_number, **info,
        ))

    if board.is_checkmate():
        result = "1-0" if board.turn == chess.BLACK else "0-1"
    elif board.is_game_over():
        result = "1/2-1/2"
    else:
        result = "*"

    return {"moves": moves_data, "level": level, "result": result}

# =====================
# ENDPOINTS
# =====================

@app.get("/generate-game", response_model=GameResponse)
def generate_game_endpoint(level: int = Query(default=1, ge=1, le=3)):
    return generate_game(level=level)

@app.get("/health")
def health():
    return {"status": "ok"}
