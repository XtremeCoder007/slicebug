from dataclasses import dataclass
from enum import Enum
from typing import Optional

from slicebug.cricut.tools import Tool, TOOLS_BY_NAME
from slicebug.exceptions import UserError

PLAN_DPI = 72


@dataclass
class PlanMat:
    """Dimensions in inches."""

    width: float
    height: float

    @classmethod
    def from_json(cls, data, version):
        assert version == 2
        return cls(
            width=data["width"],
            height=data["height"],
        )

    def to_json(self):
        return {
            "width": self.width,
            "height": self.height,
        }


@dataclass
class PlanMaterial:
    """Dimensions in inches."""

    width: float
    height: float
    cricut_api_global_id: int

    @classmethod
    def from_json(cls, data, version):
        assert version == 2
        return cls(
            width=data["width"],
            height=data["height"],
            cricut_api_global_id=data["type"],
        )

    def to_json(self):
        return {
            "width": self.width,
            "height": self.height,
            "type": self.cricut_api_global_id,
        }


class PlanPathOp(Enum):
    MOVE_TO = "M"
    LINE_TO = "L"
    CURVE_TO = "C"
    CLOSE_PATH = "Z"

    def point_count(self):
        match self:
            case (PlanPathOp.MOVE_TO | PlanPathOp.LINE_TO):
                return 1
            case PlanPathOp.CURVE_TO:
                return 3
            case PlanPathOp.CLOSE_PATH:
                return 0
            case _:
                assert False


@dataclass
class PlanPathStep:
    """A single step in a plan."""

    op: str
    points: list[tuple[float, float]]

    @classmethod
    def from_json(cls, data, version):
        assert version == 2

        op = PlanPathOp(data["op"])
        points = [(x, y) for x, y in data["points"]]

        return PlanPathStep(op, points)

    @classmethod
    def many_from_svg(cls, path_data):
        tokens = path_data.split()[::-1]
        steps = []
        while tokens:
            op_code = tokens.pop()
            op = PlanPathOp(op_code)
            points = []
            for _ in range(op.point_count()):
                x = float(tokens.pop())
                y = float(tokens.pop())
                points.append((x, y))
            steps.append(cls(op, points))

        return steps

    def to_svg(self):
        if not self.points:
            return self.op.value

        points_formatted = " ".join(f"{x} {y}" for x, y in self.points)
        return f"{self.op.value} {points_formatted}"

    def to_json(self):
        return {
            "op": self.op.value,
            "points": self.points,
        }


@dataclass
class PlanPath:
    """An SVG path at 72 DPI."""

    tool: Tool
    color: Optional[str]
    steps: list[PlanPathStep]

    @classmethod
    def from_json(cls, data, version):
        assert version == 2

        tool_name = data["tool"]
        if tool_name not in TOOLS_BY_NAME:
            raise UserError(
                f"Unknown tool {tool_name}.",
                "Try using `slicebug list-tools` to list available tools.",
            )
        tool = TOOLS_BY_NAME[tool_name]

        color = data.get("color")

        if (color is not None) and (tool.name != "pen"):
            raise UserError(
                f"Color cannot be set for tool {tool.name}.",
                "Modify your plan to avoid setting a color for tools other than the pen.",
            )

        if (color is None) and (tool.name == "pen"):
            raise UserError(
                f"A pen path does not have a color set.",
                "Modify your plan to set a color for all pen paths.",
            )

        return cls(
            tool=tool,
            color=color,
            steps=[PlanPathStep.from_json(step, version) for step in data["steps"]],
        )

    def to_json(self):
        result = {
            "tool": self.tool.name,
            "steps": [step.to_json() for step in self.steps],
        }
        if self.color is not None:
            result["color"] = self.color
        return result


@dataclass
class Plan:
    mat: PlanMat
    material: PlanMaterial
    paths: list[PlanPath]

    @classmethod
    def from_json(cls, data):
        if (version := data["version"]) != 2:
            raise UserError(
                f"Invalid plan version {version}. The plan might be corrupted, or it might be meant for a different version of slicebug."
            )

        return cls(
            mat=PlanMat.from_json(data["mat"], version),
            material=PlanMaterial.from_json(data["material"], version),
            paths=[PlanPath.from_json(path, version) for path in data["paths"]],
        )

    def to_json(self):
        return {
            "version": 2,
            "mat": self.mat.to_json(),
            "material": self.material.to_json(),
            "paths": [p.to_json() for p in self.paths],
        }
