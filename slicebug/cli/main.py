import argparse
import os.path

from slicebug.cli.cut import cut_register_args
from slicebug.cli.list_materials import list_materials_register_args
from slicebug.cli.list_tools import list_tools_register_args
from slicebug.config.config import Config


def main():
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
        print("oops no command")
        return

    config_root = os.path.expanduser("~/.slicebug")
    config = Config.load(config_root, args.profile)

    if args.cmd_needs_profile and config.profile is None:
        print("need profile! run bootstrap")
        return

    if args.cmd_needs_keys and config.keys is None:
        print("need keys! run bootstrap")
        return

    args.cmd_handler(args, config)


if __name__ == "__main__":
    main()
