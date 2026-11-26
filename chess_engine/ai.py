"""AI move selection: real Stockfish or deterministic smoke-test selector."""
from pathlib import Path
from typing import Optional

import chess
import chess.engine


class LegalMoveSelector:
    """For offline development only. This is NOT a strong chess AI."""
    def choose(self, board: chess.Board) -> chess.Move:
        moves = sorted(board.legal_moves, key=lambda m: m.uci())
        if not moves:
            raise ValueError("No legal moves available")
        return moves[0]


class StockfishSelector:
    """Runs a separately installed Stockfish UCI executable."""
    def __init__(self, executable: str, think_time: float = 0.25):
        if think_time <= 0:
            raise ValueError("think_time must be positive")
        self.executable = str(Path(executable).expanduser())
        self.think_time = think_time
        self._engine: Optional[chess.engine.SimpleEngine] = None

    def __enter__(self):
        self._engine = chess.engine.SimpleEngine.popen_uci(self.executable)
        return self

    def choose(self, board: chess.Board) -> chess.Move:
        if self._engine is None:
            raise RuntimeError("Use StockfishSelector inside a 'with' block")
        if board.is_game_over(claim_draw=False):
            raise ValueError("Game is over")
        result = self._engine.play(board, chess.engine.Limit(time=self.think_time))
        if result.move is None or result.move not in board.legal_moves:
            raise RuntimeError("Engine returned no legal move")
        return result.move

    def __exit__(self, exc_type, exc, tb):
        if self._engine is not None:
            self._engine.quit()
            self._engine = None
