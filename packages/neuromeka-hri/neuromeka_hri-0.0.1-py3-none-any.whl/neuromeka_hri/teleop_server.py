## Includes: common, interface
## Requirements: numpy scipy netifaces openvr
## Requirements: protobuf==3.19.4 grpcio==1.34.1 grpcio-tools==1.34.1
## Need to remove: condy_servicer.py
import sys
if sys.version_info >= (3, 9):
    from neuromeka.proto import *
else:
    from neuromeka.proto_step import *

import os
import socket
import netifaces
import matplotlib.pyplot as plt
from threading import Thread
import time
from datetime import datetime
import numpy as np
import grpc
from concurrent import futures
from scipy.signal import butter
from scipy.stats import pearsonr
import dtw

from neuromeka_hri.interfaces.control_socket_client import ControlSocketClient
from neuromeka_hri.interfaces.rtde_socket_client import RTDESocketClient

from neuromeka_hri.get_device_data import UDPHandler, ViveHandler

TRIGGE_NAME = "menu_button"
CONTROL_PERIOD = 0.02
VEL_SCALE = 0.8
ACC_SCALE = 10.0
DEVICE_PORT = 20500
ERROR_TIME = 5.0

start_time = None
 
def realtime_iir_filter(x, b, a, channel, x_prev, y_prev, filter_initialized):
    if not filter_initialized[channel]:
        x_prev[channel] = [x, x]
        y_prev[channel] = [x, x]
        filter_initialized[channel] = True
        return x
    x_hist = x_prev[channel]
    y_hist = y_prev[channel]
    y = b[0] * x + b[1] * x_hist[0] + b[2] * x_hist[1] - a[1] * y_hist[0] - a[2] * y_hist[1]
    x_prev[channel] = [x, x_hist[0]]
    y_prev[channel] = [y, y_hist[0]]
    return y
 
def low_pass_filter(value, b, a, x_prev, y_prev, filter_initialized):
    value = np.array(value)
    filtered_data = np.zeros_like(value)
    for channel in range(len(value)):
        filtered_data[channel] = realtime_iir_filter(value[channel], b, a, channel, x_prev, y_prev, filter_initialized)
    return filtered_data
 
def manage_Jump(value, prev_value, offset_for_jump):
    value = np.array(value)
    if prev_value is None:
        return value, offset_for_jump, value
    position_diff = value[:3] - prev_value[:3]
    angle_diff = (value[3:] - prev_value[3:] + 180) % 360 - 180
    if np.any(np.abs(position_diff) > 100):
        offset_for_jump[:3] += position_diff
    if np.any(np.abs(angle_diff) > 50):
        offset_for_jump[3:] += angle_diff
    adjusted_value = value - offset_for_jump
    return adjusted_value, offset_for_jump, value
 
def save_data(value_raw, value_adjusted, pos_robot, folder_path):
    global start_time
    elapsed_time_ms = int((time.time() - start_time) * 1000)
    info_with_time_raw = [elapsed_time_ms] + list(value_raw)
    info_with_time_adjusted = [elapsed_time_ms] + list(value_adjusted)
    info_with_time_robot = [elapsed_time_ms] + list(pos_robot)

    os.makedirs(f"{folder_path}/raw_data", exist_ok=True)
    os.makedirs(f"{folder_path}/adjusted_data", exist_ok=True)
    os.makedirs(f"{folder_path}/robot_data", exist_ok=True)
    
    timestamp = datetime.fromtimestamp(start_time).strftime('%Y_%m_%d_%H_%M_%S')
    filename_raw = f"{folder_path}/raw_data/{timestamp}.txt"
    filename_adjusted = f"{folder_path}/adjusted_data/{timestamp}.txt"
    filename_robot = f"{folder_path}/robot_data/{timestamp}.txt"
 
    with open(filename_raw, "a") as file:
        file.write(",".join(map(str, info_with_time_raw)) + "\n")
    with open(filename_adjusted, "a") as file:
        file.write(",".join(map(str, info_with_time_adjusted)) + "\n")
    with open(filename_robot, "a") as file:
        file.write(",".join(map(str, info_with_time_robot)) + "\n")
 
