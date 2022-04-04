import argparse
import json

from slicebug.cricut.device_plugin import DevicePlugin
from slicebug.cricut.material_settings import MaterialSettings
from slicebug.cricut.protobufs.NativeModel_pb2 import (
    PBAnalyticMachineSummary,
    PBSize,
    PBUserSettings,
)
from slicebug.cricut.protobufs.Bridge_pb2 import (
    PBBridgeSelectedTools,
    PBCommonBridge,
    PBInteractionHandle,
    PBInteractionStatus,
    PBMaterialSelected,
    PBMatPathData,
    PBToolInfo,
)
from slicebug.exceptions import ProtocolError, UserError
from slicebug.plan.plan import Plan
from slicebug.cricut.tools import HeadType, TOOLS_BY_PB_TOOL_TYPE
from slicebug.plan.group_paths import (
    first_pen_path_in_group,
    first_tool_in_group,
    group_and_order_paths,
)


def cut_register_args(subparsers):
    parser = subparsers.add_parser("cut", help="Execute a planned cut.")
    parser.add_argument(
        "plan", type=argparse.FileType("r"), help="Path to your plan file."
    )

    parser.set_defaults(cmd_handler=cut)
    parser.set_defaults(cmd_needs_profile=True)
    parser.set_defaults(cmd_needs_keys=True)


def plan_tool_info(config, material, grouped_paths):
    tools = []

    for tool, _ in grouped_paths:
        tools.append(
            PBToolInfo(
                tool=tool.cricut_pb_tool_type,
                line=tool.cricut_pb_art_type,
                toolFromApi=material.tools[tool.cricut_api_name].pb_tool,
            )
        )

    selected_tools = PBBridgeSelectedTools(tools=tools)

    first_pen_path = first_pen_path_in_group(grouped_paths)
    if first_pen_path is not None:
        selected_tools.firstPen = first_pen_path.color

    return selected_tools


def plan_mat_path_data(config, plan, grouped_paths):
    paths = []

    for tool, tool_paths in grouped_paths:
        for path in tool_paths:
            path_pb = PBMatPathData(
                fiducialId=-1,
                pathData=path.path,
                actualPathType=tool.cricut_pb_art_type,
            )

            if path.color is not None:
                path_pb.pathColor = path.color

            paths.append(path_pb)

    return PBMatPathData(
        materialSize=PBSize(
            height=plan.material.height,
            width=plan.material.width,
        ),
        imageData=paths,
    )


