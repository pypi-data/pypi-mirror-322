import os
import base64
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from OpenSSL import crypto


class non_repudiation_utils:
    def __init__(self, client_cert_path, private_key_path, use_non_repudiation=False):
        self.use_non_repudiation = use_non_repudiation
        self.client_cert_path = client_cert_path
        self.private_key_path = private_key_path
        self.client_cert_pem = ""
        self.client_private_key_pem = ""
        self.base64_client_cert = ""
        self.ecdsa_key_pair = None
        self.check_and_generate_certificate_and_key()


    def check_and_generate_certificate_and_key(self):
        cert_exists = os.path.exists(self.client_cert_path)
        key_exists = os.path.exists(self.private_key_path)
        cert_expired = (
            self.is_certificate_expired(self.client_cert_path) if cert_exists else True
        )

        if not cert_exists or not key_exists or cert_expired:
            print("Generating new certificate and key.")
            self.generate_certificate_and_key()
        else:
            print("Using existing certificate and key files.")
            self.load_existing_certificate_and_key()

    def is_certificate_expired(self, cert_path):
        with open(cert_path, "rb") as cert_file:
            cert_data = cert_file.read()
            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)
            return cert.has_expired()

    def generate_certificate_and_key(self):
        if not self.use_non_repudiation:
            # Generate key using cryptography
            private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
            self.ecdsa_key_pair = private_key

            # Convert private key to PEM format with 'EC PRIVATE KEY' headers
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,  # Use TraditionalOpenSSL
                encryption_algorithm=serialization.NoEncryption(),
            )
            pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, private_pem)

            # Save the private key to a file
            with open(self.private_key_path, "wb") as key_file:
                key_file.write(private_pem)

            # Generate certificate
            cert = crypto.X509()
            cert.get_subject().C = "AE"
            cert.get_subject().O = "TII"
            cert.get_subject().OU = "SSRC"
            cert.get_subject().CN = "SSRC Drone"
            cert.set_serial_number(1)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
            cert.set_issuer(cert.get_subject())
            cert.set_pubkey(pkey)
            cert.sign(pkey, "sha256")

            # Save the certificate to a file
            with open(self.client_cert_path, "wb") as cert_file:
                cert_file.write(crypto.dump_certificate(crypto.FILETYPE_ASN1, cert))

            # Store PEM representations
            self.client_cert_pem = crypto.dump_certificate(
                crypto.FILETYPE_PEM, cert
            ).decode("utf-8")
            self.base64_client_cert = base64.b64encode(
                crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
            ).decode("utf-8")
            self.client_private_key_pem = private_pem.decode("utf-8")

    def load_existing_certificate_and_key(self):
        with open(self.client_cert_path, "rb") as cert_file:
            cert_data = cert_file.read()
            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)
            self.client_cert_pem = crypto.dump_certificate(
                crypto.FILETYPE_PEM, cert
            ).decode("utf-8")
            self.base64_client_cert = base64.b64encode(cert_data).decode("utf-8")

        with open(self.private_key_path, "rb") as key_file:
            key_data = key_file.read()
            self.client_private_key_pem = key_data.decode("utf-8")
            self.ecdsa_key_pair = serialization.load_pem_private_key(
                key_data, password=None, backend=default_backend()
            )

    def sign_data_with_ecdsa_key(self, private_key_pem, sign_base):
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(), password=None, backend=default_backend()
            )
            signature = private_key.sign(sign_base.encode(), ec.ECDSA(hashes.SHA256()))
            r, s = utils.decode_dss_signature(signature)
            ieee_sig = r.to_bytes(32, byteorder="big") + s.to_bytes(32, byteorder="big")
            return base64.b64encode(ieee_sig).decode("utf-8")

    def verify_ecdsa_signature(
        self, public_key_pem, response_signature, response_sign_base
    ):
        try:
            public_key = serialization.load_pem_public_key(public_key_pem.encode())
            decoded_signature = base64.b64decode(response_signature)
            if len(decoded_signature) != 64:
                print(
                    f"Invalid signature length. Expected 64 bytes, got {len(decoded_signature)}."
                )
                return False

            r = int.from_bytes(decoded_signature[:32], byteorder="big")
            s = int.from_bytes(decoded_signature[32:], byteorder="big")

            signature = utils.encode_dss_signature(r, s)
            public_key.verify(
                signature, response_sign_base.encode(), ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {str(e)}")
            return False



    @staticmethod
    def base64_encode(data):
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def get_pem_formatted_string(input_data, data_type):
        if isinstance(input_data, bytes):
            header = f"-----BEGIN {data_type}-----".encode("ascii")
        else:
            header = f"-----BEGIN {data_type}-----"

        if header in input_data:
            print(f"{data_type} is already in PEM format.")
            if isinstance(input_data, bytes):
                return input_data.decode("utf-8")
            else:
                return input_data
        print(f"Converting {data_type} from DER to PEM format.")
        return non_repudiation_utils.convert_der_to_pem(input_data, data_type)

    @staticmethod
    def convert_der_to_pem(der_data, data_type):
        if data_type == "CERTIFICATE":
            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der_data)
            return crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8")
        elif data_type == "EC PRIVATE KEY":
            key = crypto.load_privatekey(crypto.FILETYPE_ASN1, der_data)
            return crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("utf-8")
        else:
            raise ValueError(f"Unsupported type for PEM conversion: {data_type}")

    def _parse_ec_point(self, ec_point_der):
        # Check if the first byte is the tag for OCTET STRING (0x04)
        if ec_point_der[0] != 0x04:
            raise ValueError("Invalid EC_POINT format")

        # Determine the length of the length field
        length_byte = ec_point_der[1]
        if length_byte & 0x80:
            num_length_bytes = length_byte & 0x7F
            length = int.from_bytes(
                ec_point_der[2 : 2 + num_length_bytes], byteorder="big"
            )
            ec_point_start = 2 + num_length_bytes
        else:
            length = length_byte
            ec_point_start = 2

        # Extract the EC point
        ec_point = ec_point_der[ec_point_start : ec_point_start + length]
        return ec_point
