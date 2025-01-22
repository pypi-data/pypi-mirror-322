import json
import base64
import hashlib
import time
import requests
from . import json_creators
from urllib.parse import urlparse
from OpenSSL import crypto


class network_utility_interface:
    def __init__(self, non_repudiation, cert_path):
        self.non_repudiation = non_repudiation
        self.cert_path = cert_path
        self.air_situation_data = None

    def create_content_digest(self, data):
        if isinstance(data, dict):
            json_string = json.dumps(data, separators=(",", ":"))
        elif isinstance(data, str):
            json_string = data
        else:
            raise ValueError("Data must be either a dictionary or a JSON string")

        hash_object = hashlib.sha512(json_string.encode("utf-8"))
        content_digest = f"sha-512=:{base64.b64encode(hash_object.digest()).decode()}:"
        return content_digest

    def extract_properties_from_response(self, response, url, method):
        cert_bundle_base64 = response.headers.get("x-certificate-bundle", "")
        cert_bundle_pem = base64.b64decode(cert_bundle_base64)

        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_bundle_pem)
        server_public_key = cert.get_pubkey()
        server_public_key_pem = crypto.dump_publickey(
            crypto.FILETYPE_PEM, server_public_key
        ).decode()

        response_signature = response.headers.get("signature", "").split(":")[1]
        response_sign_base = self.parse_covered_content_from_ietf_request(
            response, url, method
        )

        return {
            "serverPublicKeyPem": server_public_key_pem,
            "responseSignature": response_signature,
            "responseSignBase": response_sign_base,
        }

    def parse_covered_content_from_ietf_request(self, response, url, method):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme
        authority = parsed_url.netloc

        signature_input = response.headers.get("signature-input", "")
        signature_param = signature_input.split("sig1=")[1]
        content_digest = response.headers.get("content-digest", "")

        target_uri = f"{scheme}://{authority}{parsed_url.path}"

        result_object = {
            "@method": method,
            "@authority": authority,
            "@target-uri": target_uri,
            "content-digest": content_digest,
            "@signature-params": signature_param,
        }

        formatted_output = "\n".join([f'"{k}": {v}' for k, v in result_object.items()])
        return formatted_output.strip()

    def create_signature_input(self, current_timestamp):
        return f'sig1=("@method" "@authority" "@target-uri" "content-digest");created={current_timestamp};keyid="ecdsa";alg="ecdsa-p256-sha256"'

    def get_certificate_bundle(self, cert_path):
        with open(cert_path, "rb") as cert_file:
            cert_data = cert_file.read()

        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)
        pem_cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8")

        return base64.b64encode(pem_cert.encode("utf-8")).decode("utf-8")

    def add_headers_to_request(
        self, headers, data, token, non_repudiation, total_url, method="POST"
    ):
        headers["Accept"] = "application/json"
        if method.upper() != "GET":
            headers["Content-Type"] = "application/json"

        if non_repudiation:
            if data is not None:
                content_digest = self.create_content_digest(data)
            else:
                content_digest = ""
            current_timestamp = int(time.time())
            parsed_url = urlparse(total_url)
            authority = parsed_url.netloc
            target_uri = total_url

            signature_base = f'"@method": {method}\n"@authority": {authority}\n"@target-uri": {target_uri}'
            if content_digest:
                signature_base += f'\n"content-digest": {content_digest}'
            signature_base += f'\n"@signature-params": ("@method" "@authority" "@target-uri" "content-digest");created={current_timestamp};keyid="ecdsa";alg="ecdsa-p256-sha256"'

            signature = self.non_repudiation.sign_data_with_ecdsa_key(
                self.non_repudiation.client_private_key_pem, signature_base
            )

            cert_bundle = self.get_certificate_bundle(self.cert_path)
            signature_input = self.create_signature_input(current_timestamp)

            if content_digest:
                headers["Content-Digest"] = content_digest
            headers["Signature"] = f"sig1=:{signature}:"
            headers["X-Certificate-Bundle"] = cert_bundle
            headers["Signature-Input"] = signature_input

        if token:
            headers["Authorization"] = f"Bearer {token}"

    def authenticate(self, user_name, password, auth_url):
        auth_data = json.dumps(
            {"userName": user_name, "password": password}, separators=(",", ":")
        )
        response = self.make_request(auth_url, auth_data, None, False)

        if not self.handle_response(
            response, "Authentication", auth_url, "POST", False
        ):
            raise Exception("Authentication failed.")

        response_json = json.loads(response.body)
        token = response_json["reason"]["token"]
        self.token = token
        return token

    def make_request(
        self,
        url,
        data,
        token,
        non_repudiation,
        method="POST",
        retries=3,
        base_timeout=30,
        max_timeout=120,
    ):
        headers = self.prepare_headers(data, token, non_repudiation, url, method)
        json_data = self.convert_data_to_json(data)

        for attempt in range(retries):
            try:
                timeout = min(base_timeout * (2**attempt), max_timeout)
                if method.upper() == "POST":
                    response = requests.post(
                        url, data=json_data, headers=headers, timeout=timeout
                    )
                elif method.upper() == "PUT":
                    response = requests.put(
                        url, data=json_data, headers=headers, timeout=timeout
                    )
                elif method.upper() == "GET":
                    response = requests.get(url, headers=headers, timeout=timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                response.raise_for_status()
                return self.create_network_response(response)
            except requests.HTTPError as e:
                print(f"HTTPError: {str(e)}")
                if response.status_code == 401:
                    print("Authentication failed. Check your token.")
                elif response.status_code == 404:
                    print("Endpoint not found. Verify the URL.")
                elif response.status_code >= 500:
                    print("Server error. Try again later.")
                else:
                    print(f"Unhandled HTTPError: {response.status_code}")
                if attempt < retries - 1:
                    wait_time = 2**attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Request failed after {retries} attempts.")
                    raise
            except requests.RequestException as e:
                print(f"RequestException: {str(e)}")

    def prepare_headers(self, data, token, non_repudiation, url, method="POST"):
        headers = {}
        json_data = self.convert_data_to_json(data)
        self.add_headers_to_request(
            headers, json_data, token, non_repudiation, url, method
        )
        return headers

    @staticmethod
    def convert_data_to_json(data):
        if data is None:
            return None
        elif isinstance(data, dict):
            return json.dumps(data, separators=(",", ":"))
        elif isinstance(data, str):
            return data
        else:
            raise ValueError("Data must be either a dictionary or a JSON string")

    @staticmethod
    def create_network_response(response):
        return type(
            "NetworkResponse",
            (),
            {
                "body": response.content,
                "headers": response.headers,
                "status_code": response.status_code,
                "text": response.text,
                "json": response.json,
            },
        )

    def set_token(self, new_token):
        self.token = new_token

    def get_token(self):
        return self.token

    def handle_response(
        self,
        response,
        action,
        url,
        method,
        non_repudiation,
        expected_status_codes=[200],
    ):
        try:
            response_json = json.loads(response.body)
            if response.status_code in expected_status_codes:
                if non_repudiation:
                    try:
                        properties = self.extract_properties_from_response(
                            response, url, method
                        )
                        is_valid = self.non_repudiation.verify_ecdsa_signature(
                            properties["serverPublicKeyPem"],
                            properties["responseSignature"],
                            properties["responseSignBase"],
                        )
                        if not is_valid:
                            print("Signature verification failed.")
                            print(
                                f"{action} failed due to signature verification failure."
                            )
                            return False
                    except Exception as e:
                        print(f"Error verifying signature: {str(e)}")
                        print(
                            f"{action} failed due to error in signature verification."
                        )
                        return False
                return True
            else:
                error_message = (
                    f"{action} failed with status code {response.status_code}."
                )
                if "message" in response_json:
                    error_message += f" Error: {response_json['message']}"
                print(error_message)
                return False
        except json.JSONDecodeError:
            print(f"Failed to parse response JSON for {action}")
            print(f"Response body: {response.body.decode('utf-8', errors='replace')}")
            return False

    def send_telemetry(
        self,
        token,
        latitude,
        longitude,
        altitude,
        timestamp,
        pilot_latitude,
        pilot_longitude,
        serial_number,
        tail_number,
        telemetry_url,
        non_repudiation_flag,
    ):
        telemetry_data = json_creators.create_send_telemetry_json_body(
            latitude,
            longitude,
            altitude,
            timestamp,
            pilot_latitude,
            pilot_longitude,
            serial_number,
            tail_number,
        )
        response = self.make_request(
            telemetry_url,
            json.dumps(telemetry_data, separators=(",", ":")),
            token,
            non_repudiation_flag,
        )
        if not self.handle_response(
            response, "Telemetry", telemetry_url, "POST", non_repudiation_flag
        ):
            raise requests.exceptions.RequestException(
                f"Telemetry request failed. Response body: {response.text}"
            )

        return response.status_code

    def authenticate_blender(self, client_id, client_secret, url):
        payload = {
            "grant_type": "client_credentials",
            "scope": "blender.write blender.read",
            "audience": "blender.utm.dev.airoplatform.com",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            response.raise_for_status()
            response_data = response.json()
            self.token = response_data.get("access_token")
            return self.token
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            return None

    def send_telemetry_blender(
        self,
        token,
        flight_id,
        latitude,
        longitude,
        altitude,
        timestamp,
        aircraft_serial,
        operator_id,
        url,
        non_repudiation_flag,
    ):
        telemetry_data = json_creators.create_blender_telemetry_json_body(
            flight_id,
            latitude,
            longitude,
            altitude,
            timestamp,
            aircraft_serial,
            operator_id,
        )

        response = self.make_request(
            url,
            telemetry_data,
            token,
            non_repudiation_flag,
            method="PUT",
        )

        if self.handle_response(
            response,
            "Send Telemetry Blender",
            url,
            "PUT",
            non_repudiation_flag,
            expected_status_codes=[201],
        ):
            print(f"Telemetry sent successfully at {timestamp}")
            return True
        else:
            print(f"Error sending telemetry: {response.status_code}")
            print(f"Response: {response.text}")
            return False
