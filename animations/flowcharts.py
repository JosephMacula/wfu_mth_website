"""Narrated animations of the course flowcharts on page 2 of the brochure.

Render with, for example:
    manim -pql animations/flowcharts.py CalculusSequence
"""

from dataclasses import dataclass, field

from manim import (
    BOLD,
    DOWN,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    GrowArrow,
    Indicate,
    LaggedStart,
    RoundedRectangle,
    Text,
    VGroup,
    Write,
)
import numpy as np
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gemini import GeminiService

from course_graphs import CALCULUS_SEQUENCE, FOUNDATIONAL_COURSES, CourseGraph

# Colors sampled from the brochure.
CREAM = "#F2EEDF"
LIGHT_GOLD = "#F0CF7A"
DARK_GOLD = "#9E7E38"
INK = "#1A1A1A"

FONT = "DejaVu Serif"


@dataclass
class Step:
    """One narrated beat: speak `narration` while revealing courses and edges."""

    narration: str
    show: list[str] = field(default_factory=list)  # course codes
    connect: list[tuple[str, str]] = field(default_factory=list)  # edges
    highlight: list[str] = field(default_factory=list)  # already-shown courses


class FlowchartScene(VoiceoverScene):
    graph: CourseGraph
    steps: list[Step]

    def setup(self):
        self.camera.background_color = CREAM
        self.set_speech_service(GeminiService())

    def course_node(self, code: str) -> VGroup:
        course = self.graph.courses[code]
        label = VGroup(
            Text(course.code, font=FONT, weight=BOLD, color=INK, font_size=26),
            *(Text(line, font=FONT, color=INK, font_size=22) for line in course.title.split("\n")),
        ).arrange(DOWN, buff=0.1)
        box = RoundedRectangle(
            corner_radius=0.15,
            width=max(label.width + 0.5, 3.0),
            height=label.height + 0.3,
            fill_color=LIGHT_GOLD,
            fill_opacity=1,
            stroke_color=DARK_GOLD,
            stroke_width=3,
        )
        return VGroup(box, label).move_to([*course.pos, 0])

    def edge_arrow(self, parent: str, child: str) -> Arrow:
        # Diagonal edges leave and enter boxes off-center, toward each other, so
        # they don't share endpoints with vertical edges into the same box.
        p, c = self.nodes[parent], self.nodes[child]
        side = np.sign(c.get_x() - p.get_x())
        return Arrow(
            p.get_bottom() + side * 0.3 * p.width * RIGHT,
            c.get_top() - side * 0.3 * c.width * RIGHT,
            buff=0.1,
            color=INK,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.4,
            max_stroke_width_to_length_ratio=100,
        )

    def construct(self):
        self.nodes = {code: self.course_node(code) for code in self.graph.courses}
        title = Text(self.graph.name.upper(), font=FONT, weight=BOLD, color=DARK_GOLD, font_size=34)
        title.to_edge(UP, buff=0.2)

        self.play(Write(title))
        for step in self.steps:
            with self.voiceover(text=step.narration) as tracker:
                anims = [FadeIn(self.nodes[c], shift=0.2 * DOWN) for c in step.show]
                anims += [GrowArrow(self.edge_arrow(a, b)) for a, b in step.connect]
                anims += [Indicate(self.nodes[c], color=DARK_GOLD, scale_factor=1.08) for c in step.highlight]
                if anims:
                    self.play(LaggedStart(*anims, lag_ratio=0.5), run_time=min(2.0, tracker.duration))
        self.wait(1.5)


class CalculusSequence(FlowchartScene):
    graph = CALCULUS_SEQUENCE
    steps = [
        Step("For students considering a math major, the calculus sequence is one path through the first courses."),
        Step("It begins with MTH 106, Calculus Foundations.", show=["MTH 106"]),
        Step(
            "After Calculus Foundations, you can take MTH 111, Calculus with Analytic Geometry One.",
            show=["MTH 111"],
            connect=[("MTH 106", "MTH 111")],
        ),
        Step(
            "Next comes MTH 112, Calculus with Analytic Geometry Two.",
            show=["MTH 112"],
            connect=[("MTH 111", "MTH 112")],
        ),
        Step(
            "From there, the path branches.",
            highlight=["MTH 112"],
        ),
        Step(
            "After MTH 112, you can take MTH 113, Multivariable Calculus,",
            show=["MTH 113"],
            connect=[("MTH 112", "MTH 113")],
        ),
        Step(
            "or MTH 251, Ordinary Differential Equations.",
            show=["MTH 251"],
            connect=[("MTH 112", "MTH 251")],
        ),
    ]


class FoundationalCourses(FlowchartScene):
    graph = FOUNDATIONAL_COURSES
    steps = [
        Step("The foundational courses are a second path for students considering a math major."),
        Step(
            "Two of them are MTH 117, Discrete Mathematics, and MTH 121, Linear Algebra One.",
            show=["MTH 117", "MTH 121"],
        ),
        Step(
            "After Discrete Mathematics, you can take MTH 215, Axiomatic Systems.",
            show=["MTH 215"],
            connect=[("MTH 117", "MTH 215")],
        ),
        Step(
            "Discrete Mathematics also leads to MTH 225, Linear Algebra Two.",
            show=["MTH 225"],
            connect=[("MTH 117", "MTH 225")],
        ),
        Step(
            "And so does Linear Algebra One.",
            connect=[("MTH 121", "MTH 225")],
        ),
    ]
