import sys
import time
import grpc
from google.protobuf import json_format
from typing import List

import neuromeka_hri.common as Common
import neuromeka_hri.managers as Managers

if sys.version_info >= (3, 9):
    from neuromeka.proto import *
else:
    from neuromeka.proto_step import *

class ControlSocketClient:
    """
    gRPC client to Control Server in C++ IndyFramework v3.0
    """
    ABSOLUTE_JOINT = control_msgs.ABSOLUTE_JOINT
    RELATIVE_JOINT = control_msgs.RELATIVE_JOINT
    ABSOLUTE_TASK = control_msgs.ABSOLUTE_TASK
    RELATIVE_TASK = control_msgs.RELATIVE_TASK
    TCP_TASK = control_msgs.TCP_TASK
    CIRCLE_POINT_SET = control_msgs.POINT_SET
    CIRCLE_CENTER_AXIS = control_msgs.CENTER_AXIS
    CIRCLE_CONSTANT = control_msgs.CONSTANT
    CIRCLE_RADIAL = control_msgs.RADIAL
    CIRCLE_SMOOTH = control_msgs.SMOOTH
    STOP_IMMEDIATE_BRAKE = common_msgs.IMMEDIATE_BRAKE
    STOP_SMOOTH_BRAKE = common_msgs.SMOOTH_BRAKE
    STOP_SMOOTH_ONLY = common_msgs.SMOOTH_ONLY
    NO_BLENDING = 0
    OVERRIDE_BLENDING = 1
    DUPLICATE_BLENDING = 2

    def __init__(self, ip_addr, port=Common.Config().CONTROL_SOCKET_PORT):
        control_channel = grpc.insecure_channel("{}:{}".format(ip_addr, port))
        control_stub = ControlStub(control_channel)
        self.__control_stub = control_stub
        self._logger = Managers.LogManager()

    @Common.Utils.exception_handler
    def GetControlInfo(self):
        """
        Device Info:
            control_version -> string
            robot_model -> string
            response -> {code: int64, msg: string}
        """
        response = self.__control_stub.GetControlInfo(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def PingFromConty(self):
        response = self.__control_stub.PingFromConty(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Motion
    ############################
    @Common.Utils.exception_forwarder
    def MoveJ(self, jstart, jtarget,
              blending_type=NO_BLENDING,
              base_type=ABSOLUTE_JOINT,
              blending_radius=0.0,
              vel_ratio=Common.Limits.JogVelRatioDefault,
              acc_ratio=Common.Limits.JogAccRatioDefault,
              post_condition=Common.Property.PostCondition(),
              teaching_mode=False) -> dict:
        jtarget = control_msgs.TargetJ(j_start=list(jstart), j_target=list(jtarget), base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveJ(control_msgs.MoveJReq(
            target=jtarget,
            blending=blending,
            vel_ratio=vel_ratio, acc_ratio=acc_ratio,
            post_condition=post_cond,
            teaching_mode=teaching_mode
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveJT(self, jstart, jtarget,
               blending_type=NO_BLENDING,
               base_type=ABSOLUTE_JOINT,
               blending_radius=0.0,
               move_time=2.0,
               post_condition=Common.Property.PostCondition()) -> dict:
        """
        jpos = [deg, deg, deg, deg, deg, deg]
        move_time = seconds
        """
        jtarget = control_msgs.TargetJ(j_start=list(jstart), j_target=list(jtarget), base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveJT(control_msgs.MoveJTReq(
            target=jtarget,
            blending=blending,
            time=move_time,
            post_condition=post_cond
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_forwarder
    def MoveL(self, tstart, ttarget,
              blending_type=NO_BLENDING,
              base_type=ABSOLUTE_TASK,
              blending_radius=0.0,
              vel_ratio=Common.Limits.JogVelRatioDefault,
              acc_ratio=Common.Limits.JogAccRatioDefault,
              post_condition=Common.Property.PostCondition(),
              teaching_mode=False,
              bypass_singular=False
              ) -> dict:
        ptarget = control_msgs.TargetP(t_start=list(tstart), t_target=list(ttarget), base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveL(control_msgs.MoveLReq(
            target=ptarget,
            blending=blending,
            vel_ratio=vel_ratio, acc_ratio=acc_ratio,
            post_condition=post_cond,
            teaching_mode=teaching_mode,
            bypass_singular=bypass_singular
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveAxis(self,
                  target_mm,
                  is_absolute=True,
                  vel_ratio=Common.Limits.JogVelRatioDefault,
                  acc_ratio=Common.Limits.JogAccRatioDefault):

        # vel = Common.Limits.ExternalMotorSpeedMaxCnt * vel_ratio / 100
        # acc = vel * acc_ratio / 100

        response = self.__control_stub.MoveLinearAxis(control_msgs.MoveAxisReq(target_mm=target_mm, vel_percentage=vel_ratio, acc_percentage=acc_ratio, is_absolute=is_absolute))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_forwarder
    def MoveLF(self, tstart, ttarget, enabledAxis, desForce,
              blending_type=NO_BLENDING,
              base_type=ABSOLUTE_TASK,
              blending_radius=0.0,
              vel_ratio=Common.Limits.JogVelRatioDefault,
              acc_ratio=Common.Limits.JogAccRatioDefault,
              post_condition=Common.Property.PostCondition(),
              teaching_mode=False) -> dict:
        ptarget = control_msgs.TargetP(t_start=list(tstart), t_target=list(ttarget), base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveLF(control_msgs.MoveLFReq(
            target=ptarget,
            blending=blending,
            vel_ratio=vel_ratio, acc_ratio=acc_ratio,
            des_force=desForce, enabled_force=enabledAxis,
            post_condition=post_cond,
            teaching_mode=teaching_mode
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)
    @Common.Utils.exception_handler
    def MoveLT(self, tstart, ttarget,
               blending_type=NO_BLENDING,
               base_type=ABSOLUTE_TASK,
               blending_radius=0.0,
               move_time=2.0,
               post_condition=Common.Property.PostCondition()) -> dict:
        ptarget = control_msgs.TargetP(t_start=list(tstart), t_target=list(ttarget), base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveLT(control_msgs.MoveLTReq(
            target=ptarget,
            blending=blending,
            time=move_time,
            post_condition=post_cond
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveC(self, tstart, tpos0, tpos1,
              blending_type=NO_BLENDING,
              base_type=ABSOLUTE_TASK,
              angle=90.0,
              setting_type=CIRCLE_POINT_SET,
              move_type=control_msgs.CONSTANT,
              blending_radius=0.0,
              vel_ratio=Common.Limits.JogVelRatioDefault,
              acc_ratio=Common.Limits.JogAccRatioDefault,
              post_condition=Common.Property.PostCondition(),
              teaching_mode=False,
              bypass_singular=False) -> dict:
        ctarget = control_msgs.TargetC(t_start=list(tstart), t_pos0=list(tpos0), t_pos1=list(tpos1),
                                       base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveC(control_msgs.MoveCReq(
            target=ctarget,
            blending=blending,
            angle=angle,
            setting_type=setting_type,
            move_type=move_type,
            vel_ratio=vel_ratio, acc_ratio=acc_ratio,
            post_condition=post_cond,
            teaching_mode=teaching_mode,
            bypass_singular=bypass_singular
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveCT(self, tstart, tpos0, tpos1,
               blending_type=NO_BLENDING,
               base_type=ABSOLUTE_TASK,
               angle=90.0,
               setting_type=CIRCLE_POINT_SET,
               move_type=control_msgs.CONSTANT,
               blending_radius=0.0,
               move_time=2.0,
               post_condition=Common.Property.PostCondition()) -> dict:
        ctarget = control_msgs.TargetC(t_start=list(tstart), t_pos0=list(tpos0), t_pos1=list(tpos1),
                                       base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveCT(control_msgs.MoveCTReq(
            target=ctarget,
            blending=blending,
            angle=angle,
            setting_type=setting_type,
            move_type=move_type,
            time=move_time,
            post_condition=post_cond
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Motion
    ############################
    @Common.Utils.exception_forwarder
    def MoveConveyor(self,
                     post_condition=Common.Property.PostCondition(),
                     teaching_mode=False, bypass_singular=False,
                     acc_ratio=Common.Limits.JogAccRatioDefault) -> dict:
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveConveyor(control_msgs.MoveConveyorReq(
            teaching_mode=teaching_mode,
            bypass_singular=bypass_singular,
            acc_ratio=acc_ratio,
            post_condition=post_cond
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ##
    # @brief move along joint trajectory
    # @remark all arguments are NxD arrays (N: number of points, D: DOF)
    # @param q_list joint values (unit: rads)
    # @param qdot_list joint velocities (unit: rads/s)
    # @param qddot_list joint accelerations (unit: rads/s^2)
    @Common.Utils.exception_handler
    def MoveJointTraj(self, q_list: List[List[float]], qdot_list: List[List[float]], qddot_list: List[List[float]]) -> dict:
        traj_req = control_msgs.MoveJointTrajReq(q_list=list(map(lambda x: common_msgs.Vector(values=x), q_list)),
                                                 qdot_list=list(map(lambda x: common_msgs.Vector(values=x), qdot_list)),
                                                 qddot_list=list(map(lambda x: common_msgs.Vector(values=x), qddot_list)))
        response = self.__control_stub.MoveJointTraj(traj_req)
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ##
    # @brief move along joint trajectory
    # @remark all arguments are Nx6 arrays (N: number of points)
    # @param p_list task positions (xyzuvw), unit: m & rads
    # @param pdot_list task velocities (v, w), unit: m/s & rads/s
    # @param pddot_list task accelerations (v, w), unit: m/s^2 & rads/s^2
    @Common.Utils.exception_handler
    def MoveTaskTraj(self, p_list: List[List[float]], pdot_list: List[List[float]], pddot_list: List[List[float]]) -> dict:
        traj_req = control_msgs.MoveTaskTrajReq(p_list=list(map(lambda x: common_msgs.Vector(values=x), p_list)),
                                                pdot_list=list(map(lambda x: common_msgs.Vector(values=x), pdot_list)),
                                                pddot_list=list(map(lambda x: common_msgs.Vector(values=x), pddot_list)))
        response = self.__control_stub.MoveTaskTraj(traj_req)
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ##
    # @brief move gcode file
    # @param gcode_file file name in IndyDeployment/Gcodes folder
    # @param is_smooth_mode set True to smooth the motion
    # @param smooth_radius smoothing radius, in millimeters
    # @param vel_ratio velocity ratio in percents
    # @param acc_ratio acceleration ratio in percents
    @Common.Utils.exception_handler
    def MoveGcode(self, gcode_file, is_smooth_mode, smooth_radius, vel_ratio=25, acc_ratio=100) -> dict:
        gcode_req = control_msgs.MoveGcodeReq(gcode_file=gcode_file,
                                              is_smooth_mode=is_smooth_mode,
                                              smooth_radius=smooth_radius,
                                              vel_ratio=vel_ratio,
                                              acc_ratio=acc_ratio)
        response = self.__control_stub.MoveGcode(gcode_req)
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def WaitIO(self, di_signal_list, do_signal_list, end_di_signal_list, end_do_signal_list, conjunction=0,
               set_do_signal_list=None, set_end_do_signal_list=None,
               set_ao_signal_list=None, set_end_ao_signal_list=None):

        response = self.__control_stub.WaitIO(control_msgs.WaitIOReq(
            di_list=self.__to_digital_request_list__(di_signal_list),
            do_list=self.__to_digital_request_list__(do_signal_list),
            end_di_list=self.__to_digital_request_list__(end_di_signal_list),
            end_do_list=self.__to_digital_request_list__(end_do_signal_list),
            conjunction=conjunction,
            set_do_list=self.__to_digital_request_list__(set_do_signal_list),
            set_end_do_list=self.__to_digital_request_list__(set_end_do_signal_list),
            set_ao_list=self.__to_analog_request_list__(set_ao_signal_list),
            set_end_ao_list=self.__to_analog_request_list__(set_end_ao_signal_list)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def WaitTime(self, time: float,
                 set_do_signal_list=None, set_end_do_signal_list=None,
                 set_ao_signal_list=None, set_end_ao_signal_list=None):
        response = self.__control_stub.WaitTime(control_msgs.WaitTimeReq(
            time=time,
            set_do_list=self.__to_digital_request_list__(set_do_signal_list),
            set_end_do_list=self.__to_digital_request_list__(set_end_do_signal_list),
            set_ao_list=self.__to_analog_request_list__(set_ao_signal_list),
            set_end_ao_list=self.__to_analog_request_list__(set_end_ao_signal_list)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def WaitProgress(self, progress: int,
                     set_do_signal_list=None, set_end_do_signal_list=None,
                     set_ao_signal_list=None, set_end_ao_signal_list=None):
        response = self.__control_stub.WaitProgress(control_msgs.WaitProgressReq(
            progress=progress,
            set_do_list=self.__to_digital_request_list__(set_do_signal_list),
            set_end_do_list=self.__to_digital_request_list__(set_end_do_signal_list),
            set_ao_list=self.__to_analog_request_list__(set_ao_signal_list),
            set_end_ao_list=self.__to_analog_request_list__(set_end_ao_signal_list)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def WaitTraj(self, traj_condition,
                 set_do_signal_list=None, set_end_do_signal_list=None,
                 set_ao_signal_list=None, set_end_ao_signal_list=None):
        response = self.__control_stub.WaitTraj(control_msgs.WaitTrajReq(
            traj_condition=traj_condition,
            set_do_list=self.__to_digital_request_list__(set_do_signal_list),
            set_end_do_list=self.__to_digital_request_list__(set_end_do_signal_list),
            set_ao_list=self.__to_analog_request_list__(set_ao_signal_list),
            set_end_ao_list=self.__to_analog_request_list__(set_end_ao_signal_list)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def WaitRadius(self, radius: int,
                   set_do_signal_list=None, set_end_do_signal_list=None,
                   set_ao_signal_list=None, set_end_ao_signal_list=None):
        response = self.__control_stub.WaitRadius(control_msgs.WaitRadiusReq(
            radius=radius,
            set_do_list=self.__to_digital_request_list__(set_do_signal_list),
            set_end_do_list=self.__to_digital_request_list__(set_end_do_signal_list),
            set_ao_list=self.__to_analog_request_list__(set_ao_signal_list),
            set_end_ao_list=self.__to_analog_request_list__(set_end_ao_signal_list)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    # -------------------------#
    # Violation Recovery
    # -------------------------#
    @Common.Utils.exception_handler
    def Recover(self) -> dict:
        response = self.__control_stub.Recover(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetManualRecovery(self, enable=True) -> dict:
        response = self.__control_stub.SetManualRecovery(common_msgs.State(enable=enable))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveRecoverJoint(self, jtarget,
                         base_type=ABSOLUTE_JOINT) -> dict:
        response = self.__control_stub.MoveRecoverJoint(
            control_msgs.TargetJ(j_target=list(jtarget), base_type=base_type)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Command
    ############################
    @Common.Utils.exception_handler
    def StopMotion(self, stop_category=STOP_IMMEDIATE_BRAKE) -> dict:
        response = self.__control_stub.StopMotion(common_msgs.StopCat(category=stop_category))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetDirectTeaching(self, enable=True) -> dict:
        response = self.__control_stub.SetDirectTeaching(common_msgs.State(enable=enable))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetSimulationMode(self, enable=True) -> dict:
        response = self.__control_stub.SetSimulationMode(common_msgs.State(enable=enable))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def ActivateIndySDK(self, license_key, expire_date) -> dict:
        response = self.__control_stub.ActivateIndySDK(
            control_msgs.SDKLicenseInfo(license_key=license_key, expire_date=expire_date))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetCustomControlMode(self, mode: int) -> dict:
        response = self.__control_stub.SetCustomControlMode(common_msgs.IntMode(mode=mode))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetCustomControlMode(self) -> dict:
        response = self.__control_stub.GetCustomControlMode(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetFrictionCompensation(self, enable=False) -> dict:
        response = self.__control_stub.SetFrictionCompensation(common_msgs.State(enable=enable))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetFrictionCompensationState(self) -> dict:
        response = self.__control_stub.GetFrictionCompensationState(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)


    ############################
    # Program
    ############################
    @Common.Utils.exception_handler
    def PlayProgram(self, prog_name: str = '', prog_idx: int = -1):
        response = self.__control_stub.PlayProgram(control_msgs.Program(
            prog_name=prog_name,
            prog_idx=prog_idx
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def PlayProgramLine(self, prog_name: str = '', prog_idx: int = -1):
        response = self.__control_stub.PlayProgramLine(control_msgs.Program(
            prog_name=prog_name,
            prog_idx=prog_idx
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)
    @Common.Utils.exception_handler
    def PlayTuningProgram(self, prog_name: str = '', prog_idx: int = -1,
                          tuning_space=common_msgs.TUNE_ALL, precision=common_msgs.HIGH_PRECISION,
                          vel_level_max=9):

        tuning_prog_dict = dict(
            program=dict(
                prog_name=prog_name,
                prog_idx=prog_idx),
            tuning_space=tuning_space,
            precision=precision,
            vel_level_max=vel_level_max
        )
        tuning_req = control_msgs.TuningProgram()

        json_format.ParseDict(tuning_prog_dict, tuning_req)
        response = self.__control_stub.PlayTuningProgram(tuning_req)
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def PauseProgram(self):
        response = self.__control_stub.PauseProgram(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def ResumeProgram(self):
        response = self.__control_stub.ResumeProgram(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def StopProgram(self):
        response = self.__control_stub.StopProgram(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SendAlarm(self, content):
        response = self.__control_stub.SendAlarm(
            common_msgs.Message(content=content)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SendAnnotation(self, content):
        response = self.__control_stub.SendAnnotation(
            common_msgs.Message(content=content)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Custom Variable
    ############################
    @Common.Utils.exception_handler
    def SetModbusVariableNameList(self, modbus_list: list):
        """
        modbus_list:
            [
                {
                'server_name': 'local_server',
                'ip': '127.0.0.1',
                'port': 502,
                'variable_list': [{'name': 'home', 'addr': 1017, 'signal_type': 0}]
                },
            ]
        """
        # print("SetModbusVariableNameList modbus_list: ", modbus_list)
        modbus_variables = []
        for item in modbus_list:
            # print("SetModbusVariableNameList item: ", item)
            var_list = []
            for var in item['variable_list']:
                var_list.append(control_msgs.ModbusVariable(name=var['name'], addr=var['addr'],
                                                            signal_type=var['signal_type']))
            modbus_variables.append(control_msgs.ModbusServer(server_name=item['server_name'], ip=item['ip'],
                                                              port=item['port'], variable_list=var_list))

        response = self.__control_stub.SetModbusVariableNameList(
            control_msgs.ModbusVariableList(modbus_variables=modbus_variables)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    # @Common.Utils.exception_handler
    # def CheckModbusConnection(self, server):
    #     """
    #     {
    #     'server_name': 'local_server',
    #     'ip': '127.0.0.1',
    #     'port': 502,
    #     'variable_list': 0
    #     }
    #     """
    #     response = self.__control_stub.CheckModbusConnection(
    #         control_msgs.ModbusServer(server_name=server['server_name'], ip=server['ip'],
    #                                   port=server['port'], variable_list=[])
    #     )
    #     return json_format.MessageToDict(response,
    #                                      including_default_value_fields=True,
    #                                      preserving_proto_field_name=True,
    #                                      use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetVariableNameList(self, variables: list):
        """
        Variables:
            [
                {
                    'name' -> string
                    'addr' -> int32
                    'type' -> string
                }
            ]
        """
        variable_list = []
        for var in variables:
            variable_list.append(control_msgs.Variable(name=var['name'], addr=var['addr'], type=var['type']))

        response = self.__control_stub.SetVariableNameList(
            control_msgs.AllVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetVariableNameList(self):
        """
        Variables:
            [
                {
                    'name' -> string
                    'addr' -> int32
                    'type' -> string
                    'in_watching' -> bool
                }
            ]
        """
        response = self.__control_stub.GetVariableNameList(common_msgs.Empty())
        # print("control_socket_client.py GetVariableNameList: ", response)
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def SetIntVariable(self, int_variables: list):
        """
        Integer Variables:
            [
                addr -> int32
                value -> int64
            ]
        """
        variable_list = []
        for int_var in int_variables:
            variable_list.append(control_msgs.IntVariable(addr=int_var['addr'], value=int_var['value']))

        response = self.__control_stub.SetIntVariable(
            control_msgs.IntVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetIntVariable(self):
        """
        Integer Variables:
            [
                addr -> int32
                value -> int32
            ]
        """
        response = self.__control_stub.GetIntVariable(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def SetModbusVariable(self, modbus_variables: list):
        """
        Modbus Variables:
            [
                name -> string
                addr -> int32
                value -> int32
            ]
        """
        variable_list = []
        for modbus_var in modbus_variables:
            variable_list.append(control_msgs.ModbusVariable(name=modbus_var['name'], addr=modbus_var['addr'],
                                                             value=modbus_var['value'],
                                                             signal_type=modbus_var['signal_type']))

        response = self.__control_stub.SetModbusVariable(
            control_msgs.ModbusVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetModbusVariable(self):
        """
        Modbus Variables:
            [
                name -> string
                addr -> int32
                value -> int32
            ]
        """
        response = self.__control_stub.GetModbusVariable(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def SetBoolVariable(self, bool_variables: list):
        """
        Bool Variables:
            [
                addr -> int32
                value -> bool
            ]
        """
        variable_list = []
        for bool_var in bool_variables:
            variable_list.append(control_msgs.BoolVariable(addr=bool_var['addr'], value=bool_var['value']))

        response = self.__control_stub.SetBoolVariable(
            control_msgs.BoolVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetBoolVariable(self):
        """
        Bool Variables:
            [
                addr -> int32
                value -> bool
            ]
        """
        response = self.__control_stub.GetBoolVariable(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def SetFloatVariable(self, float_variables: list):
        """
        Float Variables:
            [
                addr -> int32
                value -> float
            ]
        """
        variable_list = []
        for float_var in float_variables:
            variable_list.append(control_msgs.FloatVariable(addr=float_var['addr'], value=float_var['value']))

        response = self.__control_stub.SetFloatVariable(
            control_msgs.FloatVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetFloatVariable(self):
        """
        Float Variables:
            [
                addr -> int32
                value -> float
            ]
        """
        response = self.__control_stub.GetFloatVariable(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def SetJPosVariable(self, jpos_variables: list):
        """
        JPos Variables:
            [
                addr -> int32
                jpos -> float[]
            ]
        """
        variable_list = []
        for jpos in jpos_variables:
            variable_list.append(control_msgs.JPosVariable(addr=jpos['addr'], jpos=jpos['jpos']))

        response = self.__control_stub.SetJPosVariable(
            control_msgs.JPosVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetJPosVariable(self):
        """
        JPos Variables:
            [
                addr -> int32
                jpos -> float[]
            ]
        """
        response = self.__control_stub.GetJPosVariable(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def SetTPosVariable(self, tpos_variables: list):
        """
        TPos Variables:
            [
                addr -> int32
                tpos -> float[]
            ]
        """
        variable_list = []
        for tpos in tpos_variables:
            variable_list.append(control_msgs.TPosVariable(addr=tpos['addr'], tpos=tpos['tpos']))

        response = self.__control_stub.SetTPosVariable(
            control_msgs.TPosVars(variables=variable_list)
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetTPosVariable(self):
        """
        TPos Variables:
            [
                addr -> int32
                tpos -> float[]
            ]
        """
        response = self.__control_stub.GetTPosVariable(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)['variables']

    @Common.Utils.exception_handler
    def GetTactTime(self):
        """
        TactTime Data:
            [
                type -> string
                tact_time -> float
            ]
        """
        response = self.__control_stub.GetTactTime(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Utility
    ############################
    @Common.Utils.exception_handler
    def Calculate_IK(self, tpos, init_jpos) -> dict:
        """
        :param tpos:
        :param init_jpos:
        :return:
            'jpos': []
        """
        response = self.__control_stub.InverseKinematics(control_msgs.InverseKinematicsReq(
            tpos=list(tpos),
            init_jpos=list(init_jpos)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Utility
    ############################
    @Common.Utils.exception_handler
    def Calculate_FK(self, jpos) -> dict:
        """
        :param jpos:
        :return:
            'tpos': []
        """
        response = self.__control_stub.ForwardKinematics(control_msgs.ForwardKinematicsReq(
            jpos=list(jpos)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def CheckAproachRetractValid(self, tpos, init_jpos, pre_tpos, post_tpos):
        response = self.__control_stub.CheckAproachRetractValid(control_msgs.CheckAproachRetractValidReq(
            tpos=list(tpos),
            init_jpos=list(init_jpos),
            pre_tpos=list(pre_tpos),
            post_tpos=list(post_tpos)
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetPalletPointList(self, tpos, jpos, pre_tpos, post_tpos, pallet_pattern, width, height):
        response = self.__control_stub.GetPalletPointList(control_msgs.GetPalletPointListReq(
            tpos=list(tpos),
            jpos=list(jpos),
            pre_tpos=list(pre_tpos),
            post_tpos=list(post_tpos),
            pallet_pattern=pallet_pattern,
            width=width,
            height=height
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def CalculateRelativePose(self, start_pos, end_pos,
                              base_type=ABSOLUTE_TASK):
        response = self.__control_stub.CalculateRelativePose(control_msgs.CalculateRelativePoseReq(
            start_pos=list(start_pos),
            end_pos=list(end_pos),
            base_type=base_type
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def CalculateCurrentPoseRel(self, current_pos, relative_pos,
                                base_type=ABSOLUTE_TASK):
        response = self.__control_stub.CalculateCurrentPoseRel(control_msgs.CalculateCurrentPoseRelReq(
            current_pos=list(current_pos),
            relative_pos=list(relative_pos),
            base_type=base_type
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetTeleOpDevice(self):
        response = self.__control_stub.GetTeleOpDevice(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetTeleOpState(self):
        response = self.__control_stub.GetTeleOpState(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def ConnectTeleOpDevice(self, name: str, type: control_msgs.TeleOpDevice, ip: str, port: int):
        response = self.__control_stub.ConnectTeleOpDevice(
            control_msgs.TeleOpDevice(name=name,type=type,ip=ip,port=port
                                      )
        )
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def DisConnectTeleOpDevice(self):
        response = self.__control_stub.DisConnectTeleOpDevice(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def ReadTeleOpInput(self):
        response = self.__control_stub.ReadTeleOpInput(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def StartTeleOp(self, method, mode=control_msgs.TeleMode.TELE_RAW):
        response = self.__control_stub.StartTeleOp(control_msgs.TeleOpState(mode=mode,method=method))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def StopTeleOp(self):
        response = self.__control_stub.StopTeleOp(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SetPlayRate(self, rate: float):
        response = self.__control_stub.SetPlayRate(control_msgs.TelePlayRate(rate=rate))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetPlayRate(self):
        response = self.__control_stub.GetPlayRate(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def EnableTeleKey(self, enable):
        response = self.__control_stub.EnableTeleKey(common_msgs.State(enable=enable))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveTeleJAbs(self, jpos, vel_ratio=0.8, acc_ratio=7.0):
        response = self.__control_stub.MoveTeleJ(
            control_msgs.MoveTeleJReq(jpos=jpos, vel_ratio=vel_ratio, acc_ratio=acc_ratio,
                                      method=control_msgs.TELE_JOINT_ABSOLUTE))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveTeleJRel(self, jpos, vel_ratio=0.8, acc_ratio=7.0):
        response = self.__control_stub.MoveTeleJ(
            control_msgs.MoveTeleJReq(jpos=jpos, vel_ratio=vel_ratio, acc_ratio=acc_ratio,
                                      method=control_msgs.TELE_JOINT_RELATIVE))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveTeleLAbs(self, tpos, vel_ratio=0.8, acc_ratio=7.0):
        response = self.__control_stub.MoveTeleL(
            control_msgs.MoveTeleLReq(tpos=tpos, vel_ratio=vel_ratio, acc_ratio=acc_ratio,
                                      method=control_msgs.TELE_TASK_ABSOLUTE))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveTeleLRel(self, tpos, vel_ratio=0.8, acc_ratio=7.0):
        response = self.__control_stub.MoveTeleL(
            control_msgs.MoveTeleLReq(tpos=tpos, vel_ratio=vel_ratio, acc_ratio=acc_ratio,
                                      method=control_msgs.TELE_TASK_RELATIVE))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def MoveTeleLTCP(self, tpos, vel_ratio=0.8, acc_ratio=7.0):
        response = self.__control_stub.MoveTeleL(
            control_msgs.MoveTeleLReq(tpos=tpos, vel_ratio=vel_ratio, acc_ratio=acc_ratio,
                                      method=control_msgs.TELE_TASK_TCP))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)
    @Common.Utils.exception_handler
    def MoveTeleLRec(self, tpos, vel_ratio=0.8, acc_ratio=7.0):
        response = self.__control_stub.MoveTeleL(
            control_msgs.MoveTeleLReq(tpos=tpos, vel_ratio=vel_ratio, acc_ratio=acc_ratio,
                                      method=control_msgs.TELE_RECORD_ABSOLUTE))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def GetTeleFileList(self):
        response = self.__control_stub.GetTeleFileList(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def SaveTeleMotion(self, name: str):
        response = self.__control_stub.SaveTeleMotion(control_msgs.TeleFileReq(name=name))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def LoadTeleMotion(self, name: str):
        response = self.__control_stub.LoadTeleMotion(control_msgs.TeleFileReq(name=name))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    @Common.Utils.exception_handler
    def DeleteTeleMotion(self, name: str):
        response = self.__control_stub.DeleteTeleMotion(control_msgs.TeleFileReq(name=name))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)
    @Common.Utils.exception_handler
    def MoveFL(self, tpos,
               blending_type=NO_BLENDING,
               base_type=ABSOLUTE_TASK,
               blending_radius=0.0,
               vel_ratio=Common.Limits.JogVelRatioDefault,
               acc_ratio=Common.Limits.JogAccRatioDefault,
               des_force=0.0,
               enable_force_control=False,
               post_condition=Common.Property.PostCondition(),
               teaching_mode=False) -> dict:
        ptarget = control_msgs.TargetP(tpos=list(tpos), base_type=base_type)
        blending = control_msgs.BlendingType(type=blending_type, blending_radius=blending_radius)
        post_cond = control_msgs.MotionCondition()
        if post_condition is not None:
            post_cond = control_msgs.MotionCondition(
                type_cond=post_condition.condition_type,
                type_react=post_condition.reaction_type,
                const_cond=post_condition.const_cond,
                io_cond=control_msgs.IOCondition(
                    di=self.__to_digital_request_list__(
                        [{'address': di[0], 'state': di[1]} for di in post_condition.digital_inputs]),
                    # di=self.__to_digital_request_list__(post_condition.digital_inputs),
                    # end_di=self.__to_digital_request_list__(post_condition['enddi_condition']),
                ),
            )

        response = self.__control_stub.MoveFL(control_msgs.MoveLReq(
            target=ptarget,
            blending=blending,
            vel_ratio=vel_ratio, acc_ratio=acc_ratio,
            des_force=des_force,
            enable_force_control=enable_force_control,
            post_condition=post_cond,
            teaching_mode=teaching_mode
        ))
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)
    @Common.Utils.exception_handler
    def GetTransformedFTSensorData(self):
        response = self.__control_stub.GetTransformedFTSensorData(common_msgs.Empty())
        return json_format.MessageToDict(response,
                                         including_default_value_fields=True,
                                         preserving_proto_field_name=True,
                                         use_integers_for_enums=True)

    ############################
    # Private
    ############################
    def __to_digital_request_list__(self, digital_signal_list) -> list:
        request_list = []
        if digital_signal_list is not None:
            for signal in digital_signal_list:
                request_list.append(device_msgs.DigitalSignal(address=signal['address'], state=signal['state']))
        return request_list

    def __to_analog_request_list__(self, analog_signal_list) -> list:
        request_list = []
        if analog_signal_list is not None:
            for signal in analog_signal_list:
                request_list.append(device_msgs.AnalogSignal(address=signal['address'], voltage=signal['voltage']))
        return request_list

    ############################
    # Console Logging
    ############################
    def _info(self, content=''):
        self._logger.info(content=content, source='ControlClient')

    def _debug(self, content='', source=''):
        self._logger.debug(content=content, source='ControlClient')

    def _warn(self, content='', source=''):
        self._logger.warn(content=content, source='ControlClient')

    def _error(self, content='', source=''):
        self._logger.error(content=content, source='ContyServicer')


############################
# Main
############################
if __name__ == "__main__":
    control_client = ControlSocketClient('192.168.1.6')

    thresholds = control_client.PlayTuningProgram(
        prog_name='test_tuning2.indy7.json',
        tuning_space=common_msgs.TUNE_ALL,
        precision=common_msgs.HIGH_PRECISION,
        vel_level_max=3
    )
    print(thresholds)
    # control_client.SetDirectTeaching(enable=True)
    # control_info = control_client.GetControlInfo()
    # print(control_info)
    # control_client.MoveJCond(
    #     jpos=[0, 90, 0, 0, 0, 0],
    #     base_type=ControlSocketClient.ABSOLUTE_JOINT,
    #     vel_ratio=20,
    #     acc_ratio=100,
    #     teaching_mode=False
    # )
    # time.sleep(1)
    # control_client.PlayProgram(prog_idx=1)
    # time.sleep(1)
    # control_client.MoveJ(
    #     jpos=[0, 90, 0, 0, 0, 0],
    #     base_type=ControlSocketClient.ABSOLUTE_JOINT,
    #     blending_type=ControlSocketClient.OVERRIDE_BLENDING,
    #     vel_ratio=20,
    #     acc_ratio=100,
    #     teaching_mode=True
    # )

    # var_list = [
    #     {'name': 'a', 'addr': 101, 'type': 'I'},
    #     {'name': 'b', 'addr': 201, 'type': 'F'},
    #     {'name': 'c', 'addr': 301, 'type': 'JPOS'},
    #     {'name': 'd', 'addr': 401, 'type': 'TPOS'},
    # ]
    # control_client.SetVariableNameList(var_list)
    # time.sleep(1)
    # print(control_client.GetVariableNameList())
    # time.sleep(1)

    # int_var_list = [
    #     {'addr': 101, 'value': 15},
    # ]
    # control_client.SetIntVariable(int_var_list)
    # time.sleep(1)
    # print(control_client.GetIntVariable())

    # control_client.PlayProgram(prog_idx=1)
    # res = control_client.SendAlarm(content="Test")
    # print(res)
