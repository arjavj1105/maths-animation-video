"""
Scene 4: Worked Example
Topic: Complete Step-by-Step Gaussian Elimination, Row Operations with Arithmetic,
       Row Echelon Form with Pivots, and Back Substitution
Narration: Original voice recording by Arjav Jain (Duration: 84.50s)
Target synchronized animation duration: 84.80s
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN, PIVOT_COLOR,
    SUCCESS_GREEN, build_augmented_matrix, create_pivot_box, create_staircase
)
from helpers.animation_helpers import setup_scene_background, create_header, create_badge

class Scene04WorkedExample(Scene):
    def construct(self):
        setup_scene_background(self)

        # -------------------------------------------------------------
        # 1. Header and Initial Matrix
        # Time: 0.0s -> 19.5s (Matches narration 0.04s -> 19.97s)
        # Arjav reads rows 1, 2, 3 until 17.00s, then pivot 1
        # -------------------------------------------------------------
        header = create_header("Worked Example: Gaussian Elimination", "Systematic row reduction to row echelon form")
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=1.0)

        # Initial augmented matrix [A | b]
        data = [
            ["1", "1", "1", "6"],
            ["2", "3", "1", "11"],
            ["1", "2", "3", "14"]
        ]
        mat_mob, grid, div_line = build_augmented_matrix(data, font_size=28)
        mat_mob.move_to(LEFT * 2.5 + UP * 0.3)

        self.play(FadeIn(mat_mob, shift=UP * 0.3), run_time=1.5)
        # Hold while Arjav reads Row 1, Row 2, Row 3
        self.wait(14.0)

        # First Pivot highlight at (0, 0)
        piv1_box = create_pivot_box(grid[0][0])
        piv1_lbl = Text("Pivot 1 = 1", font="Helvetica", weight=BOLD, font_size=16, color=PIVOT_COLOR).next_to(piv1_box, UP, buff=0.15)
        self.play(Create(piv1_box), Write(piv1_lbl), run_time=1.0)
        self.wait(2.0)

        # -------------------------------------------------------------
        # 2. Row Operation 1: R2 -> R2 - 2R1
        # Time: 19.5s -> 32.5s (Matches narration 19.97s -> 32.78s)
        # -------------------------------------------------------------
        op1_badge = create_badge("Row Operation 1:  R₂ → R₂ − 2R₁", color=ROW2_COLOR, font_size=18)
        op1_badge.move_to(RIGHT * 3.2 + UP * 1.8)

        calc1_lines = VGroup(
            Text("Clear Column 1, Row 2:", font="Helvetica", font_size=16, color=MUTED_TEXT),
            Text("  [ 2,  3,  1 | 11 ]", font="Courier New", weight=BOLD, font_size=16, color=ROW2_COLOR),
            Text("− 2[ 1,  1,  1 |  6 ]", font="Courier New", weight=BOLD, font_size=16, color=ROW1_COLOR),
            Line(LEFT * 1.8, RIGHT * 1.8, stroke_width=1.5, color=MUTED_TEXT),
            Text("= [ 0,  1, −1 | −1 ]", font="Courier New", weight=BOLD, font_size=16, color=PIVOT_COLOR)
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(op1_badge, DOWN, buff=0.25)

        card1 = RoundedRectangle(width=4.8, height=3.2, corner_radius=0.12, stroke_width=1.5, stroke_color=ROW2_COLOR, fill_color="#0F172A", fill_opacity=0.85)
        card1.move_to(VGroup(op1_badge, calc1_lines).get_center())
        step1_side = VGroup(card1, op1_badge, calc1_lines)

        self.play(FadeIn(step1_side, shift=LEFT * 0.2), run_time=1.5)

        # Animate Row 2 entries changing in the matrix
        new_r2_vals = ["0", "1", "-1", "-1"]
        r2_anims = []
        for c_idx, val in enumerate(new_r2_vals):
            new_text = Text(val, font="Helvetica", weight=BOLD, font_size=28, color=ROW2_COLOR).move_to(grid[1][c_idx].get_center())
            r2_anims.append(Transform(grid[1][c_idx], new_text))

        self.play(*r2_anims, run_time=1.5)
        self.wait(10.0)

        # -------------------------------------------------------------
        # 3. Row Operation 2: R3 -> R3 - R1
        # Time: 32.5s -> 44.5s (Matches narration 32.78s -> 45.00s)
        # -------------------------------------------------------------
        self.play(FadeOut(step1_side), run_time=1.0)

        op2_badge = create_badge("Row Operation 2:  R₃ → R₃ − R₁", color=ROW3_COLOR, font_size=18)
        op2_badge.move_to(RIGHT * 3.2 + UP * 1.8)

        calc2_lines = VGroup(
            Text("Clear Column 1, Row 3:", font="Helvetica", font_size=16, color=MUTED_TEXT),
            Text("  [ 1,  2,  3 | 14 ]", font="Courier New", weight=BOLD, font_size=16, color=ROW3_COLOR),
            Text("− [ 1,  1,  1 |  6 ]", font="Courier New", weight=BOLD, font_size=16, color=ROW1_COLOR),
            Line(LEFT * 1.8, RIGHT * 1.8, stroke_width=1.5, color=MUTED_TEXT),
            Text("= [ 0,  1,  2 |  8 ]", font="Courier New", weight=BOLD, font_size=16, color=PIVOT_COLOR)
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(op2_badge, DOWN, buff=0.25)

        card2 = RoundedRectangle(width=4.8, height=3.2, corner_radius=0.12, stroke_width=1.5, stroke_color=ROW3_COLOR, fill_color="#0F172A", fill_opacity=0.85)
        card2.move_to(VGroup(op2_badge, calc2_lines).get_center())
        step2_side = VGroup(card2, op2_badge, calc2_lines)

        self.play(FadeIn(step2_side, shift=LEFT * 0.2), run_time=1.5)

        # Animate Row 3 entries changing in matrix
        new_r3_vals = ["0", "1", "2", "8"]
        r3_anims = []
        for c_idx, val in enumerate(new_r3_vals):
            new_text = Text(val, font="Helvetica", weight=BOLD, font_size=28, color=ROW3_COLOR).move_to(grid[2][c_idx].get_center())
            r3_anims.append(Transform(grid[2][c_idx], new_text))

        self.play(*r3_anims, run_time=1.5)
        self.wait(8.0)

        # -------------------------------------------------------------
        # 4. Row Operation 3: R3 -> R3 - R2
        # Time: 44.5s -> 56.5s (Matches narration 45.00s -> 57.00s)
        # -------------------------------------------------------------
        self.play(FadeOut(step2_side), FadeOut(piv1_box), FadeOut(piv1_lbl), run_time=1.0)

        # Highlight second pivot at (1, 1)
        piv2_box = create_pivot_box(grid[1][1])
        piv2_lbl = Text("Pivot 2 = 1", font="Helvetica", weight=BOLD, font_size=16, color=PIVOT_COLOR).next_to(mat_mob, UP, buff=0.3)
        self.play(Create(piv2_box), Write(piv2_lbl), run_time=1.0)

        op3_badge = create_badge("Row Operation 3:  R₃ → R₃ − R₂", color=PIVOT_COLOR, font_size=18)
        op3_badge.move_to(RIGHT * 3.2 + UP * 1.8)

        calc3_lines = VGroup(
            Text("Clear Column 2, Row 3:", font="Helvetica", font_size=16, color=MUTED_TEXT),
            Text("  [ 0,  1,  2 |  8 ]", font="Courier New", weight=BOLD, font_size=16, color=ROW3_COLOR),
            Text("− [ 0,  1, −1 | −1 ]", font="Courier New", weight=BOLD, font_size=16, color=ROW2_COLOR),
            Line(LEFT * 1.8, RIGHT * 1.8, stroke_width=1.5, color=MUTED_TEXT),
            Text("= [ 0,  0,  3 |  9 ]", font="Courier New", weight=BOLD, font_size=16, color=PIVOT_COLOR)
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(op3_badge, DOWN, buff=0.25)

        card3 = RoundedRectangle(width=4.8, height=3.2, corner_radius=0.12, stroke_width=1.5, stroke_color=PIVOT_COLOR, fill_color="#0F172A", fill_opacity=0.85)
        card3.move_to(VGroup(op3_badge, calc3_lines).get_center())
        step3_side = VGroup(card3, op3_badge, calc3_lines)

        self.play(FadeIn(step3_side, shift=LEFT * 0.2), run_time=1.5)

        # Animate Row 3 becoming [0, 0, 3, 9]
        final_r3_vals = ["0", "0", "3", "9"]
        r3_final_anims = []
        for c_idx, val in enumerate(final_r3_vals):
            new_text = Text(val, font="Helvetica", weight=BOLD, font_size=28, color=ROW3_COLOR).move_to(grid[2][c_idx].get_center())
            r3_final_anims.append(Transform(grid[2][c_idx], new_text))

        self.play(*r3_final_anims, run_time=1.5)
        self.wait(7.0)

        # -------------------------------------------------------------
        # 5. Row Echelon Form (REF) & Pivots Highlight
        # Time: 56.5s -> 64.0s (Matches narration 57.00s -> 64.00s)
        # -------------------------------------------------------------
        self.play(FadeOut(step3_side), FadeOut(piv2_box), FadeOut(piv2_lbl), run_time=1.0)

        ref_banner = create_badge("ROW ECHELON FORM (REF) ACHIEVED", color=SUCCESS_GREEN, font_size=18)
        ref_banner.next_to(mat_mob, UP, buff=0.4)

        # All 3 pivot boxes: (0,0), (1,1), (2,2)
        box1 = create_pivot_box(grid[0][0])
        box2 = create_pivot_box(grid[1][1])
        box3 = create_pivot_box(grid[2][2])
        all_pivots = VGroup(box1, box2, box3)

        # Echelon staircase lines
        staircase = create_staircase(grid)

        # Side note on pivots
        ref_notes = VGroup(
            Text("REF Properties:", font="Helvetica", weight=BOLD, font_size=18, color=TEXT_COLOR),
            Text("• Pivots: 1, 1, 3 (all non-zero)", font="Helvetica", font_size=16, color=PIVOT_COLOR),
            Text("• Pivots advance to the right", font="Helvetica", font_size=16, color=TEXT_COLOR),
            Text("• All entries below pivots = 0", font="Helvetica", font_size=16, color=SUCCESS_GREEN)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 0.3)

        self.play(FadeIn(ref_banner), Create(all_pivots), Create(staircase), run_time=2.0)
        self.play(FadeIn(ref_notes, shift=LEFT * 0.2), run_time=1.5)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 6. Back Substitution to Final Solution
        # Time: 64.0s -> 84.8s (Matches narration 64.00s -> 84.50s)
        # -------------------------------------------------------------
        self.play(
            FadeOut(mat_mob), FadeOut(ref_banner), FadeOut(all_pivots), FadeOut(staircase), FadeOut(ref_notes),
            run_time=1.0
        )

        bs_title = Text("Back Substitution", font="Helvetica", weight=BOLD, font_size=26, color=PIVOT_COLOR).to_edge(UP, buff=1.4)
        self.play(Write(bs_title), run_time=0.8)

        # Row 3 calculation: 3z = 9 => z = 3
        bs_z = Text("From Row 3:    3z = 9                    ⇒   z = 3", font="Courier New", weight=BOLD, font_size=20, color=ROW3_COLOR)
        # Row 2 calculation: y - z = -1 => y - 3 = -1 => y = 2
        bs_y = Text("From Row 2:    y − z = −1   (y − 3 = −1) ⇒   y = 2", font="Courier New", weight=BOLD, font_size=20, color=ROW2_COLOR)
        # Row 1 calculation: x + y + z = 6 => x + 2 + 3 = 6 => x = 1
        bs_x = Text("From Row 1:    x + y + z = 6  (x + 5 = 6) ⇒   x = 1", font="Courier New", weight=BOLD, font_size=20, color=ROW1_COLOR)

        bs_group = VGroup(bs_z, bs_y, bs_x).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.3)

        self.play(FadeIn(bs_z, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(1.3)
        self.play(FadeIn(bs_y, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(5.0)
        self.play(FadeIn(bs_x, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(4.8)

        # Final Solution Banner
        sol_text = Text("Final Solution:  (x, y, z) = (1, 2, 3)", font="Helvetica", weight=BOLD, font_size=28, color=PIVOT_COLOR)
        sol_box = SurroundingRectangle(sol_text, buff=0.3, color=PIVOT_COLOR, stroke_width=2.5, corner_radius=0.12)
        final_sol_mob = VGroup(sol_box, sol_text).next_to(bs_group, DOWN, buff=0.6)

        self.play(DrawBorderThenFill(final_sol_mob), run_time=1.5)
        self.wait(2.8)
