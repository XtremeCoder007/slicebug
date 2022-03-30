import argparse
import os.path
import sys

from slicebug.cli.cut import cut_register_args
from slicebug.cli.list_materials import list_materials_register_args
from slicebug.cli.list_tools import list_tools_register_args
from slicebug.config.config import Config


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
    sys.exit(1)

config_root = os.path.expanduser("~/.slicebug")
config = Config.load(config_root, args.profile)

if args.cmd_needs_profile and config.profile is None:
    print("need profile! run bootstrap")
    sys.exit(1)

if args.cmd_needs_keys and config.keys is None:
    print("need keys! run bootstrap")
    sys.exit(1)

args.cmd_handler(args, config)
