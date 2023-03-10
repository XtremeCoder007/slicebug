# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: slicebug/cricut/protobufs/Bridge.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from slicebug.cricut.protobufs import NativeModel_pb2 as slicebug_dot_cricut_dot_protobufs_dot_NativeModel__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&slicebug/cricut/protobufs/Bridge.proto\x1a+slicebug/cricut/protobufs/NativeModel.proto\"G\n\x13PBInteractionHandle\x12\x30\n\x12\x63urrentInteraction\x18\x04 \x01(\x0e\x32\x14.PBInteractionStatus\"\xc6\x01\n\x18PBCricutDeviceSerialized\x12\x12\n\ndeviceType\x18\x05 \x01(\t\x12\x0c\n\x04port\x18\x08 \x01(\x05\x12)\n\x0e\x63onnectionType\x18\x15 \x01(\x0e\x32\x11.PBConnectionType\x12&\n\x0e\x64\x65viceTypeEnum\x18\x19 \x01(\x0e\x32\x0e.PBMachineType\x12\x0b\n\x03key\x18\x1b \x01(\t\x12\x18\n\x10supportsFastMode\x18+ \x01(\x08\x12\x0e\n\x06serial\x18\n \x01(\t\"_\n\nPBToolInfo\x12\x19\n\x04tool\x18\x01 \x01(\x0e\x32\x0b.PBToolType\x12\x18\n\x04line\x18\x02 \x01(\x0e\x32\n.PBArtType\x12\x1c\n\x0btoolFromApi\x18\x04 \x01(\x0b\x32\x07.PBTool\"E\n\x15PBBridgeSelectedTools\x12\x10\n\x08\x66irstPen\x18\x01 \x01(\t\x12\x1a\n\x05tools\x18\x04 \x03(\x0b\x32\x0b.PBToolInfo\"\xaa\x01\n\x11PBMatFiducialData\x12\x12\n\nfiducialId\x18\x01 \x01(\x05\x12\x1a\n\x08location\x18\x02 \x01(\x0b\x32\x08.PBPoint\x12\x1a\n\timageSize\x18\x03 \x01(\x0b\x32\x07.PBSize\x12\x1d\n\x0c\x66iducialSize\x18\x04 \x01(\x0b\x32\x07.PBSize\x12\x11\n\tlineWidth\x18\x05 \x01(\x01\x12\x17\n\x0f\x66iducialPadding\x18\x06 \x01(\x01\"\xf4\x01\n\rPBMatPathData\x12\x12\n\nfiducialId\x18\x01 \x01(\x05\x12\x10\n\x08pathData\x18\x02 \x01(\t\x12\"\n\x0e\x61\x63tualPathType\x18\x0e \x01(\x0e\x32\n.PBArtType\x12\x11\n\tpathColor\x18\x04 \x01(\t\x12\x1a\n\x12\x63ontourActiveFlags\x18\x15 \x03(\r\x12!\n\timageData\x18\n \x03(\x0b\x32\x0e.PBMatPathData\x12\x1d\n\x0cmaterialSize\x18\x0b \x01(\x0b\x32\x07.PBSize\x12(\n\x0c\x66iducialData\x18\x0c \x03(\x0b\x32\x12.PBMatFiducialData\"K\n\x12PBMaterialSelected\x12\x10\n\x08selected\x18\x01 \x01(\x08\x12\x11\n\tmatHeight\x18\x02 \x01(\x01\x12\x10\n\x08matWidth\x18\x0c \x01(\x01\"\xc0\x03\n\x0ePBCommonBridge\x12$\n\x06handle\x18\x02 \x01(\x0b\x32\x14.PBInteractionHandle\x12)\n\x0binteraction\x18\x03 \x01(\x0e\x32\x14.PBInteractionStatus\x12$\n\x06status\x18\x06 \x01(\x0e\x32\x14.PBInteractionStatus\x12)\n\x06\x64\x65vice\x18\t \x01(\x0b\x32\x19.PBCricutDeviceSerialized\x12(\n\x08toolInfo\x18\x0e \x01(\x0b\x32\x16.PBBridgeSelectedTools\x12!\n\x08\x61uthData\x18\x11 \x01(\x0b\x32\x0f.PBUserSettings\x12#\n\x0bmatPathData\x18\x16 \x01(\x0b\x32\x0e.PBMatPathData\x12?\n\x1c\x64\x65viceAnalyticMachineSummary\x18O \x01(\x0b\x32\x19.PBAnalyticMachineSummary\x12\x34\n\x17materialSelectedPayload\x18o \x01(\x0b\x32\x13.PBMaterialSelected\x12#\n\x0b\x61\x63\x63\x65ssoryV2\x18\x7f \x01(\x0b\x32\x0e.PBAccessoryV2\"\xae\x02\n\rPBAccessoryV2\x12\x30\n\x07\x63urrent\x18\x01 \x01(\x0b\x32\x1f.PBAccessoryV2.PBAccessoryState\x12\x31\n\x08required\x18\x02 \x01(\x0b\x32\x1f.PBAccessoryV2.PBAccessoryState\x12\x1a\n\x12requiresToolChange\x18\x03 \x01(\x08\x12\x1d\n\x15requiresPartialUnload\x18\x04 \x01(\x08\x1a}\n\x10PBAccessoryState\x12\x1d\n\x08toolType\x18\x01 \x01(\x0e\x32\x0b.PBToolType\x12\x1c\n\x08pathType\x18\x02 \x01(\x0e\x32\n.PBArtType\x12\r\n\x05\x63olor\x18\x03 \x01(\t\x12\x1d\n\x08headType\x18\x04 \x01(\x0e\x32\x0b.PBHeadType*\xf2\r\n\x13PBInteractionStatus\x12\x0b\n\x07riError\x10\x00\x12\x0e\n\nriComplete\x10\x01\x12\x12\n\x0eriStartSuccess\x10\x02\x12\x16\n\x12riCloseInteraction\x10\x03\x12\n\n\x06riPing\x10\x04\x12\x0f\n\x0briPingReply\x10\x05\x12\x1d\n\x19riCloseInteractionSuccess\x10\x06\x12\x17\n\x13riNoDeviceConnected\x10\x65\x12\x1e\n\x1ariMultipleDevicesConnected\x10\x66\x12\x1b\n\x17riSingleDeviceConnected\x10g\x12\x13\n\x0friOpeningDevice\x10h\x12\x17\n\x13riDeviceOpenSuccess\x10i\x12\x14\n\x10riDeviceOpenFail\x10j\x12\x18\n\x14riDeviceCloseSuccess\x10k\x12\x15\n\x11riDeviceCloseFail\x10l\x12\x12\n\x0eriSelectDevice\x10m\x12\x13\n\x0friWaitOnMatLoad\x10n\x12\x0f\n\x0briMatLoaded\x10o\x12\x11\n\rriMatUnloaded\x10p\x12\x15\n\x11riWaitOnMatUnload\x10q\x12\x11\n\rriDialChanged\x10r\x12\x0e\n\nriWaitOnGo\x10s\x12\x15\n\x11riWaitOnGoOrPause\x10t\x12\x0f\n\x0briGoPressed\x10u\x12\x12\n\x0eriPausePressed\x10v\x12\x17\n\x13riFiducialSearching\x10w\x12\x13\n\x0friFiducialFound\x10x\x12\x16\n\x12riFiducialNotFound\x10y\x12\x12\n\x0eriDevicePaused\x10z\x12\x13\n\x0friDeviceResumed\x10{\x12\x0f\n\x0briWaitClear\x10|\x12)\n$riNeedRestartInteractionConfirmation\x10\x81\x01\x12(\n#riSetRestartInteractionConfirmation\x10\x82\x01\x12 \n\x1briWaitingOnMaterialSelected\x10\x85\x01\x12\x17\n\x12riMaterialSelected\x10\x86\x01\x12\x14\n\x0friSendToolArray\x10\x87\x01\x12\x17\n\x12riToolInfoReceived\x10\x88\x01\x12\x14\n\x0friDetectingTool\x10\x89\x01\x12\x1d\n\x18riWaitForEndMoveProgress\x10\x9e\x01\x12\x1b\n\x16riFiducialEdgeScanning\x10\xa2\x01\x12\x1a\n\x15riFiducialEdgeScanned\x10\xa3\x01\x12!\n\x1criFiducialEdgeScanningFailed\x10\xa4\x01\x12\r\n\x08riMATCUT\x10\xbc\x05\x12\x19\n\x14riMATCUTNeedPathData\x10\xbd\x05\x12\x18\n\x13riMATCUTSetPathData\x10\xbf\x05\x12\x1f\n\x1ariMATCUTProcessingPathData\x10\xc0\x05\x12\'\n\"riMATCUTProcessingPathDataComplete\x10\xc1\x05\x12 \n\x1briMATCUTNeedAccessoryChange\x10\xc2\x05\x12\x1d\n\x18riMATCUTAccessoryChanged\x10\xc3\x05\x12\x18\n\x13riMATCUTSetProgress\x10\xc6\x05\x12\x17\n\x12riMATCUTReportTool\x10\xcb\x05\x12\x1a\n\x15riMATCUTReportToolAck\x10\xcc\x05\x12\x15\n\x10riMATCUTAbortCut\x10\xcd\x05\x12\x1c\n\x17riMATCUTPresentCarriage\x10\xce\x05\x12&\n!riMATCUTSimulateLoadButtonPressed\x10\xcf\x05\x12(\n#riMATCUTSimulateCricutButtonPressed\x10\xd0\x05\x12\'\n\"riMATCUTSimulatePauseButtonPressed\x10\xd1\x05\x12\x1d\n\x18riMATCUTSetExecutionPlan\x10\xd2\x05\x12\x1d\n\x18riMATCUTGetExecutionPlan\x10\xd3\x05\x12\x12\n\rriMATCUTUseV1\x10\xd4\x05\x12\x12\n\rriMATCUTUseV2\x10\xd5\x05\x12*\n%riMATCUTGettingDevicePressureSettings\x10\xd6\x05\x12\x1c\n\x17riMATCUTCompleteSuccess\x10\xd7\x05\x12\"\n\x1driMATCUTThetaBacklashProgress\x10\xd8\x05\x12*\n%riOPENDEVICEGetAnalyticMachineSummary\x10\xb7\t\x12*\n%riOPENDEVICESetAnalyticMachineSummary\x10\xb8\t*X\n\x10PBConnectionType\x12\x0e\n\nUNKNOWN_CT\x10\x00\x12\x10\n\x0c\x42LUETOOTH_CT\x10\x01\x12\n\n\x06USB_CT\x10\x02\x12\n\n\x06HID_CT\x10\x03\x12\n\n\x06\x42LE_CT\x10\x04\x62\x06proto3')

