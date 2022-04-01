from collections import defaultdict


def group_and_order_paths(plan):
    paths_by_tool = defaultdict(list)

    for path in plan.paths:
        paths_by_tool[path.tool.name].append(path)

    paths_grouped = []
    for paths in paths_by_tool.values():
        paths_grouped.append((paths[0].tool, paths))

    paths_grouped.sort(key=lambda p: p[0].order)

    for (tool, _), (next_tool, _) in zip(paths_grouped, paths_grouped[1:]):
        if tool.cricut_pb_art_type == next_tool.cricut_pb_art_type:
            raise ValueError(
                f"tools {tool.name} and {next_tool.name} cannot be used in the same plan"
            )

    return paths_grouped


def first_tool_in_group(paths_grouped, head_type):
    for tool, _ in paths_grouped:
        if tool.head_type == head_type:
            return tool
    return None


def first_pen_path_in_group(paths_grouped):
    for tool, paths in paths_grouped:
        if tool.name == "pen":
            return paths[0]
    return None