def load_data(folder_path, match, multi):
    timestamp = datetime.fromtimestamp(start_time).strftime('%Y_%m_%d_%H_%M_%S')
    print(f"Loading data from {timestamp}")
 
    file_path1 = f"{folder_path}/adjusted_data/{timestamp}.txt"
    file_path2 = f"{folder_path}/robot_data/{timestamp}.txt"
 
    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        return None, None
    try:
        data1 = np.loadtxt(file_path1, delimiter=",")
        data2 = np.loadtxt(file_path2, delimiter=",")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None
    
    time1 = data1[:, 0] / 1000
    time2 = data2[:, 0] / 1000
 
    controller_data = data1[:, match]
    controller_data = controller_data * multi
    robot_data = data2[:, 1:7]

    time1_offset = time1[0]
    time2_offset = time2[0]
    controller_offset = controller_data[0, :]
    robot_offset = robot_data[0, :]
 
    time1 = time1 - time1_offset
    time2 = time2 - time2_offset
    controller_data = controller_data - controller_offset
    robot_data = robot_data - robot_offset

    for i in range(3, len(controller_data[0])):
        controller_data[:, i] = np.where(controller_data[:, i] > 180, controller_data[:, i] - 360, controller_data[:, i])
        controller_data[:, i] = np.where(controller_data[:, i] < -180, controller_data[:, i] + 360, controller_data[:, i])

    for i in range(3, len(robot_data[0])):
        robot_data[:, i] = np.where(robot_data[:, i] > 180, robot_data[:, i] - 360, robot_data[:, i])
        robot_data[:, i] = np.where(robot_data[:, i] < -180, robot_data[:, i] + 360, robot_data[:, i])
        
    return time1, time2, controller_data, robot_data

def plot_data(time1, time2, controller_data, robot_data):
    # 3D Trajectory
    fig1 = plt.figure(figsize=(8, 6))
    ax_3d = fig1.add_subplot(111, projection='3d')
    ax_3d.plot(controller_data[:, 0], controller_data[:, 1], controller_data[:, 2], label='Controller value', color='orange')
    ax_3d.plot(robot_data[:, 0], robot_data[:, 1], robot_data[:, 2], label='Robot value', color='blue')
    ax_3d.set_title('3D Trajectory Plotting')
    ax_3d.set_xlabel('X')
    ax_3d.set_ylabel('Y')
    ax_3d.set_zlabel('Z')
    ax_3d.set_xlim(-150, 150)
    ax_3d.set_ylim(-150, 150)
    ax_3d.set_zlim(-150, 150)
    ax_3d.legend()
    ax_3d.grid()

    # XYZUVW 각 축별 position 플롯
    fig2, axes = plt.subplots(6, 1, figsize=(10, 12), sharex=True)
    axes_labels = ['X', 'Y', 'Z', 'U', 'V', 'W']

    for i, ax in enumerate(axes):
        ax.plot(time1, controller_data[:, i], label=f'Controller {axes_labels[i]}', linestyle='-', color='orange')
        ax.plot(time2, robot_data[:, i], label=f'Robot {axes_labels[i]}', linestyle='-', color='blue')
        ax.set_title(f"{axes_labels[i]}-Axis Comparison")
        if i<3:
            ax.set_ylim(-150, 150)
            ax.set_ylabel(f"{axes_labels[i]} (mm)")
        else:
            ax.set_ylim(-30, 30)
            
            ax.set_ylabel(f"{axes_labels[i]} (°)")
        ax.legend()
        ax.grid()

    axes[-1].set_xlabel('Time (sec)')
    fig2.tight_layout()

    plt.show()

