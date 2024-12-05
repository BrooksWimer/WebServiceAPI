# used for certificate conversion
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend


# get client specific credentials
from Properties import *

def convert_p12_to_pem(p12_path, p12_password, pem_path):
    # Read the p12 file
    with open(p12_path, "rb") as p12_file:
        p12_data = p12_file.read()

    # Load the p12 file
    p12 = pkcs12.load_key_and_certificates(p12_data, p12_password.encode(), default_backend())

    # Extract the private key
    private_key = p12[0]
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Extract the certificate
    certificate = p12[1]
    certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)

    # Extract the intermediate certificates
    intermediate_certificates = p12[2]
    intermediate_pems = b""
    for intermediate_certificate in intermediate_certificates:
        intermediate_pems += intermediate_certificate.public_bytes(serialization.Encoding.PEM)

    # Combine the private key, certificate, and intermediates into one PEM file
    with open(pem_path, "wb") as pem_file:
        pem_file.write(private_key_pem)
        pem_file.write(certificate_pem)
        pem_file.write(intermediate_pems)

    print(f"PEM file created at: {pem_path}")


# call the function
convert_p12_to_pem(CLIENT_CERT_PATH, CERT_PASSWORD, COMBINED_CERT_PATH)

