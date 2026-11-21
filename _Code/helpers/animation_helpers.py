"""
Animation layout, title cards, badges, and UI helpers for Manim.
Ensures large readable typography, consistent margins, and no overlaps.
"""

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, PIVOT_COLOR,
    BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN, SUCCESS_GREEN, ERROR_RED
)

def setup_scene_background(scene: Scene):
    """Sets the clean dark navy background for any scene."""
    scene.camera.background_color = BG_COLOR

def create_header(title_text: str, subtitle_text: str = ""):
    """Creates a consistent, elegant scene header banner."""
    title = Text(title_text, font="Helvetica", weight=BOLD, font_size=30, color=TEXT_COLOR)
    title.to_edge(UP, buff=0.4)
    
    if subtitle_text:
        subtitle = Text(subtitle_text, font="Helvetica", font_size=18, color=MUTED_TEXT)
        subtitle.next_to(title, DOWN, buff=0.12)
        divider = Line(LEFT * 6.5, RIGHT * 6.5, stroke_width=1.5, color=MUTED_TEXT).set_opacity(0.35)
        divider.next_to(subtitle, DOWN, buff=0.15)
        group = VGroup(title, subtitle, divider)
    else:
        divider = Line(LEFT * 6.5, RIGHT * 6.5, stroke_width=1.5, color=MUTED_TEXT).set_opacity(0.35)
        divider.next_to(title, DOWN, buff=0.15)
        group = VGroup(title, divider)
    return group

def create_badge(text: str, color=ACCENT_CYAN, font_size=16):
    """Creates a pill-shaped tag for metadata like Student Name or ID."""
    t = Text(text, font="Helvetica", weight=BOLD, font_size=font_size, color=color)
    box = SurroundingRectangle(t, color=color, buff=0.08, corner_radius=0.08, stroke_width=1.5)
    return VGroup(box, t)

def create_card(width: float, height: float, stroke_color=MUTED_TEXT, fill_color="#1E293B", fill_opacity=0.5):
    """Creates a rounded rectangle container card for visual grouping."""
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_width=1.5,
        stroke_color=stroke_color,
        fill_color=fill_color,
        fill_opacity=fill_opacity
    )

def create_checkmark(target_mobject=None, scale=0.35):
    """Creates a bright green vector checkmark."""
    # Checkmark drawn with two connected lines
    p1 = LEFT * 0.4 + DOWN * 0.05
    p2 = DOWN * 0.35 + RIGHT * 0.05
    p3 = UP * 0.45 + RIGHT * 0.45
    l1 = Line(p1, p2, stroke_width=4, color=SUCCESS_GREEN)
    l2 = Line(p2, p3, stroke_width=4, color=SUCCESS_GREEN)
    check = VGroup(l1, l2).scale(scale)
    if target_mobject is not None:
        check.next_to(target_mobject, RIGHT, buff=0.25)
    return check

def create_crossmark(target_mobject=None, scale=0.35):
    """Creates a red vector crossmark (X)."""
    l1 = Line(UL * 0.4, DR * 0.4, stroke_width=4, color=ERROR_RED)
    l2 = Line(UR * 0.4, DL * 0.4, stroke_width=4, color=ERROR_RED)
    cross = VGroup(l1, l2).scale(scale)
    if target_mobject is not None:
        cross.next_to(target_mobject, RIGHT, buff=0.25)
    return cross
