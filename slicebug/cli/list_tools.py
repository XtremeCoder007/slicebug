from collections import defaultdict

from slicebug.cricut.material_settings import MaterialSettings
from slicebug.cricut.tools import TOOLS
from slicebug.exceptions import UserError


def list_tools_register_args(subparsers):
    parser = subparsers.add_parser("list-tools")
    parser.add_argument("material", type=int)

    parser.set_defaults(cmd_handler=list_tools)
    parser.set_defaults(cmd_needs_profile=True)
    parser.set_defaults(cmd_needs_keys=False)


def list_tools(args, config):
    material_settings = MaterialSettings.load(config.profile.material_settings_path())
    materials = material_settings.materials

    if args.material not in materials:
        raise UserError(
            f"Material with ID {args.material} does not exist.",
            "Try `slicebug list-materials` to view a list of supported materials and their IDs.",
        )

    material = materials[args.material]

    print(f"Tools for {material.name}:")

    for tool in TOOLS:
        if tool.cricut_api_name not in material.tools:
            continue

        print(f" - {tool.name}")
