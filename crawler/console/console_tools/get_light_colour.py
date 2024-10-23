#  get_light_colour is a method to select the correct light colour.

from crawler.config import layout_config


def get_light_colour(
    level: int,
    blink_flag: bool,
) -> tuple[int, int, int]:
    """get_light_colour

    Tet_light_colour is a method to select the correct light colour.

    If the light level is 3, then the light will only show when the blink_flag flag is set.
    Otherwise the diminished colour will be returned.

    Args:
        level (int): light level.
        blink_flag (bool): flag to indicate blink_flag cycle.

    Returns:
        tuple[int, int, int, int]: selected colour.
    """

    #  Generate the diminished version of the base colour.
    #  The diminished colour is created by taking a half of the red, green, blue components of the base colour.

    diminished_colour: tuple[int, int, int] = (
        int(layout_config.colour[0] / 2),
        int(layout_config.colour[1] / 2),
        int(layout_config.colour[2] / 2),
    )

    #  Select the correct colour based on the level and blink_flag setting, and return it.

    if level == 3:
        if blink_flag is True:
            return layout_config.danger_colour
        else:
            return diminished_colour
    elif level == 2:
        return layout_config.warning_colour
    elif level == 1:
        return layout_config.colour
    else:
        return diminished_colour
