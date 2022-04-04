from collections import defaultdict

from slicebug.cricut.material_settings import MaterialSettings


def list_materials_register_args(subparsers):
    parser = subparsers.add_parser(
        "list-materials", help="List materials that can be cut and their IDs."
    )

    parser.set_defaults(cmd_handler=list_materials)
    parser.set_defaults(cmd_needs_profile=True)
    parser.set_defaults(cmd_needs_keys=False)


def list_materials(args, config):
    material_settings = MaterialSettings.load(config.profile.material_settings_path())
    materials = material_settings.materials

    categories = defaultdict(list)
    for material in materials.values():
        categories[material.category].append(material)

    for category_name, category in sorted(categories.items()):
        print(f"{category_name}:")

        for material in sorted(category, key=lambda m: m.name):
            print(f"  - [{material.global_id:3}] {material.name}")

        print()
