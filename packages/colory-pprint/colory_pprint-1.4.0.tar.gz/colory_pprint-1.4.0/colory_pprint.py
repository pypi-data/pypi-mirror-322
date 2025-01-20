import json
from termcolor import colored
from typing import Any

class ColoryPPrint:
    """
    ColoryPPrint for color-coded JSON logging.

    Available foreground colors:
        black, red, green, yellow, blue, magenta, cyan, white,
        grey, light_red, light_green, light_yellow, light_blue,
        light_magenta, light_cyan, light_white.

    Available background colors (prefix with "on_"):
        on_black, on_red, on_green, on_yellow, on_blue, on_magenta,
        on_cyan, on_white, on_grey, on_light_red, on_light_green,
        on_light_yellow, on_light_blue, on_light_magenta,
        on_light_cyan, on_light_white.

    Available text styles:
        bold, underline, reverse, concealed.

    Example usage:
        log.red.bold({"status": "error", "message": "An error occurred!"})
        log.green.on_black.underline({"status": "success", "message": "Operation successful."})
        log({"message": "Default logging with cyan."})
    """

    def __init__(self, debug: bool=False):
        self.fg = 'cyan'  # Default foreground color
        self.bg = None    # Default background color
        self.attrs = []   # Default styles
        self.debug = debug

    def _reset(self):
        """Reset styles to defaults after logging."""
        self.fg = 'cyan'
        self.bg = None
        self.attrs = []

    def _apply_formatting(self, text: str) -> str:
        """Apply formatting based on current styles."""
        return colored(text, self.fg, self.bg, attrs=self.attrs)

    def _log(self, data: Any, force: bool):
        """Dump data as JSON and apply formatting."""
        def custom_serializer(obj: Any) -> str:
            """Handle non-serializable objects by returning their `repr`."""
            try:
                return json.JSONEncoder().default(obj)
            except TypeError:
                # Use the `repr()` for non-serializable objects
                return f"<{type(obj).__name__} object at {hex(id(obj))}>"
            
        json_data = json.dumps(data, default=custom_serializer, indent=3, ensure_ascii=False)
        if self.debug or force:
            print(self._apply_formatting(json_data))
        self._reset()

    def __call__(self, data: Any, force: bool=False):
        """Allow direct logging by calling the log object."""
        self._log(data, force)

    def __getattr__(self, name: str) -> "ColoryPPrint":
        """
        Dynamically handle chaining of colors, backgrounds, and styles.

        Raises:
            AttributeError: If the attribute is invalid.
        """
        colors = {
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "grey", "light_red", "light_green", "light_yellow", "light_blue",
            "light_magenta", "light_cyan", "light_white"
        }
        backgrounds = {f"on_{color}" for color in colors}
        styles = {"bold", "underline", "reverse", "concealed"}

        if name in colors:
            self.fg = name
            return self
        elif name in backgrounds:
            self.bg = name
            return self
        elif name in styles:
            self.attrs.append(name)
            return self
        else:
            raise AttributeError(f"'ColoryPPrint' object has no attribute '{name}'")
