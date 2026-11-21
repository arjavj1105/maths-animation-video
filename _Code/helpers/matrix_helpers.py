"""
Matrix styling and visual helpers for Manim.
Maintains consistent colour schemes:
- Row 1: Blue (#3B82F6)
- Row 2: Green (#10B981)
- Row 3: Orange (#F97316)
- Pivots: Yellow (#FBBF24)
- Text: White (#F8FAFC)
- Background: Deep Dark Navy (#0B1120)
"""

from manim import *

# Colour Palette Constants
ROW1_COLOR = "#3B82F6"      # Bright Blue
ROW2_COLOR = "#10B981"      # Emerald Green
ROW3_COLOR = "#F97316"      # Vivid Orange
PIVOT_COLOR = "#FBBF24"     # Golden Yellow
BG_COLOR = "#0B1120"        # Deep Dark Navy
TEXT_COLOR = "#F8FAFC"      # Clean White
MUTED_TEXT = "#94A3B8"      # Slate Grey
ACCENT_CYAN = "#06B6D4"     # Cyan
ACCENT_PURPLE = "#A855F7"   # Purple
SUCCESS_GREEN = "#22C55E"   # Bright Green
ERROR_RED = "#EF4444"       # Soft Red

def build_augmented_matrix(
    data,
    row_colors=None,
    font_size=28,
    h_buff=0.75,
    v_buff=0.55
):
    """
    Constructs a visual 3x4 augmented matrix [A | b] with colored rows,
    aligned columns, a clean vertical augmented line, and outer brackets.
    Returns: (matrix_vgroup, entries_grid, div_line)
    """
    if row_colors is None:
        row_colors = [ROW1_COLOR, ROW2_COLOR, ROW3_COLOR]

    grid = []
    row_groups = []

    # Format numbers into Text mobjects
    for r_idx, row in enumerate(data):
        row_mob_list = []
        for c_idx, val in enumerate(row):
            val_str = str(val)
            color = row_colors[r_idx]
            t = Text(val_str, font="Helvetica", weight=BOLD if c_idx == r_idx else NORMAL, font_size=font_size, color=color)
            row_mob_list.append(t)
        grid.append(row_mob_list)

    # Column-wise alignment to guarantee straight columns
    # Find max width per column
    col_x_offsets = [0.0, 1.0, 2.0, 3.4]  # Column positions with space for augmented bar
    vgroup_all = VGroup()

    for r_idx in range(3):
        for c_idx in range(4):
            item = grid[r_idx][c_idx]
            item.move_to([col_x_offsets[c_idx], -r_idx * v_buff, 0])
            vgroup_all.add(item)

    vgroup_all.center()

    # Vertical augmented line
    bar_x = (col_x_offsets[2] + col_x_offsets[3]) / 2 + vgroup_all.get_center()[0] - (col_x_offsets[0] + col_x_offsets[3]) / 2
    top_y = grid[0][0].get_top()[1] + 0.25
    bot_y = grid[2][0].get_bottom()[1] - 0.25
    div_line = Line([bar_x, top_y, 0], [bar_x, bot_y, 0], stroke_width=2.5, color=MUTED_TEXT)

    # Left and right brackets
    bracket_h = top_y - bot_y + 0.1
    bracket_w = 0.2
    
    # Left bracket lines
    left_x = vgroup_all.get_left()[0] - 0.35
    lb_top = Line([left_x + bracket_w, top_y, 0], [left_x, top_y, 0], stroke_width=3, color=TEXT_COLOR)
    lb_vert = Line([left_x, top_y, 0], [left_x, bot_y, 0], stroke_width=3, color=TEXT_COLOR)
    lb_bot = Line([left_x, bot_y, 0], [left_x + bracket_w, bot_y, 0], stroke_width=3, color=TEXT_COLOR)
    left_bracket = VGroup(lb_top, lb_vert, lb_bot)

    # Right bracket lines
    right_x = vgroup_all.get_right()[0] + 0.35
    rb_top = Line([right_x - bracket_w, top_y, 0], [right_x, top_y, 0], stroke_width=3, color=TEXT_COLOR)
    rb_vert = Line([right_x, top_y, 0], [right_x, bot_y, 0], stroke_width=3, color=TEXT_COLOR)
    rb_bot = Line([right_x, bot_y, 0], [right_x - bracket_w, bot_y, 0], stroke_width=3, color=TEXT_COLOR)
    right_bracket = VGroup(rb_top, rb_vert, rb_bot)

    full_matrix = VGroup(left_bracket, vgroup_all, div_line, right_bracket)
    return full_matrix, grid, div_line

def create_pivot_box(target_mobject, color=PIVOT_COLOR):
    """Creates a highlighted golden yellow rectangle around a pivot element."""
    box = SurroundingRectangle(target_mobject, color=color, buff=0.12, stroke_width=2.5, corner_radius=0.08)
    return box

def create_staircase(grid, color=PIVOT_COLOR):
    """Draws the echelon staircase under pivots (0,0), (1,1), (2,2)."""
    p0 = grid[0][0].get_corner(DL) + LEFT * 0.15 + DOWN * 0.08
    p1 = grid[1][1].get_corner(UL) + LEFT * 0.15 + UP * 0.08
    p2 = grid[1][1].get_corner(DL) + LEFT * 0.15 + DOWN * 0.08
    p3 = grid[2][2].get_corner(UL) + LEFT * 0.15 + UP * 0.08
    p4 = grid[2][2].get_corner(DR) + RIGHT * 0.15 + DOWN * 0.08

    lines = VGroup(
        Line(p0, [p1[0], p0[1], 0], stroke_width=3, color=color),
        Line([p1[0], p0[1], 0], p1, stroke_width=3, color=color),
        Line(p1, [p2[0], p1[1], 0], stroke_width=3, color=color),
        Line([p2[0], p1[1], 0], p2, stroke_width=3, color=color),
        Line(p2, [p3[0], p2[1], 0], stroke_width=3, color=color),
        Line([p3[0], p2[1], 0], p3, stroke_width=3, color=color),
        Line(p3, [p4[0], p3[1], 0], stroke_width=3, color=color)
    )
    return lines
