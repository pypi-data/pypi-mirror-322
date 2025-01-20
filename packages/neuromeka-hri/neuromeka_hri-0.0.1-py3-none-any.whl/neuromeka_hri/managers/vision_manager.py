# import common
import neuromeka_hri.common as Common

from ext_parties.indyeye import IndyEyeClient
from ext_parties.indyeye import IndyWeldClient

import numpy as np
# from neuromeka import IndyEye as IndyEyeClient
from neuromeka_hri.common.utils import pos_to_transform, transform_to_pos
from neuromeka_hri.managers.config_manager import ConfigManager

class VisionManager(metaclass=Common.SingletonMeta):
    INDYEYE = 0
    PICKIT = 1

    def __init__(self):
        super().__init__()
        self._vision_dict = {}
        self._object_dict = {}
        self._m_config = ConfigManager()
        vision_servers = self._m_config.load_vision_server_list()
        # print("vision server json: ", vision_servers)
        # auto add if vision servers exist
        if vision_servers:
            for vision_server in vision_servers['vision_servers']:
                self.add_vision(
                    vision_name=vision_server['name'],
                    vision_type=vision_server['vision_server_type'],
                    ip=vision_server['ip'],
                    port=vision_server['port'],
                )
                # print("Add Vision: ", vision_server['name'])
        # self.add_vision(
        #     vision_name="IndyEye",
        #     vision_type=0,
        #     ip="192.168.1.14",
        #     port="10511",
        # )

    def add_vision(self, vision_name, vision_type, ip, port):
        if vision_type == VisionManager.INDYEYE:
            self._vision_dict[vision_name] = IndyEyeClient(ip=ip, port=port)
        elif vision_type == VisionManager.PICKIT:
            pass
        else:
            pass

    def clear_vision(self):
        self._vision_dict = {}

    def get_image(self, vision_name, request_type):
        if vision_name in self._vision_dict.keys():
            if isinstance(self._vision_dict[vision_name], IndyEyeClient):
                return self._vision_dict[vision_name].get_image(request_type=request_type)
        else:
            raise Exception("There is no vision named {}".format(vision_name))

    def detect(self, vision_name, obj_name, vision_frame, task_pos, ref_frame, tool_frame, robot_ip=None):
        # vision_name: str .Ex: "IndyEye"
        # target_name: str .Ex: "xylitol"
        # vision_frame: 0: obj, 1: ee
        # task_pos: xyzuvw .current end-effector pose: x,y,z,u,v,w, (unit: mm, deg)
        # ref_frame: xyzuvw .current reference frame: x,y,z,u,v,w, (unit: mm, deg)
        # tool_frame: xyzuvw .current tool frame: x,y,z,u,v,w, (unit: mm, deg)
        # robot_ip: ip of robot from the xavier side, for multi-robot case
        # return: resulting task pose, detected, passed, err (x,y,z,u,v,w, (unit: mm, deg))
        if vision_name in self._vision_dict.keys():
            if isinstance(self._vision_dict[vision_name], IndyEyeClient):
                obj_name_list = self.get_object_list(vision_name)
                obj_index = obj_name_list.index(obj_name)
                task_pos = pos_to_transform(task_pos)  # Trt (mm)
                ref_frame = pos_to_transform(ref_frame)  # Tbr (mm)
                tool_frame = pos_to_transform(tool_frame)  # Tet (mm)
                self.ref_frame, self.tool_frame = ref_frame, tool_frame
                # pure robot task pose: Tbe = Tbr * Trt * inv(Tet)
                robot_pos = np.matmul(np.matmul(ref_frame, task_pos),np.linalg.inv(tool_frame))
                robot_pos[:3, 3] /= 1000  # convert to m
                robot_pos = transform_to_pos(robot_pos)  # Tbe
                frame, cls, detected, passed, msg = self._vision_dict[vision_name].detect_by_object_name(obj_index, vision_frame, robot_pos, robot_ip)
                if frame is not None:
                    frame[0] *= 1000  # convert to mm
                    frame[1] *= 1000  # convert to mm
                    frame[2] *= 1000  # convert to mm
                    if vision_frame == 1:  # end-effector pose case
                        frame = pos_to_transform(frame)  # Tbe (mm)
                        # robot task pose on current frames: Trt = inv(Tbr) * Tbe * Tet
                        frame = np.matmul(np.matmul(np.linalg.inv(ref_frame), frame), tool_frame)
                        frame = transform_to_pos(frame)  # Trt (mm)
                    # else:  # object pose case
                    #    frame # Tbo
                return frame, obj_name_list[cls], detected, passed, msg
            else:
                raise Exception(f"{vision_name} type vision is not implemented")
        else:
            raise Exception("There is no vision named {}".format(vision_name))

    def extract(self, vision_name, obj_name, vision_frame):
        if vision_name in self._vision_dict.keys():
            if isinstance(self._vision_dict[vision_name], IndyEyeClient):
                obj_name_list = self.get_object_list(vision_name)
                obj_index = obj_name_list.index(obj_name)
                frame, cls, detected, passed, msg = self._vision_dict[vision_name].retrieve_by_object_name(obj_index, vision_frame)
                if frame is not None:
                    frame[0] *= 1000  # convert to mm (mm)
                    frame[1] *= 1000  # convert to mm (mm)
                    frame[2] *= 1000  # convert to mm (mm)
                    if vision_frame == 1:  # end-effector pose case
                        ref_frame, tool_frame = self.ref_frame, self.tool_frame
                        frame = pos_to_transform(frame)  # Tbe (mm)
                        # robot task pose on current frames: Trt = inv(Tbr) * Tbe * Tet
                        frame = np.matmul(np.matmul(np.linalg.inv(ref_frame), frame), tool_frame)
                        frame = transform_to_pos(frame)  # Trt (mm)
                    # else:  # object pose case
                    #    frame # Tbo
                return frame, obj_name_list[cls], detected, passed, msg
            else:
                raise Exception(f"{vision_name} type vision is not implemented")
        else:
            raise Exception("There is no vision named {}".format(vision_name))

    def get_object_list(self, name):
        result = []
        if isinstance(self._vision_dict[name], IndyEyeClient):
            result = ['all'] + self._vision_dict[name].get_object_list()
            self._object_dict[name] = result
            # print("get_object_list result: ", list(self._object_dict[name]).index('xylitol'))
        else:
            pass
        return result


class PointsManager(metaclass=Common.SingletonMeta):

    def __init__(self):
        super().__init__()
        self._vision_dict = IndyWeldClient(ip="192.168.6.122", port="20133")

    def start_calibration(self):
        ret = self._vision_dict.start_calibration()
        # ret = self._vision_dict.check_calibration()
        print("calibration results ", ret)

    def detect_welding_lines(self):
        error_state, line_info, type_info = self._vision_dict.detect_welding_lines()
        return error_state, line_info, type_info

    def detect_straight_line(self):
        error_state, line_info = self._vision_dict.detect_straight_line()
        return error_state, line_info

    def detect_circular_line(self):
        error_state, line_info = self._vision_dict.detect_circular_line()
        return error_state, line_info
