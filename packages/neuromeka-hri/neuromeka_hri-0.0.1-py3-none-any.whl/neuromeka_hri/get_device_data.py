import time
from datetime import datetime

import numpy as np
from threading import Thread

import socket

from scipy.spatial.transform import Rotation
from neuromeka_hri.interfaces.vive import triad_openvr


class UDPHandler:
    def __init__(self):
        self.filename = f"./pos_rot_data_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"

        self.start_time = time.time()

        self.IP = "0.0.0.0" 
        self.PORT = 3190 
        self.udp_thread = None

        self.sock = None
        self.val_detect = None
        self.val_enable = None
        self.val_raw_data = None

        self.pos = None
        self.rot_euler = None
        self.rotMat = None
        self.pos_rot = None
        self.last_time = time.time()
        self.stop_stream = False
        self.client_address = None

        self.last_packet_time = None 
        self.timeout = 2 

    def init_udp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.IP, self.PORT))
        self.udp_thread = Thread(target=self.get_data, daemon=True)
        self.udp_thread.start()
        self.status_thread = Thread(target=self.send_status, daemon=True)
        self.status_thread.start()

    def close_socket(self):
        self.stop_stream = True
        if self.sock:
            self.sock.close()

    def get_data(self):
        while not self.stop_stream:
            try:
                data, addr = self.sock.recvfrom(1024)
                self.client_address = addr
                self.last_packet_time = time.time()
                value = [float(x) for x in data.decode().strip().split(",")] 
                if value[0] == 0:
                    self.val_detect = False
                else:
                    self.val_detect = True
                if value[1] == 0:
                    self.val_enable = False
                else:
                    self.val_enable = True
                self.val_raw_data = value[2:]
                self.compute_pos_rot()
            except Exception as e:
                print(f"Error receiving data: {e}")

    def compute_pos_rot(self):
        current_time = time.time()

        pos = (np.array(self.val_raw_data[:3], dtype=np.float32)).tolist()
        quat = self.val_raw_data[3:]
        rotMat = Rotation.from_quat(quat).as_matrix().astype(np.float32)
        rot_euler = np.rad2deg(Rotation.from_matrix(rotMat).as_euler("xyz")).tolist()

        self.pos = pos
        self.rotMat = rotMat        
        self.rot_euler = rot_euler

        pos_rot = self.pos + self.rot_euler

        self.pos_rot = pos_rot
        self.last_time = current_time

    def send_status(self):
        while not self.stop_stream:
            current_time = time.time()
            if self.client_address:
                if self.last_packet_time and (current_time - self.last_packet_time) > 1:
                    print(f"Connection lost with {self.client_address}")
                    self.client_address = None
                else:
                    try:
                        status_server = "OK".encode('utf-8')
                        self.sock.sendto(status_server, self.client_address)
                        # print(f"Sent status to {self.client_address}: {status_server}")
                    except Exception as e:
                        print(f"Error sending status to {self.client_address}: {e}")
            # else:
            #     print("No client connected.")
            time.sleep(0.5) 

class ViveHandler:
    def __init__(self, device_name="controller_1", trigger_name="menu_button"):
        self.device_name = device_name
        self.trigger_name = trigger_name
        self.v = None

    def init_vive(self):
        self.v = triad_openvr.triad_openvr()
        self.v.print_discovered_objects()

        for _ in range(200):
            self.v.devices[self.device_name].trigger_haptic_pulse()
            time.sleep(0.01)

    def get_vive_input(self):
        controller_inputs = self.v.devices[self.device_name].get_controller_inputs()
        return controller_inputs[self.trigger_name]

    def get_vive_pose(self):
        vive_pose = self.v.devices[self.device_name].get_pose_matrix()
        pos = np.multiply(1000, [vive_pose.m[0][3], vive_pose.m[1][3], vive_pose.m[2][3]]).tolist()
        rotMat = np.array([[vive_pose.m[0][0], vive_pose.m[0][1], vive_pose.m[0][2]],
                           [vive_pose.m[1][0], vive_pose.m[1][1], vive_pose.m[1][2]],
                           [vive_pose.m[2][0], vive_pose.m[2][1], vive_pose.m[2][2]]])
        rot = np.rad2deg(Rotation.from_matrix(rotMat).as_euler("xyz")).tolist()
        
        return pos + rot
    
if __name__ == "__main__":
    udp = UDPHandler()
    udp.init_udp()

    try:
        while True:
            time.sleep(0.5)  
    except KeyboardInterrupt:
        print("Shutting down...")
        udp.close_socket()
