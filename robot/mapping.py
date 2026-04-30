from config import FILES, RANKS


def make_square_maps(
    xA1: float,
    yA1: float,
    square: float,
    z_above: float,
    z_touch: float,
    rx: float,
    ry: float,
    rz: float,
):
    above = {}
    touch = {}

    for r_idx, r in enumerate(RANKS):
        for f_idx, f in enumerate(FILES):
            name = f + r
            x = xA1 + f_idx * square
            y = yA1 + r_idx * square

            above[name] = (
                f"p[{x:.3f}, {y:.3f}, {z_above:.3f}, "
                f"{rx:.3f}, {ry:.3f}, {rz:.3f}]"
            )

            touch[name] = (
                f"p[{x:.3f}, {y:.3f}, {z_touch:.3f}, "
                f"{rx:.3f}, {ry:.3f}, {rz:.3f}]"
            )

    return above, touch