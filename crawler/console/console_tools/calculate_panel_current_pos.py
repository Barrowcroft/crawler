#  calculate_current_pos is a method to calculate the current position of a sliding panel.

from functools import cache

import crawler.constants as c


@cache
def calculate_current_pos(
    dt: float,
    appear: str,
    x_start_pos: int,
    y_start_pos: int,
    x_end_pos: int,
    y_end_pos: int,
    x_current_pos: int,
    y_current_pos: int,
    showing: bool,
) -> tuple[int, int]:

    x_target_pos: int = 0
    y_target_pos: int = 0

    if showing is True:
        x_target_pos = x_end_pos
        y_target_pos = y_end_pos
    if showing is False:
        x_target_pos = x_start_pos
        y_target_pos = y_start_pos

    #  Moving in the x direction, ie. comming in from left or right.

    if x_current_pos != x_target_pos:

        if x_current_pos == c.PANEL_POS_UNSET:
            x_current_pos = x_start_pos
        elif (x_current_pos < x_target_pos) and appear == "left":
            x_current_pos += int(c.PANEL_SPEED * dt)
            if x_current_pos > x_end_pos:
                x_current_pos = x_end_pos
        elif (x_current_pos > x_target_pos) and appear == "left":
            x_current_pos -= int(c.PANEL_SPEED * dt)
            if x_current_pos < x_start_pos:
                x_current_pos = x_start_pos
        elif (x_current_pos < x_target_pos) and appear == "right":
            x_current_pos += int(c.PANEL_SPEED * dt)
            if x_current_pos > x_start_pos:
                x_current_pos = x_start_pos
        elif (x_current_pos > x_target_pos) and appear == "right":
            x_current_pos -= int(c.PANEL_SPEED * dt)
            if x_current_pos < x_end_pos:
                x_current_pos = x_end_pos
        else:
            x_current_pos = x_target_pos

    #  Moving in the y direction, ie. comming in from top or bottom.

    if y_current_pos != y_target_pos:

        if y_current_pos == c.PANEL_POS_UNSET:
            y_current_pos = y_start_pos
        elif (y_current_pos < y_target_pos) and appear == "top":
            y_current_pos += int(c.PANEL_SPEED * dt)
            if y_current_pos > y_end_pos:
                y_current_pos = y_end_pos
        elif (y_current_pos > y_target_pos) and appear == "top":
            y_current_pos -= int(c.PANEL_SPEED * dt)
            if y_current_pos < y_start_pos:
                y_current_pos = y_start_pos
        elif (y_current_pos < y_target_pos) and appear == "bottom":
            y_current_pos += int(c.PANEL_SPEED * dt)
            if y_current_pos > y_start_pos:
                y_current_pos = y_start_pos
        elif (y_current_pos > y_target_pos) and appear == "bottom":
            y_current_pos -= int(c.PANEL_SPEED * dt)
            if y_current_pos < y_end_pos:
                y_current_pos = y_end_pos
        else:
            y_current_pos = y_target_pos

    return x_current_pos, y_current_pos
