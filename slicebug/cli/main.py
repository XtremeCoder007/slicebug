import argparse
import os.path
import sys
import traceback

from slicebug.cli.bootstrap import bootstrap_register_args
from slicebug.cli.cut import cut_register_args
from slicebug.cli.list_materials import list_materials_register_args
from slicebug.cli.list_tools import list_tools_register_args
from slicebug.cli.plan import plan_register_args
from slicebug.config.config import Config
from slicebug.exceptions import UserError
from slicebug.version import VERSION

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--profile", help="pick a machine profile to use")

    subparsers = parser.add_subparsers()

    bootstrap_register_args(subparsers)
    list_materials_register_args(subparsers)
    list_tools_register_args(subparsers)
    plan_register_args(subparsers)
    cut_register_args(subparsers)

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
    except Exception as err:
        traceback.print_exception(err)
        print("", file=sys.stderr)
        print("An unexpected error has occurred!", file=sys.stderr)
        print(
            "This might be a bug in slicebug or unexpected Cricut behavior.",
            file=sys.stderr,
        )
        print(
            "Try again. If the error persists, send a copy or screenshot of this "
            "error message (including the details above) to slicebug developers.",
            file=sys.stderr,
        )
        sys.exit(1)