def cut_inner(config, dev, plan):
    grouped_paths = group_and_order_paths(plan)

    material_settings = MaterialSettings.load(config.profile.material_settings_path())

    if plan.material.cricut_api_global_id not in material_settings.materials:
        raise UserError(
            f"Material with ID {plan.material.cricut_api_global_id} does not exist.",
            "Try `slicebug list-materials` to view a list of supported materials and their IDs, then modify the plan to use a supported material.",
        )

    material = material_settings.materials[plan.material.cricut_api_global_id]

    dev.send(
        PBCommonBridge(
            interaction=PBInteractionStatus.riMATCUT,
            authData=PBUserSettings(settings8=config.keys.settings8_raw),
        )
    )

    dev.recv(PBInteractionStatus.riStartSuccess)

    device_connected_resp = dev.recv()
    match device_connected_resp.status:
        case PBInteractionStatus.riSingleDeviceConnected:
            # great, this is what we're looking for
            pass
        case PBInteractionStatus.riNoDeviceConnected:
            raise UserError(
                "No Cricut devices connected.",
                "Connect your cutter to your computer and try again.",
            )
        case PBInteractionStatus.riMultipleDevicesConnected:
            raise UserError(
                "Multiple Cricut devices connected.",
                "Disconnect all cutters except for the one you are trying to use and try again.",
            )
        case _:
            raise ProtocolError(
                f"unexpected status after start success: {device_connected_resp.status}"
            )

    dev.send(
        PBCommonBridge(
            handle=PBInteractionHandle(currentInteraction=999),
            status=PBInteractionStatus.riSelectDevice,
            device=device_connected_resp.device,
        )
    )

    dev.recv(PBInteractionStatus.riOpeningDevice)
    machine_summary_resp = dev.recv(
        PBInteractionStatus.riOPENDEVICEGetAnalyticMachineSummary
    )
    serial = machine_summary_resp.device.serial

    if serial != config.profile.serial:
        raise UserError(
            f"Serial of connected device ({serial}) does not match profile ({config.profile.serial}).",
            "Connect the correct device or switch to a different profile with --profile.",
        )

    dev.send(
        PBCommonBridge(
            handle=PBInteractionHandle(currentInteraction=999),
            status=PBInteractionStatus.riOPENDEVICESetAnalyticMachineSummary,
            deviceAnalyticMachineSummary=PBAnalyticMachineSummary(
                firmwareValuesStored="valuesStored",
                primaryUserSet=True,
            ),
        )
    )

    dev.recv(PBInteractionStatus.riDeviceOpenSuccess)
    dev.recv(PBInteractionStatus.riDialChanged)
    dev.recv(PBInteractionStatus.riWaitingOnMaterialSelected)

    dev.send(
        PBCommonBridge(
            handle=PBInteractionHandle(currentInteraction=999),
            status=PBInteractionStatus.riMaterialSelected,
            materialSelectedPayload=PBMaterialSelected(
                selected=True,
                matHeight=plan.mat.height,
                matWidth=plan.mat.width,
            ),
        )
    )

    print("Load the following tools:")
    for head_type in [HeadType.A, HeadType.B]:
        first_tool = first_tool_in_group(grouped_paths, head_type)

        if first_tool is None:
            tool_description = "(nothing)"
        elif first_tool.name == "pen":
            color = first_pen_path_in_group(grouped_paths).color
            tool_description = f"pen ({color})"
        else:
            tool_description = first_tool.name

        print(f"Clamp {head_type.name}: {tool_description}")
    print()

    resp = dev.recv()
    match resp.status:
        case PBInteractionStatus.riWaitOnMatLoad:
            print("Insert mat and press the Load/Unload button.")
            dev.recv(PBInteractionStatus.riMatLoaded)
        case PBInteractionStatus.riMatLoaded:
            print("Mat is already loaded.")
        case _:
            raise ProtocolError(
                f"unexpected status after material selected: {resp.status}"
            )

    dev.recv(PBInteractionStatus.riWaitClear)

    dev.recv(PBInteractionStatus.riWaitOnGo)
    print("Press the Go button.")

    dev.recv(PBInteractionStatus.riGoPressed)
    dev.recv(PBInteractionStatus.riGoPressed)
    dev.recv(PBInteractionStatus.riWaitClear)

    dev.recv(PBInteractionStatus.riSendToolArray)

    dev.send(
        PBCommonBridge(
            handle=PBInteractionHandle(currentInteraction=999),
            status=PBInteractionStatus.riToolInfoReceived,
            toolInfo=plan_tool_info(config, material, grouped_paths),
        )
    )

    dev.recv(PBInteractionStatus.riMATCUTNeedPathData)

    dev.send(
        PBCommonBridge(
            handle=PBInteractionHandle(currentInteraction=999),
            status=PBInteractionStatus.riMATCUTSetPathData,
            matPathData=plan_mat_path_data(config, plan, grouped_paths),
        )
    )

    dev.recv(PBInteractionStatus.riMATCUTProcessingPathData)
    dev.recv(PBInteractionStatus.riMATCUTProcessingPathDataComplete)

    while (resp := dev.recv()).status != PBInteractionStatus.riMATCUTCompleteSuccess:
        match resp.status:
            case PBInteractionStatus.riMATCUTNeedAccessoryChange:
                tool_names = []
                for tool in [resp.accessoryV2.current, resp.accessoryV2.required]:
                    tool_type = TOOLS_BY_PB_TOOL_TYPE[tool.toolType]
                    tool_name = tool_type.name
                    if tool_type.name == "pen":
                        tool_name = f"{tool_type.name} ({tool.color})"
                    tool_names.append(tool_name)

                current, required = tool_names
                print(f"Replace the {current} with {required} and press Go.")

                dev.recv(PBInteractionStatus.riWaitOnGo)
                dev.recv(PBInteractionStatus.riGoPressed)
                dev.recv(PBInteractionStatus.riWaitClear)
            case PBInteractionStatus.riDevicePaused:
                dev.recv(PBInteractionStatus.riWaitOnGoOrPause)
                print("Cutting paused. Press Go to resume or Load/Unload to abort cut.")

                choice = dev.recv()
                if choice.status == PBInteractionStatus.riMatUnloaded:
                    print("Cutting aborted.")
                    return
                elif choice.status == PBInteractionStatus.riPausePressed:
                    print("Cutting resumed.")
                    dev.recv(PBInteractionStatus.riWaitClear)
                    dev.recv(PBInteractionStatus.riDeviceResumed)
                else:
                    raise ProtocolError(
                        f"unexpected status after pause: {choice.status}"
                    )
            case PBInteractionStatus.riMATCUTReportTool:
                current_tool = TOOLS_BY_PB_TOOL_TYPE[resp.accessoryV2.current.toolType]
                required_tool = TOOLS_BY_PB_TOOL_TYPE[
                    resp.accessoryV2.required.toolType
                ]
                # TODO: actually implement this properly. The difficulty is
                # that the plugin follows this with riSendToolArray and
                # expects you to send tool info again.
                raise UserError(
                    f"Tool error: expected {required_tool.name}, got {current_tool.name}.",
                    "Sorry, we don't currently support recovering from this, you'll have to restart the whole cut.",
                )
            case (
                PBInteractionStatus.riMATCUTGettingDevicePressureSettings
                | PBInteractionStatus.riMATCUTAccessoryChanged
                | PBInteractionStatus.riDetectingTool
                | PBInteractionStatus.riMATCUTSetProgress
                | PBInteractionStatus.riWaitForEndMoveProgress
            ):
                pass
            case _:
                raise ProtocolError(f"unexpected status in cut loop: {resp.status}")

    print("Cutting finished.")

    dev.recv(PBInteractionStatus.riWaitOnMatUnload)
    print("Press the Load/Unload button to unload mat.")

    dev.recv(PBInteractionStatus.riMatUnloaded)
    dev.recv(PBInteractionStatus.riMatUnloaded)
    dev.recv(PBInteractionStatus.riNeedRestartInteractionConfirmation)

    # TODO:
    # status: riComplete
    # status: riCloseInteractionSuccess


def cut(args, config):
    if config.device_plugin_path() is None:
        raise UserError(
            "Device plugin is missing.", "Try running `slicebug bootstrap`."
        )

    plan = Plan.from_json(json.load(args.plan))

    with DevicePlugin(
        config.device_plugin_path(), config.keys.cricutdevice_request_key
    ) as dev:
        cut_inner(config, dev, plan)