_PBINTERACTIONSTATUS = DESCRIPTOR.enum_types_by_name['PBInteractionStatus']
PBInteractionStatus = enum_type_wrapper.EnumTypeWrapper(_PBINTERACTIONSTATUS)
_PBCONNECTIONTYPE = DESCRIPTOR.enum_types_by_name['PBConnectionType']
PBConnectionType = enum_type_wrapper.EnumTypeWrapper(_PBCONNECTIONTYPE)
riError = 0
riComplete = 1
riStartSuccess = 2
riCloseInteraction = 3
riPing = 4
riPingReply = 5
riCloseInteractionSuccess = 6
riNoDeviceConnected = 101
riMultipleDevicesConnected = 102
riSingleDeviceConnected = 103
riOpeningDevice = 104
riDeviceOpenSuccess = 105
riDeviceOpenFail = 106
riDeviceCloseSuccess = 107
riDeviceCloseFail = 108
riSelectDevice = 109
riWaitOnMatLoad = 110
riMatLoaded = 111
riMatUnloaded = 112
riWaitOnMatUnload = 113
riDialChanged = 114
riWaitOnGo = 115
riWaitOnGoOrPause = 116
riGoPressed = 117
riPausePressed = 118
riFiducialSearching = 119
riFiducialFound = 120
riFiducialNotFound = 121
riDevicePaused = 122
riDeviceResumed = 123
riWaitClear = 124
riNeedRestartInteractionConfirmation = 129
riSetRestartInteractionConfirmation = 130
riWaitingOnMaterialSelected = 133
riMaterialSelected = 134
riSendToolArray = 135
riToolInfoReceived = 136
riDetectingTool = 137
riWaitForEndMoveProgress = 158
riFiducialEdgeScanning = 162
riFiducialEdgeScanned = 163
riFiducialEdgeScanningFailed = 164
riMATCUT = 700
riMATCUTNeedPathData = 701
riMATCUTSetPathData = 703
riMATCUTProcessingPathData = 704
riMATCUTProcessingPathDataComplete = 705
riMATCUTNeedAccessoryChange = 706
riMATCUTAccessoryChanged = 707
riMATCUTSetProgress = 710
riMATCUTReportTool = 715
riMATCUTReportToolAck = 716
riMATCUTAbortCut = 717
riMATCUTPresentCarriage = 718
riMATCUTSimulateLoadButtonPressed = 719
riMATCUTSimulateCricutButtonPressed = 720
riMATCUTSimulatePauseButtonPressed = 721
riMATCUTSetExecutionPlan = 722
riMATCUTGetExecutionPlan = 723
riMATCUTUseV1 = 724
riMATCUTUseV2 = 725
riMATCUTGettingDevicePressureSettings = 726
riMATCUTCompleteSuccess = 727
riMATCUTThetaBacklashProgress = 728
riOPENDEVICEGetAnalyticMachineSummary = 1207
riOPENDEVICESetAnalyticMachineSummary = 1208
UNKNOWN_CT = 0
BLUETOOTH_CT = 1
USB_CT = 2
HID_CT = 3
BLE_CT = 4


