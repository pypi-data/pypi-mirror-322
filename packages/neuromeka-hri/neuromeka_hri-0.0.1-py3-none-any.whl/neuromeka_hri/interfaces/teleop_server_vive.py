## Includes: common, interface
## Requirements: numpy scipy netifaces openvr
## Requirements: protobuf==3.19.4 grpcio==1.34.1 grpcio-tools==1.34.1
## Need to remove: condy_servicer.py
import sys
if sys.version_info >= (3, 9):
    from neuromeka.proto import *
else:
    from neuromeka.proto_step import *

import grpc
from concurrent import futures

from neuromeka_hri.interfaces.control_socket_client import ControlSocketClient
from neuromeka_hri.interfaces.config_socket_client import ConfigSocketClient
from neuromeka_hri.interfaces.rtde_socket_client import RTDESocketClient
from neuromeka_hri.interfaces.vive import triad_openvr

import time
from datetime import datetime
import numpy as np
from scipy.spatial.transform import Rotation
from threading import Thread

# DEVICE_NAME = "controller_1"
# DEVICE_NAME = "tracker_1"
TRIGGE_NAME = "menu_button"
CONTROL_PERIOD = 0.02
VEL_SCALE = 0.3
ACC_SCALE = 10.0
DEVICE_PORT = 20500
ERROR_TIME = 5.0

