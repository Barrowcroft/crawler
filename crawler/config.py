import configparser
import errno
import os
import re

import pygame

import crawler.constants as c
import crawler.customlogger as customlogger


class RootConfig:

    @customlogger.log_trace(customlogger.Levels.INFO)
    def get_config(self, name: str) -> None:
        """get_config

        Args:
            name (str): filename to read from.

        Initialises the config parser and reads the root config from the given file.
        If the config file does not exist it will be created and default logging level (INFO) set.
        """

        #  Set up config file.

        _filename = os.path.join(os.getcwd(), f"{c.GAME_NAME}", f"{c.GAME_NAME}.ini")
        self.root_config: configparser.ConfigParser = configparser.ConfigParser()

        if os.path.exists(_filename):
            self.root_config.read(_filename)
        else:

            #  The config file does not exist, so create it and set the default logging level.

            self.root_config["logging"] = {"logging_level": c.DEFAULT_LOGGING_LEVEL}
            with open(_filename, "w") as configfile:
                self.root_config.write(configfile)

            #  Log creation of config file.

            customlogger.log_message(
                f"Config file '{_filename}' does not exist - created.",
                customlogger.Levels.WARNING,
            )

            #  Log creation of 'logging/logging_level' entry.

            customlogger.log_message(
                f"Config file missing 'logging/logging_level' entry - default created '{c.DEFAULT_LOGGING_LEVEL}'.",
                customlogger.Levels.WARNING,
            )


