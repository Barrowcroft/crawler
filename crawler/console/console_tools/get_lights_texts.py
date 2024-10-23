#  get_lights_texts is a method to assemble the light texts from two strings.


def get_lights_texts(text: list[str], percent: list[int]) -> list[str]:
    """get_lights_texts

    get_lights_texts is a method to assemble the light texts from two strings.
    One string is the text the other is a percentage value.

    Args:
        text (list[str]): text string.
        percentage (list[str]): percentage value.

    Returns:
        list[str]: new lights texts.
    """

    #  Initliaise enpty list to contain texts.

    _new_text: list[str] = []

    #  Create new texts with percentage added.

    for _text, _percent in zip(text, percent):
        _new_text.append(f"{_text} {_percent}%")

    #  Return nre list of texts.

    return _new_text
