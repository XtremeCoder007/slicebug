import argparse
import os.path
import sys

from slicebug.cli.cut import cut_register_args
from slicebug.cli.list_materials import list_materials_register_args
from slicebug.cli.list_tools import list_tools_register_args
from slicebug.config.config import Config
from slicebug.exceptions import UserError

parser = argparse.ArgumentParser()
parser.add_argument("--profile")

subparsers = parser.add_subparsers()

list_materials_register_args(subparsers)
list_tools_register_args(subparsers)
cut_register_args(subparsers)
# plan_register_args(subparsers)
# bootstrap_register_args(subparsers)

args = parser.parse_args()

if "cmd_handler" not in args:
    parser.print_help()
    sys.exit(1)

try:
    config_root = os.path.expanduser("~/.slicebug")
    config = Config.load(config_root, args.profile)

    if args.cmd_needs_profile and config.profile is None:
        raise UserError(
            "A machine profile is required to run this command, but it was not found.",
            "Try running `slicebug bootstrap`.",
        )

    if args.cmd_needs_keys and config.keys is None:
        raise UserError(
            "Keys are required to run this command, but they were not found.",
            "Try running `slicebug bootstrap`.",
        )

    args.cmd_handler(args, config)
except UserError as err:
    message, resolution = err.args
    print(f"Error: {message}", file=sys.stderr)
    if resolution is not None:
        print(resolution, file=sys.stderr)
    sys.exit(1)
