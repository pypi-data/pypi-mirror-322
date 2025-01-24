# CreateWorld/__init__.py
from .CreateWorld import (
    init_sdl as _init_sdl,
    create_window as _create_window,
    load_background as _load_background,
    clear_screen as _clear_screen,
    update_screen as _update_screen,
    quit_sdl as _quit_sdl,
    draw_rect as _draw_rect,
    draw_circle as _draw_circle,
    poll_event as _poll_event
)

class CreateWorld:
    @staticmethod
    def init():
        """Initialize SDL2 and SDL_image."""
        return _init_sdl()

    @staticmethod
    def create(title, width, height):
        """Create a window with the given title, width, and height."""
        return _create_window(title, width, height)

    @staticmethod
    def load_background(image_path, width, height):
        """Load a background image and resize it to fit the window dimensions."""
        return _load_background(image_path, width, height)

    @staticmethod
    def clear():
        """Clear the screen and draw the background if loaded."""
        return _clear_screen()

    @staticmethod
    def update():
        """Update the screen."""
        return _update_screen()

    @staticmethod
    def quit():
        """Quit SDL2 and clean up resources."""
        return _quit_sdl()

    @staticmethod
    def draw_rect(x, y, width, height, r, g, b):
        """Draw a rectangle with the given position, size, and color (RGB)."""
        return _draw_rect(x, y, width, height, r, g, b)

    @staticmethod
    def draw_circle(x, y, radius, r, g, b):
        """Draw a circle with the given position, radius, and color (RGB)."""
        return _draw_circle(x, y, radius, r, g, b)

    @staticmethod
    def poll_event():
        """
        Poll for SDL events and return the event type.
        
        Returns:
            str: Event type (e.g., "quit", "keydown", "keyup", "mousebuttondown", "mousebuttonup", "mousemotion", "none").
        """
        return _poll_event()

