import math
import os
import json
import logging
import grpc
import string
from google.protobuf import json_format


# from ommon.new_impl import common_msgs_pb2 as common_data
# from common.new_impl import config_msgs_pb2 as config_data
# from common.new_impl import config_pb2_grpc as config_grpc

from neuromeka_hri.managers.log_manager import LogManager
import neuromeka_hri.interfaces as SocketInf
import neuromeka_hri.common as Common

class ConfigManager(metaclass=Common.SingletonMeta):
    def __init__(self) -> None:
        super().__init__()
        self.__logger = LogManager()
        # self.__logger = logging.getLogger()
        # self.__logger.setLevel(level=logging.DEBUG)
        self.__program_speed_ratio = 100
        self._joint_limits_default = [[360.0, 360.0, 360.0, 360.0, 360.0, 360.0],
                                      [-360.0, -360.0, -360.0, -360.0, -360.0, -360.0]]
        self._config_client = SocketInf.ConfigClient(Common.Config().CONTROLLER_IP_ADDRESS,
                                                     Common.Config().CONFIG_SOCKET_PORT)
        params_dir = os.path.dirname(Common.Config().CONTROL_GAIN_DIR)
        os.makedirs(params_dir, exist_ok=True)

    def get_robot_name(self) -> str:
        return Common.Config().ROBOT_MODEL

    def get_robot_dof(self) -> int:
        return Common.Config().ROBOT_DOF

    def get_joint_limits(self):
        safety_limits = self._config_client.GetSafetyLimits()
        if safety_limits is not None:
            return safety_limits['joint_upper_limits'], safety_limits['joint_lower_limits']
        return self._joint_limits_default

    def get_config_path(self) -> str:
        return Common.Config().ROBOT_CONFIG_PATH

    def get_program_path(self) -> str:
        return Common.Config().PROGRAM_DIR

    def get_idx_program_path(self) -> str:
        return Common.Config().INDEX_PROGRAM_DIR

    def get_middleware_log_path(self) -> str:
        return Common.Config().SERVER_LOG_PATH

    def get_control_log_path(self) -> str:
        return Common.Config().LOG_PATH

    def get_robot_sn(self):
        system_info = Common.Utils.load_json(Common.Config().SYSTEM_INFO_DIR)
        if system_info is not None and system_info['robotSN'] is not None:
            return system_info['robotSN']
        else:
            return "robot_sn"

    def get_cb_sn(self):
        system_info = Common.Utils.load_json(Common.Config().SYSTEM_INFO_DIR)
        if system_info is not None and system_info['cbSN'] is not None:
            return system_info['cbSN']
        else:
            return "cb_sn"

    def get_cb_type(self):
        system_info = Common.Utils.load_json(Common.Config().SYSTEM_INFO_DIR)
        if system_info is not None and system_info['cbType'] is not None:
            return system_info['cbType']
        else:
            return 0

    def get_payload(self):
        system_info = Common.Utils.load_json(Common.Config().SYSTEM_INFO_DIR)
        if system_info is not None and system_info['cbSN'] is not None:
            return system_info['cbSN']
        else:
            return "cb_sn"

    def set_program_speed_ratio(self, speed_ratio: int):
        """
        speed_ratio = 0 ~ 100
        """
        if speed_ratio < 0:
            speed_ratio = 0
        if speed_ratio > 100:
            speed_ratio = 100
        res = self._config_client.SetSpeedRatio(speed_ratio=speed_ratio)
        if res is not None:
            self.__program_speed_ratio = speed_ratio
        return res

    def get_program_speed_ratio(self) -> int:
        """
        speed_ratio = 0 ~ 100
        """
        return self.__program_speed_ratio

    def set_home_pos(self, jpos: list):
        self.__logger.debug("Config Manager: SetHomePos " + ', '.join(str(j) for j in jpos))
        Common.Utils.write_json(Common.Config().HOME_POS_DIR, dict(jpos=jpos))
        self._config_client.SetHomePos(home_jpos=jpos)

    def get_home_pos(self):
        self.__logger.debug("Config Manager: GetHomePos")
        home_pos = Common.Utils.load_json(Common.Config().HOME_POS_DIR)
        if home_pos is None:
            jpos = [0 for _ in range(self.get_robot_dof())]
            jpos[2] = -90
            jpos[4] = -90
            return jpos
        else:
            return home_pos['jpos']

    def get_pack_pos(self):
        self.__logger.debug("Config Manager: GetHomePos")
        pack_pos = self._config_client.GetPackPos()
        if pack_pos is None:
            jpos = [0 for _ in range(self.get_robot_dof())]
            return jpos
        else:
            return pack_pos['jpos']

    def get_tool_name_list(self):
        tool_list_dict = Common.Utils.load_json(Common.Config().TOOL_DIR)
        name_list = []
        for tool in tool_list_dict['tools']:
            name_list.append(tool['name'])
        return name_list

    def save_tool_list(self, tool_list: dict):
        Common.Utils.write_json(Common.Config().TOOL_DIR, tool_list)

    def load_tool_list(self) -> dict:
        return Common.Utils.load_json(Common.Config().TOOL_DIR)

    def save_pallet_maker_list(self, pallet_maker_list: dict):
        Common.Utils.write_json(Common.Config().PALLET_MAKER_DIR, pallet_maker_list)

    def load_pallet_maker_list(self) -> dict:
        return Common.Utils.load_json(Common.Config().PALLET_MAKER_DIR)

    def save_conveyor_list(self, conveyor_list: dict):
        Common.Utils.write_json(Common.Config().CONVEYOR_CONFIG_DIR, conveyor_list)

    def load_conveyor_list(self) -> dict:
        return Common.Utils.load_json(Common.Config().CONVEYOR_CONFIG_DIR)

    def get_pallet_name_list(self):
        pallet_maker_list = self.load_pallet_maker_list()
        name_list = []
        if pallet_maker_list:
            for pallet_maker in pallet_maker_list['pallet_makers']:
                name_list.append(pallet_maker['name'])
        return name_list

    def get_pallet(self, name):
        pallet_maker_list = self.load_pallet_maker_list()

        target_pallet_maker = None
        if pallet_maker_list:
            for pallet_maker in pallet_maker_list['pallet_makers']:
                if name == pallet_maker['name']:
                    target_pallet_maker = pallet_maker
                    break

        if target_pallet_maker is None:
            raise Exception("There are no named {}".format(name))
        elif target_pallet_maker['pallet_pattern'] > 3:
            raise Exception("The selected pattern cannot be used {}".format(target_pallet_maker['pallet_pattern']))
        else:
            pallet_pattern = target_pallet_maker['pallet_pattern']
            m = target_pallet_maker['width_num']
            n = target_pallet_maker['height_num']

            tpos = []
            for i in range(self.get_robot_dof()):
                tpos.append(target_pallet_maker['tpos0'][i])
            for i in range(self.get_robot_dof()):
                tpos.append(target_pallet_maker['tpos1'][i])
            for i in range(self.get_robot_dof()):
                tpos.append(target_pallet_maker['tpos2'][i])

            jpos = []
            for i in range(self.get_robot_dof()):
                jpos.append(target_pallet_maker['jpos0'][i])
            for i in range(self.get_robot_dof()):
                jpos.append(target_pallet_maker['jpos1'][i])
            for i in range(self.get_robot_dof()):
                jpos.append(target_pallet_maker['jpos2'][i])

            return tpos, pallet_pattern, m, n, jpos

    def load_default_collision_params(self):
        """
        Collision Parameters
          j_torque_bases              : list,
          j_torque_tangents           : list,
          t_torque_bases              : list,
          t_torque_tangents           : list,
          t_constvel_torque_bases     : list,
          t_constvel_torque_tangents  : list,
          t_conveyor_torque_bases     : list,
          t_conveyor_torque_tangents  : list,
          error_bases                 : list,
          error_tangents              : list,
        """
        DEFAULT_COLLISION_GAIN_BASE = Common.Property.DEFAULT_COLLISION_GAIN_BASE
        base_keys = ['jTorqueBases', 'tTorqueBases', 'tConstVelTorqueBases', 'tConveyorTorqueBases', 'errBases']
        tangent_keys = ['jTorqueTangents', 'tTorqueTangents', 'tConstVelTorqueTangents', 'tConveyorTorqueTangents', 'errTangents']
        default_collision_params = {key: [DEFAULT_COLLISION_GAIN_BASE for _ in range(self.get_robot_dof())] for key in base_keys}
        default_collision_params.update({key: [0.0 for _ in range(self.get_robot_dof())] for key in tangent_keys})
        factory_collision_params = {}
        if os.path.isfile(Common.Config().COLLISION_DEFAULT_DIR):
            try:
                factory_collision_params = Common.Utils.load_json(Common.Config().COLLISION_DEFAULT_DIR)
            except:
                self.__logger.error(f"Factory Collision Setting Not Found in {Common.Config().COLLISION_DEFAULT_DIR}")
            factory_file_ok = True
            if isinstance(factory_collision_params, dict):
                for key in base_keys + tangent_keys:
                    if key in factory_collision_params \
                            and isinstance(factory_collision_params[key], list) \
                            and (len(factory_collision_params[key]) == self.get_robot_dof()):
                        pass
                    else:
                        factory_file_ok = False
                        break
            else:
                factory_file_ok = False
            if factory_file_ok:
                default_collision_params = factory_collision_params
            else:
                self.__logger.error(f"Wrong Factory Collision Setting File: {Common.Config().COLLISION_DEFAULT_DIR}")

        return dict(j_torque_bases=list(default_collision_params['jTorqueBases']),
                    j_torque_tangents=list(default_collision_params['jTorqueTangents']),
                    t_torque_bases=list(default_collision_params['tTorqueBases']),
                    t_torque_tangents=list(default_collision_params['tTorqueTangents']),
                    t_constvel_torque_bases=list(default_collision_params['tConstVelTorqueBases']),
                    t_constvel_torque_tangents=list(default_collision_params['tConstVelTorqueTangents']),
                    t_conveyor_torque_bases=list(default_collision_params['tConveyorTorqueBases']),
                    t_conveyor_torque_tangents=list(default_collision_params['tConveyorTorqueTangents']),
                    error_bases=list(default_collision_params['errBases']),
                    error_tangents=list(default_collision_params['errTangents']),
                    )

    def set_custom_collision_params(self,
                                    j_torque_bases: list, j_torque_tangents: list,
                                    t_torque_bases: list, t_torque_tangents: list,
                                    t_constvel_torque_bases: list, t_constvel_torque_tangents: list,
                                    t_conveyor_torque_bases: list, t_conveyor_torque_tangents: list,
                                    error_bases: list, error_tangents: list):
        res = self._config_client.SetCollSensParam(j_torque_bases=j_torque_bases,
                                                   j_torque_tangents=j_torque_tangents,
                                                   t_torque_bases=t_torque_bases,
                                                   t_torque_tangents=t_torque_tangents,
                                                   t_constvel_torque_bases=t_constvel_torque_bases,
                                                   t_constvel_torque_tangents=t_constvel_torque_tangents,
                                                   t_conveyor_torque_bases=t_conveyor_torque_bases,
                                                   t_conveyor_torque_tangents=t_conveyor_torque_tangents,
                                                   error_bases=error_bases,
                                                   error_tangents=error_tangents)

        if res is not None:
            collision_params = dict(jTorqueBases=list(j_torque_bases),
                                    jTorqueTangents=list(j_torque_tangents),
                                    tTorqueBases=list(t_torque_bases),
                                    tTorqueTangents=list(t_torque_tangents),
                                    tConstVelTorqueBases=list(t_constvel_torque_bases),
                                    tConstVelTorqueTangents=list(t_constvel_torque_tangents),
                                    tConveyorTorqueBases=list(t_conveyor_torque_bases),
                                    tConveyorTorqueTangents=list(t_conveyor_torque_tangents),
                                    errBases=list(error_bases), errTangents=list(error_tangents),
                                    )
            Common.Utils.write_json(Common.Config().COLLISION_CUSTOM_DIR, collision_params)
        return res

    def get_custom_collision_params(self):
        """
        Collision Parameters
          j_torque_bases              : list,
          j_torque_tangents           : list,
          t_torque_bases              : list,
          t_torque_tangents           : list,
          t_constvel_torque_bases     : list,
          t_constvel_torque_tangents  : list,
          t_conveyor_torque_bases     : list,
          t_conveyor_torque_tangents  : list,
          error_bases                 : list,
          error_tangents              : list,
        """
        collision_params = self._config_client.GetCollSensParam()
        return collision_params

    def save_tool_frame_list(self, tool_frame_list: dict):
        Common.Utils.write_json(Common.Config().TOOL_FRAME_DIR, tool_frame_list)

    def load_tool_frame_list(self) -> dict:
        return Common.Utils.load_json(Common.Config().TOOL_FRAME_DIR)

    def set_tool_frame(self, fpos: list):
        return self._config_client.SetToolFrame(fpos=fpos)

    def save_ref_frame_list(self, ref_frame_list: dict):
        Common.Utils.write_json(Common.Config().REF_FRAME_DIR, ref_frame_list)

    def load_ref_frame_list(self) -> dict:
        return Common.Utils.load_json(Common.Config().REF_FRAME_DIR)

    def set_ref_frame(self, fpos: list):
        return self._config_client.SetRefFrame(fpos=fpos)

    def set_ref_frame_planar(self, fpos0: list, fpos1: list, fpos2: list) -> {list, str}:
        result = self._config_client.SetRefFramePlanar(fpos0=fpos0, fpos1=fpos1, fpos2=fpos2)

        if result is not None:
            if 'fpos' in result:
                self.__logger.debug('Result: ' + str(result))
                return dict(ref_frame=result['fpos'], msg='')
            elif 'response' in result:
                self.__logger.debug('Result res: ' + str(result['response']))
                self.__logger.debug('Result msg: ' + str(result['response']['msg']))
                return dict(ref_frame=[0, 0, 0, 0, 0, 0], msg=result['response']['msg'])
            else:
                return None
        else:
            return None

    def get_ref_frame_name(self, ref_frame: list = None) -> str:
        if ref_frame is None or len(ref_frame) == 0:
            return 'Unknown'

        ref_frame_list = self.load_ref_frame_list()['ref_frames']
        for saved_frame in ref_frame_list:
            matched = True
            for i in range(len(saved_frame['tpos'])):
                if math.fabs(ref_frame[i] - saved_frame['tpos'][i]) > 1e-3:
                    matched = False
                    break
            if matched:
                return saved_frame['name']
        return 'Unknown'

    def get_tool_frame_name(self, tool_frame: list = None) -> str:
        if tool_frame is None or len(tool_frame) == 0:
            return 'Unknown'
        tool_frame_list = self.load_tool_frame_list()['tool_frames']
        for saved_frame in tool_frame_list:
            matched = True
            for i in range(len(saved_frame['tpos'])):
                if math.fabs(tool_frame[i] - saved_frame['tpos'][i]) > 1e-3:
                    matched = False
                    break
            if matched:
                return saved_frame['name']
        return 'Unknown'

    def save_custom_pos_list(self, custom_pos_list: dict):
        Common.Utils.write_json(Common.Config().CUSTOM_POS_DIR, custom_pos_list)

    def load_custom_pos_list(self):
        return Common.Utils.load_json(Common.Config().CUSTOM_POS_DIR)

    def save_vision_server_list(self, vision_server_list: dict):
        Common.Utils.write_json(Common.Config().VISION_DIR, vision_server_list)

    def load_vision_server_list(self):
        return Common.Utils.load_json(Common.Config().VISION_DIR)

    def save_modbus_server(self, modbus_server: dict):
        Common.Utils.write_json(Common.Config().MODBUS_DIR, modbus_server)

    def load_modbus_server(self):
        return Common.Utils.load_json(Common.Config().MODBUS_DIR)

    def save_di_config_list(self, di_config_list: dict):
        cur_di_config = Common.Utils.load_json(Common.Config().DI_CONFIG_DIR)
        for di_conf in di_config_list['di_configs']:
            for cur_config in cur_di_config['di_configs']:
                if cur_config['function_code'] == di_conf['function_code']:
                    cur_config['function_name'] = di_conf['function_name']
                    cur_config['triggerSignals'] = di_conf['triggerSignals']
                    cur_config['successSignals'] = di_conf['successSignals']
                    cur_config['failureSignals'] = di_conf['failureSignals']
        self._config_client.SetDIConfigList(cur_di_config)
        # self._config_client.SetDIConfigList(di_config_list)
        Common.Utils.write_json(Common.Config().DI_CONFIG_DIR, cur_di_config)

    def load_di_config_list(self):
        return Common.Utils.load_json(Common.Config().DI_CONFIG_DIR)

    def save_do_config_list(self, do_config_list: dict):
        cur_do_config = Common.Utils.load_json(Common.Config().DO_CONFIG_DIR)
        for do_conf in do_config_list['do_configs']:
            for cur_config in cur_do_config['do_configs']:
                if cur_config['state_code'] == do_conf['state_code']:
                    cur_config['state_name'] = do_conf['state_name']
                    cur_config['onSignals'] = do_conf['onSignals']
                    cur_config['offSignals'] = do_conf['offSignals']
        self._config_client.SetDOConfigList(cur_do_config)
        # self._config_client.SetDOConfigList(do_config_list)
        Common.Utils.write_json(Common.Config().DO_CONFIG_DIR, cur_do_config)

    def load_do_config_list(self):
        return Common.Utils.load_json(Common.Config().DO_CONFIG_DIR)

    def save_on_start_program_config(self, auto_run=True, index=0):
        onstart_dict = dict(auto_run=auto_run, index=index)
        Common.Utils.write_json(Common.Config().ON_START_PROGRAM_CONFIG_DIR, onstart_dict)

    # def save_on_start_program_config(self, index: dict):
    #     self.__write_json(ON_START_PROGRAM_CONFIG_DIR, index)

    def load_on_start_program_config(self):
        return Common.Utils.load_json(Common.Config().ON_START_PROGRAM_CONFIG_DIR)

    def save_friction_config(self, friction_config: dict):
        """
        DEPRECATED
        """
        Common.Utils.write_json(Common.Config().FRICTION_CONFIG_DIR, friction_config)

    def set_friction_config(self,
                            control_comp: bool, control_comp_levels: list,
                            dt_comp: bool, dt_comp_levels: list):
        res = self._config_client.SetFrictionComp(
            control_comp=control_comp,
            control_comp_levels=control_comp_levels,
            dt_comp=dt_comp,
            dt_comp_levels=dt_comp_levels
        )
        if res is not None:
            Common.Utils.write_json(Common.Config().FRICTION_CONFIG_DIR,
                                    dict(
                                        control_comp=control_comp,
                                        control_comp_levels=control_comp_levels,
                                        dt_comp=dt_comp,
                                        dt_comp_levels=dt_comp_levels,
                                        id_joint=-1
                                    ))
        return res

    def get_friction_config(self):
        fric_comp = self._config_client.GetFrictionComp()
        if fric_comp is None:
            return None

        fric_config = dict(
            control_comp=fric_comp['control_comp_enable'],
            control_comp_levels=fric_comp['control_comp_levels'],
            dt_comp=fric_comp['teaching_comp_enable'],
            dt_comp_levels=fric_comp['teaching_comp_levels'],
        )
        return fric_config

    def load_collision_config(self) -> int:
        collision_config_dict = Common.Utils.load_json(Common.Config().COLLISION_CONFIG_DIR)
        if collision_config_dict is None:
            collision_level = self._config_client.GetCollSensLevel()['level']
            collision_policy = self._config_client.GetCollPolicy()
            collision_config_dict = dict(sensitivityLevel=collision_level,
                                         sleepTime=collision_policy['sleep_time'],
                                         gravity_time=collision_policy['gravity_time'],
                                         policy=collision_policy['policy'])
            Common.Utils.write_json(Common.Config().COLLISION_CONFIG_DIR, collision_config_dict)

        return collision_config_dict

    def set_collision_sensitivity(self, level: int = 5):
        collision_config_dict = Common.Utils.load_json(Common.Config().COLLISION_CONFIG_DIR)
        if collision_config_dict is None:
            collision_config_dict = dict()

        res = self._config_client.SetCollSensLevel(level=level)
        if res is not None:
            collision_config_dict['sensitivityLevel'] = level
            Common.Utils.write_json(Common.Config().COLLISION_CONFIG_DIR, collision_config_dict)
        return res

    def get_collision_sensitivity(self) -> int:
        """
        Collision Sensitivity Level:
            level -> uint32
        """
        collision_level = self._config_client.GetCollSensLevel()['level']
        return collision_level

    def set_collision_policy(self, policy=0, sleep_time=1.0, gravity_time=0.1):
        res = self._config_client.SetCollPolicy(
            policy=policy,
            sleep_time=sleep_time,
            gravity_time=gravity_time
        )
        if res is not None:
            collision_config_dict = Common.Utils.load_json(Common.Config().COLLISION_CONFIG_DIR)
            if collision_config_dict is None:
                collision_config_dict = dict(sleepTime=sleep_time,
                                             gravity_time=gravity_time,
                                             policy=policy)
            else:
                collision_config_dict['sleepTime'] = sleep_time
                collision_config_dict['gravity_time'] = gravity_time
                collision_config_dict['policy'] = policy
            Common.Utils.write_json(Common.Config().COLLISION_CONFIG_DIR, collision_config_dict)
        return res

    def get_collision_policy(self):
        """
        Collision Policies:
            policy -> uint32
            sleep_time -> float
            gravity_time -> float
        """
        collision_policy = self._config_client.GetCollPolicy()
        if collision_policy is None:
            return None

        collision_config_dict = Common.Utils.load_json(Common.Config().COLLISION_CONFIG_DIR)
        if collision_config_dict is None:
            collision_config_dict = dict()

        collision_config_dict['sleepTime'] = collision_policy['sleep_time']
        collision_config_dict['gravity_time'] = collision_policy['gravity_time']
        collision_config_dict['policy'] = collision_policy['policy']
        return collision_config_dict

    def set_tool_property(self, mass: float, center_of_mass: list, inertia: list):
        res = self._config_client.SetToolProperty(
            mass=mass,
            center_of_mass=center_of_mass,
            inertia=inertia
        )
        if res is not None:
            tool_property = dict(
                mass=mass,
                center_of_mass=center_of_mass,
                inertia=inertia
            )
            Common.Utils.write_json(Common.Config().TOOL_PROPERTY_DIR, tool_property)
        return res

    def get_tool_property(self):
        """
        Tool Properties:
            mass   -> float
            center_of_mass   -> float[3]
            inertia   -> float[6]
        """
        tool_property = self._config_client.GetToolProperty()
        return tool_property

    def set_mount_angles(self, rot_y: float, rot_z: float):
        res = self._config_client.SetMountPos(rot_y=rot_y,
                                              rot_z=rot_z)
        if res is not None:
            mount_angle_config = dict(rot_y=rot_y, rot_z=rot_z)
            Common.Utils.write_json(Common.Config().MOUNT_ANGLE_DIR, mount_angle_config)
        return res

    def get_mount_angles(self):
        """
        Mounting Angles:
            rot_y   -> float
            rot_z   -> float
        """
        mounting_angles = self._config_client.GetMountPos()
        if mounting_angles is None:
            return None

        mount_angle_config = dict(
            rot_y=mounting_angles['ry'], rot_z=mounting_angles['rz']
        )
        return mount_angle_config

    def set_ft_sensor_config(self, dev_type, com_type, ip_address,
                             ft_frame_translation_offset_x: float,
                             ft_frame_translation_offset_y: float,
                             ft_frame_translation_offset_z: float,
                             ft_frame_rotation_offset_r: float,
                             ft_frame_rotation_offset_p: float,
                             ft_frame_rotation_offset_y: float):

        res = self._config_client.SetFTSensorConfig(dev_type=dev_type,
                                                    com_type=com_type,
                                                    ip_address=ip_address,
                                                    ft_frame_translation_offset_x=ft_frame_translation_offset_x,
                                                    ft_frame_translation_offset_y=ft_frame_translation_offset_y,
                                                    ft_frame_translation_offset_z=ft_frame_translation_offset_z,
                                                    ft_frame_rotation_offset_r=ft_frame_rotation_offset_r,
                                                    ft_frame_rotation_offset_p=ft_frame_rotation_offset_p,
                                                    ft_frame_rotation_offset_y=ft_frame_rotation_offset_y)
        if res is not None:
            ft_sensor_type_config = dict(ft_sensor_type=dev_type, ft_com_type=com_type, ip_address=ip_address)
            Common.Utils.write_json(Common.Config().FT_TYPE_DIR, ft_sensor_type_config)

            ft_sensor_frame_config = dict(translation_x=ft_frame_translation_offset_x,
                                          translation_y=ft_frame_translation_offset_y,
                                          translation_z=ft_frame_translation_offset_z,
                                          rotation_r=ft_frame_rotation_offset_r,
                                          rotation_p=ft_frame_rotation_offset_p,
                                          rotation_y=ft_frame_rotation_offset_y)
            Common.Utils.write_json(Common.Config().FT_FRAME_DIR, ft_sensor_frame_config)

        return res

    def get_ft_sensor_config(self):
        """
        Mounting Angles:
            rot_y   -> float
            rot_z   -> float
        """
        ft_config = self._config_client.GetFTSensorConfig()
        if ft_config is None:
            return None
        return ft_config

    def set_auto_servooff_config(self, enable: bool, time: float):
        res = self._config_client.SetAutoServoOff(enable=enable, time=time)
        if res is not None:
            Common.Utils.write_json(Common.Config().AUTO_SERVO_OFF_DIR, dict(
                enable=enable, time=time
            ))
        return res

    def get_auto_servooff_config(self):
        """
        Auto Servo-Off Config
            enable -> bool
            time -> float
        """
        autooff_config = self._config_client.GetAutoServoOff()
        return autooff_config

    def set_joint_control_gains(self, kp, kv, kl2):
        res = self._config_client.SetJointControlGain(
            kp=list(kp), kv=list(kv), kl2=list(kl2)
        )

        if res is not None:
            control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
            if control_gain_dict is None:
                control_gain_dict = dict()

            control_gain_dict['jointGain'] = {}
            control_gain_dict['jointGain']['index'] = [i for i in range(len(kp))]
            control_gain_dict['jointGain']['kp'] = list(kp)
            control_gain_dict['jointGain']['kv'] = list(kv)
            control_gain_dict['jointGain']['invL2Sqr'] = list(kl2)
            Common.Utils.write_json(Common.Config().CONTROL_GAIN_DIR, control_gain_dict)
        return res

    def get_joint_control_gains(self):
        """
        Joint Control Gains:
            kp   -> float[6]
            kv   -> float[6]
            kl2  -> float[6]
        """
        joint_gain_dict = None
        joint_gains = self._config_client.GetJointControlGain()
        if joint_gains is not None:
            joint_gain_dict = dict(kp=joint_gains['kp'], kv=joint_gains['kv'], kl2=joint_gains['kl2'])
        # control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
        # if control_gain_dict is None:
        #     joint_gains = self._config_client.GetJointControlGain()
        #     if joint_gains is not None:
        #         joint_gain_dict = dict(kp=joint_gains['kp'], kv=joint_gains['kv'], kl2=joint_gains['kl2'])
        # else:
        #     joint_gain_dict = dict()
        #     joint_gain_dict['kp'] = control_gain_dict['jointGain']['kp']
        #     joint_gain_dict['kv'] = control_gain_dict['jointGain']['kv']
        #     joint_gain_dict['kl2'] = control_gain_dict['jointGain']['invL2Sqr']
        return joint_gain_dict

    def set_task_control_gains(self, kp, kv, kl2):
        res = self._config_client.SetTaskControlGain(
            kp=list(kp), kv=list(kv), kl2=list(kl2)
        )

        if res is not None:
            control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
            if control_gain_dict is None:
                control_gain_dict = dict()
            control_gain_dict['taskGain'] = {}
            control_gain_dict['taskGain']['jointType'] = {}
            control_gain_dict['taskGain']['jointType']['index'] = [i for i in range(len(kp))]
            control_gain_dict['taskGain']['jointType']['kp'] = list(kp)
            control_gain_dict['taskGain']['jointType']['kv'] = list(kv)
            control_gain_dict['taskGain']['jointType']['invL2Sqr'] = list(kl2)
            Common.Utils.write_json(Common.Config().CONTROL_GAIN_DIR, control_gain_dict)
        return res

    def get_task_control_gains(self):
        """
        Task Control Gains:
            kp   -> float[6]
            kv   -> float[6]
            kl2  -> float[6]
        """
        task_gain_dict = None
        task_gains = self._config_client.GetTaskControlGain()
        if task_gains is not None:
            task_gain_dict = dict(kp=task_gains['kp'], kv=task_gains['kv'], kl2=task_gains['kl2'])
        # control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
        # if control_gain_dict is None:
        #     task_gains = self._config_client.GetTaskControlGain()
        #     if task_gains is not None:
        #         task_gain_dict = dict(kp=task_gains['kp'], kv=task_gains['kv'], kl2=task_gains['kl2'])
        # else:
        #     task_gain_dict = dict()
        #     task_gain_dict['kp'] = control_gain_dict['taskGain']['jointType']['kp']
        #     task_gain_dict['kv'] = control_gain_dict['taskGain']['jointType']['kv']
        #     task_gain_dict['kl2'] = control_gain_dict['taskGain']['jointType']['invL2Sqr']
        return task_gain_dict

    def set_impedance_control_gains(self, mass, damping, stiffness, kl2):
        res = self._config_client.SetImpedanceControlGain(
            mass=list(mass), damping=list(damping), stiffness=list(stiffness),
            kl2=list(kl2)
        )
        if res is not None:
            control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
            if control_gain_dict is None:
                control_gain_dict = dict()

            axis_name = ['x', 'y', 'z', 'u', 'v', 'w']
            control_gain_dict['impedanceGain'] = {}
            control_gain_dict['impedanceGain']['index'] = axis_name
            control_gain_dict['impedanceGain']['mass'] = list(mass)
            control_gain_dict['impedanceGain']['damping'] = list(damping)
            control_gain_dict['impedanceGain']['stiffness'] = list(stiffness)
            control_gain_dict['impedanceGain']['invL2Sqr'] = list(kl2)
            Common.Utils.write_json(Common.Config().CONTROL_GAIN_DIR, control_gain_dict)
        return res

    def get_impedance_control_gains(self):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        impedance_gain_dict = None
        impedance_gains = self._config_client.GetImpedanceControlGain()
        if impedance_gains is not None:
            impedance_gain_dict = dict(
                mass=impedance_gains['mass'],
                damping=impedance_gains['damping'],
                stiffness=impedance_gains['stiffness'],
                kl2=impedance_gains['kl2']
            )
        # control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
        # if control_gain_dict is None:
        #     impedance_gains = self._config_client.GetImpedanceControlGain()
        #     if impedance_gains is not None:
        #         impedance_gain_dict = dict(
        #             mass=impedance_gains['mass'],
        #             damping=impedance_gains['damping'],
        #             stiffness=impedance_gains['stiffness'],
        #             kl2=impedance_gains['kl2']
        #         )
        # else:
        #     impedance_gain_dict = dict()
        #     impedance_gain_dict['mass'] = control_gain_dict['impedanceGain']['mass']
        #     impedance_gain_dict['damping'] = control_gain_dict['impedanceGain']['damping']
        #     impedance_gain_dict['stiffness'] = control_gain_dict['impedanceGain']['stiffness']
        #     impedance_gain_dict['kl2'] = control_gain_dict['impedanceGain']['invL2Sqr']

        return impedance_gain_dict

    def set_force_control_gains(self, kp, kv, kl2, mass, damping, stiffness, kpf, kif):
        res = self._config_client.SetForceControlGain(
            kp=list(kp), kv=list(kv), kl2=list(kl2), mass=list(mass), damping=list(damping),
            stiffness=list(stiffness), kpf=list(kpf), kif=list(kif)
        )
        if res is not None:
            control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
            if control_gain_dict is None:
                control_gain_dict = dict()

            control_gain_dict['forceGain'] = {'jointType': {}}
            control_gain_dict['forceGain']['jointType']['index'] = [i for i in range(len(kp))]
            control_gain_dict['forceGain']['jointType']['kp'] = list(kp)
            control_gain_dict['forceGain']['jointType']['kv'] = list(kv)
            control_gain_dict['forceGain']['jointType']['invL2Sqr'] = list(kl2)
            control_gain_dict['forceGain']['jointType']['mass'] = list(mass )
            control_gain_dict['forceGain']['jointType']['damping'] = list(damping )
            control_gain_dict['forceGain']['jointType']['stiffness'] = list(stiffness)
            control_gain_dict['forceGain']['jointType']['kpf'] = list(kpf)
            control_gain_dict['forceGain']['jointType']['kif'] = list(kif)
            Common.Utils.write_json(Common.Config().CONTROL_GAIN_DIR, control_gain_dict)
        return res

    def get_force_control_gains(self):
        """
        Impedance Control Gains:
            mass   -> float[6]
            damping   -> float[6]
            stiffness   -> float[6]
            kl2  -> float[6]
        """
        force_gain_dict = None
        force_gains = self._config_client.GetForceControlGain()
        if force_gains is not None:
            force_gain_dict = dict(
                kp=force_gains['kp'],
                kv=force_gains['kv'],
                kl2=force_gains['kl2'],
                mass=force_gains['mass'],
                damping=force_gains['damping'],
                stiffness=force_gains['stiffness'],
                kpf=force_gains['kpf'],
                kif=force_gains['kif']
            )
        # control_gain_dict = Common.Utils.load_json(Common.Config().CONTROL_GAIN_DIR)
        # if control_gain_dict is None:
        #     force_gains = self._config_client.GetForceControlGain()
        #     if force_gains is not None:
        #         force_gain_dict = dict(
        #             kp=force_gains['kp'],
        #             kv=force_gains['kv'],
        #             kl2=force_gains['kl2'],
        #             mass=force_gains['mass'],
        #             damping=force_gains['damping'],
        #             stiffness=force_gains['stiffness'],
        #             kpf=force_gains['kpf'],
        #             kif=force_gains['kif']
        #         )
        # else:
        #     force_gain_dict = dict()
        #     force_gain_dict['kp'] = control_gain_dict['forceGain']['jointType']['kp']
        #     force_gain_dict['kv'] = control_gain_dict['forceGain']['jointType']['kv']
        #     force_gain_dict['kl2'] = control_gain_dict['forceGain']['jointType']['invL2Sqr']
        #     force_gain_dict['mass'] = control_gain_dict['forceGain']['jointType']['mass']
        #     force_gain_dict['damping'] = control_gain_dict['forceGain']['jointType']['damping']
        #     force_gain_dict['stiffness'] = control_gain_dict['forceGain']['jointType']['stiffness']
        #     force_gain_dict['kpf'] = control_gain_dict['forceGain']['jointType']['kpf']
        #     force_gain_dict['kif'] = control_gain_dict['forceGain']['jointType']['kif']
        return force_gain_dict

    def set_tele_op_params(self, smooth_factor, cutoff_freq, error_gain):
        res = self._config_client.SetTeleOpParams(smooth_factor, cutoff_freq, error_gain)
        if res is not None:
            tele_op_params_dict = Common.Utils.load_json(Common.Config().TELE_OP_PARAMS_DIR)
            if tele_op_params_dict is None:
                tele_op_params_dict = dict()

            tele_op_params_dict['smooth_factor'] = smooth_factor
            tele_op_params_dict['cuttoff_freq'] = cutoff_freq
            tele_op_params_dict['error_gain'] = error_gain
            Common.Utils.write_json(Common.Config().TELE_OP_PARAMS_DIR, tele_op_params_dict)
        return res

    def get_tele_op_params(self):
        return self._config_client.GetTeleOpParams()

    def set_safety_limit_config(self, power_limit, power_limit_ratio,
                                tcp_force_limit, tcp_force_limit_ratio,
                                tcp_speed_limit, tcp_speed_limit_ratio):
        res = self._config_client.SetSafetyLimits(
            power_limit=power_limit, power_limit_ratio=power_limit_ratio,
            tcp_force_limit=tcp_force_limit, tcp_force_limit_ratio=tcp_force_limit_ratio,
            tcp_speed_limit=tcp_speed_limit, tcp_speed_limit_ratio=tcp_speed_limit_ratio  # ,
            # joint_limits=list(self._joint_limits_default)
        )
        if res is not None:
            safety_limit_config_dict = Common.Utils.load_json(Common.Config().SAFETY_CONFIG_DIR)
            if safety_limit_config_dict is None:
                safety_limit_config_dict = dict()

            safety_limit_config_dict['powerLimit']['limit'] = power_limit
            safety_limit_config_dict['powerLimit']['reducedRatio'] = power_limit_ratio
            safety_limit_config_dict['tcpForceLimit']['limit'] = tcp_force_limit
            safety_limit_config_dict['tcpForceLimit']['reducedRatio'] = tcp_force_limit_ratio
            safety_limit_config_dict['tcpSpeedLimit']['limit'] = tcp_speed_limit
            safety_limit_config_dict['tcpSpeedLimit']['reducedRatio'] = tcp_speed_limit_ratio

            Common.Utils.write_json(Common.Config().SAFETY_CONFIG_DIR, safety_limit_config_dict)
        return res

    def get_safety_limit_config(self):
        """
        Safety Limits:
            power_limit             -> float
            power_limit_ratio       -> float
            tcp_force_limit         -> float
            tcp_force_limit_ratio   -> float
            tcp_speed_limit         -> float
            tcp_speed_limit_ratio   -> float
            joint_upper_limits   -> float[]
            joint_lower_limits   -> float[]
        """
        safety_limits = self._config_client.GetSafetyLimits()

        return safety_limits

    def set_safety_stop_config(self, joint_position_limit_stop_cat, joint_speed_limit_stop_cat,
                               joint_torque_limit_stop_cat, tcp_speed_limit_stop_cat,
                               tcp_force_limit_stop_cat, power_limit_stop_cat):
        res = self._config_client.SetSafetyStopConfig(
            jpos_limit_stop_cat=joint_position_limit_stop_cat,
            jvel_limit_stop_cat=joint_speed_limit_stop_cat,
            jtau_limit_stop_cat=joint_torque_limit_stop_cat,
            tvel_limit_stop_cat=tcp_speed_limit_stop_cat,
            tforce_limit_stop_cat=tcp_force_limit_stop_cat,
            power_limit_stop_cat=power_limit_stop_cat,
        )
        if res is not None:
            safety_stop_config_dict = Common.Utils.load_json(Common.Config().SAFETY_CONFIG_DIR)
            if safety_stop_config_dict is None:
                safety_stop_config_dict = dict()

            safety_stop_config_dict['safeState']['jointPosLimit'] = joint_position_limit_stop_cat
            safety_stop_config_dict['safeState']['jointVelLimit'] = joint_speed_limit_stop_cat
            safety_stop_config_dict['safeState']['jointTorLimit'] = joint_torque_limit_stop_cat
            safety_stop_config_dict['safeState']['tcpSpeedLimit'] = tcp_speed_limit_stop_cat
            safety_stop_config_dict['safeState']['tcpForceLimit'] = tcp_force_limit_stop_cat
            safety_stop_config_dict['safeState']['powerLimit'] = power_limit_stop_cat

            Common.Utils.write_json(Common.Config().SAFETY_CONFIG_DIR, safety_stop_config_dict)
        return res

    def get_safety_stop_config(self):
        """
        Safety Stop Category:
            joint_position_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            joint_speed_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            joint_torque_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            tcp_speed_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            tcp_force_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
            power_limit_stop_cat = IMMEDIATE_BRAKE(0) | SMOOTH_BRAKE(1) | SMOOTH_ONLY(2)
        """
        safety_stop_config = self._config_client.GetSafetyStopConfig()
        return safety_stop_config

    def get_reduced_ratio(self):
        return self._config_client.GetReducedRatio()

    def get_reduced_speed(self):
        return self._config_client.GetReducedSpeed()

    def set_reduced_speed(self, speed):
        safety_stop_config_dict = Common.Utils.load_json(Common.Config().SAFETY_CONFIG_DIR)
        safety_stop_config_dict['reducedSpeed'] = speed * 1e-3
        Common.Utils.write_json(Common.Config().SAFETY_CONFIG_DIR, safety_stop_config_dict)
        Common.Config().update_conversion()
        return self._config_client.SetReducedSpeed(speed)

    def get_safety_hash(self):
        concatenated_content = ""
        if os.path.isfile(Common.Config().SAFETY_CONFIG_DIR):
            with open(Common.Config().SAFETY_CONFIG_DIR, 'r', encoding='utf-8') as file:
                concatenated_content += file.read()
        if os.path.isfile(Common.Config().CONTROL_GAIN_DIR):
            with open(Common.Config().CONTROL_GAIN_DIR, 'r', encoding='utf-8') as file:
                concatenated_content += file.read()
        if os.path.isfile(Common.Config().COLLISION_CUSTOM_DIR):
            with open(Common.Config().COLLISION_CUSTOM_DIR, 'r', encoding='utf-8') as file:
                concatenated_content += file.read()
        hash_value = self.fnv1a_24(concatenated_content)
        self.__logger.debug(f"FNV-1a Hash: {hash_value:04X}")
        base62_hash = self.to_base62(hash_value, 4)
        self.__logger.debug(f"FNV-1a 24-bit Base62 Hash: {base62_hash}")
        return base62_hash

    def get_kinematics_params(self):
        return self._config_client.GetKinematicsParams()

    # FNV-1a 24비트 해시 함수
    def fnv1a_24(self, data: str) -> int:
        FNV_prime = 0x01000193
        offset_basis = 0x811C9DC5
        hash = offset_basis

        for byte in data.encode('utf-8'):
            hash ^= byte
            hash *= FNV_prime
            hash &= 0xFFFFFFFF  # Ensure we remain within 32-bit range

        return hash & 0xFFFFFF  # Return only the lower 24 bits

    def to_base62(self, num: int, length: int) -> str:
        BASE62 = string.ascii_uppercase + string.ascii_lowercase + string.digits
        base62 = []
        while num:
            num, rem = divmod(num, 62)
            base62.append(BASE62[rem])
        while len(base62) < length:
            base62.append('0')
        return ''.join(reversed(base62))
