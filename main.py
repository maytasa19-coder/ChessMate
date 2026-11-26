"""Offline ChessMate smoke test. No camera/robot actions are performed."""
import argparse

from chess_engine import ChessController, LegalMoveSelector, StockfishSelector


def demo(selector) -> None:
    controller = ChessController(selector)
    human = controller.record_human_move("e2e4")
    print("Human:", human.to_dict())
    plan = controller.plan_robot_move()
    print("Robot move plan (NOT executed):", plan.to_dict())
    print("Waiting for physical execution and verification...")
    print("Board unchanged until confirm_robot_move(plan.uci) is called.")
    print("Current FEN:", controller.game.state()["fen"])


def main() -> None:
    parser = argparse.ArgumentParser(description="ChessMate software-only demo")
    parser.add_argument("--stockfish", help="Path to Stockfish UCI executable")
    args = parser.parse_args()
    if args.stockfish:
        with StockfishSelector(args.stockfish) as selector:
            demo(selector)
    else:
        print("Using a deterministic legal-move selector; not a chess-strength engine.")
        demo(LegalMoveSelector())


if __name__ == "__main__":
    main()
