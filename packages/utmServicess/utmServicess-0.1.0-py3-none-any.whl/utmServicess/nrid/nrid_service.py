import json
import logging
import os
import ssl
import sys
import threading
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
import serial
from pynmeagps import NMEAReader

from .ussp.message_security import message_security_utils
from .ussp.network_utility_interface import network_utility_interface
from .ussp.non_repudiation import non_repudiation_utils


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger = logging.getLogger(__name__)
    logger.exception(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = handle_uncaught_exception


class nrid_service:
    def __init__(
        self,
        port,
        baudrate,
        broker_type=1,
        fake_gnss=False,
        store_log=False,
        nrid_frequency=1,
    ):
        self.port = port
        self.baudrate = baudrate
        self.ussp_type = os.getenv("USSP")
        self.headers = {"Content-Type": "application/json"}
        self.fake_gnss = fake_gnss
        self.store_log = store_log
        self.gcs_lat = None
        self.gcs_lon = None
        self.min_sat = 4  # Minimum number of satellites required
        self.nrid_frequency = nrid_frequency

        # MQTT parameters
        self.cert_dir_path = "/usr/local/bin/utm/nrid/ussp/test_certificates/"
        self.PUBLIC_BROKER = {
            "address": "broker.hivemq.com",
            "port": 1883,
            "use_tls": False,
        }
        self.PRIVATE_BROKER = {
            "address": "139.59.99.151",
            "port": 8883,
            "use_tls": True,
            "username": "admin",
            "password": "password",
            "ca_cert": os.path.join(self.cert_dir_path, "ca.crt"),
        }
        self.pub_topic = "drone_identification"
        self.command_topic = "ground_control_commands"
        self.telemetry_topic = "drone_telemetry"
        self.ACTIVE_BROKER = self.PRIVATE_BROKER if broker_type else self.PUBLIC_BROKER
        self.RESTART_DEV_ID_AFTER_TELEMETRY = True
        self.send_id_flag = True
        self.telemetry_flag = False
        self.flight_plan_id = ""
        self.gcs_id = ""

        self.non_repudiation = non_repudiation_utils(
            os.path.join(self.cert_dir_path, "cert.txt"),
            os.path.join(self.cert_dir_path, "key.txt"),
        )
        self.message_security = message_security_utils(
            self.non_repudiation,
            os.path.join(self.cert_dir_path, "cert.txt"),
            os.path.join(self.cert_dir_path, "key.txt"),
        )
        self.network_interface = network_utility_interface(
            self.non_repudiation, os.path.join(self.cert_dir_path, "cert.txt")
        )

        # Set up MQTT client
        self.client = mqtt.Client(
            client_id="ssrc_drone_tracker",
            protocol=mqtt.MQTTv311,
            transport="tcp",
        )
        if self.ACTIVE_BROKER["use_tls"]:
            self.client.username_pw_set(
                self.ACTIVE_BROKER["username"], self.ACTIVE_BROKER["password"]
            )
            self.client.tls_set(
                ca_certs=self.ACTIVE_BROKER["ca_cert"],
                tls_version=ssl.PROTOCOL_TLSv1_2,
                cert_reqs=ssl.CERT_REQUIRED,
                ciphers=None,
            )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.non_repudiation_flag = os.getenv("ENABLE_NON_REPUDIATION")
        self.led1_status = 0
        self.mesh_status = 0

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            # Create formatter
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            # Create console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
            if self.store_log:
                # Create file handler with date and hour in filename
                log_filename = (
                    "nrid_service_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
                )
                fh = logging.FileHandler(log_filename)
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

        # Initialize USSP-specific parameters
        self.initialize_ussp_parameters()

        self.jwt = "INVALID"
        self._token = None
        self._token_timestamp = 0
        self._token_validity = 3500  # 58.3 minutes in seconds
        self._token_lock = threading.Lock()

        self._gps_data = None
        self._gps_lock = threading.Lock()
        self._last_telemetry_sent = 0

    def initialize_ussp_parameters(self):
        if self.ussp_type == "HIGHLANDER":
            self.logger.info("Initializing Highlander USSP parameters.")
            print("-----------------------------------------------------------------------------------")
            print(" _    _   _   ______  _    _	  _	      ______   __   _   _____    ______   ______  ")
            print("| |  | | | | |  ___| | |  | | | |     |  __  | |  \ | | |  __ \  | _____| |  __  | ")
            print("| |__| | | | | |	    | |__| | | |     | |__| | |   \| | | |  | | | |__    | |__| | ")
            print("|  __  | | | | |  _  |  __  | | | 	 |  __  | | |\   | | |  | | |  __|   |  _  _| ")
            print("| |  | | | | | |_| | | |  | | | |___	 | |  | | | | \  | | |__| | | |____  | | \ \  ")
            print("|_|  |_| |_| |_____| |_|  |_| |_____| |_|  |_| |_|  \_| |_____/  |______| |_|  \_\ ")
            print("-----------------------------------------------------------------------------------")
            # Highlander Parameters
            self.secure_user = os.getenv("HIGHLANDER_USER")
            self.secure_password = os.getenv("HIGHLANDER_PASSWORD")
            self.endpoint_secure_auth_url_hl = (
                os.getenv("HIGHLANDER_URL") + "api/en-us/auth/authenticate"
            )
            self.endpoint_secure_send_telemetry_url = (
                os.getenv("HIGHLANDER_URL") + "api/en-us/uavs/telemetry"
            )
            self.endpoint_secure_rid_url = (
                os.getenv("HIGHLANDER_URL") + "api/en-us/uavs/rid"
            )
            self.model = os.getenv("DRONE_MODEL")
            self.tail_number = os.getenv("TAIL_NUMBER")
            self.serial_number = os.getenv("SERIAL_NUMBER")
            self.type = "hover"
            self.battery = 75
            self.heading = 0
            self.takeoff_location = None
            self.is_flying = False
            self.flight_status = "notactive"
            self.satellite = 10
            self.velocity_x = 0
            self.velocity_y = 0
            self.velocity_z = 0
            self.pitch = 0
            self.roll = 0
            self.yaw = 0
            self.AGL = 0
            self.ASL = 206
            self.flight_mode = "controlled"
            self.timestamp = "timestamp_date_time"
            self.up_link = 75
            self.sign = "USS-10"
            self.waypoint_index = -1
            self.user_email = os.getenv("USER_EMAIL")
            self.pilot_lat = 24.436357
            self.pilot_lon = 54.613838
            self.air_situation = "full"
        elif self.ussp_type == "BLENDER":
            self.logger.info("Initializing Blender USSP parameters.")
            print("----------------------------------------------------------")
            print(" ____    _       _____   __   _   ____    _____   ______  ")
            print("|  _ \  | |     |  ___| |  \ | | |  _ \  | ____| |  __  | ")
            print("| |_) | | |     | |__   |   \| | | | | | | |__   | |__| | ")
            print("|  _ <  | |     |  __|  | |\   | | | | | |  __|  |  _  _| ")
            print("| |_) | | |___  | |___  | | \  | | |_| | | |___  | | \ \  ")
            print("|____/  |_____| |_____| |_|  \_| |____/  |_____| |_|  \_\ ")
            print("----------------------------------------------------------")
            # Blender Parameters
            self.client_id = os.getenv("CLIENT_ID")
            self.client_secret = os.getenv("CLIENT_SECRET")
            self.endpoint_auth_url_blender = os.getenv("TOKEN_URL") + "oauth/token/"
            self.endpoint_send_telemetry_url_blender = (
                os.getenv("BLENDER_URL") + "flight_stream/set_telemetry"
            )
            self.endpoint_signed_send_telemetry_url_blender = (
                os.getenv("BLENDER_URL") + "flight_stream/set_signed_telemetry"
            )
            self.timestamp_format = "RFC3339"
            self.timestamp_accuracy = 0
            self.operational_status = "Undeclared"
            self.position_alt = 206
            self.position_accuracy_h = "HAUnknown"
            self.position_accuracy_v = "VAUnknown"
            self.extrapolated = True
            self.pressure_altitude = 0
            self.track = 0
            self.speed = 1.9
            self.speed_accuracy = "SAUnknown"
            self.vertical_speed = 0.2
            self.height_distance = 0
            self.height_reference = "TakeoffLocation"
            self.group_radius = 0
            self.group_ceiling = 0
            self.group_floor = 0
            self.group_count = 0
            self.group_time_start = "2023-08-09T23:20:50.52Z"
            self.group_time_end = "2023-08-09T23:20:50.52Z"
            self.rid_id = "a3423b-213401-0023"
            self.operator_id = "N.OP123456"
            self.operation_description = "TII company doing survey with T-Motor. See my privacy policy www.example.com/privacy."
            self.eu_category = "EUCategoryUndefined"
            self.eu_class = "EUClassUndefined"
            self.serial_number = os.getenv("SERIAL_NUMBER")
            self.tail_number = os.getenv("TAIL_NUMBER")
            self.user_email = os.getenv("USER_EMAIL")
            self.registration_id = "N.123456"
            self.utm_id = "ae1fa066-6d68-4018-8274-af867966978e"
            self.specific_session_id = "02-a1b2c3d4e5f60708"
            self.operator_lat = 24.436357
            self.operator_lon = 54.613838
            self.operator_alt = 0
            self.altitude_type = "Takeoff"
            self.auth_format = "string"
            self.auth_data = "string"
            self.registration_number = "FA12345897"
        else:
            self.logger.error("Invalid USSP type")
            raise ValueError("Invalid USSP type")

    def get_auth_token(self):
        try:
            if self.ussp_type == "HIGHLANDER":
                token = self.network_interface.authenticate(
                    self.secure_user,
                    self.secure_password,
                    self.endpoint_secure_auth_url_hl,
                )
                if not token:
                    self.logger.error("Authentication failed for Highlander.")
                    raise RuntimeError("Authentication failed")
                return token
            else:
                token = self.network_interface.authenticate_blender(
                    self.client_id, self.client_secret, self.endpoint_auth_url_blender
                )
                if not token:
                    self.logger.error("Authentication failed for Blender.")
                    raise RuntimeError("Authentication failed")
                return token
        except Exception as e:
            self.logger.exception(f"Error obtaining auth token: {e}")
            raise

    def get_cached_token(self):
        with self._token_lock:
            current_time = time.time()
            if (
                self._token is None
                or (current_time - self._token_timestamp) > self._token_validity
            ):
                self._token = self.get_auth_token()
                self._token_timestamp = current_time
            return self._token

    def is_valid_coordinates(self, lat, lon):
        return (
            lat is not None
            and lon is not None
            and isinstance(lat, (int, float))
            and isinstance(lon, (int, float))
        )

    def update_gps_data(self, lat, lon, alt, gps_time):
        with self._gps_lock:
            self._gps_data = {
                "lat": lat,
                "lon": lon,
                "alt": alt,
                "timestamp": gps_time,
            }

    def get_latest_gps(self):
        with self._gps_lock:
            return self._gps_data

    def send_telemetry_with_cached_token(self, gps_data):
        try:
            token = self.get_cached_token()
            if self.ussp_type == "HIGHLANDER":
                return self.network_interface.send_telemetry(
                    token,
                    gps_data["lat"],
                    gps_data["lon"],
                    gps_data["alt"],
                    gps_data["timestamp"],
                    self.gcs_lat,
                    self.gcs_lon,
                    self.serial_number,
                    self.tail_number,
                    self.endpoint_secure_send_telemetry_url,
                    self.non_repudiation_flag,
                )
            else:
                telemetry_url = (
                    self.endpoint_signed_send_telemetry_url_blender
                    if self.non_repudiation_flag
                    else self.endpoint_send_telemetry_url_blender
                )
                return self.network_interface.send_telemetry_blender(
                    token,
                    self.flight_plan_id,
                    gps_data["lat"],
                    gps_data["lon"],
                    gps_data["alt"],
                    gps_data["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    self.serial_number,
                    self.gcs_id,
                    telemetry_url,
                    self.non_repudiation_flag,
                )
        except Exception as e:
            self.logger.exception(f"Error sending telemetry: {e}")
            return False

    def read_nmea_data(self):
        try:
            if not self.fake_gnss:
                stream = serial.Serial(
                    self.port, baudrate=self.baudrate, timeout=0.1, write_timeout=1
                )
                nmr = NMEAReader(stream)
                self.logger.info("Serial port opened and NMEAReader initialized.")
            else:
                self.logger.info("Using fake GNSS data.")

            # Get initial token
            self.get_cached_token()

            latest_gga_data = None  # Initialize to store the latest valid GGA data

            while self.telemetry_flag:
                current_time = time.time()
                time_since_last = current_time - self._last_telemetry_sent

                if not self.fake_gnss:
                    # Read all available data from the serial port
                    while stream.in_waiting:
                        try:
                            raw_data, parsed_data = nmr.read()
                            if parsed_data and parsed_data.msgID == "GGA":
                                fixquality = getattr(parsed_data, "quality", 0)
                                numsats = getattr(parsed_data, "numSV", 0)
                                if fixquality != 0 and numsats >= self.min_sat:
                                    lat = parsed_data.lat
                                    lon = parsed_data.lon
                                    alt = parsed_data.alt
                                    gps_time = datetime.combine(
                                        datetime.today(), parsed_data.time
                                    ).replace(tzinfo=timezone.utc)

                                    if self.is_valid_coordinates(lat, lon):
                                        # Store the latest valid GGA data
                                        latest_gga_data = {
                                            "lat": lat,
                                            "lon": lon,
                                            "alt": alt,
                                            "timestamp": gps_time,
                                        }
                                    else:
                                        self.logger.warning("Invalid GPS coordinates")
                                else:
                                    self.logger.debug(
                                        f"Ignoring due to fixquality={fixquality} or numsats={numsats}"
                                    )
                        except Exception as e:
                            self.logger.error(f"Error reading GPS data: {e}")
                            break  # Exit the reading loop on error

                if time_since_last >= self.nrid_frequency:
                    if self.fake_gnss:
                        # Generate fake GNSS data
                        lat = (
                            self.pilot_lat
                            if self.ussp_type == "HIGHLANDER"
                            else self.operator_lat
                        )
                        lon = (
                            self.pilot_lon
                            if self.ussp_type == "HIGHLANDER"
                            else self.operator_lon
                        )
                        alt = 0
                        gps_time = datetime.now(timezone.utc)
                        self.update_gps_data(lat, lon, alt, gps_time)
                    else:
                        if latest_gga_data:
                            # Use the latest valid GPS data
                            self.update_gps_data(
                                latest_gga_data["lat"],
                                latest_gga_data["lon"],
                                latest_gga_data["alt"],
                                latest_gga_data["timestamp"],
                            )
                            latest_gga_data = None  # Reset for next iteration
                        else:
                            self.logger.warning(
                                "Skipping telemetry due to lack of valid GPS data"
                            )
                            continue

                    # Get the latest GPS data for telemetry
                    gps_data = self.get_latest_gps()
                    if gps_data:
                        self.logger.debug(
                            f"Lat: {gps_data['lat']}, Lon: {gps_data['lon']}, Alt: {gps_data['alt']}"
                        )
                        if self.send_telemetry_with_cached_token(gps_data):
                            self._last_telemetry_sent = current_time
                            self.logger.debug(
                                f"Telemetry sent successfully at {gps_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')}"
                            )
                            if not self.fake_gnss:
                                self.update_led_status(
                                    "/sys/class/leds/led1/brightness", "led1_status"
                                )
                        else:
                            self.logger.error("Failed to send telemetry")
                            if not self.fake_gnss:
                                self.update_led_status(
                                    "/sys/class/leds/mesh/brightness", "mesh_status"
                                )

                            fail_message = {
                                "status": "telemetry_failed",
                                "flight_plan_id": self.flight_plan_id,
                                "serial_number": self.serial_number,
                                "detail": {
                                    "lat": gps_data["lat"],
                                    "lon": gps_data["lon"],
                                    "alt": gps_data["alt"],
                                    "timestamp": gps_data["timestamp"].strftime(
                                        "%Y-%m-%dT%H:%M:%SZ"
                                    ),
                                },
                            }

                            self.publish_signed_message(
                                self.telemetry_topic, fail_message
                            )
                    else:
                        self.logger.warning("No Valid GPS data available for telemetry")
                else:
                    # Sleep briefly to reduce CPU usage
                    time.sleep(0.1)
        except Exception as e:
            self.logger.exception(f"Error in read_nmea_data: {e}")
        finally:
            if not self.fake_gnss:
                try:
                    stream.close()
                    self.logger.info("Serial port closed")
                except Exception as e:
                    self.logger.exception(f"Error closing serial port: {e}")

    def update_led_status(self, led_path, status_attr):
        """Update LED status"""
        try:
            with open(led_path, "w") as f:
                current_status = getattr(self, status_attr)
                new_status = 1 if current_status == 0 else 0
                f.write(str(new_status))
                setattr(self, status_attr, new_status)
        except Exception as e:
            self.logger.exception(f"Error updating LED status: {e}")

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info(f"Connected to MQTT broker with result code {rc}")
        try:
            client.subscribe(self.command_topic)
            self.logger.debug(f"Subscribed to topic: {self.command_topic}")
        except Exception as e:
            self.logger.exception(
                f"Error subscribing to topic {self.command_topic}: {e}"
            )

    def on_message(self, client, userdata, msg):
        if msg.topic == self.command_topic:
            try:
                message = json.loads(msg.payload.decode())
                self.logger.info(
                    f"Received message on topic {msg.topic}: {json.dumps(message, indent=4)}"
                )

                if not self.message_security.verify_message(message):
                    self.logger.warning(
                        f"Received message with invalid signature on topic: {msg.topic}"
                    )
                    return

                command_msg = {k: v for k, v in message.items() if k != "security"}
                self.logger.debug(
                    f"Processing command: {json.dumps(command_msg, indent=4)}"
                )

                command = command_msg.get("command")
                if not command:
                    self.logger.warning("Received message without command field")
                    return

                if command == "stop_sending_id":
                    self.logger.info("Stopping ID transmission")
                    self.send_id_flag = False

                elif command == "start_telemetry":
                    if self.telemetry_flag:
                        self.logger.info("Telemetry already running")
                        return

                    # Get required fields
                    self.flight_plan_id = command_msg.get("flight_plan_id")
                    self.gcs_id = command_msg.get("gcs_id")

                    if not self.flight_plan_id or not self.gcs_id:
                        self.logger.error("Missing required fields for telemetry start")
                        return

                    self.logger.info("Starting telemetry transmission")
                    self.telemetry_flag = True
                    self.send_id_flag = False
                    # Reset GCS coordinates
                    self.gcs_lat = None
                    self.gcs_lon = None

                    # Send telemetry start confirmation
                    confirmation = {
                        "status": "telemetry_started",
                        "flight_plan_id": self.flight_plan_id,
                        "serial_number": self.serial_number,
                    }
                    self.publish_signed_message(self.telemetry_topic, confirmation)

                    telemetry_thread = threading.Thread(
                        target=self.read_nmea_data, name="TelemetryThread"
                    )
                    telemetry_thread.daemon = (
                        True  # Ensure thread doesn't block program exit
                    )
                    telemetry_thread.start()

                elif command == "stop_telemetry":
                    if not self.telemetry_flag:
                        self.logger.info("Telemetry already stopped")
                        return

                    self.logger.info("Stopping telemetry transmission")
                    self.telemetry_flag = False

                    # Send telemetry end message
                    end_message = {
                        "status": "telemetry_ended",
                        "flight_plan_id": self.flight_plan_id,
                        "serial_number": self.serial_number,
                    }
                    self.logger.info(
                        f"Telemetry ended, sending message: {json.dumps(end_message, indent=4)}"
                    )
                    self.publish_signed_message(self.telemetry_topic, end_message)

                    if self.RESTART_DEV_ID_AFTER_TELEMETRY:
                        self.logger.info("Restarting ID transmission")
                        self.send_id_flag = True

                else:
                    self.logger.warning(f"Unknown command received: {command}")

            except json.JSONDecodeError as e:
                self.logger.error(
                    f"Invalid JSON on topic: {msg.topic}. Error: {e}. Payload: {msg.payload.decode()}"
                )
            except Exception as e:
                self.logger.exception(
                    f"Error processing message on topic: {msg.topic}. Error: {e}. Payload: {msg.payload.decode()}"
                )

    def publish_signed_message(self, topic, message):
        try:
            signed_message = self.message_security.sign_message(message)
            self.logger.debug(
                f"Sending signed message: {json.dumps(signed_message, indent=4)}"
            )
            self.client.publish(topic, json.dumps(signed_message))
        except Exception as e:
            self.logger.exception(
                f"Error publishing signed message to topic {topic}: {e}"
            )

    def send_dev_id(self):
        dev_id = {
            "snum": self.serial_number,
            "tnum": self.tail_number,
            "name": self.user_email,
        }
        self.logger.debug(f"Sending dev_id: {json.dumps(dev_id, indent=4)}")
        self.publish_signed_message(self.pub_topic, dev_id)

    def send_id(self):
        """Send device ID periodically when enabled"""
        while True:
            try:
                if self.send_id_flag and not self.telemetry_flag:
                    self.logger.info("Sending device identification")
                    self.send_dev_id()
                time.sleep(60)
            except Exception as e:
                self.logger.exception(f"Error in send_id loop: {e}")
                time.sleep(60)  # Keep trying even if there's an error

    def run(self):
        try:
            self.client.connect(
                self.ACTIVE_BROKER["address"], self.ACTIVE_BROKER["port"], 60
            )
            id_thread = threading.Thread(target=self.send_id)
            id_thread.daemon = True
            id_thread.start()
            self.client.loop_start()

            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        except Exception as e:
            self.logger.exception(f"Error running MQTT client: {e}")
        finally:
            try:
                self.telemetry_flag = False
                time.sleep(1)  # Give telemetry thread time to stop
                self.logger.info("Stopping MQTT client")
                self.client.disconnect()
                self.client.loop_stop()
            except Exception as e:
                self.logger.exception(f"Error during cleanup: {e}")

            # Close logging handlers
            handlers = self.logger.handlers[:]
            for handler in handlers:
                try:
                    handler.flush()
                    handler.close()
                    self.logger.removeHandler(handler)
                except Exception as e:
                    print(f"Error closing logging handler: {e}")