def calculate_perform(time1, time2, controller_data, robot_data):
    axes = ['X', 'Y', 'Z', 'U', 'V', 'W']
    
    # Speed and Acceleration 
    print(f"\n=== Speed and Acceleration ===")
    # for each axis
    print(f"<For each axis>")
    for i in range(3):
        print(f"{axes[i].upper()}:")
        controller_times = np.diff(time1)
        robot_times = np.diff(time2)

        controller_speeds = np.abs(np.diff(controller_data[:, i]) / controller_times)
        robot_speeds = np.abs(np.diff(robot_data[:, i]) / robot_times)
        controller_accelerations = np.abs(np.diff(controller_speeds) / controller_times[:-1])
        robot_accelerations = np.abs(np.diff(robot_speeds) / robot_times[:-1])

        max_speed_controller = np.max(controller_speeds)  
        max_speed_robot = np.max(robot_speeds)          
        max_accel_controller = np.max(controller_accelerations) 
        max_accel_robot = np.max(robot_accelerations)          

        print(f"    Controller Max Speed: {max_speed_controller:.4f}")
        print(f"    Robot Max Speed: {max_speed_robot:.4f}")
        print(f"    Controller Max Acceleration: {max_accel_controller:.4f}")
        print(f"    Robot Max Acceleration: {max_accel_robot:.4f}\n")

    # for xyz postion vector 
    print(f"For xyz postion vector:")
    controller_distances = np.sqrt(np.sum(np.diff(controller_data[:, :3], axis=0) ** 2, axis=1))
    robot_distances = np.sqrt(np.sum(np.diff(robot_data[:, :3], axis=0) ** 2, axis=1))
    controller_times = np.diff(time1)
    robot_times = np.diff(time2)
 
    controller_speeds = controller_distances / controller_times
    robot_speeds = robot_distances / robot_times
    controller_accelerations = np.abs(np.diff(controller_speeds) / controller_times[:-1])
    robot_accelerations = np.abs(np.diff(robot_speeds) / robot_times[:-1])

    max_speed_controller = np.max(controller_speeds)  
    max_speed_robot = np.max(robot_speeds)          
    max_accel_controller = np.max(controller_accelerations) 
    max_accel_robot = np.max(robot_accelerations)          

    print(f"    Controller Max Speed: {max_speed_controller:.4f}")
    print(f"    Robot Max Speed: {max_speed_robot:.4f}")
    print(f"    Controller Max Acceleration: {max_accel_controller:.4f}")
    print(f"    Robot Max Acceleration: {max_accel_robot:.4f}\n")

    # RMSE
    print(f"\n=== RMSE ===")
    for i in range(6):
        rmse = np.sqrt(np.mean((controller_data[:, i] - robot_data[:, i]) ** 2))
        print(f"{axes[i].upper()}: {rmse:.4f}")

    # PCC
    print(f"\n=== PCC & R^2 ===")
    print("(If P-Value>0.05, the correlation is weak.)\n")
    for i in range(6):
        print(f"{axes[i].upper()}:")
        pearson_corr, p_value = pearsonr(controller_data[:, i], robot_data[:, i])
        print(f"    PCC: {pearson_corr:.4f}")
        print(f"    R^2: {pearson_corr*pearson_corr:.4f}")
        print(f"    P-Value: {p_value:.4f}")

    # DTW
    print(f"\n=== Normalized DTW ===")
    for i in range(6):
        alignment = dtw.dtw(controller_data[:, i], robot_data[:, i], keep_internals=False)
        dtw_value = alignment.distance
        normalized_dtw = dtw_value / len(alignment.index1)
        print(f"{axes[i].upper()}: {normalized_dtw:.4f}")
 
