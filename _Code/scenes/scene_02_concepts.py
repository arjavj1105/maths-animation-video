"""
Scene 2: Concept Introduction
Topic: Notation, Ax = b, Augmented Matrix, Row Operations, Learning Objective
Narration: Original voice recording by Arjav Jain (Duration: 46.21s)
Target synchronized animation duration: 46.50s
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN, PIVOT_COLOR,
    build_augmented_matrix
)
from helpers.animation_helpers import setup_scene_background, create_header, create_badge

class Scene02Concepts(Scene):
    def construct(self):
        setup_scene_background(self)

        # -------------------------------------------------------------
        # 1. Header & Matrix Equation Ax = b
        # Time: 0.0s -> 9.8s (Matches narration 0.04s -> 10.18s)
        # -------------------------------------------------------------
        header = create_header("Concept Foundation: Matrix Representation", "Formulating the linear system as A x = b")
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=1.0)

        # Matrix Equation Ax = b visual
        eq_label = Text("Matrix Form:   A · x = b", font="Helvetica", weight=BOLD, font_size=26, color=ACCENT_CYAN)
        eq_label.to_edge(UP, buff=1.6)
        self.play(Write(eq_label), run_time=1.0)

        # Components breakdown: A, x, b
        card_a = VGroup(
            Text("Coefficient Matrix (A)", font="Helvetica", weight=BOLD, font_size=16, color=TEXT_COLOR),
            Text("[ 1   1   1 ]\n[ 2   3   1 ]\n[ 1   2   3 ]", font="Courier New", weight=BOLD, font_size=18, color=ROW1_COLOR)
        ).arrange(DOWN, buff=0.15)
        card_a_rect = SurroundingRectangle(card_a, color=MUTED_TEXT, buff=0.2, stroke_width=1.5, corner_radius=0.1)
        group_a = VGroup(card_a_rect, card_a)

        card_x = VGroup(
            Text("Unknowns (x)", font="Helvetica", weight=BOLD, font_size=16, color=TEXT_COLOR),
            Text("[ x ]\n[ y ]\n[ z ]", font="Courier New", weight=BOLD, font_size=18, color=ROW2_COLOR)
        ).arrange(DOWN, buff=0.15)
        card_x_rect = SurroundingRectangle(card_x, color=MUTED_TEXT, buff=0.2, stroke_width=1.5, corner_radius=0.1)
        group_x = VGroup(card_x_rect, card_x)

        card_b = VGroup(
            Text("Constants (b)", font="Helvetica", weight=BOLD, font_size=16, color=TEXT_COLOR),
            Text("[  6 ]\n[ 11 ]\n[ 14 ]", font="Courier New", weight=BOLD, font_size=18, color=ROW3_COLOR)
        ).arrange(DOWN, buff=0.15)
        card_b_rect = SurroundingRectangle(card_b, color=MUTED_TEXT, buff=0.2, stroke_width=1.5, corner_radius=0.1)
        group_b = VGroup(card_b_rect, card_b)

        components = VGroup(group_a, group_x, group_b).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        self.play(FadeIn(components, shift=UP * 0.2), run_time=1.2)
        self.wait(6.6)

        # -------------------------------------------------------------
        # 2. Augmented Matrix [A | b]
        # Time: 9.8s -> 14.0s (Matches narration 10.18s -> 14.06s)
        # -------------------------------------------------------------
        aug_label = Text("Augmented Matrix:  [ A | b ]", font="Helvetica", weight=BOLD, font_size=24, color=PIVOT_COLOR)
        aug_label.to_edge(UP, buff=1.6)

        mat_mob, grid, div_line = build_augmented_matrix([
            ["1", "1", "1", "6"],
            ["2", "3", "1", "11"],
            ["1", "2", "3", "14"]
        ], font_size=26)
        mat_mob.move_to(DOWN * 0.1)

        self.play(
            FadeOut(components),
            Transform(eq_label, aug_label),
            FadeIn(mat_mob, shift=UP * 0.2),
            run_time=1.2
        )
        self.wait(3.0)

        # -------------------------------------------------------------
        # 3. Exact Learning Objective Display
        # Time: 14.0s -> 27.5s (Matches narration 14.06s -> 27.67s)
        # -------------------------------------------------------------
        self.play(FadeOut(mat_mob), FadeOut(eq_label), run_time=1.0)

        lo_badge = create_badge("OFFICIAL LEARNING OBJECTIVE", color=PIVOT_COLOR, font_size=18)
        lo_badge.to_edge(UP, buff=1.5)

        lo_box = RoundedRectangle(width=11.2, height=2.4, corner_radius=0.15, stroke_width=2, stroke_color=PIVOT_COLOR, fill_color="#0F172A", fill_opacity=0.9)
        lo_box.next_to(lo_badge, DOWN, buff=0.25)

        lo_text = Text(
            "\"By the end of this video, the viewer will be able to explain how\n"
            "Gaussian elimination uses row operations to reduce a 3×3 system\n"
            "to row echelon form, why those operations do not change the\n"
            "solution set, and what the solution means geometrically.\"",
            font="Helvetica", font_size=20, color=TEXT_COLOR, line_spacing=1.3
        ).move_to(lo_box.get_center())

        self.play(FadeIn(lo_badge, shift=DOWN * 0.1), Create(lo_box), Write(lo_text), run_time=2.0)
        self.wait(9.5)

        # -------------------------------------------------------------
        # 4. Elementary Row Operations & Row Echelon Form
        # Time: 27.5s -> 46.5s (Matches narration 27.67s -> 45.56s)
        # -------------------------------------------------------------
        self.play(FadeOut(lo_badge), FadeOut(lo_box), FadeOut(lo_text), run_time=1.0)

        ops_title = Text("Three Elementary Row Operations", font="Helvetica", weight=BOLD, font_size=24, color=TEXT_COLOR)
        ops_title.to_edge(UP, buff=1.5)

        op1 = Text("1. Row Swap:         R_i ↔ R_j                       (Interchange two rows)", font="Courier New", font_size=18, color=ROW1_COLOR)
        op2 = Text("2. Row Scaling:      R_i → k · R_i   (k ≠ 0)         (Multiply row by non-zero scalar)", font="Courier New", font_size=18, color=ROW2_COLOR)
        op3 = Text("3. Row Replacement:  R_i → R_i + k · R_j             (Add multiple of row to another)", font="Courier New", font_size=18, color=ROW3_COLOR)

        ops_vgroup = VGroup(op1, op2, op3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.1)

        key_note = Text(
            "Key Principle: All row operations are strictly REVERSIBLE, preserving the solution set!",
            font="Helvetica", weight=BOLD, font_size=18, color=PIVOT_COLOR
        ).next_to(ops_vgroup, DOWN, buff=0.5)

        self.play(Write(ops_title), run_time=1.0)
        self.play(FadeIn(op1, shift=RIGHT * 0.2), run_time=0.8)
        self.wait(1.7)
        self.play(FadeIn(op2, shift=RIGHT * 0.2), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(op3, shift=RIGHT * 0.2), run_time=0.8)
        self.play(FadeIn(key_note, shift=UP * 0.2), run_time=1.0)
        self.wait(11.7)
