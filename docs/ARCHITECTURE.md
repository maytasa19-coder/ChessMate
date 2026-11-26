# ChessMate Architecture (initial foundation)

## Data flow
1. Human physically moves a chess piece.
2. vision/ or an operator recognizes and verifies that move (NOT YET IMPLEMENTED).
3. ChessController.record_human_move(uci) updates the logical board.
4. ChessController.plan_robot_move() asks a selector for a legal move; board stays unchanged.
5. MovePlan describes chess squares and special cases (capture, castling, promotion).
6. A future robot_control/ adapter will map board squares to calibrated coordinates and move the arm (NOT YET IMPLEMENTED).
7. Camera/operator verifies successful physical execution.
8. ChessController.confirm_robot_move(uci) commits the move to the virtual board. On failure, cancel the pending move and reconcile actual board state; do not blindly replay.

## Modules
- chess_engine/game.py: rules, FEN state, legal moves, MovePlan.
- chess_engine/ai.py: deterministic test selector or optional external Stockfish binary.
- chess_engine/controller.py: glue and confirmation gate between planning and actual motion.
- main.py: software-only demonstration, never commands motors.
- tests/: chess logic and planning tests.
- POC_test_move_robot/: existing arm/camera experiments; untouched.
- vision/ (future): locate board, detect pieces and verify resulting positions.
- robot_control/ (future): hardware-specific ROS bridge, safe motion, calibration, gripper.
- config/ (future): board-to-robot coordinates, limits, camera calibration.
- database/ (future): games, errors and telemetry (SQLite), not required at this stage.
- interface/ (future): desktop/web user interactions and live state.

## Notes
- Uses **standard chess**, 8x8 board (not Chess960).
- A Stockfish executable must be installed separately and supplied using `--stockfish PATH`. The default selector is intentionally weak for testing.
- UCI examples: `e2e4`, promotion `a7a8q`. A physical mover must handle captured piece removal, rook movement during castling, en passant, and replacement on promotion.
- No ROS, robot SDK, database, computer vision or networking package is required to run this engine in the development PC.
- Do not run existing arm POC without verifying the servo IDs, mechanical limits and safe position for the actual robot model.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m pytest -q
python main.py
# optional, when Stockfish is installed:
python main.py --stockfish /path/to/stockfish
```
