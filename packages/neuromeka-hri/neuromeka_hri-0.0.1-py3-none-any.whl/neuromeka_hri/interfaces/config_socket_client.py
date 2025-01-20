import sys
import time
import grpc
from google.protobuf import json_format

import neuromeka_hri.common as Common

if sys.version_info >= (3, 9):
    from neuromeka.proto import *
else:
    from neuromeka.proto_step import *

class ConfigSocketClient:
    """
    gRPC client to Config Server in C++ IndyFramework v3.0
    """
    COLLISION_NO_DETECT = common_msgs.COLL_NO_DETECT
    COLLISION_PAUSE = common_msgs.COLL_PAUSE
    COLLISION_RESUME_AFTER_SLEEP = common_msgs.COLL_RESUME_AFTER_SLEEP
    COLLISION_STOP = common_msgs.COLL_STOP
    STOPCAT_IMMEDIATE_BRAKE = common_msgs.IMMEDIATE_BRAKE
    STOPCAT_SMOOTH_BRAKE = common_msgs.SMOOTH_BRAKE
    STOPCAT_SMOOTH_ONLY = common_msgs.SMOOTH_ONLY

    def __init__(self, ip_addr, port=Common.Config().CONFIG_SOCKET_PORT):
        config_channel = grpc.insecure_channel("{}:{}".format(ip_addr, port))
        config_stub = ConfigStub(config_channel)

        self.__config_stub = config_stub

    @Common.Utils.exception_handler
    def SetRefFrame(self, fpos: list):
        """
        Ref Frame
            fpos -> float[6]
        """
        response = self.__config_stub.SetRefFrame(config_msgs.Frame(
            fpos=list(fpos)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetRefFramePlanar(self, fpos0: list, fpos1: list, fpos2: list):
        """
        Ref Frame
            fpos -> float[6]
        """
        response = self.__config_stub.SetRefFramePlanar(config_msgs.PlanarFrame(
            fpos0=list(fpos0), fpos1=list(fpos1), fpos2=list(fpos2)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetToolFrame(self, fpos: list):
        """
        Tool Frame
            fpos -> float[6]
        """
        response = self.__config_stub.SetToolFrame(config_msgs.Frame(
            fpos=list(fpos)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetSpeedRatio(self, speed_ratio: int):
        """
        Speed Ratio
            ratio -> uint32 {0 ~ 100}
        """
        response = self.__config_stub.SetSpeedRatio(config_msgs.Ratio(
            ratio=speed_ratio
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetHomePos(self, home_jpos: list):
        """
        Joint Home Position
            jpos -> double[]
        """
        response = self.__config_stub.SetHomePosition(config_msgs.JointPos(
            jpos=home_jpos
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetHomePos(self):
        """
        Joint Home Position
            jpos -> double[]
        """
        response = self.__config_stub.GetHomePosition(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetPackPos(self):
        """
        Joint Pack Position
            jpos -> double[]
        """
        response = self.__config_stub.GetPackPosition(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetDIConfigList(self, di_config_list: dict):
        """
        DI Configuration List
            {
                'di_configs': [
                    {
                        'function_code': 2,
                        'function_name': "name",
                        'triggerSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}]
                        'successSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}]
                        'failureSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}]
                    }
                ]
            }
        """
        di_list_request = config_msgs.DIConfigList()
        json_format.ParseDict(di_config_list, di_list_request)

        response = self.__config_stub.SetDIConfigList(di_list_request)

        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetDIConfigList(self):
        """
        DI Configuration List
            {
                'di_configs': [
                    {
                        'function_code': 2,
                        'function_name': "name",
                        'triggerSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}],
                        'successSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}],
                        'failureSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}]
                    }
                ]
            }
        """
        response = self.__config_stub.GetDIConfigList(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetDOConfigList(self, do_config_list: dict):
        """
        DO Configuration List
            {
                'do_configs': [
                    {
                        'state_code': 2,
                        'state_name': "name",
                        'onSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}],
                        'offSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}]
                    }
                ]
            }
        """
        do_list_request = config_msgs.DOConfigList()
        json_format.ParseDict(do_config_list, do_list_request)

        response = self.__config_stub.SetDOConfigList(do_list_request)

        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetDOConfigList(self):
        """
        DO Configuration List
            {
                'do_configs': [
                    {
                        'state_code': 2,
                        'state_name': "name",
                        'onSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}],
                        'offSignals': [{'address': 1, 'state': 1}, {'address': 2, 'state': 0}]
                    }
                ]
            }
        """
        response = self.__config_stub.GetDOConfigList(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetAutoServoOff(self, enable: bool, time: float):
        """
        Auto Servo-Off Config
            enable -> bool
            time -> float
        """
        response = self.__config_stub.SetAutoServoOff(config_msgs.AutoServoOffConfig(
            enable=enable, time=time
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetAutoServoOff(self):
        """
        Auto Servo-Off Config
            enable -> bool
            time -> float
        """
        response = self.__config_stub.GetAutoServoOff(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetJointControlGain(self, kp: list, kv: list, kl2: list):
        """
        Joint Control Gains:
            kp   -> float[6]
            kv   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.SetJointControlGain(config_msgs.JointGainSet(
            kp=list(kp), kv=list(kv), kl2=list(kl2)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetJointControlGain(self):
        """
        Joint Control Gains:
            kp   -> float[6]
            kv   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.GetJointControlGain(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetTaskControlGain(self, kp, kv, kl2):
        """
        Task Control Gains:
            kp   -> float[6]
            kv   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.SetTaskControlGain(config_msgs.TaskGainSet(
            kp=list(kp), kv=list(kv), kl2=list(kl2)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetTaskControlGain(self):
        """
        Task Control Gains:
            kp   -> float[6]
            kv   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.GetTaskControlGain(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetImpedanceControlGain(self, mass, damping, stiffness, kl2):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.SetImpedanceControlGain(config_msgs.ImpedanceGainSet(
            mass=list(mass), damping=list(damping), stiffness=list(stiffness), kl2=list(kl2)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetImpedanceControlGain(self):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.GetImpedanceControlGain(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetForceControlGain(self, kp, kv, kl2, mass, damping, stiffness, kpf, kif):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.SetForceControlGain(config_msgs.ForceGainSet(
            kp=list(kp), kv=list(kv), kl2=list(kl2), mass=list(mass), damping=list(damping), stiffness=list(stiffness),
            kpf=list(kpf), kif=list(kif)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetForceControlGain(self):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.GetForceControlGain(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)
    @Common.Utils.exception_handler
    def SetCustomControlGain2(self, gain0, gain1):
        return self._set_custom_control_gain(gain0, gain1, *[([0]*6) for _ in range(8)])

    @Common.Utils.exception_handler
    def SetCustomControlGain3(self, gain0, gain1, gain2):
        return self._set_custom_control_gain(gain0, gain1, gain2, *[([0]*6) for _ in range(7)])

    @Common.Utils.exception_handler
    def SetCustomControlGain6(self, gain0, gain1, gain2, gain3, gain4, gain5):
        return self._set_custom_control_gain(gain0, gain1, gain2, gain3, gain4, gain5, *[([0]*6) for _ in range(4)])

    @Common.Utils.exception_handler
    def SetCustomControlGain(self, gain0, gain1, gain2, gain3, gain4, gain5, gain6, gain7, gain8, gain9):
        return self._set_custom_control_gain(gain0, gain1, gain2, gain3, gain4, gain5, gain6, gain7, gain8, gain9)

    def _set_custom_control_gain(self, *gains):
        """
        Private method to set custom control gains with a variable number of gain arrays.

        Args:
            *gains: Up to 10 lists of gain values. Each gain should be a list of floats.
        """
        response = self.__config_stub.SetCustomControlGain(config_msgs.CustomGainSet(
            gain0=list(gains[0]), gain1=list(gains[1]), gain2=list(gains[2]), gain3=list(gains[3]),
            gain4=list(gains[4]), gain5=list(gains[5]), gain6=list(gains[6]), gain7=list(gains[7]),
            gain8=list(gains[8]), gain9=list(gains[9])
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)


    @Common.Utils.exception_handler
    def GetCustomControlGain(self):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        response = self.__config_stub.GetCustomControlGain(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetFrictionComp(self, control_comp: bool, control_comp_levels: list,
                        dt_comp: bool, dt_comp_levels: list):
        """
        Friction Compensation Set:
            joint_idx   -> uint32
            control_comp_enable   -> bool
            control_comp_levels   -> int32[6]
            teaching_comp_enable   -> bool
            teaching_comp_levels   -> int32[6]
        """
        response = self.__config_stub.SetFrictionComp(config_msgs.FrictionCompSet(
            control_comp_enable=control_comp, control_comp_levels=list(control_comp_levels),
            teaching_comp_enable=dt_comp, teaching_comp_levels=list(dt_comp_levels)
        ))

        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetFrictionComp(self):
        """
        Friction Compensation Set:
            joint_idx   -> uint32
            control_comp_enable   -> bool
            control_comp_levels   -> int32[6]
            teaching_comp_enable   -> bool
            teaching_comp_levels   -> int32[6]
        """
        response = self.__config_stub.GetFrictionComp(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetMountPos(self, rot_y=0.0, rot_z=0.0):
        """
        Mounting Angles:
            rot_y   -> float
            rot_z   -> float
        """
        response = self.__config_stub.SetMountPos(config_msgs.MountingAngles(
            ry=rot_y, rz=rot_z
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetMountPos(self):
        """
        Mounting Angles:
            rot_y   -> float
            rot_z   -> float
        """
        response = self.__config_stub.GetMountPos(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetFTSensorConfig(self,
                          dev_type, com_type, ip_address,
                               ft_frame_translation_offset_x=0.0,
                               ft_frame_translation_offset_y=0.0,
                               ft_frame_translation_offset_z=0.0,
                               ft_frame_rotation_offset_r=0.0,
                               ft_frame_rotation_offset_p=0.0,
                               ft_frame_rotation_offset_y=0.0):
        response = self.__config_stub.SetFTSensorConfig(config_msgs.FTSensorDevice(
            dev_type=dev_type, com_type=com_type,ip_address=ip_address,
            ft_frame_translation_offset_x=ft_frame_translation_offset_x,
            ft_frame_translation_offset_y=ft_frame_translation_offset_y,
            ft_frame_translation_offset_z=ft_frame_translation_offset_z,
            ft_frame_rotation_offset_r=ft_frame_rotation_offset_r,
            ft_frame_rotation_offset_p=ft_frame_rotation_offset_p,
            ft_frame_rotation_offset_y=ft_frame_rotation_offset_y))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetFTSensorConfig(self):
        response = self.__config_stub.GetFTSensorConfig(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetToolProperty(self, mass: float, center_of_mass: list, inertia: list):
        """
        Tool Properties:
            mass   -> float
            center_of_mass   -> float[3]
            inertia   -> float[6]
        """
        response = self.__config_stub.SetToolProperty(config_msgs.ToolProperties(
            mass=mass, center_of_mass=list(center_of_mass), inertia=list(inertia)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetToolProperty(self):
        """
        Tool Properties:
            mass   -> float
            center_of_mass   -> float[3]
            inertia   -> float[6]
        """
        response = self.__config_stub.GetToolProperty(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetCollSensLevel(self, level: int):
        """
        Collision Sensitivity Level:
            level -> uint32
        """
        response = self.__config_stub.SetCollSensLevel(config_msgs.CollisionSensLevel(
            level=level
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetCollSensLevel(self):
        """
        Collision Sensitivity Level:
            level -> uint32
        """
        response = self.__config_stub.GetCollSensLevel(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetCollSensParam(self, j_torque_bases, j_torque_tangents,
                         t_torque_bases, t_torque_tangents,
                         t_constvel_torque_bases, t_constvel_torque_tangents,
                         t_conveyor_torque_bases, t_conveyor_torque_tangents,
                         error_bases, error_tangents):
        """
        Collision Params:
            j_torque_bases                  -> double[6]
            j_torque_tangents               -> double[6]
            t_torque_bases                  -> double[6]
            t_torque_tangents               -> double[6]
            error_bases                     -> double[6]
            error_tangents                  -> double[6]
            t_constvel_torque_bases         -> double[6]
            t_constvel_torque_tangents      -> double[6]
            t_conveyor_torque_bases         -> double[6]
            t_conveyor_torque_tangents      -> double[6]
        """
        response = self.__config_stub.SetCollSensParam(config_msgs.CollisionThresholds(
            j_torque_bases=list(j_torque_bases), j_torque_tangents=list(j_torque_tangents),
            t_torque_bases=list(t_torque_bases), t_torque_tangents=list(t_torque_tangents),
            error_bases=list(error_bases), error_tangents=list(error_tangents),
            t_constvel_torque_bases=list(t_constvel_torque_bases),
            t_constvel_torque_tangents=list(t_constvel_torque_tangents),
            t_conveyor_torque_bases=list(t_conveyor_torque_bases),
            t_conveyor_torque_tangents=list(t_conveyor_torque_tangents)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetCollSensParam(self):
        """
        Collision Params:
            j_torque_bases                  -> double[6]
            j_torque_tangents               -> double[6]
            t_torque_bases                  -> double[6]
            t_torque_tangents               -> double[6]
            error_bases                     -> double[6]
            error_tangents                  -> double[6]
            t_constvel_torque_bases         -> double[6]
            t_constvel_torque_tangents      -> double[6]
            t_conveyor_torque_bases         -> double[6]
            t_conveyor_torque_tangents      -> double[6]
        """
        response = self.__config_stub.GetCollSensParam(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetCollPolicy(self, policy=COLLISION_NO_DETECT,
                      sleep_time=0, gravity_time=0.1):
        """
        Collision Policies:
            policy -> uint32
            sleep_time -> float
            gravity_time -> float
        """
        response = self.__config_stub.SetCollPolicy(config_msgs.CollisionPolicy(
            policy=policy, sleep_time=sleep_time, gravity_time=gravity_time
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetCollPolicy(self):
        """
        Collision Policy:
            policy -> uint32
            sleep_time -> float
            gravity_time -> float
        """
        response = self.__config_stub.GetCollPolicy(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetSafetyLimits(self, power_limit: float, power_limit_ratio: float,
                        tcp_force_limit: float, tcp_force_limit_ratio: float,
                        tcp_speed_limit: float, tcp_speed_limit_ratio: float):
        # joint_limits: list):
        """
        Safety Limits:
            power_limit             -> float
            power_limit_ratio       -> float
            tcp_force_limit         -> float
            tcp_force_limit_ratio   -> float
            tcp_speed_limit         -> float
            tcp_speed_limit_ratio   -> float
            # joint_limits   -> float[]
        """
        response = self.__config_stub.SetSafetyLimits(config_msgs.SafetyLimits(
            power_limit=power_limit, power_limit_ratio=power_limit_ratio,
            tcp_force_limit=tcp_force_limit, tcp_force_limit_ratio=tcp_force_limit_ratio,
            tcp_speed_limit=tcp_speed_limit, tcp_speed_limit_ratio=tcp_speed_limit_ratio  # ,
            # joint_limits=list(joint_limits)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetSafetyLimits(self):
        """
        Safety Limits:
            power_limit             -> float
            power_limit_ratio       -> float
            tcp_force_limit         -> float
            tcp_force_limit_ratio   -> float
            tcp_speed_limit         -> float
            tcp_speed_limit_ratio   -> float
            joint_limits   -> float[]
        """
        response = self.__config_stub.GetSafetyLimits(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetSafetyStopConfig(self, jpos_limit_stop_cat=STOPCAT_IMMEDIATE_BRAKE,
                            jvel_limit_stop_cat=STOPCAT_IMMEDIATE_BRAKE,
                            jtau_limit_stop_cat=STOPCAT_IMMEDIATE_BRAKE,
                            tvel_limit_stop_cat=STOPCAT_IMMEDIATE_BRAKE,
                            tforce_limit_stop_cat=STOPCAT_IMMEDIATE_BRAKE,
                            power_limit_stop_cat=STOPCAT_IMMEDIATE_BRAKE):
        """
        Safety Stop Category:
            jpos_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            jvel_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            jtau_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            tvel_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            tforce_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            power_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
        """
        response = self.__config_stub.SetSafetyStopConfig(config_msgs.SafetyStopConfig(
            joint_position_limit_stop_cat=jpos_limit_stop_cat,
            joint_speed_limit_stop_cat=jvel_limit_stop_cat,
            joint_torque_limit_stop_cat=jtau_limit_stop_cat,
            tcp_speed_limit_stop_cat=tvel_limit_stop_cat,
            tcp_force_limit_stop_cat=tforce_limit_stop_cat,
            power_limit_stop_cat=power_limit_stop_cat
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetSafetyStopConfig(self):
        """
        Safety Stop Category:
            joint_position_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            joint_speed_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            joint_torque_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            tcp_speed_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            tcp_force_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            power_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
        """
        response = self.__config_stub.GetSafetyStopConfig(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetReducedRatio(self):
        response = self.__config_stub.GetReducedRatio(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetReducedSpeed(self):
        response = self.__config_stub.GetReducedSpeed(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetReducedSpeed(self, speed):
        response = self.__config_stub.SetReducedSpeed(config_msgs.SetReducedSpeedReq(speed=speed))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetTeleOpParams(self, smooth_factor, cutoff_freq, error_gain):
        response = self.__config_stub.SetTeleOpParams(
            config_msgs.TeleOpParams(smooth_factor=smooth_factor,
                                     cutoff_freq=cutoff_freq,
                                     error_gain=error_gain))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetTeleOpParams(self):
        response = self.__config_stub.GetTeleOpParams(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetKinematicsParams(self):
        response = self.__config_stub.GetKinematicsParams(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)


############################
# Main
############################
if __name__ == "__main__":
    config_client = ConfigSocketClient(Common.Config().CONTROLLER_IP_ADDRESS, Common.Config().CONFIG_SOCKET_PORT)

    # di_list = [{'address': 0, 'state': 1}, {'address': 2, 'state': 0}]
    # di_config_list = config_client.GetDIConfigList()
    # print(di_config_list)
    time.sleep(1)

    fric_comp = config_client.GetFrictionComp()
    print(fric_comp)

    config_client.SetFrictionComp(control_comp=False, control_comp_levels=[1, 1, 1, 1, 1, 1],
                                  dt_comp=True, dt_comp_levels=[1, 1, 1, 1, 1, 1])
    time.sleep(1)
