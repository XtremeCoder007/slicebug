import base64
import hashlib
import json
import os.path
import re
import shutil
from collections import defaultdict

from slicebug.config.keys import Keys
from slicebug.config.machine_profile import MachineProfile, MachineProfiles
from slicebug.exceptions import UserError


def bootstrap_register_args(subparsers):
    parser = subparsers.add_parser(
        "bootstrap",
        help="Prepare slicebug for use by copying required information from Cricut Design Space.",
    )
    parser.add_argument(
        "--design-space-path",
        help="Path to where Cricut Design Space is installed. Defaults to %(default)s, you likely don't need to change this.",
        default=os.path.expanduser("~/AppData/Local/Programs/Cricut Design Space"),
    )
    parser.add_argument(
        "--design-space-profile-path",
        help="Path to where Cricut Design Space stores your user data. Defaults to %(default)s, you likely don't need to change this.",
        default=os.path.expanduser("~/.cricut-design-space"),
    )

    parser.set_defaults(cmd_handler=bootstrap)
    parser.set_defaults(cmd_needs_profile=False)
    parser.set_defaults(cmd_needs_keys=False)


def import_keys(cds_root, cds_profile_root, cds_user, config):
    xor = lambda data, key: bytes(v ^ key[i % len(key)] for i, v in enumerate(data))

    print("Locating obfuscation key.")
    with open(os.path.join(cds_root, "resources", "app.asar"), "rb") as f:
        asar = f.read()
        # this matches ([0x01, 0x02, ...]) with exactly 64 elements.
        obfuscation_key_pattern = (
            rb"""\(\[((?:0x[0-9a-f]{1,2},){63}(?:0x[0-9a-f]{1,2}))\]\)"""
        )
        matches = list(re.finditer(obfuscation_key_pattern, asar))
        assert len(matches) == 1
        obfuscation_key = bytes(
            int(x, 16) for x in matches[0].group(1).decode().split(",")
        )

    user_settings_path = os.path.join(
        cds_profile_root, "LocalData", cds_user, "UserSessionData", "UserSettings"
    )
    print(f"Importing keys from {user_settings_path}.")

    with open(user_settings_path) as f:
        user_settings = json.load(f)

    settings3_sha512 = hashlib.sha512(user_settings["settings3"].encode()).digest()
    settings2 = xor(
        base64.b64decode(user_settings["settings2"].encode()), settings3_sha512
    )
    cricutdevice_request_key_b64 = xor(settings2, obfuscation_key)
    cricutdevice_request_key = base64.b64decode(cricutdevice_request_key_b64)

    settings8_raw = xor(
        base64.b64decode(user_settings["settings8"].encode()), settings3_sha512
    ).decode()

    keys = Keys(
        cricutdevice_request_key=cricutdevice_request_key,
        settings8_raw=settings8_raw,
    )

    keys.save(config.config_root)
    print("Keys imported.")
    print()


def import_plugins(cds_root, config):
    plugin_dir = os.path.join(cds_root, "resources", "plugins")
    print(f"Importing plugins from {cds_root}.")

    for plugin in ["device-common", "crigeo-cli"]:
        print(f"Importing plugin {plugin}.")
        shutil.copytree(
            os.path.join(plugin_dir, plugin),
            os.path.join(config.plugin_root(), plugin),
            dirs_exist_ok=True,
        )

    print("Plugins imported.")
    print()


def import_machine_profiles(cds_profile_root, cds_users, config):
    # TODO: make this more user-friendly for the case where the same serial appears for multiple users?
    machines_found = []
    for user in cds_users:
        machines_found.extend(
            (subdir.name, subdir.path)
            for subdir in os.scandir(
                os.path.join(cds_profile_root, "LocalData", user, "MaterialSettings")
            )
            if subdir.is_dir()
        )

    if len(machines_found) == 0:
        print("No machine profiles found.")
        print(
            "You will not be able to execute cuts with slicebug without a machine profile."
        )
        print(
            "Make sure that you have logged into Cricut Design Space and made at least one cut there, then run this again."
        )
        profiles_to_import = {}
    elif len(machines_found) == 1:
        print(
            f"Found one machine {machines_found[0][0]}. Importing and setting it as default."
        )
        profiles_to_import = {"default": machines_found[0]}
    else:
        found_serials = [serial for serial, _ in machines_found]
        print(f"Found multiple machines: {found_serials}.")
        print("We will now ask you to set a name for each one.")
        print(
            "When cutting, you will need to provide the name of the profile for the machine you want to use."
        )
        print(
            "For example, if you name your machine 'maker', you will need to supply `--profile maker` on the command line."
        )
        print(
            "If you name a machine 'default', it will be used by default when multiple machines are found."
        )
        print("If you name a machine '-', it will not be imported.")
        print()

        profiles_to_import = {}
        for serial, path in machines_found:
            name = input(f"Name for {serial}: ")
            if (name == "-") or (name == ""):
                continue
            profiles_to_import[name] = (serial, path)

    profiles_root = MachineProfiles.profiles_root(config.config_root)
    machine_profiles = MachineProfiles(profiles={})

    for name, (serial, path) in profiles_to_import.items():
        print(f"Importing machine {serial}.")
        profile_root = os.path.join(profiles_root, serial)
        os.makedirs(profile_root, exist_ok=True)

        profile = MachineProfile(serial=serial, profile_root=profile_root)

        shutil.copyfile(
            os.path.join(path, "MaterialSettings"),
            profile.material_settings_path(),
        )

        machine_profiles.profiles[name] = profile

    machine_profiles.save(config.config_root)
    print("Machines imported.")


def bootstrap(args, config):
    config.create_dirs()

    if not os.path.isdir(args.design_space_path):
        raise UserError(
            f"Cricut Design Space not found at {args.design_space_path}.",
            "Ensure that CDS is installed. If needed, specify a different path using --design-space-path.",
        )

    if not os.path.isdir(args.design_space_profile_path):
        raise UserError(
            f"Cricut Design Space profile not found at {args.design_space_profile_path}.",
            "Ensure that CDS is installed and has been used to make at least one cut. "
            "If needed, specify a different path using --design-space-profile-path.",
        )

    cds_users = [
        subdir.name
        for subdir in os.scandir(
            os.path.join(args.design_space_profile_path, "LocalData")
        )
        if subdir.is_dir()
    ]

    if len(cds_users) == 0:
        raise UserError(
            f"No user data found in the CDS profile.",
            "Ensure that CDS has been used to make at least one cut.",
        )

    import_plugins(args.design_space_path, config)
    import_keys(
        args.design_space_path, args.design_space_profile_path, cds_users[0], config
    )
    import_machine_profiles(args.design_space_profile_path, cds_users, config)
