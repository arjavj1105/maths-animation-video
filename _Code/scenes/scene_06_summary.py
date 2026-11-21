"""
Scene 6: Summary and Credits
Topic: Three Key Takeaways, Final Solution Restatement,
       Academic References, AI Tool Disclosure, Thank You Closing Frame
Target duration: ~55.0s (Audio duration: 54.62s)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN,
    PIVOT_COLOR, SUCCESS_GREEN
)
from helpers.animation_helpers import setup_scene_background, create_header, create_badge

class Scene06Summary(Scene):
    def construct(self):
        setup_scene_background(self)

        # -------------------------------------------------------------
        # 1. Header & Three Core Takeaways
        # Time: 0.0s -> 24.0s (24.0s)
        # -------------------------------------------------------------
        header = create_header("Summary & Key Takeaways", "Core principles of Gaussian Elimination")
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=1.0)

        # Three Takeaways
        t1 = VGroup(
            Text("1. Systematic Reduction", font="Helvetica", weight=BOLD, font_size=18, color=PIVOT_COLOR),
            Text("Gaussian elimination systematically converts any linear system into row echelon form.", font="Helvetica", font_size=16, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        t2 = VGroup(
            Text("2. Reversible Row Operations", font="Helvetica", weight=BOLD, font_size=18, color=SUCCESS_GREEN),
            Text("Elementary row operations strictly preserve the solution set because every step is reversible.", font="Helvetica", font_size=16, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        t3 = VGroup(
            Text("3. Back Substitution", font="Helvetica", weight=BOLD, font_size=18, color=ACCENT_CYAN),
            Text("Back substitution cleanly unpacks the triangular system from bottom to top.", font="Helvetica", font_size=16, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        takeaways = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.3)

        self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(5.0)
        self.play(FadeIn(t2, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(5.0)
        self.play(FadeIn(t3, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(5.0)

        # Final Solution Re-statement
        sol_badge = create_badge("FINAL SOLUTION:  (x, y, z) = (1, 2, 3)", color=PIVOT_COLOR, font_size=18)
        sol_badge.next_to(takeaways, DOWN, buff=0.35)
        self.play(DrawBorderThenFill(sol_badge), run_time=1.0)
        self.wait(3.4)

        # -------------------------------------------------------------
        # 2. Academic References & AI Tool Disclosure
        # Time: 24.0s -> 42.0s (18.0s)
        # -------------------------------------------------------------
        self.play(FadeOut(takeaways), FadeOut(sol_badge), FadeOut(header), run_time=1.2)

        ref_header = Text("Academic References", font="Helvetica", weight=BOLD, font_size=20, color=PIVOT_COLOR).to_edge(UP, buff=1.0)
        r1 = Text("• Gilbert Strang, Introduction to Linear Algebra, 5th Edition, Wellesley-Cambridge Press.", font="Helvetica", font_size=14, color=TEXT_COLOR)
        r2 = Text("• David C. Lay, Linear Algebra and Its Applications, 5th Edition, Pearson.", font="Helvetica", font_size=14, color=TEXT_COLOR)
        r3 = Text("• Manim Community Documentation (v0.22.1) — Mathematical Animation Engine.", font="Helvetica", font_size=14, color=TEXT_COLOR)
        refs_group = VGroup(r1, r2, r3).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(ref_header, DOWN, buff=0.25)

        ai_header = Text("AI Disclosure & Methodology", font="Helvetica", weight=BOLD, font_size=20, color=ACCENT_CYAN).next_to(refs_group, DOWN, buff=0.4)
        ai_p1 = Text("AI tools assisted in preparing the script, animation code, and narration.", font="Helvetica", font_size=14, color=TEXT_COLOR)
        ai_p2 = Text("Developed using Google Antigravity. Voice: Microsoft Edge TTS (en-US-GuyNeural).", font="Helvetica", font_size=14, color=TEXT_COLOR)
        ai_p3 = Text("All mathematical calculations and row operations were independently verified with NumPy.", font="Helvetica", weight=BOLD, font_size=14, color=SUCCESS_GREEN)
        ai_group = VGroup(ai_p1, ai_p2, ai_p3).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(ai_header, DOWN, buff=0.25)

        self.play(Write(ref_header), FadeIn(refs_group), run_time=1.5)
        self.play(Write(ai_header), FadeIn(ai_group), run_time=1.5)
        self.wait(13.8)

        # -------------------------------------------------------------
        # 3. Final Closing Frame
        # Time: 42.0s -> 55.0s (13.0s)
        # -------------------------------------------------------------
        self.play(FadeOut(ref_header), FadeOut(refs_group), FadeOut(ai_header), FadeOut(ai_group), run_time=1.2)

        thank_you = Text("Thank You", font="Helvetica", weight=BOLD, font_size=48, color=PIVOT_COLOR)
        student_name = Text("Arjav Jain", font="Helvetica", weight=BOLD, font_size=26, color=TEXT_COLOR)
        student_id = Text("Student ID: E25B070861", font="Helvetica", font_size=20, color=ACCENT_CYAN)
        course_info = Text("Mathematics 3 – Linear Algebra and Calculus  |  Batch: Ramanujan", font="Helvetica", font_size=16, color=MUTED_TEXT)

        closing_card = VGroup(thank_you, student_name, student_id, course_info).arrange(DOWN, buff=0.25).center()
        closing_box = SurroundingRectangle(closing_card, buff=0.45, color=PIVOT_COLOR, stroke_width=2.5, corner_radius=0.15)
        closing_group = VGroup(closing_box, closing_card)

        self.play(DrawBorderThenFill(closing_group), run_time=2.0)
        self.wait(9.8)
