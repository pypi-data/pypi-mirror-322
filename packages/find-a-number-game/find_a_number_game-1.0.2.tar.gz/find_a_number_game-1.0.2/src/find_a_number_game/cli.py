# src/find_a_number/cli.py
import random
import os
import click
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

PKG_ABSOLUTE_PATH = os.path.dirname(__file__)
FONT_FILES = [os.path.abspath(f"{PKG_ABSOLUTE_PATH}/fonts/{font}") for font in os.listdir(f"{PKG_ABSOLUTE_PATH}/fonts")]

# Output PDF filepath
output_file = "fang"

# Letter size dimensions
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 20  # Safe margin from edges


def load_fonts(font_files: list) -> list:
    """Register fonts dynamically for ReportLab."""
    font_names = []
    for font_path in font_files:
        try:
            font_name = os.path.basename(font_path).split(".")[0]
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            font_names.append(font_name)
        except Exception as e:
            print(f"Could not load font {font_path}: {e}")
    return font_names


def random_color(use_colors):
    """Generate a random color."""
    if use_colors:
        return Color(
            random.random(),
            random.random(),
            random.random(),
            alpha=random.uniform(0.5, 1),
        )
    return Color(0, 0, 0, alpha=random.uniform(0.5, 1))


def generate_random_font_sizes():
    """Generate a list of random font sizes, ensuring fonts above 60 are used only once."""
    font_sizes = []
    used_large_fonts = set()

    for _ in range(100):
        if len(used_large_fonts) < 30:  # Allow up to 30 large fonts
            font_size = random.randint(61, 250)
            if font_size not in used_large_fonts:
                used_large_fonts.add(font_size)
                font_sizes.append(font_size)
                continue

        # Add smaller font sizes
        font_sizes.append(random.randint(10, 60))

    random.shuffle(font_sizes)  # Shuffle the font sizes for randomness
    return font_sizes


def random_rotation():
    """Generate a random rotation angle."""
    return random.randint(0, 360)


def generate_grid_cells(rows, cols, margin, page_width, page_height):
    """Generate a grid with dynamically varying cell sizes."""
    total_width = page_width - 2 * margin
    total_height = page_height - 2 * margin

    # Divide total space into rows and columns
    cell_widths = [
        random.randint(int(total_width / cols * 0.8), int(total_width / cols * 1.2))
        for _ in range(cols)
    ]
    cell_heights = [
        random.randint(int(total_height / rows * 0.8), int(total_height / rows * 1.2))
        for _ in range(rows)
    ]

    # Adjust cell sizes to fit the page exactly
    total_width_adjustment = total_width / sum(cell_widths)
    total_height_adjustment = total_height / sum(cell_heights)
    cell_widths = [int(w * total_width_adjustment) for w in cell_widths]
    cell_heights = [int(h * total_height_adjustment) for h in cell_heights]

    # Generate cell coordinates
    cells = []
    y_offset = margin
    for height in cell_heights:
        x_offset = margin
        for width in cell_widths:
            cells.append((x_offset, y_offset, x_offset + width, y_offset + height))
            x_offset += width
        y_offset += height

    return cells


def generate_pdf(output_file, fonts, use_colors):
    """Generate a PDF with random numbers, fonts, sizes, rotations, and positions."""
    c = canvas.Canvas(output_file, pagesize=letter)

    # Generate grid cells and shuffle them for random placement
    grid_cells = generate_grid_cells(10, 10, MARGIN, PAGE_WIDTH, PAGE_HEIGHT)
    random.shuffle(grid_cells)

    # Generate random font sizes
    font_sizes = generate_random_font_sizes()

    for num, cell, font_size in zip(range(1, 101), grid_cells, font_sizes):
        # Randomize font, color, and rotation
        font = random.choice(fonts)
        color = random_color(use_colors)
        rotation = random_rotation()

        # Get cell boundaries
        x_min, y_min, x_max, y_max = cell
        cell_width = x_max - x_min
        cell_height = y_max - y_min

        # Adjust font size if it doesn't fit within the cell
        max_font_size = min(cell_width, cell_height)
        if font_size > max_font_size:
            font_size = max_font_size

        # Calculate random position within the cell
        if font_size * 2 < cell_width and font_size * 2 < cell_height:
            x = random.randint(x_min + font_size, x_max - font_size)
            y = random.randint(y_min + font_size, y_max - font_size)
        else:
            # Default to center the number if space is tight
            x = (x_min + x_max) // 2
            y = (y_min + y_max) // 2

        # Save the current state for rotation
        c.saveState()
        c.translate(x, y)
        c.rotate(rotation)
        c.setFont(font, font_size)
        c.setFillColor(color)

        # Draw the number
        c.drawString(-font_size // 2, -font_size // 2, str(num))

        # Restore state
        c.restoreState()

    # Save the PDF
    c.save()


@click.command
@click.option(
    "-p", "--players", default=4, help="Number of players", type=int, show_default=True
)
@click.option(
    "-c",
    "--use-colors",
    default=False,
    help="Generate the numbers using colors",
    type=bool,
    show_default=True,
)
def main(players, use_colors):
    """_summary_

    Args:
        players (_type_): _description_
        use_colors (_type_): _description_

    Raises:
        Exception: _description_
    """
    loaded_fonts = load_fonts(FONT_FILES)

    if not loaded_fonts:
        raise Exception("No fonts were loaded. Exiting")
    else:
        for i in range(players):
            generate_pdf(f"{output_file}_{i}.pdf", loaded_fonts, use_colors)


if __name__ == "__main__":
    main()
