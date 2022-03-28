import json

from dataclasses import dataclass


@dataclass
class Tool:
    id_: str
    name: str
    categories: list[str]

    @classmethod
    def from_json(cls, data):
        return Tool(
            id_=data["name"],
            name=data["displayName"],
            categories=data["toolType"],
        )


@dataclass
class Material:
    global_id: int
    id_: str
    name: str
    category: str
    tools: dict[str, Tool]

    @classmethod
    def from_json(cls, data):
        machine_data = data["machineMaterials"][0]
        tools = {tool.id_: tool for tool in map(Tool.from_json, machine_data["tools"])}

        return Material(
            global_id=data["globalId"],
            id_=data["_id"],
            name=data["materialName"],
            category=data["tag"],
            tools=tools,
        )


@dataclass
class MaterialSettings:
    materials: dict[int, Material]

    @classmethod
    def load(cls, path):
        with open(path) as ms_file:
            materials = {
                material.global_id: material
                for material in map(Material.from_json, json.load(ms_file))
            }
        return cls(materials=materials)