class TeleOpDeviceServicer(TeleOpDeviceServicer):
    ip_indy: str
    port_indy: str
    control: ControlSocketClient
    config: ConfigSocketClient
    rtde: RTDESocketClient
    _thread: Thread
    _stop_stream: bool

    def __init__(self, device_name="controller_1", device_port=DEVICE_PORT):
        self.device_name = device_name
        self.device_port = device_port
        print(self.device_name, self.device_port)
        self.ip_indy = None
        self.port_indy = None
        self.control = None
        self.config = None
        self._stop_stream = False
        self._stream_running = False
        self.init_vive()
        self._error_lasttime = False
        self.pos_vive = None
        self.pos_robot = None
        self.isOffset_for_save = False
        self.prev_value = None
        self.offset_for_jump = None
        self.filename_vive = f"./saved_data/pos_vive_data/star_data_vive_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"
        self.filename_robot = f"./saved_data/pos_robot_data/star_data_robot_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"
        self.start_time = None

    def StartTeleOpStream(self, request: teleop_data.TeleOpStreamReq, context) -> teleop_data.Response:
        if self._stream_running and self._thread is not None:
            if self.ip_indy == request.ip_indy:
                print(f"StartTeleOpStream re-requested from {request.ip_indy}:{request.port}")
                return teleop_data.Response()
            self._stop_stream = True
            self._thread.join()
        print(f"StartTeleOpStream to {request.ip_indy}:{request.port}")
        self.ip_indy = request.ip_indy
        self.port_indy = request.port
        self.control = ControlSocketClient(self.ip_indy, port=self.port_indy)
        self.rtde = RTDESocketClient(self.ip_indy)
        self.config = ConfigSocketClient(self.ip_indy, port=self.port_indy)
        self._stop_stream = False
        self._thread = Thread(target=self._stream_fun, daemon=True)
        self._thread.start()
        return teleop_data.Response()

    def StopTeleOpStream(self, request: teleop_data.Empty, context) -> teleop_data.Response:
        print(f"StopTeleOpStream to {self.ip_indy}")
        self._stop_stream = True
        return teleop_data.Response()
    
    def save_data(self):
        if not hasattr(self, 'isOffset_for_save') or not self.isOffset_for_save:
            self.offset_vive = np.array(self.pos_vive[0:3])  
            self.offset_robot = np.array(self.pos_robot[0:3])
            self.isOffset_for_save = True
            self.start_time = time.time()
 
        pos_vive_save = self.pos_vive[:]
        pos_robot_save = self.pos_robot[:]
        pos_vive_save[0:3] = np.array(self.pos_vive[0:3]) - self.offset_vive
        pos_robot_save[0:3] = np.array(self.pos_robot[0:3]) - self.offset_robot

        elapsed_time_ms = int((time.time() - self.start_time) * 1000)
        info_with_time_pos_vive = [elapsed_time_ms] + list(pos_vive_save)
        info_with_time_pos_robot = [elapsed_time_ms] + list(pos_robot_save)

        with open(self.filename_vive, "a") as file:
            file.write(",".join(map(str, info_with_time_pos_vive)) + "\n")
        with open(self.filename_robot, "a") as file:
            file.write(",".join(map(str, info_with_time_pos_robot)) + "\n")
 
    def checkErr(self, value):
        value = np.array(value)
        if self.prev_value is None:
            self.prev_value = value
            self.offset_for_jump = np.zeros_like(value)
            return value
        diff = np.abs(value[:3] - self.prev_value[:3])
        if np.any(diff > 50): 
            print(f"Sudden change detected, {diff}")
            self.offset_for_jump[:3] += value[:3] - self.prev_value[:3]  
            adjusted_value = value - np.concatenate((self.offset_for_jump[:3], np.zeros_like(value[:3])))
        else:
            adjusted_value = value - np.concatenate((self.offset_for_jump[:3], np.zeros_like(value[:3])))
        self.prev_value = value
 
        return adjusted_value

    def _stream_fun(self):
        self._stream_running = True
        time_last = time.time()
        self._error_count = 0
        while not self._stop_stream:
            try:
                step_time = time.time() - time_last
                if step_time > CONTROL_PERIOD:
                    enable = self.get_vive_input()
                    value = self.get_vive_pose()
                    self.pos_vive = self.checkErr(value)
                    # self.pos_vive = value
                    res = self.control.EnableTeleKey(enable)
                    if res is not None:
                        # self.config.SetToolFrame([0,0,58,0,0,0])
                        # print(self.pos_vive)
                        res = self.control.MoveTeleLRec(self.pos_vive, VEL_SCALE, ACC_SCALE)
                    if res is None:
                        raise(RuntimeError("Communication Failure"))

                    self.pos_robot = self.rtde.GetControlData()['p']
                    if self.rtde.GetControlData()['op_state'] == 17:
                        self.save_data()

                else:
                    time.sleep(CONTROL_PERIOD - step_time)
                self._error_lasttime = False
                self._error_count = 0
            except Exception as e:
                if not self._error_lasttime:
                    self._error_lasttime = True
                    print(f'Error in stream {e}')
                self._error_count += 1
                if self._error_count > 10:
                    print(f'Stop Stream By Error')
                    self._stop_stream = True
        self._stream_running = False

    def init_vive(self):
        self.v = triad_openvr.triad_openvr()
        self.v.print_discovered_objects()

        for i in range(200):
            self.v.devices[self.device_name].trigger_haptic_pulse()
            time.sleep(0.01)

    def get_vive_input(self):
        controller_inputs = self.v.devices[self.device_name].get_controller_inputs()
        # print(f"controller_inputs keys: {controller_inputs}")
        return controller_inputs[TRIGGE_NAME]

    def get_vive_pose(self):
        vivePose = self.v.devices[self.device_name].get_pose_matrix()
        pos = np.multiply(1000, [vivePose.m[0][3], vivePose.m[1][3], vivePose.m[2][3]]).tolist()
        rotMat = np.array([[vivePose.m[0][0], vivePose.m[0][1], vivePose.m[0][2]],
                           [vivePose.m[1][0], vivePose.m[1][1], vivePose.m[1][2]],
                           [vivePose.m[2][0], vivePose.m[2][1], vivePose.m[2][2]]])
        rot = np.rad2deg(Rotation.from_matrix(rotMat).as_euler("xyz")).tolist()

        return pos + rot


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         options=
                         [('grpc.max_send_message_length', 10 * 1024 * 1024),
                          ('grpc.max_receive_message_length', 10 * 1024 * 1024)]
                         )
    servicer = TeleOpDeviceServicer()
    add_TeleOpDeviceServicer_to_server(servicer=servicer, server=server)

    server.add_insecure_port('[::]:{}'.format(DEVICE_PORT))
    server.start()
