"""Course flowcharts from page 2 of the Math Department brochure.

Each chart is a directed graph: an edge (a, b) means a student can take course b
after completing course a. Positions are in manim scene units and mirror the
brochure's layout.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    code: str  # e.g. "MTH 106"
    title: str  # line breaks placed as in the brochure
    pos: tuple[float, float]


@dataclass(frozen=True)
class CourseGraph:
    name: str
    courses: dict[str, Course]  # keyed by course code
    edges: list[tuple[str, str]]  # (parent code, child code)

    def children(self, code: str) -> list[str]:
        return [b for a, b in self.edges if a == code]

    def parents(self, code: str) -> list[str]:
        return [a for a, b in self.edges if b == code]


def _graph(name: str, courses: list[Course], edges: list[tuple[str, str]]) -> CourseGraph:
    by_code = {c.code: c for c in courses}
    for a, b in edges:
        assert a in by_code and b in by_code, f"edge ({a}, {b}) names an unknown course"
    return CourseGraph(name, by_code, edges)


CALCULUS_SEQUENCE = _graph(
    "Calculus Sequence",
    [
        Course("MTH 106", "Calculus Foundations", (0, 2.6)),
        Course("MTH 111", "Calculus with\nAnalytic Geometry I", (0, 0.82)),
        Course("MTH 112", "Calculus with\nAnalytic Geometry II", (0, -1.18)),
        Course("MTH 113", "Multivariable\nCalculus", (-3.2, -3.18)),
        Course("MTH 251", "Ordinary\nDifferential Equations", (3.2, -3.18)),
    ],
    [
        ("MTH 106", "MTH 111"),
        ("MTH 111", "MTH 112"),
        ("MTH 112", "MTH 113"),
        ("MTH 112", "MTH 251"),
    ],
)

FOUNDATIONAL_COURSES = _graph(
    "Foundational Courses",
    [
        Course("MTH 117", "Discrete\nMathematics", (-3.2, 1.2)),
        Course("MTH 121", "Linear\nAlgebra I", (3.2, 1.2)),
        Course("MTH 215", "Axiomatic\nSystems", (-3.2, -1.8)),
        Course("MTH 225", "Linear\nAlgebra II", (3.2, -1.8)),
    ],
    [
        ("MTH 117", "MTH 215"),
        ("MTH 117", "MTH 225"),
        ("MTH 121", "MTH 225"),
    ],
)