class PhoneManager():
    def __init__(self):
        self.prev_value = None
        self.offset_for_jump = np.zeros(6)
        self.folder_path = "./dataList"
        self.save_count = 0
        self.x_prev = [[0.0, 0.0] for _ in range(6)]
        self.y_prev = [[0.0, 0.0] for _ in range(6)]
        self.filter_initialized = [False] * 6
        self.fs = 50.0
        self.fc = 3.0
        self.wn = self.fc / (self.fs / 2)
        self.b, self.a = butter(2, self.wn, btype='low', analog=False)
        self.udp = UDPHandler()
        self.udp.init_udp()
 
    def get_data(self):
        return self.udp.pos_rot, self.udp.val_detect, self.udp.val_enable
   
    def adjust_value(self, value):
        adjusted_value, self.offset_for_jump, self.prev_value = manage_Jump(value, self.prev_value, self.offset_for_jump)
        return low_pass_filter(adjusted_value, self.b, self.a, self.x_prev, self.y_prev, self.filter_initialized)
    
    def save_data(self, value_raw, value_adjusted, pos_robot):
        save_data(value_raw, value_adjusted, pos_robot, self.folder_path)
 
    def plot_data(self):
        try:
            time1, time2, controller_data, robot_data = load_data(self.folder_path, [1, 3, 2, 6, 5, 4], [1, -1, 1, 1, -1, -1])
            if controller_data is None or robot_data is None:
                print("No data available for plotting.")
                return
            plot_data(time1, time2, controller_data, robot_data)
        except Exception as e:
            print(f"Error while plotting data: {e}")
 
    def calculate_perform(self):
        try:
            time1, time2, controller_data, robot_data = load_data(self.folder_path, [1, 3, 2, 6, 5, 4], [1, -1, 1, 1, -1, -1])
            if controller_data is None or robot_data is None:
                print("No data available for calculating performance")
                return
            calculate_perform(time1, time2, controller_data, robot_data)
        except Exception as e:
            print(f"Error while calculating performance: {e}")
        
class ViveManager():
    def __init__(self):
        self.prev_value = None
        self.offset_for_jump = np.zeros(6)
        self.folder_path = "./dataList_vive"
        self.vive = ViveHandler()
        self.vive.init_vive()
 
    def get_data(self):
        return self.vive.get_vive_pose(), True, self.vive.get_vive_input()
   
    def adjust_value(self, value):
        adjusted_value, self.offset_for_jump, self.prev_value = manage_Jump(value, self.prev_value, self.offset_for_jump)
        return adjusted_value
    
    def save_data(self, value_raw, value_adjusted, pos_robot):
        save_data(value_raw, value_adjusted, pos_robot, self.folder_path)
 
    def plot_data(self):
        try:
            time1, time2, controller_data, robot_data = load_data(self.folder_path, [1, 3, 2, 4, 6, 5], [-1, 1, 1, -1, 1, 1])
            if controller_data is None or robot_data is None:
                print("No data available for plotting.")
                return
            plot_data(time1, time2, controller_data, robot_data)
        except Exception as e:
            print(f"Error while plotting data: {e}")
 
    def calculate_perform(self):
        try:
            time1, time2, controller_data, robot_data = load_data(self.folder_path, [1, 3, 2, 4, 6, 5], [-1, 1, 1, -1, 1, 1])
            if controller_data is None or robot_data is None:
                print("No data available for calculating performance")
                return
            calculate_perform(time1, time2, controller_data, robot_data)
        except Exception as e:
            print(f"Error while calculating performance: {e}")
 
