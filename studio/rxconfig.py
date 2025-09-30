import reflex as rx

# style.py
from reflex.constants.colors import ColorType


# Default Radix Colors
def create_colors_dict() -> dict:
    colors_dict = {}
    for color in ColorType.__args__:
        if color not in ["black", "white"]:
            colors_dict[color] = {
                shade: f"var(--{color}-{shade})" for shade in range(1, 13)
            }
            # Append the alpha colors
            colors_dict[f"{color}A"] = {
                shade: f"var(--{color}-a{shade})" for shade in range(1, 13)
            }

    # Add accent palette
    colors_dict["accent"] = {shade: f"var(--accent-{shade})" for shade in range(1, 13)}
    colors_dict["accentA"] = {
        shade: f"var(--accent-a{shade})" for shade in range(1, 13)
    }

    return colors_dict


config = rx.Config(
    app_name="studio",
    api_url="http://localhost:9000",
    backend_port=9000,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(
            {
                "darkMode": "class",
                "theme": {
                    "colors": {
                        **create_colors_dict(),
                    },
                },
            }
        ),
    ],
)