class LayoutConfig:

    @customlogger.log_trace(customlogger.Levels.INFO)
    def __init__(self) -> None:

        #  Initialise variables.

        self.name: str = ""
        self.font_name: str = ""
        self.font_size: int = 0
        self.font_small_size: int = 0
        self.font_large_size: int = 0
        self.font_banner_size: int = 0
        self.colour: tuple[int, int, int] = (0, 0, 0)
        self.muted_colour: tuple[int, int, int] = (0, 0, 0)
        self.warning_colour: tuple[int, int, int] = (0, 0, 0)
        self.danger_colour: tuple[int, int, int] = (0, 0, 0)
        self.alternative_colours: tuple[
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
        ] = (
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
        )
        self.corner_radius: int = 0
        self.background_flag: bool = False
        self.frame_flag: bool = False
        self.streamer_flag: bool = False
        self.map_position: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.terminal_position: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.menu_position: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.inventory_position: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.status_position: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.status_right_flag: bool = True
        self.terminal_right_flag: bool = True
        self.minimap_top_flag: bool = True
        self.hold_top_flag: bool = True
        self.scanlines_flag: bool = True
        self.alarm_sound_flag: bool = True
        self.key_sound_flag: bool = True
        self.button_sound_flag: bool = True
        self.ambient_sound_flag: bool = True
        self.scanlines_flag: bool = True
        self.alarm_sound_name: str = ""
        self.key_sound_name: str = ""
        self.button_sound_name: str = ""
        self.scanner_sound_name: str = ""
        self.buzz_sound_name: str = ""
        self.ambient_sound_name: str = ""

    @customlogger.log_trace(customlogger.Levels.INFO)
    def get_config(self) -> None:
        """get_config

        Checks root config file exists and exits with an error if it does not.
        Reads console layout filename from the 'console_layout/current' entry from the root config file.
        Loads the layout config file.

        There are two configparsers: one is config_parser which relates to the main configuration file,
        an entry in which names the layout configuration file loaded as layout_parser.

        Raises:
            FileNotFoundError: if the config file does not exist at this point it is an error condition.
        """
        #  Get the configuration filename and create configparser object.

        _root_config_filename = os.path.join(
            os.getcwd(), f"{c.GAME_NAME}", f"{c.GAME_NAME}.ini"
        )
        _root_config_parser: configparser.ConfigParser = configparser.ConfigParser()

        #  Check the configuration file exists; if it does, read it.
        #  If it didn't exist when the program started it should have been created by now.
        #  If it's not found return an error.

        if os.path.exists(_root_config_filename):
            _root_config_parser.read(_root_config_filename)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), _root_config_filename
            )

        #  Get the name of the file containing the console layout information.

        _current_layout_name: str = self.get_current_layout_filename(
            _root_config_parser, _root_config_filename
        )

        #  Load the layout information.

        self.load_current_layout(_current_layout_name)

        #  Generate the actual layout values from the layout config.

        self.name = self.generate_name_value(self.layout_config)

        self.font_name = self.generate_font_value(self.layout_config)

        self.font_size = self.generate_font_size_value(self.layout_config)

        self.font_small_size = self.generate_font_small_size_value(self.layout_config)

        self.font_large_size = self.generate_font_large_size_value(self.layout_config)

        self.font_banner_size = self.generate_font_banner_size_value(self.layout_config)

        self.colour = self.generate_colour_value(self.layout_config)

        self.muted_colour = self.generate_muted_colour_value(self.layout_config)

        self.danger_colour = self.generate_danger_colour_value(self.layout_config)

        self.warning_colour = self.generate_warning_colour_value(self.layout_config)

        self.alternative_colours = self.generate_alternative_colour_values(
            self.layout_config
        )

        self.corner_radius = self.generate_corner_radius_value(self.layout_config)

        self.background_flag = self.generate_background_flag_value(self.layout_config)

        self.frame_flag = self.generate_frame_flag_value(self.layout_config)

        self.streamer_flag = self.generate_streamer_flag_value(self.layout_config)

        #  Generate the pane layout values.

        _layout: tuple[
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
        ] = self.generate_pane_positions(self.layout_config)

        #  Save the generated values.

        self.map_position = _layout[0]

        self.terminal_position = _layout[1]

        self.menu_position = _layout[2]

        self.inventory_position = _layout[3]

        self.status_position = _layout[4]

        self.status_right_flag = self.generate_status_right_flag_value(
            self.layout_config
        )

        self.terminal_right_flag = self.generate_terminal_right_flag_value(
            self.layout_config
        )

        self.minimap_top_flag = self.generate_minimap_top_flag_value(self.layout_config)

        self.hold_top_flag = self.generate_hold_top_flag_value(self.layout_config)

        self.scanlines_flag = self.generate_scanlines_flag_value(self.layout_config)

        self.alarm_sound_flag = self.generate_alarm_sound_flag_value(self.layout_config)

        self.key_sound_flag = self.generate_key_sound_flag_value(self.layout_config)

        self.button_sound_flag = self.generate_button_sound_flag_value(
            self.layout_config
        )

        self.scanner_sound_flag = self.generate_scanner_sound_flag_value(
            self.layout_config
        )

        self.ambient_sound_flag = self.generate_ambient_sound_flag_value(
            self.layout_config
        )

        self.alarm_sound_name = self.generate_alarm_sound_name_value(self.layout_config)

        self.key_sound_name = self.generate_key_sound_name_value(self.layout_config)

        self.button_sound_name = self.generate_button_sound_name_value(
            self.layout_config
        )

        self.scanner_sound_name = self.generate_scan_sound_name_value(
            self.layout_config
        )

        self.buzz_sound_name = self.generate_buzz_sound_name_value(self.layout_config)

        self.ambient_sound_name = self.generate_ambient_sound_name_value(
            self.layout_config
        )

        #  Generate the required font objects.

        self.font: pygame.font.Font = pygame.font.SysFont(
            self.font_name, self.font_size
        )

        self.small_font_obj: pygame.font.Font = pygame.font.SysFont(
            self.font_name, self.font_small_size
        )

        self.large_font_obj: pygame.font.Font = pygame.font.SysFont(
            self.font_name, self.font_large_size
        )

    @customlogger.log_trace(customlogger.Levels.INFO)
    def get_current_layout_filename(
        self, root_config_parser: configparser.ConfigParser, filename: str
    ) -> str:
        """get_current_layout_filename

        Gets the 'console_layout/current' from the root config parser.
        If it does not exist it creates it.

        Args:
            root_config_parser (configparser.ConfigParser): root config parser from which to get filename of layout.
            filename (str): filename of config parser.

        Returns:
            str: _description_
        """
        #  Get the name of the file containing the console layout information.
        #  If the config file does not contain an entry for the current console layout then create it.

        _current_layout_name: str = ""

        try:
            _current_layout_name = root_config_parser.get("console_layout", "current")
        except (configparser.NoSectionError, configparser.NoOptionError):

            #  Create missing 'console_layout/current' entry, and log it.

            _current_layout_name = c.DEFAULT_LAYOUT_FILENAME
            root_config_parser["console_layout"] = {"current": _current_layout_name}
            with open(filename, "w") as configfile:
                root_config_parser.write(configfile)

            customlogger.log_message(
                f"Config file missing 'console_layout/current' entry - default created '{_current_layout_name}'.",
                customlogger.Levels.WARNING,
            )

        return _current_layout_name

    @customlogger.log_trace(customlogger.Levels.INFO)
    def load_current_layout(self, current_layout_filename: str) -> None:
        """load_current_layout

        Checks if the layout file exists.
        If it does not exist, it will be created.
        Reads the layout file, and creates any missing entries from default values.

        Args:
            current_layout (str): Filename of layout file for current configuration.
        """
        #  Chec that the layouts directory exisits and create it if it doesnt, and log it.

        _diectory: str = os.path.join(os.getcwd(), f"{c.GAME_NAME}", c.DIR_LAYOUTS)

        if not os.path.exists(_diectory):
            os.makedirs(_diectory)

            customlogger.log_message(
                f"Layout direcotry '{c.DIR_LAYOUTS}' does not exist - created.",
                customlogger.Levels.WARNING,
            )

        #  Get the configuration filename and create configparser object.

        self.layout_filename = os.path.join(
            os.getcwd(), f"{c.GAME_NAME}", c.DIR_LAYOUTS, current_layout_filename
        )

        self.layout_config: configparser.ConfigParser = configparser.ConfigParser()

        #  If the current layout file does not exist, create it.

        if os.path.exists(self.layout_filename):
            self.layout_config.read(self.layout_filename)
        else:

            #  The layout file does not exist, so create it and log it.

            with open(self.layout_filename, "w") as layoutfile:
                self.layout_config.write(layoutfile)

            _current_layout_name = c.DEFAULT_LAYOUT_FILENAME
            self.layout_config["console_layout"] = {"name": _current_layout_name}
            with open(self.layout_filename, "w") as configfile:
                self.layout_config.write(configfile)

            customlogger.log_message(
                f"Layout file '{self.layout_filename}' does not exist - created.",
                customlogger.Levels.WARNING,
            )

            customlogger.log_message(
                f"Layout file missing 'console_layout/name' entry - default created '{_current_layout_name}'.",
                customlogger.Levels.WARNING,
            )

        #  Now check each of the layout items, creating them from default if not found.

        self.layout_config = self.load_layout_item(
            self.layout_config, self.layout_filename, "name", current_layout_filename
        )

        self.layout_config = self.load_layout_item(
            self.layout_config, self.layout_filename, "font", c.DEFAULT_CONSOLE_FONT
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "font_size",
            str(c.DEFAULT_CONSOLE_FONT_SIZE),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "font_small_size",
            str(c.DEFAULT_CONSOLE_FONT_SMALL_SIZE),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "font_large_size",
            str(c.DEFAULT_CONSOLE_FONT_LARGE_SIZE),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "font_banner_size",
            str(c.DEFAULT_CONSOLE_FONT_BANNER_SIZE),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "colour",
            str(c.DEFAULT_CONSOLE_COLOUR),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "danger_colour",
            str(c.DEFAULT_CONSOLE_DANGER_COLOUR),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "warning_colour",
            str(c.DEFAULT_CONSOLE_WARNING_COLOUR),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "alternative_colours",
            str(c.DEFAULT_CONSOLE_ALTERNATIVE_COLOURS),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "corner_radius",
            str(c.DEFAULT_CONSOLE_CORNER_RADIUS),
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "background_flag",
            c.DEFAULT_CONSOLE_BACKGROUND_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "frame_flag",
            c.DEFAULT_CONSOLE_FRAME_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "streamer_flag",
            c.DEFAULT_CONSOLE_STREAMER_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "map_position",
            c.DEFAULT_CONSOLE_MAP_POSITION,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "status_right_flag",
            c.DEFAULT_CONSOLE_STATUS_RIGHT_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "terminal_right_flag",
            c.DEFAULT_CONSOLE_TERMINAL_RIGHT_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "minimap_top_flag",
            c.DEFAULT_CONSOLE_MINIMAP_TOP_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "hold_top_flag",
            c.DEFAULT_CONSOLE_HOLD_TOP_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "scanlines_flag",
            c.DEFAULT_CONSOLE_SCANLINES_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "alarm_sound_flag",
            c.DEFAULT_CONSOLE_ALARM_SOUND_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "key_sound_flag",
            c.DEFAULT_CONSOLE_KEY_SOUND_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "button_sound_flag",
            c.DEFAULT_CONSOLE_BUTTON_SOUND_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "scanner_sound_flag",
            c.DEFAULT_CONSOLE_SCANNER_SOUND_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "ambient_sound_flag",
            c.DEFAULT_CONSOLE_AMBIENT_SOUND_FLAG,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "alarm_sound_name",
            c.DEFAULT_CONSOLE_ALARM_SOUND_NAME,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "key_sound_name",
            c.DEFAULT_CONSOLE_KEY_SOUND_NAME,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "button_sound_name",
            c.DEFAULT_CONSOLE_BUTTON_SOUND_NAME,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "scanner_sound_name",
            c.DEFAULT_CONSOLE_SCAN_SOUND_NAME,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "buzz_sound_name",
            c.DEFAULT_CONSOLE_BUZZ_SOUND_NAME,
        )

        self.layout_config = self.load_layout_item(
            self.layout_config,
            self.layout_filename,
            "ambient_sound_name",
            c.DEFAULT_CONSOLE_AMBIENT_SOUND_NAME,
        )

    def load_layout_item(
        self,
        layout_config: configparser.ConfigParser,
        layout_filename: str,
        name: str,
        default: str,
    ) -> configparser.ConfigParser:
        """load_layout_item

        Args:
            layout_config (configparser.ConfigParser): _description_
            layout_filename (str): _description_
            name (str): _description_
            default (str): _description_

        Returns:
            configparser.ConfigParser: _description_
        """
        try:
            layout_config.get("console_layout", name)
        except (configparser.NoSectionError, configparser.NoOptionError):

            layout_config["console_layout"][name] = str(default)
            with open(layout_filename, "w") as configfile:
                layout_config.write(configfile)

            customlogger.log_message(
                f"Layout file missing 'console_layout/{name}' entry - default created '{default}'.",
                customlogger.Levels.WARNING,
            )

        return layout_config

    def save_current_layout(
        self,
    ) -> None:
        """save_current_layout

        Saves the current layout to the cirrent configuration file.
        """
        with open(self.layout_filename, "w") as layoutfile:
            self.layout_config.write(layoutfile)

        customlogger.log_message(
            f"Layout file  '{self.layout_filename}' saved.",
            customlogger.Levels.INFO,
        )

    #  Read the layout config and create values.

    def generate_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_name_value

        Reads the name from the layout configuration.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: name.
        """
        return layout_config["console_layout"]["name"]

    def generate_font_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_font_value

        Reads the font from the layout configuration.
        Genertes font objects.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: font name.
        """

        self.font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_size"]),
        )

        self.small_font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_small_size"]),
        )

        self.large_font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_large_size"]),
        )

        return layout_config["console_layout"]["font"]

    def generate_font_size_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> int:
        """generate_font_size_value

        Reads the font size from the layout configuration.
        Generates font object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            int: font size.
        """

        self.font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_size"]),
        )

        return int(layout_config["console_layout"]["font_size"])

    def generate_font_small_size_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> int:
        """generate_font_small_size_value

        Reads the font small size from the layout configuration.
        Generates font object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            int: font small size.
        """

        self.small_font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_small_size"]),
        )

        return int(layout_config["console_layout"]["font_small_size"])

    def generate_font_large_size_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> int:
        """generate_font_large_size_value

        Reads the font large size from the layout configuration.
        Generates font object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            int: font large size.
        """

        self.large_font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_large_size"]),
        )

        return int(layout_config["console_layout"]["font_large_size"])

    def generate_font_banner_size_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> int:
        """generate_font_large_size_value

        Reads the font banner size from the layout configuration.
        Generates font object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            int: font banner size.
        """

        self.banner_font: pygame.font.Font = pygame.font.SysFont(
            layout_config["console_layout"]["font"],
            int(layout_config["console_layout"]["font_banner_size"]),
        )

        return int(layout_config["console_layout"]["font_banner_size"])

    def generate_colour_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> tuple[int, int, int]:
        """generate_colour_value

        Reads the colour from the layout configuration and generates the correct colour values as (r, g, b).

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            tuple[int, int, int]: colour value.
        """
        red, green, blue = (
            layout_config["console_layout"]["colour"].strip("(").strip(")").split(",")
        )
        return (int(red), int(green), int(blue))

    def generate_muted_colour_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> tuple[int, int, int]:
        """generate_colour_value

        Reads the colour from the layout configuration and generates the correct muted colour values as (r, g, b).
        Muted colour is created by taking a fifth of the red, green, blue components of the Base colour

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            tuple[int, int, int]: colour value.
        """
        red, green, blue = (
            layout_config["console_layout"]["colour"].strip("(").strip(")").split(",")
        )
        return (int(int(red) / 5), int(int(green) / 5), int(int(blue) / 5))

    def generate_warning_colour_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> tuple[int, int, int]:
        """generate_warning_colour_value

        Reads the warning colour from the layout configuration and generates the corect colour values as (r, g, b).

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            tuple[int, int, int]: warning colour value.
        """
        red, green, blue = (
            layout_config["console_layout"]["warning_colour"]
            .strip("(")
            .strip(")")
            .split(",")
        )
        return (int(red), int(green), int(blue))

    def generate_danger_colour_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> tuple[int, int, int]:
        """generate_danger_colour_value

        Reads the danger colour from the layout configuration and generates the corect colour values as (r, g, b).

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            tuple[int, int, int]: danger colour value.
        """
        red, green, blue = (
            layout_config["console_layout"]["danger_colour"]
            .strip("(")
            .strip(")")
            .split(",")
        )
        return (int(red), int(green), int(blue))

    def generate_alternative_colour_values(
        self,
        layout_config: configparser.ConfigParser,
    ) -> tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ]:
        """generate_alternative_colour_values

        Reads the alternative colours from the layout configuration and generates a list of colour value strings as "(r, g, b)".

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            list[Any]: list of alternative colour values, strings as "(r, g, b)"
        """
        colour_string = layout_config["console_layout"]["alternative_colours"]
        colour_string = colour_string[1 : len(colour_string) - 1]
        numbers = re.findall(r"\d+", colour_string)
        return (
            (numbers[0], numbers[1], numbers[2]),
            (numbers[3], numbers[4], numbers[5]),
            (numbers[6], numbers[7], numbers[8]),
            (numbers[9], numbers[10], numbers[11]),
            (numbers[12], numbers[13], numbers[14]),
        )

    def generate_corner_radius_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> int:
        """generate_corner_radius_value

        Reads the corner radius from the layout configuration and returns it as an integer.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            int: corner radius.
        """
        return int(layout_config["console_layout"]["corner_radius"])

    def generate_background_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_background_flag_value

        Reads the background from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: background flag.
        """
        if layout_config["console_layout"]["background_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_frame_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_frame_flag_value

        Reads the frame flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: frame flag.
        """
        if layout_config["console_layout"]["frame_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_streamer_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_streamer_flag_value

        Reads the streamer flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: streamer flag.
        """
        if layout_config["console_layout"]["streamer_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_pane_positions(
        self,
        layout_config: configparser.ConfigParser,
    ) -> tuple[
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
    ]:
        """generate_pane_positions

        Selects the correct pane layout from the predefined layouts based on the map layout selected.
        Also adjusted for the 'status_right' and 'terminal_right' settings.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            tuple[ tuple[int, int, int, int], tuple[int, int, int, int], tuple[int, int, int, int], tuple[int, int, int, int], tuple[int, int, int, int], ]: _description_
        """

        #  Select the basic layout.

        _layout: tuple[
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
        ] = ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))

        if layout_config["console_layout"]["map_position"] == "LEFT_TOP":
            if self.streamer_flag is True:
                _layout = c.MAP_LEFT_TOP_STREAMER
            else:
                _layout = c.MAP_LEFT_TOP
        if layout_config["console_layout"]["map_position"] == "LEFT_BOTTOM":
            if self.streamer_flag is True:
                _layout = c.MAP_LEFT_BOTTOM_STREAMER
            else:
                _layout = c.MAP_LEFT_BOTTOM
        if layout_config["console_layout"]["map_position"] == "MIDDLE_TOP":
            if self.streamer_flag is True:
                _layout = c.MAP_MIDDLE_TOP_STREAMER
            else:
                _layout = c.MAP_MIDDLE_TOP
        if layout_config["console_layout"]["map_position"] == "MIDDLE_BOTTOM":
            if self.streamer_flag is True:
                _layout = c.MAP_MIDDLE_BOTTOM_STREAMER
            else:
                _layout = c.MAP_MIDDLE_BOTTOM
        if layout_config["console_layout"]["map_position"] == "RIGHT_TOP":
            if self.streamer_flag is True:
                _layout = c.MAP_RIGHT_TOP_STREAMER
            else:
                _layout = c.MAP_RIGHT_TOP
        if layout_config["console_layout"]["map_position"] == "RIGHT_BOTTOM":
            if self.streamer_flag is True:
                _layout = c.MAP_RIGHT_BOTTOM_STREAMER
            else:
                _layout = c.MAP_RIGHT_BOTTOM

        #  Move status pane as required.

        if layout_config["console_layout"]["status_right_flag"] == "TRUE":
            ...
        else:
            _layout = (_layout[0], _layout[1], _layout[2], _layout[4], _layout[3])

        _adjust: int = 450
        if self.streamer_flag is True:
            _adjust = 150

        #  Move terminal pane as required.

        if layout_config["console_layout"]["terminal_right_flag"] == "TRUE":
            _layout = (
                _layout[0],
                (
                    _layout[2][0] - _adjust,
                    _layout[2][1],
                    _layout[1][2],
                    _layout[1][3],
                ),
                (
                    _layout[1][0],
                    _layout[1][1],
                    _layout[2][2],
                    _layout[2][3],
                ),
                _layout[3],
                _layout[4],
            )

        return _layout

    def generate_status_right_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_status_right_flag_value

        Reads the minimap status right flag from the layout configuration and returns it as a boolean.
        This determines if the status pane will be drawn at the right of the inventory panel.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: status right flag.
        """
        if layout_config["console_layout"]["status_right_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_terminal_right_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_terminal_right_flag_value

        Reads the minimap terminal right flag from the layout configuration and returns it as a boolean.
        This determines if the terminal pane will be drawn at the right of the inventory panel.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: terminal right flag.
        """
        if layout_config["console_layout"]["terminal_right_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_minimap_top_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_minimap_top_flag_value

        Reads the minimap top flag from the layout configuration and returns it as a boolean.
        This determines if the minimap will be drawn at the top of the status panel.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: mnimap top flag.
        """
        if layout_config["console_layout"]["minimap_top_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_hold_top_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_hold_top_flag_value

        Reads the hold top flag from the layout configuration and returns it as a boolean.
        This determines if the hold will be drawn at the top of the inventory panel.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: hold top flag.
        """
        if layout_config["console_layout"]["hold_top_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_scanlines_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_scanlines_flag_value

        Reads the scanlines flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: scanlines flag.
        """
        if layout_config["console_layout"]["scanlines_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_alarm_sound_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_alarm_sound_flag_value

        Reads the alarm sound flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: alarm sound flag.
        """
        if layout_config["console_layout"]["alarm_sound_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_key_sound_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_key_sound_flag_value

        Reads the key sound flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: key sound flag.
        """
        if layout_config["console_layout"]["key_sound_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_button_sound_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_button_sound_flag_value

        Reads the button sound flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: button sound flag.
        """
        if layout_config["console_layout"]["button_sound_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_scanner_sound_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_scanner_sound_flag_value

        Reads the scanner sound flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: scanner sound flag.
        """
        if layout_config["console_layout"]["scanner_sound_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_ambient_sound_flag_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> bool:
        """generate_ambient_sound_flag_value

        Reads the ambient sound flag from the layout configuration and returns it as a boolean.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration

        Returns:
            bool: ambient sound flag.
        """
        if layout_config["console_layout"]["ambient_sound_flag"] == "TRUE":
            return True
        else:
            return False

    def generate_alarm_sound_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_alarm_sound_name_value

        Reads the alarm sound from the layout configuration.
        Generates the sound object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: alarm_sound name.
        """
        self.alarm_sound = pygame.mixer.Sound(
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_SOUNDS,
                layout_config["console_layout"]["alarm_sound_name"],
            )
        )

        return layout_config["console_layout"]["alarm_sound_name"]

    def generate_scan_sound_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_scan_sound_name_value

        Reads the scan sound from the layout configuration.
        Generates the soun dobject.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: scan_sound name.
        """
        self.scan_sound = pygame.mixer.Sound(
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_SOUNDS,
                layout_config["console_layout"]["scanner_sound_name"],
            )
        )

        return layout_config["console_layout"]["scanner_sound_name"]

    def generate_key_sound_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_key_sound_name_value

        Reads the key sound from the layout configuration.
        Generates the sound object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: key_sound name.
        """
        self.key_sound = pygame.mixer.Sound(
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_SOUNDS,
                layout_config["console_layout"]["key_sound_name"],
            )
        )

        return layout_config["console_layout"]["key_sound_name"]

    def generate_button_sound_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_button_sound_name_value

        Reads the button sound from the layout configuration.
        Generates the sound object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: button_sound name.
        """
        self.button_sound = pygame.mixer.Sound(
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_SOUNDS,
                layout_config["console_layout"]["button_sound_name"],
            )
        )

        return layout_config["console_layout"]["button_sound_name"]

    def generate_buzz_sound_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_buzz_sound_name_value

        Reads the buzz sound from the layout configuration.
        Generates the sound object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: buzz_sound name.
        """
        self.buzz_sound = pygame.mixer.Sound(
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_SOUNDS,
                layout_config["console_layout"]["buzz_sound_name"],
            )
        )
        self.buzz_sound.set_volume(0.3)

        return layout_config["console_layout"]["buzz_sound_name"]

    def generate_ambient_sound_name_value(
        self,
        layout_config: configparser.ConfigParser,
    ) -> str:
        """generate_ambient_sound_name_value

        Reads the ambient sound from the layout configuration.
        Generates the sound object.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.

        Returns:
            str: ambient_sound name.
        """
        self.ambient_sound = pygame.mixer.Sound(
            os.path.join(
                "crawler",
                c.DIR_ASSETS,
                c.DIR_MUSIC,
                layout_config["console_layout"]["ambient_sound_name"],
            )
        )
        self.ambient_sound.set_volume(0.1)

        return layout_config["console_layout"]["ambient_sound_name"]

    #  Update the layout data and regenerate values.

    def update_name_value(
        self, layout_config: configparser.ConfigParser, name: str
    ) -> None:
        """update_name_value

        Updates the name in the layout config and regenerates the name value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            name (str): new name to enter into the layout configuration.
        """
        layout_config["console_layout"]["name"] = name
        self.name = self.generate_name_value(layout_config)

    def update_font_name_value(
        self, layout_config: configparser.ConfigParser, font_name: str
    ) -> None:
        """update_font_name_value

        Updates the font name in the layout config and regenerates font name value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            font_name (str): new font name to enter into the layout configuration.
        """
        layout_config["console_layout"]["font"] = font_name
        self.font_name = self.generate_font_value(layout_config)

    def update_font_size_value(
        self, layout_config: configparser.ConfigParser, font_size: int
    ) -> None:
        """update_font_size_value

        Updates the font size in the layout config and regenerates font size value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            font_size (str): new font size to enter into the layout configuration.
        """
        layout_config["console_layout"]["font_size"] = str(font_size)
        self.font_size = self.generate_font_size_value(layout_config)

    def update_font_small_size_value(
        self, layout_config: configparser.ConfigParser, font_small_size: int
    ) -> None:
        """update_font_small_size_value

        Updates the font small size in the layout config and regenerates font small size value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            font_small_size (str): new font small size to enter into the layout configuration.
        """
        layout_config["console_layout"]["font_small_size"] = str(font_small_size)
        self.font_small_size = self.generate_font_small_size_value(layout_config)

    def update_font_large_size_value(
        self, layout_config: configparser.ConfigParser, font_large_size: int
    ) -> None:
        """update_font_large_size_value

        Updates the font large size in the config parser and regenerates the font large size value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            font_large_size (str): new font large size to enter into the layout configuration.
        """
        layout_config["console_layout"]["font_large_size"] = str(font_large_size)
        self.font_large_size = self.generate_font_large_size_value(layout_config)

    def update_banner_large_size_value(
        self, layout_config: configparser.ConfigParser, font_banner_size: int
    ) -> None:
        """update_font_large_size_value

        Updates the banner large size in the config parser and regenerates the banner large size value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            font_large_size (str): new banner large size to enter into the layout configuration.
        """
        layout_config["console_layout"]["font_banner_size"] = str(font_banner_size)
        self.font_large_size = self.generate_font_banner_size_value(layout_config)

    def update_colour_value(
        self, layout_config: configparser.ConfigParser, colour: tuple[int, int, int]
    ) -> None:
        """update_colour_value

        Updates the colour in the layout config and regenerates the colour (and muted colour) value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            colour (tuple[int,int,int]): new colour to enter into the layout configuration.
        """
        layout_config["console_layout"][
            "colour"
        ] = f"({colour[0]},{colour[1]},{colour[2]})"
        self.colour = self.generate_colour_value(layout_config)
        self.muted_colour = self.generate_muted_colour_value(layout_config)

    def update_warning_colour_value(
        self,
        layout_config: configparser.ConfigParser,
        warning_colour: tuple[int, int, int],
    ) -> None:
        """update_warning_colour_value

        Updates the warning colour in the layout config and regenerates the warning colour value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            warning_colour (tuple[int,int,int]): new warning colour to enter into the layout configuration.
        """
        layout_config["console_layout"][
            "warning_colour"
        ] = f"({warning_colour[0]},{warning_colour[1]},{warning_colour[2]})"
        self.warning_colour = self.generate_warning_colour_value(layout_config)

    def update_danger_colour_value(
        self,
        layout_config: configparser.ConfigParser,
        danger_colour: tuple[int, int, int],
    ) -> None:
        """update_danger_colour_value

        Updates the danger value in the layout config and regenerates the danger colour value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            danger_colour (tuple[int,int,int]): new danger colour to enter into the layout configuration.
        """
        layout_config["console_layout"][
            "danger_colour"
        ] = f"({danger_colour[0]},{danger_colour[1]},{danger_colour[2]})"
        self.danger_colour = self.generate_danger_colour_value(layout_config)

    def update_alternative_colour_values(
        self,
        layout_config: configparser.ConfigParser,
        alternative_colours: tuple[
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
        ],
    ) -> None:
        """update_alternative_colour_values

        Updates the alternative colour in the layout config and regenerates the alternative colour value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            alternative_colours (tuple[int,int,int]): new alternative colours to enter into the layout configuration.
        """
        layout_config["console_layout"][
            "alt_colours"
        ] = f"({alternative_colours[0][0]},{alternative_colours[0][1]},{alternative_colours[0][2]}),({alternative_colours[1][0]},{alternative_colours[1][1]},{alternative_colours[1][2]}),({alternative_colours[2][0]},{alternative_colours[2][1]},{alternative_colours[2][2]}),({alternative_colours[3][0]},{alternative_colours[3][1]},{alternative_colours[3][2]}),({alternative_colours[4][0]},{alternative_colours[4][1]},{alternative_colours[4][2]})"
        self.alternative_colours = self.generate_alternative_colour_values(
            self.layout_config
        )

    def update_corner_radius_value(
        self, layout_config: configparser.ConfigParser, corner_radius: int
    ) -> None:
        """update_corner_radius_value

        Updates the corner radius in the layout config and regenerates the corner radius value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            corner_radius (tuple[int,int,int]): new corner radius to enter into the layout configuration.
        """
        layout_config["console_layout"]["corner_radius"] = str(corner_radius)
        self.corner_radius = self.generate_corner_radius_value(layout_config)

    def update_background_flag_value(
        self, layout_config: configparser.ConfigParser, background_flag: bool
    ) -> None:
        """update_background_flag_value

        Updates the background flag in the layout config and regenerates the background flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            background_flag (bool): new background flag to enter into the layout configuration.
        """
        if background_flag is True:
            layout_config["console_layout"]["background_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["background_flag"] = "FALSE"
        self.background_flag = self.generate_background_flag_value(layout_config)

    def update_frame_flag_value(
        self, layout_config: configparser.ConfigParser, frame_flag: bool
    ) -> None:
        """update_frame_flag_value

        Updates the frame flag in the layout config and regenerates the frame flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            frame_flag (bool): new frame flag to enter into the layout configuration.
        """
        if frame_flag is True:
            layout_config["console_layout"]["frame_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["frame_flag"] = "FALSE"

        self.frame_flag = self.generate_frame_flag_value(layout_config)

    def update_streamer_flag_value(
        self, layout_config: configparser.ConfigParser, streamer_flag: bool
    ) -> None:
        """update_streamer_flag_value

        Updates the streamer flag in the layout config and regenerates the streamer flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            streamer_flag (bool): new streamer flag to enter into the layout configuration.
        """
        if streamer_flag is True:
            layout_config["console_layout"]["streamer_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["streamer_flag"] = "FALSE"

        self.streamer_flag = self.generate_streamer_flag_value(layout_config)

        _layout: tuple[
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
        ] = self.generate_pane_positions(layout_config)

        #  Save the generated values.

        self.map_position = _layout[0]

        self.terminal_position = _layout[1]

        self.menu_position = _layout[2]

        self.inventory_position = _layout[3]

        self.status_position = _layout[4]

    def update_pane_positions(
        self, layout_config: configparser.ConfigParser, map_position: str
    ) -> None:
        """update_pane_positions

        Updates the layout in the layout config and regenerates the layout values.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            map_position (str): new map position to enter into the layout configuration.
        """

        layout_config["console_layout"]["map_position"] = map_position

        _layout: tuple[
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
        ] = self.generate_pane_positions(layout_config)

        #  Save the generated values.

        self.map_position = _layout[0]

        self.terminal_position = _layout[1]

        self.menu_position = _layout[2]

        self.inventory_position = _layout[3]

        self.status_position = _layout[4]

    def update_status_right_flag(
        self, layout_config: configparser.ConfigParser, status_right_flag: bool
    ) -> None:
        """update_status_right_flag

        Updates the status right flag in the layout config and regenerates the layout values.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            status_right_flag (bool): new statsu rght flag to enter into the layout configuration.
        """

        if status_right_flag is True:
            layout_config["console_layout"]["status_right_flag"] = "TRUE"
            self.status_right_flag = True
        else:
            layout_config["console_layout"]["status_right_flag"] = "FALSE"
            self.status_right_flag = False

        _layout: tuple[
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
        ] = self.generate_pane_positions(layout_config)

        #  Save the generated values.

        self.map_position = _layout[0]

        self.terminal_position = _layout[1]

        self.menu_position = _layout[2]

        self.inventory_position = _layout[3]

        self.status_position = _layout[4]

        self.status_right_flag = self.generate_status_right_flag_value(layout_config)

    def update_terminal_right_flag(
        self, layout_config: configparser.ConfigParser, status_right_flag: bool
    ) -> None:
        """update_terminal_right_flag

        Updates the terminal right flag in the layout config and regenerates the layout values.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            terminal_right_flag (bool): new terminal right flag to enter into the layout configuration.
        """

        if status_right_flag is True:
            layout_config["console_layout"]["terminal_right_flag"] = "TRUE"
            self.terminal_right_flag = True
        else:
            layout_config["console_layout"]["terminal_right_flag"] = "FALSE"
            self.terminal_right_flag = False

        _layout: tuple[
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
        ] = self.generate_pane_positions(layout_config)

        #  Save the generated values.

        self.map_position = _layout[0]

        self.terminal_position = _layout[1]

        self.menu_position = _layout[2]

        self.inventory_position = _layout[3]

        self.status_position = _layout[4]

        self.terminal_right_flag = self.generate_terminal_right_flag_value(
            layout_config
        )

    def update_minimap_top_flag_value(
        self, layout_config: configparser.ConfigParser, minimap_top_flag: bool
    ) -> None:
        """update_minimap_top_flag_value

        Updates the minimap_top flag in the layout config and regenerates the minimap_top flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            minimap_top_flag (bool): new minimap_top flag to enter into the layout configuration.
        """
        if minimap_top_flag is True:
            layout_config["console_layout"]["minimap_top_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["minimap_top_flag"] = "FALSE"
        self.minimap_top_flag = self.generate_minimap_top_flag_value(layout_config)

    def update_hold_top_flag_value(
        self, layout_config: configparser.ConfigParser, hold_top_flag: bool
    ) -> None:
        """update_hold_top_flag_value

        Updates the hold_top flag in the layout config and regenerates the hold_top flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            hold_top_flag (bool): new hold_top flag to enter into the layout configuration.
        """
        if hold_top_flag is True:
            layout_config["console_layout"]["hold_top_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["hold_top_flag"] = "FALSE"
        self.hold_top_flag = self.generate_hold_top_flag_value(layout_config)

    def update_scanlines_flag_value(
        self, layout_config: configparser.ConfigParser, scanlines_flag: bool
    ) -> None:
        """update_scanlines_flag_value

        Updates the scanlines flag in the layout config and regenerates the scanlines flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            scanlines_flag (bool): new scanlines flag to enter into the layout configuration.
        """
        if scanlines_flag is True:
            layout_config["console_layout"]["scanlines_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["scanlines_flag"] = "FALSE"
        self.scanlines_flag = self.generate_scanlines_flag_value(layout_config)

    def update_alarm_sound_flag_value(
        self, layout_config: configparser.ConfigParser, alarm_sound_flag: bool
    ) -> None:
        """update_alarm_sound_flag_value

        Updates the alarm_sound flag in the layout config and regenerates the alarm sound flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            alarm_sound_flag (bool): new alarm_sound flag to enter into the layout configuration.
        """
        if alarm_sound_flag is True:
            layout_config["console_layout"]["alarm_sound_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["alarm_sound_flag"] = "FALSE"
        self.alarm_sound_flag = self.generate_alarm_sound_flag_value(layout_config)

    def update_key_sound_flag_value(
        self, layout_config: configparser.ConfigParser, key_sound_flag: bool
    ) -> None:
        """update_key_sound_flag_value

        Updates the key_sound flag in the layout config and regenerates the key sound flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            key_sound_flag (bool): new key_sound flag to enter into the layout configuration.
        """
        if key_sound_flag is True:
            layout_config["console_layout"]["key_sound_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["key_sound_flag"] = "FALSE"
        self.key_sound_flag = self.generate_key_sound_flag_value(layout_config)

    def update_button_sound_flag_value(
        self, layout_config: configparser.ConfigParser, button_sound_flag: bool
    ) -> None:
        """update_button_sound_flag_value

        Updates the button_sound flag in the layout config and regenerates the button sound flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            button_sound_flag (bool): new button_sound flag to enter into the layout configuration.
        """
        if button_sound_flag is True:
            layout_config["console_layout"]["button_sound_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["button_sound_flag"] = "FALSE"
        self.button_sound_flag = self.generate_button_sound_flag_value(layout_config)

    def update_scanner_sound_flag_value(
        self, layout_config: configparser.ConfigParser, scanner_sound_flag: bool
    ) -> None:
        """update_scanner_sound_flag_value

        Updates the scanner_sound flag in the layout config and regenerates the scanner sound flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            scanner_sound_flag (bool): new scanner_sound flag to enter into the layout configuration.
        """
        if scanner_sound_flag is True:
            layout_config["console_layout"]["scanner_sound_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["scanner_sound_flag"] = "FALSE"
        self.scanner_sound_flag = self.generate_scanner_sound_flag_value(layout_config)

    def update_ambient_sound_flag_value(
        self, layout_config: configparser.ConfigParser, ambient_sound_flag: bool
    ) -> None:
        """update_ambient_sound_flag_value

        Updates the ambient_sound flag in the layout config and regenerates the ambient sound flag value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration
            ambient_sound_flag (bool): new ambient_sound flag to enter into the layout configuration.
        """
        if ambient_sound_flag is True:
            layout_config["console_layout"]["ambient_sound_flag"] = "TRUE"
        else:
            layout_config["console_layout"]["ambient_sound_flag"] = "FALSE"
        self.ambient_sound_flag = self.generate_ambient_sound_flag_value(layout_config)

    def update_alarm_sound_name_value(
        self, layout_config: configparser.ConfigParser, alarm_sound_name: str
    ) -> None:
        """update_alarm_sound_name_value

        Updates the alarm sound name in the layout config and regenerates alarm sound name value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            alarm_sound_name (str): new alarm sound name to enter into the layout configuration.
        """
        layout_config["console_layout"]["alarm_sound_name"] = alarm_sound_name
        self.alarm_sound_name = self.generate_alarm_sound_name_value(layout_config)

    def update_scan_sound_name_value(
        self, layout_config: configparser.ConfigParser, scanner_sound_name: str
    ) -> None:
        """update_scan_sound_name_value

        Updates the scan sound name in the layout config and regenerates scan sound name value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            scanner_sound_name (str): new scan sound name to enter into the layout configuration.
        """
        layout_config["console_layout"]["scanner_sound_name"] = scanner_sound_name
        self.scanner_sound_name = self.generate_scan_sound_name_value(layout_config)

    def update_key_sound_name_value(
        self, layout_config: configparser.ConfigParser, key_sound_name: str
    ) -> None:
        """update_key_sound_name_value

        Updates the key sound name in the layout config and regenerates key sound name value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            key_sound_name (str): new key sound name to enter into the layout configuration.
        """
        layout_config["console_layout"]["key_sound_name"] = key_sound_name
        self.key_sound_name = self.generate_key_sound_name_value(layout_config)

    def update_button_sound_name_value(
        self, layout_config: configparser.ConfigParser, button_sound_name: str
    ) -> None:
        """update_button_sound_name_value

        Updates the button sound name in the layout config and regenerates button sound name value.

        Args:
            layout_config (configparser.ConfigParser): the layout configuration.
            button_sound_name (str): new button sound name to enter into the layout configuration.
        """
        layout_config["console_layout"]["button_sound_name"] = button_sound_name
        self.button_sound_name = self.generate_button_sound_name_value(layout_config)


#  Initialise the root config and layout config objects.

root_config = RootConfig()
layout_config = LayoutConfig()
