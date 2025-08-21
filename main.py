
import os 
import sys
import csv
import serial
import threading
import queue
import serial.tools.list_ports
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox
from PySide6.QtWidgets import QLCDNumber
from PySide6.QtGui import QIcon
from PySide6.QtSerialPort import QSerialPortInfo
from PySide6.QtCore import QTimer


from ui_interface import *  # Import Ui_Form class from ui_interface file
# from ui_interface import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        ################################################################################################
        # Setup the UI main window
        ################################################################################################
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Serial port setup
        self.ser = None
        self.command_queue = queue.Queue()
        self.receive_thread = None
        self.running = False
        
        # Variable to store command status
        self.command_status = None  ## power on/off 
        self.aqi_value = None       ## AQI index (8,9)
        self.rpm = None             ## rpm (10,11)
        self.fan_speed = None        ## fan speed (13)
        self.aqi_grade = None        ## aqi_grade (14)
        self.filter_time = None      # filter used time (17,18)
        self.temperature = None             # temperature (28,29)
        self.ledbrightness = None    #led birghtness (31)
        self.status = None           # status (12)
        # self.ui.label_fw_version = None 

        self.touch_Filter_keypad = None        ## touch_Filter_keypad
        self.touch_Power_keypad = None
        self.touch_Display_keypad = None
        self.touch_Mode_keypad = None 
        self.keypad_status = None 

        self.ver1 = None
        self.ver2 = None
        self.ver3 = None
        self.ver4 = None
        self.ver5 = None
        self.ver6 = None
        self.ver7 = None
        self.ver8 = None
        self.ver8 = None


        self.save_csv = False
        self.csv_file = None 
        self.csv_writer = None 

        self.csv_file = None
        self.csv_writer = None
        self.csv_file_name = ''
        self.lock = threading.Lock()
        # self.create_new_csv_file()
        # self.schedule_next_file_creation()

        ##############################################################
        ## Fan mode  
        ##############################################################
        self.Fan_auto   = 0x01
        self.Fan_1      = 0x02
        self.Fan_2      = 0x04
        self.Fan_3      = 0x08
        self.Fan_4      = 0x10
        ##############################################################

        ########################################################
        ## Setting the LCD number format 
        ########################################################
        # self.ui.lcdNumber_aqi.setDigitCount(3)        
        ########################################################

        
        # Search and connect to serial port
        # self.search_and_connect_comport()
        self.populate_serial_ports()
        self.ui.comboBox_port.currentIndexChanged.connect(self.search_and_connect_comport)
        if self.ui.comboBox_port.count() == 1:
            self.search_and_connect_comport()


        # self.ui.textEdit_log = self.ui.findChild(QtWidgets.QTextEdit, 'logTextEdit')
        # self.ui.textEdit_log = self.findChild(QTextEdit, 'textEdit_log')

        # Connect button click event
        self.ui.pushButton_open.clicked.connect(self.comport_open_command)   
        # self.ui.pushButton_onoff.clicked.connect(self.power_on_command)        
        # self.ui.pushButton_display.clicked.connect(self.display_command)
        # self.ui.pushButton_mode.clicked.connect(self.mode_command)
        # self.ui.pushButton_power_on.clicked.connect(self.power_on_command)
        # self.ui.pushButton_power_off.clicked.connect(self.power_off_command)
        
        # self.ui.pushButton_led_display.clicked.connect(self.led_display_command)
        # self.ui.pushButton_all_led_onoff.clicked.connect(self.all_led_onoff_command)

        # self.ui.pushButton_fan_mode.clicked.connect(self.fan_mode_command)
        # self.ui.pushButton_fan_manual_1.clicked.connect(self.fan_manual_1_command)
        # self.ui.pushButton_fan_manual_2.clicked.connect(self.fan_manual_2_command)
        # self.ui.pushButton_fan_manual_3.clicked.connect(self.fan_manual_3_command)
        # self.ui.pushButton_fan_Auto.clicked.connect(self.fan_auto_command)  

        # self.ui.pushButton_max_filter.clicked.connect(self.max_filter_command)
        # self.ui.pushButton_reset_filter.clicked.connect(self.reset_filter_command)
        # self.ui.pushButton_buzzer_test.clicked.connect(self.buzzer_test_command)
        # self.ui.pushButton_factory_initialize.clicked.connect(self.factory_initialize_command)


        self.ui.label_fw_version.setFont(QFont("Arial",16))



        # self.ui.pushButton_debug_on.clicked.connect(self.debug_on_command)
        # self.ui.pushButton_debug_off.clicked.connect(self.debug_off_command)

        # Variable to store toggle state
        # self.toggle_state = True  # initial value
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.create_new_csv_file)


        # Show window
        self.show()

    def populate_serial_ports(self):
        self.ui.comboBox_port.clear()  
        port_list = QSerialPortInfo.availablePorts()
        for port_info in port_list:
            self.ui.comboBox_port.addItem(port_info.portName())  # addItem

    # def search_and_connect_comport(self):
    #     ports = serial.tools.list_ports.comports()
    #     print(f"####### PORT : {ports}")
    #     available_ports = [port.device for port in ports]
    #     print(f"####### available_ports : {available_ports}")

    #     if not available_ports:
    #         QMessageBox.critical(self, "Error", "No available serial ports found.")
    #         return

    #     if len(available_ports) == 1:
            
    #         selected_port = available_ports[0]
    #         print(f"Only one available port found: {selected_port}")
    #     else:
            
    #         selected_port = self.ui.comboBox_port.currentText()
    #         print(f"Multiple ports found. Selected port from combo box: {selected_port}")
            
        
    #     if selected_port in available_ports:
    #         try:
    #             self.ser = serial.Serial(selected_port, baudrate=115200, timeout=1)  
    #             if self.ser.is_open:
    #                 print(f"Connected to {selected_port}")
    #                 self.start_receiving()
    #         except serial.SerialException as e:
    #             QMessageBox.critical(self, "Error", f"Failed to connect to {selected_port}: {e}")
    #             print(f"Failed to connect to {selected_port}: {e}")
    #     else:
    #         QMessageBox.critical(self, "Error", f"Selected port {selected_port} is not available.")
    #         print(f"Selected port {selected_port} is not available.")

    def search_and_connect_comport(self):
        ports = serial.tools.list_ports.comports()
        print(f"####### PORT : {ports}")
        available_ports = [port.device for port in ports]
        print(f"####### available_ports : {available_ports}")

        if not available_ports:
            QMessageBox.critical(self, "Error", "No available serial ports found.")
            return

        if len(available_ports) == 1:
            selected_port = available_ports[0]
            print(f"Only one available port found: {selected_port}")
        else:
            selected_port = self.ui.comboBox_port.currentText()
            print(f"Multiple ports found. Selected port from combo box: {selected_port}")

        if selected_port in available_ports:
            try:
                # 이미 열려 있다면 닫기
                if hasattr(self, "ser") and self.ser is not None and self.ser.is_open:
                    self.ser.close()
                    print("Previous port closed")

                self.ser = serial.Serial(selected_port, baudrate=115200, timeout=1)
                if self.ser.is_open:
                    print(f"Connected to {selected_port}")
                    self.start_receiving()
                else:
                    print("Port could not be opened.")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to connect to {selected_port}: {e}")
                print(f"Failed to connect to {selected_port}: {e}")
            except OSError as e:
                QMessageBox.critical(self, "Error", f"OSError while connecting: {e}")
                print(f"OSError while connecting: {e}")
        else:
            QMessageBox.critical(self, "Error", f"Selected port {selected_port} is not available.")
            print(f"Selected port {selected_port} is not available.")



    def start_receiving(self):
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.receive_thread.start()

    # def append_log(self, message):
    #     self.ui.textEdit_log.append(message)

    def toggle_csv_saving(self):
        status = "enabled" if self.save_csv else "disabled"
        # self.append_log(f"CSV saving {status}")

    def receive_data(self):
        if self.ser:
            self.ser.timeout = 0.1  
    
        while self.running:
            if self.ser and self.ser.is_open:
                try:
                    self.ser.timeout = None

                    # Read first 2 bytes to check if the data is valid
                    header = self.ser.read(2)  # Read 2 bytes first

                    if header and header[0] == 0xFA and header[1] == 0x4E:
                        # Now read the remaining 36 bytes
                        data = self.ser.read(36)  # Read the remaining 36 bytes
                        if data:
                            # Concatenate the header and data to form the full 38-byte array
                            byte_array = [header[i] for i in range(2)] + [data[i] for i in range(36)]
                            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                            # Process and display data
                            for i in range(38):
                                if i == 8:
                                    self.aqi_value = (byte_array[i] << 8) | byte_array[i + 1]
                                    print(f'AQI_Idx[{i},{i+1}] : {self.aqi_value} ')  # dec 
                                    self.ui.lcdNumber_aqi_index.display(self.aqi_value)

                                elif i == 10:
                                    self.rpm = (byte_array[i] << 8) | byte_array[i + 1]
                                    print(f'Fan_rpm[{i},{i+1}] : {self.rpm} ')  # dec 
                                    self.ui.lcdNumber_rpm.display(self.rpm)

                                elif i == 13:
                                    self.fan_speed = (byte_array[i]) & 0x0F
                                    print(f'fan_speed [{i}] : {self.fan_speed}') # dec 
                                    self.ui.lcdNumber_fan_speed.display(self.fan_speed)

                                elif i == 12:
                                    self.status = (byte_array[i]) & 0x0F
                                    print(f'status [{i}] : {self.status:02X}')
                                    # self.fan_mode_command(self.keypad_status)
                                    self.ui.lcdNumber_status.display(self.status)
                                    
                                elif i == 14:
                                    self.aqi_grade = (byte_array[i]) & 0x0F
                                    # print(f'aqi_grade [{i}] : {byte_array[i]:02X}')
                                    print(f'aqi_grade [{i}] : {self.aqi_grade:02X}')                                
                                    self.ui.lcdNumber_aqi_grade.display(self.aqi_grade)

                                elif i == 17:
                                    self.filter_time = (byte_array[i] << 8) | byte_array[i + 1]
                                    print(f'filter_used_time[{i},{i+1}] : {self.filter_time} ')  # dec 
                                    # if self.touch_Filter_keypad & 0x8000:
                                    #     self.touch_Filter_keypad -= 0x10000
                                    # self.ui.lcdNumber_touch_filter.display(self.touch_Filter_keypad)
                                    self.ui.lcdNumber_filter_time.display(self.filter_time)
                                
                                elif i == 19:
                                    self.fw_ver1 = byte_array[i]
                                    self.fw_ver2 = byte_array[i+1]
                                    self.fw_ver3 = byte_array[i+2]
                                    self.fw_ver4 = byte_array[i+3]
                                    self.fw_ver5 = byte_array[i+4]
                                    self.fw_ver6 = byte_array[i+5]
                                    self.fw_ver7 = byte_array[i+6]
                                    self.fw_ver8 = byte_array[i+7]
                                    self.fw_ver9 = byte_array[i+8]

                                    # 9媛쒖쓽 諛붿씠�듃 媛믪쓣 �븘�뒪�궎 臾몄옄濡� 蹂��솚
                                    ascii_values = [
                                        chr(self.fw_ver1),
                                        chr(self.fw_ver2),
                                        chr(self.fw_ver3),
                                        chr(self.fw_ver4),
                                        chr(self.fw_ver5),
                                        chr(self.fw_ver6),
                                        chr(self.fw_ver7),
                                        chr(self.fw_ver8),
                                        chr(self.fw_ver9),
                                    ]
                                    ascii_string = ''.join(ascii_values)  # 怨듬갚 �뾾�씠 寃고빀 (�븘�슂 �떆 怨듬갚�쑝濡� 援щ텇 媛��뒫)
                                    
                                    self.ui.label_fw_version.setText(f"FW : {ascii_string}")

                                elif i == 28:
                                    self.temperature = (byte_array[i] << 8) | byte_array[i + 1]
                                    print(f'temperature[{i},{i+1}] : {self.temperature} ')  # dec 
                                    # if self.touch_Power_keypad & 0x8000:
                                    #     self.touch_Power_keypad -= 0x10000
                                    # self.ui.lcdNumber_touch_power.display(self.touch_Power_keypad)
                                    self.ui.lcdNumber_temperature.display(self.temperature)

                                elif i == 30:
                                    self.command_status = byte_array[i]
                                    print(f'command_status [{i}] : {byte_array[i]:02X}')
                                    # self.ui.lcdNumber_status.display(self.command_status)
                                    self.ui.lcdNumber_command_status.display(self.command_status)

                                elif i == 31:
                                    self.ledbrightness = byte_array[i]
                                    print(f'ledbrightness [{i}] : {byte_array[i]:02X}')
                                    self.ui.lcdNumber_led_brightness.display(self.ledbrightness)
                                    # self.ui.lcd

                                # elif i == 24:
                                #     self.touch_Display_keypad = (byte_array[i] << 8) | byte_array[i + 1]
                                #     print(f'touch_Display_keypad[{i},{i+1}] : {self.touch_Display_keypad:02X} ')  # dec
                                #     if self.touch_Display_keypad & 0x8000:
                                #         self.touch_Display_keypad -= 0x10000
                                #     self.ui.lcdNumber_touch_display.display(self.touch_Display_keypad)

                                # elif i == 26:
                                #     self.touch_Mode_keypad = (byte_array[i] << 8) | byte_array[i + 1]
                                #     print(f'touch_Mode_keypad[{i},{i+1}] : {self.touch_Mode_keypad:02X} ')  # dec  
                                #     if self.touch_Mode_keypad & 0x8000:
                                #         self.touch_Mode_keypad -= 0x10000
                                #     self.ui.lcdNumber_touch_mode.display(self.touch_Mode_keypad)
                                # elif i == 30:
                                #     self.command_status = byte_array[i]
                                #     print(f"Command status : {self.command_status:02X}")  # hex

                        # if self.save_csv:
                        #     with open(self.csv_file_name, mode='a', newline='') as file:
                        #         writer = csv.writer(file)
                        #         writer.writerow([current_time, self.touch_Mode_keypad, self.touch_Display_keypad, self.touch_Filter_keypad, self.touch_Power_keypad, self.keypad_status])

                except serial.SerialException as e:
                    print(f"Failed to receive data: {e}")
                    break                
                    # self.running = False
        print("Receive thread terminated")

    def fan_mode_command(self, fan_mode):
        if self.fan_mode == self.Fan_auto:
            print(f"fan_mode = {self.fan_mode:02X}")
            self.ui.pushButton_fan.setStyleSheet(u"border-image: url('C:/DATA/pic/fan5_auto.JPG');")
        elif self.fan_mode == self.Fan_1:
            print(f"fan_mode = {self.fan_mode:02X}")
            self.ui.pushButton_fan.setStyleSheet(u"border-image: url('C:/DATA/pic/fan1.JPG');")
        elif self.fan_mode == self.Fan_2:
            print(f"fan_mode = {self.fan_mode:02X}")
            self.ui.pushButton_fan.setStyleSheet(u"border-image: url('C:/DATA/pic/fan2.JPG');")
        elif self.fan_mode == self.Fan_3:
            print(f"fan_mode = {self.fan_mode:02X}")
            self.ui.pushButton_fan.setStyleSheet(u"border-image: url('C:/DATA/pic/fan3.JPG');")
        elif self.fan_mode == self.Fan_4:
            print(f"fan_mode = {self.fan_mode:02X}")
            self.ui.pushButton_fan.setStyleSheet(u"border-image: url('C:/DATA/pic/fan4.JPG');")
        else:
            print("Invalid fan mode")

    def mode_command(self):
        if self.ser and self.ser.is_open:    
            command = bytearray([0xFB, 0xA6, 0x0D, 0xAE])  # Mode command
            try:
                self.ser.write(command)
                print(f"Sent command[mode]: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def display_command(self):
        if self.ser and self.ser.is_open:    
            command = bytearray([0xFB, 0xA7, 0x0D, 0xAF])  # Display command
            try:
                self.ser.write(command)
                print(f"Sent command[display]: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")


    def create_new_csv_file(self):
        with self.lock:
            if not os.path.exists('keypad'):
                os.makedirs('keypad')

            # Close the previous file if it exists
            if self.csv_file:
                self.csv_file.close()
                print(f"Closed CSV file: {self.csv_file_name}")

            # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Include milliseconds
            current_time = datetime.now().strftime('%m-%d-%H-%M-%S.%f')[:-3]  # Include milliseconds

            # Create a new CSV file with the current timestamp
            self.csv_file_name = os.path.join('keypad', datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv')
            self.csv_file = open(self.csv_file_name, mode='w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(["Time", "touch_Mode_keypad", "touch_Display_keypad", "touch_Filter_keypad", "touch_Power_keypad", "keypad_status"])

            self.csv_file.flush()  # Ensure data is written to disk
            print(f"Created new CSV file: {self.csv_file_name} at {current_time}")
    
    def schedule_next_file_creation(self):
        next_minute = (datetime.now() + timedelta(minutes=1)).replace(second=0, microsecond=0)
        delay = (next_minute - datetime.now()).total_seconds()
        threading.Timer(delay, self.create_new_csv_file).start()

    # def write_to_csv(self, data):
    #     with self.lock:
    #         if self.csv_writer:
    #             self.csv_writer.writerow(data)
    #             self.csv_file.flush()  # Ensure data is written to disk
    #             print(f"Written data to CSV file: {self.csv_file_name}")

    def write_to_csv(self, data):
        with self.lock:
            if self.csv_writer:
                current_time = datetime.now()                
                formatted_time = current_time.strftime('%m-%d-%H-%M-%S.%f')[:-3]
                timestamp_ms = int(datetime.now().timestamp() * 1000)
                print("#### formatted_time:  ", formatted_time)
                print("#### Timestamp:  ", timestamp_ms)
                # formatted_time = self.datetime.now().strftime('%m-%d-%H-%M-%S.%f')[:-3]
                # formatted_time = timestamp_ms 
                print(f"formatted_time : {timestamp_ms}")  # Time stamp 

                data = [timestamp_ms] + data
                self.csv_writer.writerow(data)
                self.csv_file.flush()  # Ensure data is written to disk
                print(f"Written data to CSV file: {self.csv_file_name} with time {formatted_time}")

    # def round_ms(self, dt):
    #     microsecond = (dt.microsecond // 500000) * 500000
    #     if dt.microsecond % 500000 >= 250000:
    #         microsecond += 500000
    #     return dt.replace(microsecond=0) + timedelta(microseconds=microsecond)

    # def debug_on_command(self):
    #     self.save_csv = True
    #     self.create_new_csv_file()
    #     # self.timer.start(60000)  # 60000 milliseconds = 1 minute
        
    #     self.toggle_csv_saving()
    #     if self.ser and self.ser.is_open:    
    #         command = bytearray([0xFB, 0xA0, 0x00])  # debug on command
    #         try:
    #             self.ser.write(command)
    #             print(f"Sent command[debug_on]: {command.hex().upper()}")
    #         except serial.SerialException as e:
    #             QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
    #     else:
    #         QMessageBox.critical(self, "Error", "Serial port is not connected.")   

    # def debug_off_command(self):
    #     self.save_csv = False
    #     self.toggle_csv_saving()
    #     if self.ser and self.ser.is_open:    
    #         command = bytearray([0xFB, 0xA3, 0x00])  # debug off command
    #         try:
    #             self.ser.write(command)
    #             print(f"Sent command[debug_off]: {command.hex().upper()}")
    #         except serial.SerialException as e:
    #             QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
    #     else:
    #         QMessageBox.critical(self, "Error", "Serial port is not connected.")        

    def comport_open_command(self):
        if hasattr(self, "ser") and self.ser and self.ser.is_open:
            # Close
            self.running = False
            if hasattr(self, "receive_thread") and self.receive_thread.is_alive():
                self.receive_thread.join(timeout=1.0)
            self.ser.close()
            print("Serial port closed")
            self.ui.pushButton_open.setText("Open")
        else:
            # Open
            self.search_and_connect_comport()
            if hasattr(self, "ser") and self.ser.is_open:
                self.ui.pushButton_open.setText("Close")

            


    def power_on_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA5, 0xFD, 0x9D])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] power_on_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def power_off_command(self):
        if self.ser and self.ser.is_open:            
            # command = None  # 湲곕낯 媛믪쓣 None�쑝濡� 珥덇린�솕
            command = bytearray([0xFB, 0xA5, 0x0D, 0xAD])  # ON command
            # if self.command_status == 0x32:  # off condition
                # command = bytearray([0xFB, 0xA5, 0xFD, 0x9D])  # ON command
            # elif self.command_status == 0x33:  # on condition
            #     command = bytearray([0xFB, 0xA5, 0x0D, 0xAD])  # OFF command
            try:
                self.ser.write(command)
                print(f"[SENT] power_off_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")

            # if command:  # command媛� None�씠 �븘�땶 寃쎌슦�뿉留� write �샇異�
            #     # try:
            #     #     for i in range(3):  # Send the command 3 times
            #     #         self.ser.write(command)
            #     #         print(f"Sent command {i + 1}: {command.hex().upper()}")
            #     # except serial.SerialException as e:
            #     #     QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
            # else:
            #     QMessageBox.critical(self, "Error", "No valid command to send.")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")


    
    # def power_on_command(self):
    #     if self.ser and self.ser.is_open:            
    #         command = bytearray([0xFB, 0xA5, 0xFD, 0x9D])  # ON command
    #         try:
    #             self.ser.write(command)
    #             print(f"[SENT] power_on_command: {command.hex().upper()}")
    #         except serial.SerialException as e:
    #             QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
    #     else:
    #         QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def led_display_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA7, 0x0D, 0xAF])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] led_display_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def all_led_onoff_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xAA, 0x0D, 0xB2])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] all_led_onoff_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")
    
    def fan_mode_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA6, 0x0D, 0xAE])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] fan_mode_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")
    
    def fan_manual_1_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA6, 0x01, 0xA2])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] fan_manual_1_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def fan_manual_2_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA6, 0x02, 0xA3])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] fan_manual_2_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def fan_manual_3_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA6, 0x03, 0xA4])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] fan_manual_3_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def fan_auto_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA9, 0x0D, 0xB1])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] fan_auto_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def max_filter_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xE2, 0x0D, 0xEA])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] max_filter_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")


    def reset_filter_command(self):
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xE7, 0x0D, 0xEF])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] reset_filter_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")

    def buzzer_test_command(self): 
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xA4, 0x0D, 0xAC])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] buzzer_test_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")
    
    def factory_initialize_command(self): 
        if self.ser and self.ser.is_open:            
            command = bytearray([0xFB, 0xE1, 0x0D, 0xE9])  # ON command
            try:
                self.ser.write(command)
                print(f"[SENT] factory_initialize_command: {command.hex().upper()}")
            except serial.SerialException as e:
                QMessageBox.critical(self, "Error", f"Failed to send command: {e}")
        else:
            QMessageBox.critical(self, "Error", "Serial port is not connected.")


    def closeEvent(self, event):
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()
        if self.ser:
            self.ser.close()
        event.accept()

########################################################################
## EXECUTE APP
########################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

########################################################################
## END===>
########################################################################
