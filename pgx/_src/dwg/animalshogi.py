from pgx.animal_shogi import State as AnimalShogiState


def _make_animalshogi_dwg(dwg, state: AnimalShogiState, config: dict):
    BOARD_WIDTH = 3
    BOARD_HEIGHT = config["BOARD_HEIGHT"]
    GRID_SIZE = config["GRID_SIZE"]
    color_set = config["COLOR_SET"]
    MOVE = {
        "P": [(0, -1)],
        "R": [(1, 0), (0, 1), (-1, 0), (0, -1)],
        "B": [(1, 1), (-1, 1), (-1, -1), (1, -1)],
        "K": [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, 1),
            (-1, -1),
            (1, -1),
        ],
        "G": [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, -1)],
    }

    # background
    dwg.add(
        dwg.rect(
            (0, 0),
            (
                (BOARD_WIDTH + 2) * GRID_SIZE,
                (BOARD_HEIGHT + 1) * GRID_SIZE,
            ),
            fill=color_set.background_color,
        )
    )

    # board
    # grid
    board_g = dwg.g()
    hlines = board_g.add(dwg.g(id="hlines", stroke=color_set.grid_color))
    for y in range(1, BOARD_HEIGHT):
        hlines.add(
            dwg.line(
                start=(0, GRID_SIZE * y),
                end=(
                    GRID_SIZE * BOARD_WIDTH,
                    GRID_SIZE * y,
                ),
            )
        )
    vlines = board_g.add(dwg.g(id="vline", stroke=color_set.grid_color))
    for x in range(1, BOARD_WIDTH):
        vlines.add(
            dwg.line(
                start=(GRID_SIZE * x, 0),
                end=(
                    GRID_SIZE * x,
                    GRID_SIZE * BOARD_HEIGHT,
                ),
            )
        )
    board_g.add(
        dwg.rect(
            (0, 0),
            (
                BOARD_WIDTH * GRID_SIZE,
                BOARD_HEIGHT * GRID_SIZE,
            ),
            fill="none",
            stroke=color_set.grid_color,
        )
    )

    # pieces
    p1_pieces_g = dwg.g()
    p2_pieces_g = dwg.g()

    # -1: EMPTY
    #  0: PAWN
    #  1: ROOK
    #  2: BISHOP
    #  3: KING
    #  4: GOLD
    #  5: OPP_PAWN
    #  6: OPP_ROOK
    #  7: OPP_BISHOP
    #  8: OPP_KING
    #  9: OPP_GOLD

    if state._turn == 0:
        board = state._board
    else:
        board = state._board[::-1]
    for xy in range(12):
        piece_type = "EMPTY"
        n = board[xy]
        if n in (0, 5):
            piece_type = "P"
        if n in (1, 6):
            piece_type = "B"
        if n in (2, 7):
            piece_type = "R"
        if n in (3, 8):
            piece_type = "K"
        if n in (4, 9):
            piece_type = "G"

        if piece_type == "EMPTY":
            continue

        if state._turn == 0:
            is_black = 0 <= n < 5
        else:
            is_black = 5 <= n

        if is_black:
            pieces_g = p1_pieces_g
            x = 2 - xy // BOARD_HEIGHT  # AnimalShogiStateは右上原点
            y = xy % BOARD_HEIGHT
            fill_color = color_set.p1_color
            stroke = color_set.p1_outline
        else:
            pieces_g = p2_pieces_g
            x = xy // BOARD_HEIGHT
            y = 3 - xy % BOARD_HEIGHT
            fill_color = color_set.p2_color
            stroke = color_set.p2_outline

        pieces_g.add(
            dwg.rect(
                insert=(
                    (x + 0.1) * GRID_SIZE,
                    (y + 0.1) * GRID_SIZE,
                ),
                size=(
                    0.8 * GRID_SIZE,
                    0.8 * GRID_SIZE,
                ),
                rx="3px",
                ry="3px",
                stroke=stroke,
                fill=fill_color,
            )
        )
        pieces_g.add(
            dwg.text(
                text=piece_type,
                insert=(
                    (x + 0.27) * GRID_SIZE,
                    (y + 0.72) * GRID_SIZE,
                ),
                fill=stroke,
                font_size="46px",
                font_family="Courier",
            )
        )
        # 移動可能方向
        for _x, _y in MOVE[piece_type]:
            pieces_g.add(
                dwg.circle(
                    center=(
                        (x + 0.5 + _x * 0.35) * GRID_SIZE,
                        (y + 0.5 + _y * 0.35) * GRID_SIZE,
                    ),
                    r=GRID_SIZE * 0.01,
                    stroke=stroke,
                    fill=stroke,
                )
            )

    # # hand
    for i, piece_num, piece_type in zip(
        range(6), state._hand.flatten(), ["P", "R", "B", "P", "R", "B"]
    ):
        is_black = i < 3 if state._turn == 0 else 3 <= i  # type: ignore
        _g = p1_pieces_g if is_black else p2_pieces_g
        _g.add(
            dwg.text(
                text=f"{piece_type}:{piece_num}",
                insert=(
                    3.1 * GRID_SIZE,
                    (3.3 + (i % 3) * 0.3) * GRID_SIZE,
                ),
                fill=color_set.p1_outline,
                font_size="20px",
                font_family="Courier",
            )
        )

    board_g.add(p1_pieces_g)
    p2_pieces_g.rotate(
        angle=180,
        center=(GRID_SIZE * BOARD_WIDTH / 2, GRID_SIZE * BOARD_HEIGHT / 2),
    )
    board_g.add(p2_pieces_g)
    board_g.translate(GRID_SIZE / 2, 0)

    return board_g
