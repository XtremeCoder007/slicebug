from enum import Enum
from dataclasses import dataclass

from slicebug.cricut.protobufs.NativeModel_pb2 import PBArtType, PBToolType


class HeadType(Enum):
    A = 0
    B = 1


@dataclass
class Tool:
    name: str
    # The CricutDevice plugin has a predetermined order of operations
    # (scoring goes first, then drawing, then debossing...). We need to know
    # it in advance in order to tell the user which tools to load first,
    # because the plugin won't tell us until it's too late. CDS appears to
    # have a similar list hardcoded somewhere.(This is probably more of a
    # property of art type than tool, but we don't care very much about art
    # types, so it lives here.)
    order: int
    cricut_api_name: str
    cricut_pb_tool_type: int
    cricut_pb_art_type: int
    head_type: HeadType


# This list *must* be sorted by order.
TOOLS = [
    Tool(
        name="scoring_stylus",
        order=101,
        cricut_api_name="score",
        cricut_pb_tool_type=PBToolType.STYLUS_TT,
        cricut_pb_art_type=PBArtType.SCORE_ART_TYPE,
        head_type=HeadType.A,
    ),
    Tool(
        name="scoring_wheel",
        order=102,
        cricut_api_name="scoringWheel",
        cricut_pb_tool_type=PBToolType.SCORING_WHEEL_TT,
        cricut_pb_art_type=PBArtType.SCORE_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="double_scoring_wheel",
        order=103,
        cricut_api_name="doubleScoringWheel",
        cricut_pb_tool_type=PBToolType.DOUBLE_SCORING_WHEEL_TT,
        cricut_pb_art_type=PBArtType.SCORE_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="pen",
        order=201,
        cricut_api_name="feltPen",
        cricut_pb_tool_type=PBToolType.PEN_DT_TT,
        cricut_pb_art_type=PBArtType.DRAW_ART_TYPE,
        head_type=HeadType.A,
    ),
    Tool(
        name="debossing_tip",
        order=301,
        cricut_api_name="debossFineTip",
        cricut_pb_tool_type=PBToolType.DEBOSSING_TOOL_TT,
        cricut_pb_art_type=PBArtType.DEBOSS_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="engraving_tip",
        order=401,
        cricut_api_name="engravingTip",
        cricut_pb_tool_type=PBToolType.ENGRAVE_TOOL_TT,
        cricut_pb_art_type=PBArtType.ENGRAVE_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="foil_transfer_fine",
        order=501,
        cricut_api_name="midasFine",
        cricut_pb_tool_type=PBToolType.MIDAS_FINE_TOOL_TT,
        cricut_pb_art_type=PBArtType.MIDAS_FINE_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="foil_transfer_regular",
        order=502,
        cricut_api_name="midasRegular",
        cricut_pb_tool_type=PBToolType.MIDAS_REGULAR_TOOL_TT,
        cricut_pb_art_type=PBArtType.MIDAS_REGULAR_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="foil_transfer_bold",
        order=503,
        cricut_api_name="midasBold",
        cricut_pb_tool_type=PBToolType.MIDAS_BOLD_TOOL_TT,
        cricut_pb_art_type=PBArtType.MIDAS_BOLD_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="perforation_wheel",
        order=601,
        cricut_api_name="perfBasic",
        cricut_pb_tool_type=PBToolType.PERFORATION_WHEEL_TT,
        cricut_pb_art_type=PBArtType.PERFORATE_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="wavy_blade",
        order=701,
        cricut_api_name="wavyBlade",
        cricut_pb_tool_type=PBToolType.WAVE_TOOL_TT,
        cricut_pb_art_type=PBArtType.WAVE_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="fine_point_blade",
        order=801,
        cricut_api_name="dragKnife",
        cricut_pb_tool_type=PBToolType.DRAG_KNIFE_TT,
        cricut_pb_art_type=PBArtType.CUT_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="deep_point_blade",
        order=802,
        cricut_api_name="deepCut",
        cricut_pb_tool_type=PBToolType.DEEP_CUT_TT,
        cricut_pb_art_type=PBArtType.CUT_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="rotary_blade",
        order=803,
        cricut_api_name="rollingBlade",
        cricut_pb_tool_type=PBToolType.ROLLING_BLADE_TT,
        cricut_pb_art_type=PBArtType.CUT_ART_TYPE,
        head_type=HeadType.B,
    ),
    Tool(
        name="knife_blade",
        order=804,
        cricut_api_name="tangentialBlade",
        cricut_pb_tool_type=PBToolType.TANGENTIAL_BLADE_TT,
        cricut_pb_art_type=PBArtType.CUT_ART_TYPE,
        head_type=HeadType.B,
    ),
]

TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}
TOOLS_BY_PB_TOOL_TYPE = {tool.cricut_pb_tool_type: tool for tool in TOOLS}