_PBINTERACTIONHANDLE = DESCRIPTOR.message_types_by_name['PBInteractionHandle']
_PBCRICUTDEVICESERIALIZED = DESCRIPTOR.message_types_by_name['PBCricutDeviceSerialized']
_PBTOOLINFO = DESCRIPTOR.message_types_by_name['PBToolInfo']
_PBBRIDGESELECTEDTOOLS = DESCRIPTOR.message_types_by_name['PBBridgeSelectedTools']
_PBMATFIDUCIALDATA = DESCRIPTOR.message_types_by_name['PBMatFiducialData']
_PBMATPATHDATA = DESCRIPTOR.message_types_by_name['PBMatPathData']
_PBMATERIALSELECTED = DESCRIPTOR.message_types_by_name['PBMaterialSelected']
_PBCOMMONBRIDGE = DESCRIPTOR.message_types_by_name['PBCommonBridge']
_PBACCESSORYV2 = DESCRIPTOR.message_types_by_name['PBAccessoryV2']
_PBACCESSORYV2_PBACCESSORYSTATE = _PBACCESSORYV2.nested_types_by_name['PBAccessoryState']
PBInteractionHandle = _reflection.GeneratedProtocolMessageType('PBInteractionHandle', (_message.Message,), {
  'DESCRIPTOR' : _PBINTERACTIONHANDLE,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBInteractionHandle)
  })
