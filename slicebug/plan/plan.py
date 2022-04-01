from dataclasses import dataclass
from typing import Optional

from slicebug.cricut.tools import Tool, TOOLS_BY_NAME


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
            raise ValueError(f"unknown tool {tool_name}")
        tool = TOOLS_BY_NAME[tool_name]

        color = data.get("color")

        if (color is not None) and (tool.name != "pen"):
            raise ValueError(f"color cannot be set for tool {tool.name}")

        return cls(
            tool=TOOLS_BY_NAME[tool_name],
            color=data.get("color"),
            path=data["path"],
        )


@dataclass
class Plan:
    mat: PlanMat
    material: PlanMaterial
    paths: list[PlanPath]

    @classmethod
    def from_json(cls, data):
        if (version := data["version"]) != 1:
            raise ValueError(f"invalid plan version {version}")

        return cls(
            mat=PlanMat.from_json(data["mat"], version),
            material=PlanMaterial.from_json(data["material"], version),
            paths=[PlanPath.from_json(path, version) for path in data["paths"]],
        )
