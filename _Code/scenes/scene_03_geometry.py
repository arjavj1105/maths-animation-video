"""
Scene 3: Visual Intuition
Topic: 3D Geometric Planes, Intersection Point (1, 2, 3), Invariance under Row Operations
Narration: Original voice recording by Arjav Jain (Duration: 41.01s)
Target synchronized animation duration: 41.30s
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from helpers.matrix_helpers import (
    ROW1_COLOR, ROW2_COLOR, ROW3_COLOR, BG_COLOR, TEXT_COLOR, MUTED_TEXT, ACCENT_CYAN, PIVOT_COLOR
)
from helpers.animation_helpers import setup_scene_background, create_header

class Scene03Geometry(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # -------------------------------------------------------------
        # 1. 2D Overlay Header & Legend
        # Time: 0.0s -> 3.5s (Matches narration 0.04s -> 4.36s)
        # -------------------------------------------------------------
        header_title = Text("3D Geometric Intuition", font="Helvetica", weight=BOLD, font_size=28, color=TEXT_COLOR)
        header_title.to_corner(UL, buff=0.4)
        subtitle = Text("Each equation defines a plane; the solution is their common intersection", font="Helvetica", font_size=16, color=MUTED_TEXT)
        subtitle.next_to(header_title, DOWN, buff=0.1, aligned_edge=LEFT)
        header_group = VGroup(header_title, subtitle)
        self.add_fixed_in_frame_mobjects(header_group)
        self.play(FadeIn(header_group), run_time=1.0)

        # Legend card (Fixed in frame)
        leg1 = Text("Plane 1 (Blue):   x + y + z = 6", font="Helvetica", weight=BOLD, font_size=15, color=ROW1_COLOR)
        leg2 = Text("Plane 2 (Green):  2x + 3y + z = 11", font="Helvetica", weight=BOLD, font_size=15, color=ROW2_COLOR)
        leg3 = Text("Plane 3 (Orange): x + 2y + 3z = 14", font="Helvetica", weight=BOLD, font_size=15, color=ROW3_COLOR)
        legend_vgroup = VGroup(leg1, leg2, leg3).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        leg_box = SurroundingRectangle(legend_vgroup, buff=0.15, color=MUTED_TEXT, stroke_width=1.2, fill_color="#0F172A", fill_opacity=0.85)
        legend = VGroup(leg_box, legend_vgroup).to_corner(DL, buff=0.4)
        self.add_fixed_in_frame_mobjects(legend)
        self.play(FadeIn(legend), run_time=1.0)

        # -------------------------------------------------------------
        # 2. 3D Setup: Axes, Planes, Intersection Point
        # Time: 3.5s -> 18.5s (Matches narration 4.36s -> 17.07s)
        # -------------------------------------------------------------
        axes = ThreeDAxes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            z_range=[-1, 5, 1],
            x_length=5.5,
            y_length=5.5,
            z_length=4.5
        ).move_to(RIGHT * 1.0 + DOWN * 0.2)

        # Initial camera angle
        self.set_camera_orientation(phi=68 * DEGREES, theta=25 * DEGREES)

        # Create planes using parametric surfaces
        # Plane 1: x + y + z = 6  =>  z = 6 - x - y
        p1 = Surface(
            lambda u, v: axes.c2p(u, v, 6.0 - u - v),
            u_range=[0, 3.5],
            v_range=[0, 3.5],
            resolution=(8, 8),
            fill_color=ROW1_COLOR,
            fill_opacity=0.35,
            stroke_width=0.8,
            stroke_color=ROW1_COLOR
        )

        # Plane 2: 2x + 3y + z = 11  =>  z = 11 - 2x - 3y
        p2 = Surface(
            lambda u, v: axes.c2p(u, v, 11.0 - 2.0*u - 3.0*v),
            u_range=[0, 3.0],
            v_range=[0.5, 3.0],
            resolution=(8, 8),
            fill_color=ROW2_COLOR,
            fill_opacity=0.35,
            stroke_width=0.8,
            stroke_color=ROW2_COLOR
        )

        # Plane 3: x + 2y + 3z = 14  =>  z = (14 - x - 2y)/3
        p3 = Surface(
            lambda u, v: axes.c2p(u, v, (14.0 - u - 2.0*v) / 3.0),
            u_range=[0, 3.0],
            v_range=[0.5, 3.2],
            resolution=(8, 8),
            fill_color=ROW3_COLOR,
            fill_opacity=0.35,
            stroke_width=0.8,
            stroke_color=ROW3_COLOR
        )

        # Solution Point (1, 2, 3)
        sol_pos = axes.c2p(1, 2, 3)
        sol_dot = Sphere(radius=0.18, color=PIVOT_COLOR).move_to(sol_pos)

        # 2D callout label for intersection point
        sol_card = VGroup(
            Text("Unique Common Solution", font="Helvetica", weight=BOLD, font_size=16, color=PIVOT_COLOR),
            Text("(x, y, z) = (1, 2, 3)", font="Helvetica", weight=BOLD, font_size=20, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.1)
        sol_box = SurroundingRectangle(sol_card, buff=0.15, color=PIVOT_COLOR, stroke_width=2, fill_color="#0F172A", fill_opacity=0.9)
        sol_badge = VGroup(sol_box, sol_card).to_corner(UR, buff=0.4)
        self.add_fixed_in_frame_mobjects(sol_badge)

        self.play(Create(axes), run_time=1.5)
        # Plane 1 appears with narration
        self.play(FadeIn(p1), run_time=1.5)
        self.wait(2.5)
        # Plane 2 appears with narration
        self.play(FadeIn(p2), run_time=1.5)
        self.wait(2.5)
        # Plane 3 appears with narration
        self.play(FadeIn(p3), run_time=1.5)
        self.wait(4.0)

        # Solution Point & Badge appear
        self.play(GrowFromCenter(sol_dot), FadeIn(sol_badge), run_time=1.5)

        # -------------------------------------------------------------
        # 3. Controlled Camera Rotation (Revealing Intersection Line & Point)
        # Time: 18.5s -> 26.0s (Matches narration 17.07s -> 26.00s)
        # -------------------------------------------------------------
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(7.5)
        self.stop_ambient_camera_rotation()

        # -------------------------------------------------------------
        # 4. Row Operation Geometric Intuition
        # Time: 26.0s -> 41.3s (Matches narration 26.00s -> 40.48s)
        # -------------------------------------------------------------
        row_op_note = Text(
            "Row operations replace a plane with a linear combination,\n"
            "tilting it while PRESERVING the common intersection point (1, 2, 3).",
            font="Helvetica", weight=BOLD, font_size=18, color=PIVOT_COLOR, line_spacing=1.3
        )
        row_op_box = SurroundingRectangle(row_op_note, buff=0.2, color=ACCENT_CYAN, stroke_width=2, fill_color="#0F172A", fill_opacity=0.9)
        row_op_card = VGroup(row_op_box, row_op_note).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(row_op_card)

        self.play(FadeIn(row_op_card, shift=UP * 0.2), run_time=1.5)
        self.move_camera(phi=75 * DEGREES, theta=80 * DEGREES, run_time=4.0)
        self.wait(9.8)
