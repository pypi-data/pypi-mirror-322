import sys
# import math
import grpc
from google.protobuf import json_format
import neuromeka_hri.common as Common

if sys.version_info >= (3, 9):
    from neuromeka.proto import *
else:
    from neuromeka.proto_step import *

class RTDESocketClient:
    """
    gRPC client to RTDE Server in C++ IndyFramework v3.0
    """
    PROG_IDLE = common_msgs.PROG_IDLE
    PROG_RUNNING = common_msgs.PROG_RUNNING
    PROG_PAUSING = common_msgs.PROG_PAUSING
    PROG_STOPPING = common_msgs.PROG_STOPPING
    CTRL_IDLE = common_msgs.OpState.OP_IDLE
    CTRL_VIOLATE = common_msgs.OpState.OP_VIOLATE
    CTRL_MANUAL_RECOVER = common_msgs.OpState.OP_MANUAL_RECOVER
    CTRL_SYSTEM_OFF = common_msgs.OpState.OP_SYSTEM_OFF
    CTRL_BRAKE = common_msgs.OpState.OP_BRAKE_CONTROL

    def __init__(self, ip_addr, port=Common.Config().RTDE_SOCKET_PORT):
        rtde_channel = grpc.insecure_channel("{}:{}".format(ip_addr, port))
        rtde_stub = RTDataExchangeStub(rtde_channel)
        self.__rtde_stub = rtde_stub

    @Common.Utils.exception_handler
    def GetMotionData(self):
        """
        Motion Data:
            traj_state   -> TrajState
            traj_progress   -> int32
            is_in_motion  -> bool
            is_target_reached  -> bool
            is_pausing  -> bool
            is_stopping  -> bool
            has_motion  -> bool
            speed_ratio  -> int32
            motion_id  -> int32
            remain_distance  -> float
            motion_queue_size  -> uint32
            cur_traj_progress  -> int32
            response  -> Response
        """
        response = self.__rtde_stub.GetMotionData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetControlData(self):
        """
        Control Data:
            running_hours   -> uint32
            running_mins   -> uint32
            running_secs  -> uint32
            op_state  -> OpState
            sim_mode  -> bool
            q  -> float[6]
            qdot  -> float[6]
            p  -> float[6]
            pdot  -> float[6]
            ref_frame  -> float[6]
            tool_frame  -> float[6]
            response  -> Response
        """
        response = self.__rtde_stub.GetControlData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetIOData(self):
        """
        IO Data:
            di   -> DigitalSignal[]
            do   -> DigitalSignal[]
            ai  -> AnalogSignal[]
            ao  -> AnalogSignal[]
            end_di  -> EndtoolSignal[]
            end_do  -> EndtoolSignal[]
            end_ai  -> AnalogSignal[]
            end_ao  -> AnalogSignal[]
            response  -> Response
        """
        response = self.__rtde_stub.GetIOData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetServoData(self):
        """
        Servo Data:
            status_codes   -> string[]
            temperatures   -> float[]
            voltages  -> float[]
            currents  -> float[]
            servo_actives  -> bool[]
            brake_actives  -> bool[]
            response  -> Response
        """
        response = self.__rtde_stub.GetServoData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetViolationData(self):
        """
        Violation Data:
            violation_code   -> uint64
            j_index   -> uint32
            i_args  -> int32[]
            f_args  -> float[]
            violation_str  -> string
            response  -> Response
        """
        response = self.__rtde_stub.GetViolationData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetViolationMessageQueue(self):
        """
        Violation Data:
            violation_code   -> uint64
            j_index   -> uint32
            i_args  -> int32[]
            f_args  -> float[]
            violation_str  -> string
            response  -> Response
        """
        response = self.__rtde_stub.GetViolationMessageQueue(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetProgramData(self):
        """
        Program Data:
            program_state   -> ProgramState
            cmd_id   -> int32
            sub_cmd_id  -> int32
            running_hours  -> int32
            running_mins  -> int32
            running_secs  -> int32
            program_name  -> string
            program_alarm  -> string
            program_annotation  -> string
            response  -> Response
        """
        response = self.__rtde_stub.GetProgramData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetStopState(self):
        response = self.__rtde_stub.GetStopState(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    def TestFunction(self, code: int, msg: str):
        try:
            response = self.__rtde_stub.TestFunction(rtde_msgs.TestRequest(
                intVal=code, strVal=msg
            ))
            return json_format.MessageToDict(response,
                                             including_default_value_fields=True,
                                             preserving_proto_field_name=True,
                                             use_integers_for_enums=True)
        except grpc.RpcError as ex:
            print('GRPC Exception: code ' + str(ex.code()) + ' - details: ' + str(ex.details()))
            return None


############################
# Main
############################
if __name__ == "__main__":
    rtde_client = RTDESocketClient(Common.Config().CONTROLLER_IP_ADDRESS, Common.Config().RTDE_SOCKET_PORT)
    control_data = rtde_client.GetControlData()
    print(control_data)
    # rtde_msgs = rtde_client.GetMotionData()
    # print(rtde_msgs)
    print('Test 0: ' + str(rtde_client.TestFunction(code=0, msg='Test 0')))
    print('Test 1: ' + str(rtde_client.TestFunction(code=1, msg='Test 1')))
    print('Test 2: ' + str(rtde_client.TestFunction(code=2, msg='Test 2')))
    print('Test 3: ' + str(rtde_client.TestFunction(code=3, msg='Test 3')))
