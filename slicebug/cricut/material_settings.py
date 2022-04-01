import json

from dataclasses import dataclass

from slicebug.cricut.protobufs.NativeModel_pb2 import PBModeApi, PBTool


@dataclass
class MaterialToolInfo:
    id_: str
    name: str
    pb_tool: PBTool

    @classmethod
    def from_json(cls, data):
        pb_tool_fields = (
            "displayName",
            "name",
            "isSelected",
            "minRangePressure",
            "maxRangePressure",
            "toolTypeEnum",
            "toolType",
            "preferredOrder",
            "isPreferred",
        )
        pb_tool = PBTool(
            **{field: data[field] for field in pb_tool_fields if field in data}
        )

        for mode_name in ("precisionMode", "draftMode"):
            if mode_name not in data:
                continue

            mode_data = data[mode_name]
            mode_fields = (
                "deltaAdjustment",
                "selectPressure",
                "yMoveToSpeed",
                "pressure",
                "yMoveToAccel",
                "moveToSpeed",
                "multiPass",
                "maxPressure",
                "moveToAccel",
                "cutSpeed",
                "yCutSpeed",
                "cutAccel",
                "yCutAccel",
                "minPressure",
                "multiPressure",
            )
            getattr(pb_tool, mode_name).CopyFrom(
                PBModeApi(
                    **{
                        field: mode_data[field]
                        for field in mode_fields
                        if field in mode_data
                    }
                )
            )

        return cls(
            id_=data["name"],
            name=data["displayName"],
            pb_tool=pb_tool,
        )


@dataclass
class Material:
    global_id: int
    id_: str
    name: str
    category: str
    tools: dict[str, MaterialToolInfo]

    @classmethod
    def from_json(cls, data):
        machine_data = data["machineMaterials"][0]
        tools = {
            tool.id_: tool
            for tool in map(MaterialToolInfo.from_json, machine_data["tools"])
        }

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
        # TODO: encoding?
        with open(path, encoding="utf-8") as ms_file:
            materials_json = json.load(ms_file)["customMaterials"]["materials"]
            materials = {
                material.global_id: material
                for material in map(Material.from_json, materials_json)
            }
        return cls(materials=materials)