_sym_db.RegisterMessage(PBInteractionHandle)

PBCricutDeviceSerialized = _reflection.GeneratedProtocolMessageType('PBCricutDeviceSerialized', (_message.Message,), {
  'DESCRIPTOR' : _PBCRICUTDEVICESERIALIZED,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBCricutDeviceSerialized)
  })
_sym_db.RegisterMessage(PBCricutDeviceSerialized)

PBToolInfo = _reflection.GeneratedProtocolMessageType('PBToolInfo', (_message.Message,), {
  'DESCRIPTOR' : _PBTOOLINFO,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBToolInfo)
  })
_sym_db.RegisterMessage(PBToolInfo)

PBBridgeSelectedTools = _reflection.GeneratedProtocolMessageType('PBBridgeSelectedTools', (_message.Message,), {
  'DESCRIPTOR' : _PBBRIDGESELECTEDTOOLS,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBBridgeSelectedTools)
  })
_sym_db.RegisterMessage(PBBridgeSelectedTools)

PBMatFiducialData = _reflection.GeneratedProtocolMessageType('PBMatFiducialData', (_message.Message,), {
  'DESCRIPTOR' : _PBMATFIDUCIALDATA,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBMatFiducialData)
  })
_sym_db.RegisterMessage(PBMatFiducialData)

