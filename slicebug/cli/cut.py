import argparse


def cut_register_args(subparsers):
    parser = subparsers.add_parser("cut")
    parser.add_argument("plan", type=argparse.FileType("r"))

    parser.set_defaults(cmd_handler=cut)
    parser.set_defaults(cmd_needs_profile=True)
    parser.set_defaults(cmd_needs_keys=True)


def cut(args, config):
    print("hi from cut. plan is", args.plan, config.profile_name)
