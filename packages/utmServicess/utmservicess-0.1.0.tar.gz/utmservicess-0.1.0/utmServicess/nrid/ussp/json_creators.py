def create_send_telemetry_json_body(
    latitude,
    longitude,
    altitude,
    timestamp,
    pilot_latitude,
    pilot_longitude,
    serial_number,
    tail_number,
):
    return {
        "telemetry": {
            "model": "Mavic 2 Enterprise Dual",
            "tailNumber": tail_number,
            "serialNumber": serial_number,
            "type": "hover",
            "battery": 75,
            "heading": 0,
            "takeoffLocation": "null",
            "isFlying": False,
            "flightStatus": "notactive",
            "satellite": 10,
            "velocity": {"x": 0.0, "y": 0.0, "z": 0.0},
            "pitch": 0,
            "roll": 0,
            "yaw": 0,
            "position": {
                "coordinates": {"latitude": latitude, "longitude": longitude},
                "AGL": altitude,
                "ASL": 0,
            },
            "flightMode": "controlled",
            "timestamp": timestamp.strftime("%a %b %d %Y %H:%M:%S GMT+0000"),
            "upLinkRemoteControllerSignalQuality": 75,
            "sign": "USS-10",
            "waypointIndex": -1,
            "pilot": {
                "userEmail": '"EG"',
                "location": {
                    "AGL": 0,
                    "coordinates": {
                        "latitude": pilot_latitude,
                        "longitude": pilot_longitude,
                    },
                },
            },
        },
        "airSituationType": "full",
    }


def create_blender_telemetry_json_body(
    flight_id,
    latitude,
    longitude,
    altitude,
    timestamp,
    aircraft_serial,
    operator_id,
):
    telemetry_data = {
        "observations": [
            {
                "current_states": [
                    {
                        "timestamp": {"value": timestamp, "format": "RFC3339"},
                        "timestamp_accuracy": 0.0,
                        "operational_status": "Undeclared",
                        "position": {
                            "lat": latitude,
                            "lng": longitude,
                            "alt": altitude,
                            "accuracy_h": "HAUnknown",
                            "accuracy_v": "VAUnknown",
                            "extrapolated": True,
                        },
                        "track": 0,
                        "speed": 0,
                        "speed_accuracy": "SAUnknown",
                        "vertical_speed": 0,
                        "height": {
                            "distance": 0,
                            "reference": "TakeoffLocation",
                        },
                    }
                ],
                "flight_details": {
                    "rid_details": {
                        "id": flight_id,
                        "operator_id": operator_id,
                        "operation_description": "Test operation",
                    },
                    "eu_classification": {
                        "category": "EUCategoryUndefined",
                        "class": "EUClassUndefined",
                    },
                    "uas_id": {
                        "serial_number": aircraft_serial,
                        "registration_number": operator_id,
                        "utm_id": aircraft_serial,
                        "specific_session_id": "Unknown",
                    },
                    "operator_location": {
                        "position": {
                            "lng": longitude,
                            "lat": latitude,
                            "accuracy_h": "HAUnknown",
                            "accuracy_v": "VAUnknown",
                        },
                        "altitude": altitude,
                        "altitude_type": "Takeoff",
                    },
                    "auth_data": {"format": "string", "data": 0},
                    "serial_number": aircraft_serial,
                    "registration_number": operator_id,
                },
            }
        ]
    }
    return telemetry_data
