"""
Scene 5: Interpretation
Topic: Verification into Original 3 Equations, 3D Point Reconnection,
       Special Cases (Inconsistent vs Dependent Systems)
Target duration: ~61.0s (Audio duration: 60.50s)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN,
    PIVOT_COLOR, SUCCESS_GREEN, ERROR_RED
)
from helpers.animation_helpers import setup_scene_background, create_header, create_badge, create_checkmark, create_crossmark

class Scene05Interpretation(Scene):
    def construct(self):
        setup_scene_background(self)

        # -------------------------------------------------------------
        # 1. Header & Verification by Substitution
        # Time: 0.0s -> 28.0s (28.0s)
        # -------------------------------------------------------------
        header = create_header("Verification & Geometric Interpretation", "Substituting solution (x=1, y=2, z=3) into all original equations")
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=1.0)

        # Equation 1 Verification
        eq1_card = VGroup(
            Text("Equation 1:", font="Helvetica", weight=BOLD, font_size=18, color=ROW1_COLOR),
            Text("x + y + z = 6    ⇒    1 + 2 + 3 = 6    ⇒    6 = 6", font="Courier New", weight=BOLD, font_size=18, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.4)
        chk1 = create_checkmark(eq1_card)
        row1_grp = VGroup(eq1_card, chk1)

        # Equation 2 Verification
        eq2_card = VGroup(
            Text("Equation 2:", font="Helvetica", weight=BOLD, font_size=18, color=ROW2_COLOR),
            Text("2x + 3y + z = 11  ⇒  2(1) + 3(2) + 3 = 11  ⇒  11 = 11", font="Courier New", weight=BOLD, font_size=18, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.4)
        chk2 = create_checkmark(eq2_card)
        row2_grp = VGroup(eq2_card, chk2)

        # Equation 3 Verification
        eq3_card = VGroup(
            Text("Equation 3:", font="Helvetica", weight=BOLD, font_size=18, color=ROW3_COLOR),
            Text("x + 2y + 3z = 14  ⇒  1 + 2(2) + 3(3) = 14  ⇒  14 = 14", font="Courier New", weight=BOLD, font_size=18, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.4)
        chk3 = create_checkmark(eq3_card)
        row3_grp = VGroup(eq3_card, chk3)

        verif_table = VGroup(row1_grp, row2_grp, row3_grp).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.4)

        # Animate equations and checks one by one
        self.play(FadeIn(eq1_card, shift=RIGHT * 0.2), run_time=1.2)
        self.play(Create(chk1), run_time=0.8)
        self.wait(3.0)

        self.play(FadeIn(eq2_card, shift=RIGHT * 0.2), run_time=1.2)
        self.play(Create(chk2), run_time=0.8)
        self.wait(3.0)

        self.play(FadeIn(eq3_card, shift=RIGHT * 0.2), run_time=1.2)
        self.play(Create(chk3), run_time=0.8)
        self.wait(4.0)

        # Confirmation badge
        all_verified = create_badge("ALL THREE EQUATIONS SATISFIED  (100% ACCURATE)", color=SUCCESS_GREEN, font_size=18)
        all_verified.next_to(verif_table, DOWN, buff=0.45)
        self.play(DrawBorderThenFill(all_verified), run_time=1.2)
        self.wait(9.6)

        # -------------------------------------------------------------
        # 2. Geometric Reconnection & Special Cases
        # Time: 28.0s -> 61.0s (33.0s)
        # -------------------------------------------------------------
        self.play(FadeOut(verif_table), FadeOut(all_verified), FadeOut(header), run_time=1.2)

        sc_title = Text("Special Cases in Gaussian Elimination", font="Helvetica", weight=BOLD, font_size=26, color=TEXT_COLOR)
        sc_title.to_edge(UP, buff=0.8)
        sc_sub = Text("Contrasting inconsistent systems with dependent systems", font="Helvetica", font_size=16, color=MUTED_TEXT).next_to(sc_title, DOWN, buff=0.12)
        sc_div = Line(LEFT * 5.5, RIGHT * 5.5, stroke_width=1.5, color=MUTED_TEXT).set_opacity(0.35).next_to(sc_sub, DOWN, buff=0.15)
        self.play(Write(sc_title), FadeIn(sc_sub), Create(sc_div), run_time=1.0)

        # Case 1: Inconsistent System
        case1_header = Text("Case 1: Inconsistent System (No Solution)", font="Helvetica", weight=BOLD, font_size=18, color=ERROR_RED)
        case1_row = Text("Row: [ 0   0   0 |  5 ]", font="Courier New", weight=BOLD, font_size=18, color=TEXT_COLOR)
        case1_eq = Text("Equation: 0x + 0y + 0z = 5  ⇒  0 = 5  (Contradiction!)", font="Helvetica", font_size=15, color=ERROR_RED)
        case1_geom = Text("Geometry: Planes are parallel or have no mutual meeting line.", font="Helvetica", font_size=14, color=MUTED_TEXT)
        case1_vgroup = VGroup(case1_header, case1_row, case1_eq, case1_geom).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        case1_box = RoundedRectangle(width=5.8, height=2.6, corner_radius=0.12, stroke_width=1.5, stroke_color=ERROR_RED, fill_color="#0F172A", fill_opacity=0.9)
        case1_card = VGroup(case1_box, case1_vgroup).move_to(LEFT * 3.1 + DOWN * 0.3)

        # Case 2: Dependent System
        case2_header = Text("Case 2: Dependent System (Infinite Solutions)", font="Helvetica", weight=BOLD, font_size=18, color=ACCENT_CYAN)
        case2_row = Text("Row: [ 0   0   0 |  0 ]", font="Courier New", weight=BOLD, font_size=18, color=TEXT_COLOR)
        case2_eq = Text("Equation: 0x + 0y + 0z = 0  ⇒  0 = 0  (Tautology)", font="Helvetica", font_size=15, color=ACCENT_CYAN)
        case2_geom = Text("Geometry: Redundant plane; planes intersect along an entire line.", font="Helvetica", font_size=14, color=MUTED_TEXT)
        case2_vgroup = VGroup(case2_header, case2_row, case2_eq, case2_geom).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        case2_box = RoundedRectangle(width=5.8, height=2.6, corner_radius=0.12, stroke_width=1.5, stroke_color=ACCENT_CYAN, fill_color="#0F172A", fill_opacity=0.9)
        case2_card = VGroup(case2_box, case2_vgroup).move_to(RIGHT * 3.1 + DOWN * 0.3)

        self.play(FadeIn(case1_card, shift=UP * 0.2), run_time=1.5)
        self.wait(12.0)

        self.play(FadeIn(case2_card, shift=UP * 0.2), run_time=1.5)
        self.wait(15.0)
