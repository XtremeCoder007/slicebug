import argparse
import json
import re
from collections import defaultdict

from slicebug.cricut.path_util_plugin import PathUtilPlugin
from slicebug.cricut.tools import TOOLS_BY_NAME
from slicebug.plan.plan import PlanMaterial, PlanMat, PlanPath, Plan
from slicebug.exceptions import ProtocolError, UserError


def parse_dimensions(string):
    dimensions_re = r"^(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)$"
    match = re.match(dimensions_re, string)

    if match is None:
        raise argparse.ArgumentTypeError(
            f"Invalid dimensions {string}. Must be a string like 12x12 or 8.5x11, in inches."
        )

    width, height = match.groups()
    return (float(width), float(height))


def parse_color_tool_mapping(string):
    map_re = r"^#?([\dA-Fa-f]{6}):([a-z_]+)$"
    match = re.match(map_re, string)

    if match is None:
        raise argparse.ArgumentTypeError(
            f"Invalid mapping {string}. Must be a string like FF0000:scoring_stylus."
        )

    color, tool = match.groups()

    if not color.startswith("#"):
        color = f"#{color}"

    if tool not in TOOLS_BY_NAME:
        raise argparse.ArgumentTypeError(
            f"Invalid tool name {tool}. Try `slicebug list-tools` to get a list of available tools."
        )

    return (color.upper(), TOOLS_BY_NAME[tool])


def plan_register_args(subparsers):
    parser = subparsers.add_parser("plan")
    parser.add_argument("input_file", type=argparse.FileType("r"))
    parser.add_argument("output_file", type=argparse.FileType("w"))
    parser.add_argument(
        "--map", action="append", default=[], type=parse_color_tool_mapping
    )
    parser.add_argument("--material", type=int, required=True)
    parser.add_argument("--material-size", default=(12.0, 12.0), type=parse_dimensions)
    parser.add_argument("--mat-size", default=(13.0, 12.0), type=parse_dimensions)

    parser.set_defaults(cmd_handler=plan)
    parser.set_defaults(cmd_needs_profile=True)
    parser.set_defaults(cmd_needs_keys=False)


def get_paths_from_canvas(canvas_json):
    layer_data = canvas_json["imageLayerData"]
    paths = []

    def extract_paths(group):
        nonlocal paths
        for subgroup in group["groupGroups"]:
            if len(subgroup) == 0:
                continue

            subgroup_type = subgroup.get("groupType")
            if subgroup_type == "GROUP":
                extract_paths(subgroup)
                continue
            elif subgroup_type != "LAYER":
                raise ProtocolError(f"unexpected group type {subgroup_type}")

            stroke = subgroup.get("layerStroke")
            if (stroke is None) or len(stroke) != 1:
                continue
            stroke = stroke[0]

            stroke_color = (
                stroke.get("strokeColor", "#000000").replace(" ", "0").upper()
            )
            path_data = layer_data[subgroup["groupGUID"]][1]

            # CricutDevice seems to get sad when there are commas
            path_data = path_data.replace(",", " ")

            paths.append((stroke_color, path_data))

    extract_paths(canvas_json["imageModel"])

    return paths


def plan(args, config):
    if config.path_util_plugin_path() is None:
        raise UserError(
            "Path util plugin is missing.", "Try running `slicebug bootstrap`."
        )

    with PathUtilPlugin(config.path_util_plugin_path()) as path_util:
        canvas_json = path_util.svg_to_canvas(args.input_file.read())

    if len(canvas_json) != 1:
        raise ProtocolError("multiple entries in canvas_json")
    canvas_json = canvas_json[0]

    parsed_paths = get_paths_from_canvas(canvas_json)

    stroke_to_tool = dict(args.map)
    stroke_stats = defaultdict(int)

    for stroke, _ in parsed_paths:
        stroke_stats[stroke] += 1

    print(f"Found {len(parsed_paths)} paths:")
    for stroke, path_count in sorted(stroke_stats.items()):
        tool = stroke_to_tool.get(stroke)
        if tool is not None:
            mapped = f"mapped to {tool.name}"
        else:
            mapped = "not mapped to any tool"

        print(f" - {path_count} paths with stroke color {stroke}, {mapped}")

    mat = PlanMat(width=args.mat_size[0], height=args.mat_size[1])
    material = PlanMaterial(
        width=args.material_size[0],
        height=args.material_size[1],
        cricut_api_global_id=args.material,
    )

    paths = []
    for stroke, path in parsed_paths:
        tool = stroke_to_tool.get(stroke)
        if tool is None:
            continue

        paths.append(
            PlanPath(
                tool=tool,
                path=path,
                color=stroke if tool.name == "pen" else None,
            )
        )

    plan = Plan(
        mat=mat,
        material=material,
        paths=paths,
    )

    json.dump(plan.to_json(), args.output_file, indent=4)
