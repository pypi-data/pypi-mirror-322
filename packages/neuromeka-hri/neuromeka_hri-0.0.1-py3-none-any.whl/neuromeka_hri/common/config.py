import os
from . import version as middleware_version
from .utils import get_abs_path, load_json
from .singleton_meta import SingletonMeta
from . import limits as Limits
from math import radians

class ConfigLibrary(metaclass=SingletonMeta):
    DEPLOY_JSON_DEFAULT = 'indyDeploy.json'
    CONFIG_JSON_DEFAULT = 'configPath.json'
    CONTROL_TASK_BIN_DEFAULT = 'IndyControlTask'
    PROGRAM_DIR = ''
    ## SET DEFAULT PORTS FOR CLIENTS
    ETHERCAT_SOCKET_PORT = 20000
    CONTROL_SOCKET_PORT = 20001
    DEVICE_SOCKET_PORT = 20002
    CONFIG_SOCKET_PORT = 20003
    RTDE_SOCKET_PORT = 20004
    MOBY_SOCKET_PORT = 20200
    CONTY_SOCKET_PORT = 20131
    CRI_SOCKET_PORT = 20181
    LINEAR_SOCKET_PORT = 20300
    MOBY_V2_PORT = 50051
    LOG_PATH = get_abs_path("LogData/")
    SERVER_LOG_PATH = LOG_PATH + "Server/"
    FRICTION_LOG_PATH = LOG_PATH + "Friction/"

    SW_UPDATE_FILE_NAME = get_abs_path('indy_sw.zip')

    # deploy_json_abs = get_abs_path(DEPLOY_JSON_DEFAULT)
    # deploy_config = load_json(deploy_json_abs)
    # deploy_config

    ############################
    #    Exit Code             #
    ############################
    EXIT_NORMAL = 0
    EXIT_REBOOT = 1
    EXIT_UPDATE = 2
    EXIT_PW_OFF = 3

    ############################
    #    Vel Level Conversion  #
    ############################
    JogVelRatioMax = 25  # %
    VelAutoLevelValue = (Limits.VelRatioMax - JogVelRatioMax) / (Limits.LevelMax - Limits.JogLevelMax)  # %
    VelManualLevelValue = (JogVelRatioMax - Limits.JogVelRatioMin) / (Limits.JogLevelMax - Limits.JogLevelMin)  # %

    def __init__(self):
        self.VERSION_INFO = middleware_version.VERSION_INFO
        self.VERSION_DETAIL = middleware_version.VERSION_DETAIL
        self.VERSION_DATE = middleware_version.VERSION_DATE

    ##
    # @return list of names of tasks of which binary file is task_bin
    def get_robot_tasks(self, deploy_json=DEPLOY_JSON_DEFAULT, task_bin=CONTROL_TASK_BIN_DEFAULT):
        deploy_json_abs = get_abs_path(deploy_json)
        deploy_config = load_json(deploy_json_abs)
        task_names = []
        for task_name, task_config in deploy_config["RTTasks"].items():
            if task_name == task_bin:
                task_names.append(task_name)
        return task_names

    ##
    # @return relative path for config json file
    def get_task_config(self, deploy_json=DEPLOY_JSON_DEFAULT, task_name=CONTROL_TASK_BIN_DEFAULT):
        deploy_json_abs = get_abs_path(deploy_json)
        deploy_config = load_json(deploy_json_abs)
        return deploy_config["RTTasks"][task_name]["ConfigFile"]

    def load_config(self, deploy_json=DEPLOY_JSON_DEFAULT, config_json=CONFIG_JSON_DEFAULT):
        deploy_json_abs = get_abs_path(deploy_json)
        deploy_config = load_json(deploy_json_abs)
        self.task_order = deploy_config["RTTasks"]["IndyControlTask"]["Order"]

        config_dict = load_json(get_abs_path(config_json))
        robot_configs = load_json(get_abs_path(config_dict["Config"]))

        bot_type = "Cobot"
        if bot_type in robot_configs:
            robot_config = robot_configs[bot_type][self.task_order]
            self.ROBOT_NAME = robot_config['robot_name']
            self.ROBOT_MODEL = f"NRMK-{self.ROBOT_NAME}"
            self.ROBOT_DOF = robot_config['DOF']
        else:
            self.ROBOT_MODEL = f"Empty"
            self.ROBOT_DOF = 0
            self.ROBOT_NAME = None

        mobile_key = "MobileRobot"
        bridge_key = "use_v2_bridge"
        self.USE_V2_BRIDGE = False
        if mobile_key in robot_configs:
            mobile_config = robot_configs[mobile_key]
            if bridge_key in mobile_config:
                self.USE_V2_BRIDGE = mobile_config[bridge_key]

        control_box_set = False
        if "ControlBox" in robot_configs:
            control_box = robot_configs["ControlBox"]
            if "type" in control_box:
                if control_box["type"]=="CB2.0":
                    self.USE_SAFETYIO = control_box.get("use_safetyio", False)
                    self.USE_NPAD = control_box.get("use_npad", False)
                    self.USE_AUTO_MODE = robot_config.get('use_auto_mode', False)
                    control_box_set = True
                elif control_box["type"]=="CB3.0":
                    self.USE_SAFETYIO = control_box.get("use_safetyio", True)
                    self.USE_NPAD = control_box.get("use_npad", False)
                    self.USE_AUTO_MODE = robot_config.get('use_auto_mode', True)
                    control_box_set = True
        if not control_box:
            self.USE_SAFETYIO = control_box.get("use_safetyio", False)
            self.USE_NPAD = control_box.get("use_npad", False)
            self.USE_AUTO_MODE = robot_config.get('use_auto_mode', False)


        # self.CONTROLLER_IP_ADDRESS = '192.168.6.138'
        # self.CONTROLLER_IP_ADDRESS = '192.168.1.8'
        self.CONTROLLER_IP_ADDRESS = '127.0.0.1'

        port_config = load_json(get_abs_path(config_dict["Ports"]))
        self.ETHERCAT_SOCKET_PORT = port_config["EtherCAT"]
        self.CONTROL_SOCKET_PORT = port_config["Control"][self.task_order]
        self.DEVICE_SOCKET_PORT = port_config["Device"][self.task_order]
        self.CONFIG_SOCKET_PORT = port_config["Config"][self.task_order]
        self.RTDE_SOCKET_PORT = port_config["RTDE"][self.task_order]
        self.CRI_SOCKET_PORT = port_config["CRI"][self.task_order]
        if "Moby" in port_config:
            self.MOBY_SOCKET_PORT = port_config["Moby"]
        if "Linear" in port_config:
            self.LINEAR_SOCKET_PORT = port_config["Linear"]
        if "Conty" in port_config:
            self.CONTY_SOCKET_PORT = port_config["Conty"][self.task_order]

        ############################
        #    Configuration Files   #
        ############################
        self.CONSTANTS_DIR = get_abs_path(config_dict["Constants"])
        self.CONSTANTS_CUSTOM_DIR = get_abs_path(config_dict["CustomConstants"])
        self.CONTROL_GAIN_DIR = get_abs_path(config_dict["ControlGain"])
        self.COLLISION_DEFAULT_DIR = get_abs_path(config_dict["DefaultCollisionGain"])
        self.COLLISION_CUSTOM_DIR = get_abs_path(config_dict["CollisionGain"])
        self.FRICTION_PARAMETER_DIR = get_abs_path(config_dict["FrictionParameter"])

        self.SYSTEM_INFO_DIR = get_abs_path(config_dict["SerialNumber"])

        self.FRICTION_CONFIG_DIR = get_abs_path(config_dict["FrictionConfig"])
        self.SAFETY_CONFIG_DIR = get_abs_path(config_dict["SafetyConfig"])
        self.COLLISION_CONFIG_DIR = get_abs_path(config_dict["CollisionConfig"])

        self.HOME_POS_DIR = get_abs_path(config_dict["HomePos"])
        self.CUSTOM_POS_DIR = get_abs_path(config_dict["CustomPos"])
        self.TOOL_DIR = get_abs_path(config_dict["ToolList"])
        self.TOOL_PROPERTY_DIR = get_abs_path(config_dict["ToolProperty"])
        self.MOUNT_ANGLE_DIR = get_abs_path(config_dict["MountingAngle"])
        self.AUTO_SERVO_OFF_DIR = get_abs_path(config_dict["AutoServoOff"])
        self.DI_CONFIG_DIR = get_abs_path(config_dict["DIConfig"])
        self.DO_CONFIG_DIR = get_abs_path(config_dict["DOConfig"])
        self.TOOL_FRAME_DIR = get_abs_path(config_dict["ToolFrameConfig"])
        self.REF_FRAME_DIR = get_abs_path(config_dict["RefFrameConfig"])
        self.VISION_DIR = get_abs_path(config_dict["VisionConfig"])
        self.ON_START_PROGRAM_CONFIG_DIR = get_abs_path(config_dict["OnStartProgram"])
        self.FT_FRAME_DIR = get_abs_path(config_dict["FTFrameConfig"])
        self.FT_TYPE_DIR = get_abs_path(config_dict["FTTypeConfig"])
        self.TELE_OP_PARAMS_DIR = get_abs_path(config_dict["TeleOpParams"])

        ############################
        #    Configuration Paths   #
        ############################
        self.ROBOT_CONFIG_PATH = os.path.dirname(self.HOME_POS_DIR)+"/"
        if not os.path.exists(self.ROBOT_CONFIG_PATH):
            os.makedirs(self.ROBOT_CONFIG_PATH, exist_ok=True)

        self.CONVEYOR_CONFIG_DIR = get_abs_path(config_dict.get("Conveyor", self.ROBOT_CONFIG_PATH + "Conveyor.json"))
        self.PROGRAM_DIR = get_abs_path('ProgramScripts')
        self.INDEX_PROGRAM_DIR = self.PROGRAM_DIR + '/index'

        self.LOG_PATH = get_abs_path("LogData/")
        self.SERVER_LOG_PATH = self.LOG_PATH + "Server/"
        self.FRICTION_LOG_PATH = self.LOG_PATH + "Friction/"

        self.GCODE_DIR = get_abs_path('Gcodes')

        ######################
        #    Derived Paths   #
        ######################
        self.MODBUS_DIR = self.ROBOT_CONFIG_PATH + "Modbus.json"
        self.PALLET_MAKER_DIR = self.ROBOT_CONFIG_PATH + "Pallet.json"

        self.FRICTION_LOG_DIR = self.FRICTION_LOG_PATH + "FrictionData.csv"

        self.WELDING_MACHINE_DIR = self.ROBOT_CONFIG_PATH + "WeldingMachineConfig.json"
        self.WELDING_LINES_DIR = self.ROBOT_CONFIG_PATH + "WeldingLinesInfo.json"
        self.DETECTED_WELDING_LINES_DIR = self.ROBOT_CONFIG_PATH + "DetectedWeldingLinesInfo.json"

        ######################
        #    Update values   #
        ######################
        self.update_conversion()

    def update_conversion(self):
        constants_dict = load_json(self.CONSTANTS_DIR)
        if os.path.isfile(self.CONSTANTS_CUSTOM_DIR):
            constants_dict.update(load_json(self.CONSTANTS_CUSTOM_DIR))
        safety_stop_config_dict = load_json(self.SAFETY_CONFIG_DIR)
        constants = constants_dict[self.ROBOT_NAME] if self.ROBOT_NAME in constants_dict else {}
        self.taskDistSpeedMax = constants.get("TaskDistSpeedMax", Limits.TaskDispVelValueMax/1000)
        self.taskRotSpeedMax = constants.get("TaskRotSpeedMax", radians(Limits.TaskRotVelValueMax))
        self.linearSpeedMax = constants.get("LinearSpeedMax", Limits.ExternalMotorSpeedMax/1000)
        self.taskDistSpeedReduced = constants.get("TaskDistSpeedReduced", Limits.TaskDispVelValueDefault/1000)
        self.taskDistSpeedReduced = safety_stop_config_dict.get('reducedSpeed', self.taskDistSpeedReduced)
        self.reducedRatio = self.taskDistSpeedReduced/self.taskDistSpeedMax * 100
        self.JogVelRatioMax = self.reducedRatio
        self.VelAutoLevelValue = (Limits.VelRatioMax - self.JogVelRatioMax) / (Limits.LevelMax - Limits.JogLevelMax)  # %
        self.VelManualLevelValue = (self.JogVelRatioMax - Limits.JogVelRatioMin) / (Limits.JogLevelMax - Limits.JogLevelMin)  # %

    def to_vel_ratio(self, level):
        if level < Limits.LevelMin:
            level = Limits.LevelMin
        if level > Limits.LevelMax:
            level = Limits.LevelMax

        if level > Limits.JogLevelMax:
            vel_ratio = self.JogVelRatioMax + self.VelAutoLevelValue * (level - Limits.JogLevelMax)
        else:
            vel_ratio = Limits.JogVelRatioMin + self.VelManualLevelValue * (level - Limits.JogLevelMin)
        return vel_ratio

    def to_acc_ratio(self, level):
        if level < Limits.LevelMin:
            level = Limits.LevelMin
        if level > Limits.LevelMax:
            level = Limits.LevelMax
        acc_ratio = Limits.JogAccRatioDefault * level
        return acc_ratio

    def check_Cobot(self, config_json=CONFIG_JSON_DEFAULT):
        config_dict = load_json(get_abs_path(config_json))
        robot_configs = load_json(get_abs_path(config_dict["Config"]))
        bot_type = "Cobot"
        if bot_type in robot_configs:
            return True
        return False
