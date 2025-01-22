import json
import time
import base64
from OpenSSL import crypto
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class message_security_utils:
    def __init__(self, non_repudiation, cert_path, key_path):
        self.non_repudiation = non_repudiation
        self.cert_path = cert_path
        self.key_path = key_path
        self.load_certificate_and_key()

    def load_certificate_and_key(self):
        with open(self.cert_path, "rb") as cert_file:
            cert_data = cert_file.read()
            self.certificate = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)

        with open(self.key_path, "rb") as key_file:
            key_data = key_file.read()
            self.private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_data)

    def sign_message(self, message):
        content_digest = self.create_content_digest(json.dumps(message))
        current_timestamp = int(time.time())

        signature_base = f'"content-digest": {content_digest}\n"@signature-params": ("content-digest");created={current_timestamp};keyid="ecdsa";alg="ecdsa-p256-sha256"'

        signature = self.non_repudiation.sign_data_with_ecdsa_key(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, self.private_key).decode(
                "utf-8"
            ),
            signature_base,
        )

        cert_bundle = self.get_certificate_bundle()

        message["security"] = {
            "content_digest": content_digest,
            "signature": signature,
            "cert_bundle": cert_bundle,
            "timestamp": current_timestamp,
        }

        return message

    def verify_message(self, message):
        if "security" not in message:
            print("No security information in message")
            return False

        security = message["security"]
        content_digest = self.create_content_digest(
            json.dumps({k: v for k, v in message.items() if k != "security"})
        )

        if content_digest != security["content_digest"]:
            print("Content digest mismatch")
            return False

        signature_base = f'"content-digest": {content_digest}\n"@signature-params": ("content-digest");created={security["timestamp"]};keyid="ecdsa";alg="ecdsa-p256-sha256"'

        try:
            public_key_pem = self.extract_public_key_from_cert_bundle(
                security["cert_bundle"]
            )
        except Exception as e:
            print(f"Failed to extract public key: {str(e)}")
            return False

        verification_result = self.non_repudiation.verify_ecdsa_signature(
            public_key_pem, security["signature"], signature_base
        )

        return verification_result

    def create_content_digest(self, data):
        serialized = json.dumps(json.loads(data), separators=(",", ":"))

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(serialized.encode())
        hash_bytes = digest.finalize()

        base64_encoded = base64.b64encode(hash_bytes).decode()

        result = f"sha-256=:{base64_encoded}:"
        return result

    def get_certificate_bundle(self):
        bundle = base64.b64encode(
            crypto.dump_certificate(crypto.FILETYPE_ASN1, self.certificate)
        ).decode()
        return bundle

    def extract_public_key_from_cert_bundle(self, cert_bundle):
        try:
            cert_data = base64.b64decode(cert_bundle)

            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)

            public_key = cert.get_pubkey()
            public_key_pem = crypto.dump_publickey(
                crypto.FILETYPE_PEM, public_key
            ).decode("utf-8")
            return public_key_pem
        except Exception as e:
            print(f"Error in extract_public_key_from_cert_bundle: {str(e)}")
            print(f"Cert bundle: {cert_bundle}")
            raise
