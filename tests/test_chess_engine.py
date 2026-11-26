import pytest

from chess_engine import ChessController, ChessGame, LegalMoveSelector


def test_standard_start_and_legal_move():
    game = ChessGame()
    assert game.state()["turn"] == "white"
    assert len(game.state()["legal_moves"]) == 20
    plan = game.apply_move("e2e4")
    assert plan.from_square == "e2"
    assert plan.to_square == "e4"
    assert game.state()["turn"] == "black"


def test_illegal_move_does_not_change_board():
    game = ChessGame()
    initial = game.state()["fen"]
    with pytest.raises(ValueError):
        game.apply_move("e2e5")
    assert game.state()["fen"] == initial


def test_castling_produces_rook_move():
    game = ChessGame("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    plan = game.plan_move("e1g1")
    assert (plan.rook_from, plan.rook_to) == ("h1", "f1")
    assert game.state()["turn"] == "white"


def test_en_passant_capture_square():
    game = ChessGame("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1")
    plan = game.plan_move("e5d6")
    assert plan.captured_square == "d5"


def test_promotion_plan():
    game = ChessGame("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
    assert game.plan_move("a7a8q").promotion == "q"


def test_robot_move_requires_physical_confirmation():
    controller = ChessController(LegalMoveSelector())
    initial = controller.game.state()["fen"]
    plan = controller.plan_robot_move()
    assert controller.game.state()["fen"] == initial
    assert controller.plan_robot_move() == plan
    with pytest.raises(ValueError):
        controller.confirm_robot_move("a1a2")
    assert controller.game.state()["fen"] == initial
    controller.confirm_robot_move(plan.uci)
    assert controller.game.state()["fen"] != initial


def test_checkmate():
    game = ChessGame()
    for uci in ("f2f3", "e7e5", "g2g4", "d8h4"):
        game.apply_move(uci)
    assert game.state()["game_over"] is True
    assert game.state()["result"] == "0-1"
