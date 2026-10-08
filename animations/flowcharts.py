"""Narrated animations of the course flowcharts on page 2 of the brochure.

Render with, for example:
    manim -pql animations/flowcharts.py CalculusSequence
"""

from dataclasses import dataclass, field

from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Brace,
    FadeIn,
    GrowArrow,
    GrowFromCenter,
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
    brace: list[str] = field(default_factory=list)  # courses whose brace to draw


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

    def brace(self, code: str) -> Brace:
        # The brace sits on the side of the group facing the braced course.
        group = next(g for c, g in self.graph.braces if c == code)
        boxes = VGroup(*(self.nodes[g] for g in group))
        side = RIGHT if self.nodes[code].get_x() > boxes.get_x() else LEFT
        return Brace(boxes, direction=side, buff=0.15, color=INK)

    def construct(self):
        self.nodes = {code: self.course_node(code) for code in self.graph.courses}
        title = Text(self.graph.name.upper(), font=FONT, weight=BOLD, color=DARK_GOLD, font_size=34)
        title.to_edge(UP, buff=0.2)

        self.play(Write(title))
        for step in self.steps:
            with self.voiceover(text=step.narration) as tracker:
                anims = [FadeIn(self.nodes[c], shift=0.2 * DOWN) for c in step.show]
                anims += [GrowArrow(self.edge_arrow(a, b)) for a, b in step.connect]
                anims += [GrowFromCenter(self.brace(c)) for c in step.brace]
                anims += [Indicate(self.nodes[c], color=DARK_GOLD, scale_factor=1.08) for c in step.highlight]
                if anims:
                    self.play(LaggedStart(*anims, lag_ratio=0.5), run_time=min(2.0, tracker.duration))
        self.wait(1.5)


class CalculusSequence(FlowchartScene):
    graph = CALCULUS_SEQUENCE
    steps = [
        Step("If you're considering a math major, the calculus sequence is a great place to start. There are several options of where to begin."),
        Step("If you've never taken calculus before and you think a year-long course is best for you, start with math 106, Calculus Foundations. "
        "If you took calculus in high school, but still want a solid grounding in the fundamentals, you're still welcome to start here.", 
        show=["MTH 106"]),
        Step(
            "Math 111 is our one-semester introductory calculus course. This course does not assume you've taken calculus before, and is a common first math class for students.",
            show=["MTH 111"],
            connect=[("MTH 106", "MTH 111")],
        ),
        Step(
            "Math 104 is a half semester course intended for future calculus students who want a comprehensive review of algebra and trigonometry before tackling Math 111 or Math 106. "
            "The course is 2 credit hours with pass/fail grading.",
            show=["MTH 104"],
            brace=["MTH 104"],
        ),
        Step(
            "Next comes Math 112, Calculus with Analytic Geometry Two. We recommend that you start here if you took AP calculus AB in high school and scored well on the AP exam.",
            show=["MTH 112"],
            connect=[("MTH 111", "MTH 112")],
        ),
        Step(
            "After Math 112, there are now two courses you can take.",
            highlight=["MTH 112"],
        ),
        Step(
            "You can continue with the traditional calculus sequence and take math 113, Multivariable Calculus. If you took both AP calculus AB and BC in high school, and scored well on both AP exams, you can even start here.",
            show=["MTH 113"],
            connect=[("MTH 112", "MTH 113")],
        ),
        Step(
            "You can also take Math 251, Ordinary Differential Equations. This is a great option for students who are interested in applied mathematics or engineering.",
            show=["MTH 251"],
            connect=[("MTH 112", "MTH 251")],
        ),
    ]


class FoundationalCourses(FlowchartScene):
    graph = FOUNDATIONAL_COURSES
    steps = [
        Step("Alongside the calculus sequence is our sequence of 'foundational' courses. These courses help you build your problem-solving skills, and introduce you to fundamental mathematics outside of calculus."),
        Step(
            "The first two courses in this sequence are math 117, Discrete Mathematics, and Math 121, Linear Algebra One. Neither course has any prerequisites, but students generally take a calculus course before enrolling in these courses. "
            "Additionally, students often find it helpful to take math 117 before taking math 121.",
            show=["MTH 117", "MTH 121"],
        ),
        Step(
            "Once you've taken math 117, you can take math 215, Axiomatic Systems.",
            show=["MTH 215"],
            connect=[("MTH 117", "MTH 215")],
        ),
        Step(
            "Completing math 117 also allows you to take math 225, Linear Algebra Two.",
            show=["MTH 225"],
            connect=[("MTH 117", "MTH 225")],
        ),
        Step(
            "Alternatively, completing math 121 also allows you to take math 225.",
            connect=[("MTH 121", "MTH 225")],
        ),
    ]
