"""Orchestrates chess rules and AI, without moving hardware."""
from typing import Optional

from .game import ChessGame, MovePlan


class ChessController:
    def __init__(self, selector, game: Optional[ChessGame] = None):
        self.game = game or ChessGame()
        self.selector = selector
        self.pending_robot_plan: Optional[MovePlan] = None

    def record_human_move(self, uci: str) -> MovePlan:
        """Call only after the vision/operator verified the human's physical move."""
        if self.pending_robot_plan is not None:
            raise RuntimeError("Robot move still pending confirmation")
        return self.game.apply_move(uci)

    def plan_robot_move(self) -> MovePlan:
        """Generate a move plan but do NOT alter board or activate the robot."""
        if self.pending_robot_plan is not None:
            return self.pending_robot_plan
        move = self.selector.choose(self.game.board.copy())
        plan = self.game.plan_move(move.uci())
        self.pending_robot_plan = plan
        return plan

    def confirm_robot_move(self, uci: str) -> MovePlan:
        """Call ONLY after execution and physical verification succeeded."""
        if self.pending_robot_plan is None:
            raise RuntimeError("No robot move is pending")
        if uci != self.pending_robot_plan.uci:
            raise ValueError("Confirmation does not match pending move")
        plan = self.game.apply_move(uci)
        self.pending_robot_plan = None
        return plan

    def cancel_robot_move(self) -> None:
        """Cancel plan without altering the virtual board."""
        self.pending_robot_plan = None