class TeleOpDeviceServicer(TeleOpDeviceServicer):
    ip_indy: str
    port_indy: str
    control: ControlSocketClient
    rtde: RTDESocketClient
    _thread: Thread
    _stop_stream: bool
   
    def __init__(self, device_type):
        self.device = PhoneManager() if device_type == "phone" else ViveManager()
        self.ip_indy = None
        self.port_indy = None
        self.control = None
        self.rtde = None
        self._stop_stream = False
        self._stream_running = False
        self._thread = None
        self.value_raw = None
        self.value_adjusted = None
        self.pos_robot = None
        self.save_enabled = False
           
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
        self._stop_stream = False
        self._thread = Thread(target=self._stream_fun, daemon=True)
        self._thread.start()
        return teleop_data.Response()
           
    def StopTeleOpStream(self, request: teleop_data.Empty, context) -> teleop_data.Response:
        print(f"StopTeleOpStream to {self.ip_indy}")
        self._stop_stream = True
        if self._thread and self._thread.is_alive():
            self._thread.join()
        return teleop_data.Response()
   
    def _stream_fun(self):
        self._stream_running = True
        self._error_count = 0
        time_last = time.time()
        while not self._stop_stream:
            try:
                step_time = time.time() - time_last
                if step_time > CONTROL_PERIOD:
                    self.value_raw, detecv, enable = self.device.get_data()
                    self.value_adjusted = self.device.adjust_value(self.value_raw)
 
                    res = self.control.EnableTeleKey(enable)
                    if res is not None and detecv is not False and enable is not None:
                        res = self.control.MoveTeleLRec(self.value_adjusted, VEL_SCALE, ACC_SCALE)
                    if res is None:
                        raise(RuntimeError("Communication Failure"))
                    
                    self.pos_robot = self.rtde.GetControlData()['p']
                    if self.save_enabled and self.rtde.GetControlData()['op_state']==17 and enable:
                        # if not enable:
                        self.device.save_data(self.value_raw, self.value_adjusted, self.pos_robot)
                else :
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
 
class TeleOp:
    def __init__(self, port=20500):
        self.device_type = None
        self.save_enabled = False
        self.port = port
        self.server_ip_address = None
        self.server = None
        self.servicer = None
        self.exit_flag = False
 
    def get_server_ip(self):
        try:
            for iface_name in netifaces.interfaces():
                iface_details = netifaces.ifaddresses(iface_name)
                if netifaces.AF_INET in iface_details:
                    for addr in iface_details[netifaces.AF_INET]:
                        ip_address = addr.get('addr')
                        if ip_address and ip_address.startswith(("192.168", "10.", "172.")):
                            print(f"Local IP address: {ip_address}")
                            return ip_address
            print("No local IP address found.")
            return None
        except Exception as e:
            print(f"Error retrieving server IP: {e}")
            return None
        
    def select_device(self):
        device_option = input("Select device (1: phone, 0: vive): ").strip()
        if device_option not in ["0", "1"]:
            print("Invalid input. Please enter 1 (phone) or 0 (vive).")
            sys.exit(1)
        self.device_type = "phone" if device_option == "1" else "vive"
        
    def enableSave(self):
        save_option = input("Enable data saving? (1: Yes, 0: No): ").strip()
        if save_option not in ["0", "1"]:
            print("Invalid input. Please enter 1 (Yes) or 0 (No).")
            sys.exit(1)
        self.save_enabled = save_option == "1"
 
    def initialize_server(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.servicer = TeleOpDeviceServicer(device_type=self.device_type)
        add_TeleOpDeviceServicer_to_server(servicer=self.servicer, server=self.server)
        self.server.add_insecure_port(f'[::]:{DEVICE_PORT}')
        self.servicer.save_enabled = self.save_enabled
 
    def open_server(self):
        def server_thread():
            self.server.start()
            print(f"\nServer started for {self.device_type}")
            while not self.exit_flag:
                time.sleep(1)
            self.server.stop(0)
        Thread(target=server_thread, daemon=True).start()
 
    def wait_for_exit(self):
        print("\nPress 'q' to stop the server...")
        while not self.exit_flag:
            user_input = input().strip()
            if user_input.lower() == 'q':
                self.exit_flag = True
                break
        
    def plot_data(self):
        if self.save_enabled:
            self.servicer.device.calculate_perform()
            self.servicer.device.plot_data()
        else:
            return
 
if __name__ == "__main__":
    start_time = time.time()
    teleop = TeleOp()
    teleop.get_server_ip()
    teleop.select_device()
    teleop.enableSave()
    teleop.initialize_server()
    teleop.open_server()
    time.sleep(0.5)
    teleop.wait_for_exit()
    time.sleep(0.5)
    teleop.plot_data()