PBMatPathData = _reflection.GeneratedProtocolMessageType('PBMatPathData', (_message.Message,), {
  'DESCRIPTOR' : _PBMATPATHDATA,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBMatPathData)
  })
_sym_db.RegisterMessage(PBMatPathData)

PBMaterialSelected = _reflection.GeneratedProtocolMessageType('PBMaterialSelected', (_message.Message,), {
  'DESCRIPTOR' : _PBMATERIALSELECTED,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBMaterialSelected)
  })
_sym_db.RegisterMessage(PBMaterialSelected)

PBCommonBridge = _reflection.GeneratedProtocolMessageType('PBCommonBridge', (_message.Message,), {
  'DESCRIPTOR' : _PBCOMMONBRIDGE,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBCommonBridge)
  })
_sym_db.RegisterMessage(PBCommonBridge)

PBAccessoryV2 = _reflection.GeneratedProtocolMessageType('PBAccessoryV2', (_message.Message,), {

  'PBAccessoryState' : _reflection.GeneratedProtocolMessageType('PBAccessoryState', (_message.Message,), {
    'DESCRIPTOR' : _PBACCESSORYV2_PBACCESSORYSTATE,
    '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
    # @@protoc_insertion_point(class_scope:PBAccessoryV2.PBAccessoryState)
    })
  ,
  'DESCRIPTOR' : _PBACCESSORYV2,
  '__module__' : 'slicebug.cricut.protobufs.Bridge_pb2'
  # @@protoc_insertion_point(class_scope:PBAccessoryV2)
  })
_sym_db.RegisterMessage(PBAccessoryV2)
_sym_db.RegisterMessage(PBAccessoryV2.PBAccessoryState)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PBINTERACTIONSTATUS._serialized_start=1783
  _PBINTERACTIONSTATUS._serialized_end=3561
  _PBCONNECTIONTYPE._serialized_start=3563
  _PBCONNECTIONTYPE._serialized_end=3651
  _PBINTERACTIONHANDLE._serialized_start=87
  _PBINTERACTIONHANDLE._serialized_end=158
  _PBCRICUTDEVICESERIALIZED._serialized_start=161
  _PBCRICUTDEVICESERIALIZED._serialized_end=359
  _PBTOOLINFO._serialized_start=361
  _PBTOOLINFO._serialized_end=456
  _PBBRIDGESELECTEDTOOLS._serialized_start=458
  _PBBRIDGESELECTEDTOOLS._serialized_end=527
  _PBMATFIDUCIALDATA._serialized_start=530
  _PBMATFIDUCIALDATA._serialized_end=700
  _PBMATPATHDATA._serialized_start=703
  _PBMATPATHDATA._serialized_end=947
  _PBMATERIALSELECTED._serialized_start=949
  _PBMATERIALSELECTED._serialized_end=1024
  _PBCOMMONBRIDGE._serialized_start=1027
  _PBCOMMONBRIDGE._serialized_end=1475
  _PBACCESSORYV2._serialized_start=1478
  _PBACCESSORYV2._serialized_end=1780
  _PBACCESSORYV2_PBACCESSORYSTATE._serialized_start=1655
  _PBACCESSORYV2_PBACCESSORYSTATE._serialized_end=1780
# @@protoc_insertion_point(module_scope)
