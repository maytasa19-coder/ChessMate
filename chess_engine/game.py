"""Rules, board state, and physical move descriptions for standard chess."""
from dataclasses import asdict, dataclass
from typing import Optional

import chess


@dataclass(frozen=True)
class MovePlan:
    """Chess squares only, NOT robot motor coordinates or execution instructions."""
    uci: str
    san: str
    from_square: str
    to_square: str
    captured_square: Optional[str] = None
    rook_from: Optional[str] = None
    rook_to: Optional[str] = None
    promotion: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class ChessGame:
    def __init__(self, fen: Optional[str] = None):
        self.board = chess.Board(fen) if fen else chess.Board()
        if self.board.chess960:
            raise ValueError("Chess960 is not supported")

    def state(self) -> dict:
        outcome = self.board.outcome(claim_draw=False)
        return {
            "fen": self.board.fen(),
            "turn": "white" if self.board.turn == chess.WHITE else "black",
            "in_check": self.board.is_check(),
            "game_over": outcome is not None,
            "result": outcome.result() if outcome else None,
            "legal_moves": [m.uci() for m in self.board.legal_moves],
        }

    def plan_move(self, uci: str) -> MovePlan:
        if self.board.is_game_over(claim_draw=False):
            raise ValueError("Game is over")
        try:
            move = chess.Move.from_uci(uci.strip())
        except ValueError as exc:
            raise ValueError(f"Invalid UCI move: {uci}") from exc
        if move not in self.board.legal_moves:
            raise ValueError(f"Illegal move in current position: {uci}")

        src = chess.square_name(move.from_square)
        dst = chess.square_name(move.to_square)
        captured = None
        if self.board.is_capture(move):
            if self.board.is_en_passant(move):
                square = move.to_square - 8 if self.board.turn == chess.WHITE else move.to_square + 8
            else:
                square = move.to_square
            captured = chess.square_name(square)

        rook_from = rook_to = None
        if self.board.is_castling(move):
            rank = "1" if self.board.turn == chess.WHITE else "8"
            if self.board.is_kingside_castling(move):
                rook_from, rook_to = "h" + rank, "f" + rank
            else:
                rook_from, rook_to = "a" + rank, "d" + rank

        return MovePlan(
            uci=move.uci(),
            san=self.board.san(move),
            from_square=src,
            to_square=dst,
            captured_square=captured,
            rook_from=rook_from,
            rook_to=rook_to,
            promotion=chess.piece_symbol(move.promotion) if move.promotion else None,
        )

    def apply_move(self, uci: str) -> MovePlan:
        """Update virtual board AFTER move is confirmed in the physical world."""
        plan = self.plan_move(uci)
        self.board.push(chess.Move.from_uci(plan.uci))
        return plan

    def reset(self) -> None:
        self.board.reset()
