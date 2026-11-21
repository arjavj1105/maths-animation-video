"""
Scene 1: Hook and Context + Opening Frame
Student Name: Arjav Jain | Student ID: E25B070861 | Batch: Ramanujan
Topic: Gaussian Elimination: Solving a 3x3 System of Linear Equations
Target duration: ~34.5s (Audio duration: 34.06s)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN, PIVOT_COLOR
)
from helpers.animation_helpers import setup_scene_background, create_badge

class Scene01Hook(Scene):
    def construct(self):
        setup_scene_background(self)

        # -------------------------------------------------------------
        # 1. Opening Title Frame (Mandatory Academic Credentials)
        # Time: 0.0s -> 7.5s (7.5s)
        # -------------------------------------------------------------
        title = Text("Gaussian Elimination: Solving a 3×3 System", font="Helvetica", weight=BOLD, font_size=32, color=TEXT_COLOR)
        subtitle = Text("M3 Internal Assessment – Animation Video", font="Helvetica", font_size=22, color=ACCENT_CYAN)
        name_id = Text("Arjav Jain  |  Student ID: E25B070861", font="Helvetica", weight=BOLD, font_size=20, color=TEXT_COLOR)
        batch = Text("Batch: Ramanujan  |  Course: Mathematics 3", font="Helvetica", font_size=18, color=MUTED_TEXT)

        title_card = VGroup(title, subtitle, name_id, batch).arrange(DOWN, buff=0.25).center()
        card_box = SurroundingRectangle(title_card, buff=0.4, color=ACCENT_CYAN, stroke_width=2, corner_radius=0.15)
        opening_group = VGroup(card_box, title_card)

        self.play(FadeIn(opening_group, shift=UP * 0.3), run_time=1.5)
        self.wait(4.5)
        self.play(FadeOut(opening_group, shift=UP * 0.5), run_time=1.5)

        # -------------------------------------------------------------
        # 2. Introduce the 3 Simultaneous Equations
        # Time: 7.5s -> 18.0s (10.5s)
        # -------------------------------------------------------------
        header = Text("System of 3 Linear Equations", font="Helvetica", weight=BOLD, font_size=26, color=TEXT_COLOR)
        header.to_edge(UP, buff=0.6)
        div = Line(LEFT * 5, RIGHT * 5, stroke_width=1.5, color=MUTED_TEXT).set_opacity(0.4).next_to(header, DOWN, buff=0.15)
        self.play(Write(header), Create(div), run_time=1.0)

        eq1 = Text("x + y + z = 6", font="Helvetica", weight=BOLD, font_size=30, color=ROW1_COLOR)
        eq2 = Text("2x + 3y + z = 11", font="Helvetica", weight=BOLD, font_size=30, color=ROW2_COLOR)
        eq3 = Text("x + 2y + 3z = 14", font="Helvetica", weight=BOLD, font_size=30, color=ROW3_COLOR)

        eqs_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.45).move_to(UP * 0.2)

        # Labels for equations
        l1 = Text("Equation 1:", font="Helvetica", font_size=18, color=ROW1_COLOR).next_to(eq1, LEFT, buff=0.6)
        l2 = Text("Equation 2:", font="Helvetica", font_size=18, color=ROW2_COLOR).next_to(eq2, LEFT, buff=0.6)
        l3 = Text("Equation 3:", font="Helvetica", font_size=18, color=ROW3_COLOR).next_to(eq3, LEFT, buff=0.6)

        self.play(FadeIn(eq1, shift=RIGHT * 0.3), FadeIn(l1), run_time=1.2)
        self.play(FadeIn(eq2, shift=RIGHT * 0.3), FadeIn(l2), run_time=1.2)
        self.play(FadeIn(eq3, shift=RIGHT * 0.3), FadeIn(l3), run_time=1.2)
        self.wait(5.9)

        # -------------------------------------------------------------
        # 3. The Dilemma: Trial & Error vs Systematic Algorithm
        # Time: 18.0s -> 26.5s (8.5s)
        # -------------------------------------------------------------
        dilemma_text = Text(
            "Trial & error or ad-hoc substitution quickly becomes tangled...",
            font="Helvetica", font_size=20, color=MUTED_TEXT
        ).next_to(eqs_group, DOWN, buff=0.55)

        question = Text(
            "Is there a systematic method to solve all three efficiently?",
            font="Helvetica", weight=BOLD, font_size=22, color=PIVOT_COLOR
        ).next_to(dilemma_text, DOWN, buff=0.3)

        self.play(Write(dilemma_text), run_time=1.5)
        self.wait(2.0)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=1.5)
        self.wait(3.5)

        # -------------------------------------------------------------
        # 4. Reveal: Gaussian Elimination!
        # Time: 26.5s -> 34.5s (8.0s)
        # -------------------------------------------------------------
        self.play(
            FadeOut(eqs_group), FadeOut(l1), FadeOut(l2), FadeOut(l3),
            FadeOut(dilemma_text), FadeOut(question), FadeOut(header), FadeOut(div),
            run_time=1.2
        )

        answer_title = Text("The Solution:", font="Helvetica", font_size=24, color=MUTED_TEXT).to_edge(UP, buff=2.2)
        solution_banner = Text("Gaussian Elimination", font="Helvetica", weight=BOLD, font_size=46, color=ACCENT_CYAN)
        solution_banner.next_to(answer_title, DOWN, buff=0.35)
        sub_banner = Text("A systematic algorithmic reduction using elementary row operations", font="Helvetica", font_size=18, color=TEXT_COLOR)
        sub_banner.next_to(solution_banner, DOWN, buff=0.3)

        glow_box = SurroundingRectangle(solution_banner, color=PIVOT_COLOR, buff=0.25, stroke_width=2.5, corner_radius=0.12)

        self.play(Write(answer_title), run_time=0.8)
        self.play(DrawBorderThenFill(solution_banner), Create(glow_box), run_time=1.5)
        self.play(FadeIn(sub_banner, shift=UP * 0.2), run_time=1.0)
        self.wait(3.5)
