from dataclasses import dataclass
from typing import Optional

from slicebug.cricut.tools import Tool, TOOLS_BY_NAME
from slicebug.exceptions import UserError


@dataclass
class PlanMat:
    """Dimensions in inches."""

    width: float
    height: float

    @classmethod
    def from_json(cls, data, version):
        assert version == 1
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
        assert version == 1
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


@dataclass
class PlanPath:
    """An SVG path at 72 DPI."""

    tool: Tool
    color: Optional[str]
    path: str

    @classmethod
    def from_json(cls, data, version):
        assert version == 1

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
            tool=TOOLS_BY_NAME[tool_name],
            color=data.get("color"),
            path=data["path"],
        )

    def to_json(self):
        result = {
            "tool": self.tool.name,
            "path": self.path,
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
        if (version := data["version"]) != 1:
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
            "version": 1,
            "mat": self.mat.to_json(),
            "material": self.material.to_json(),
            "paths": [p.to_json() for p in self.paths],
        }
