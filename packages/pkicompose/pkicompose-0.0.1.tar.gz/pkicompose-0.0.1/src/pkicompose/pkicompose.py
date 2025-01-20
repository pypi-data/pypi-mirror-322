import datetime
import os
from typing import Annotated

import typer
from cryptography import x509
from cryptography.hazmat._oid import NameOID
from loguru import logger
import yaml
from pycertauthority.CertificateAuthority import CertificateAuthority, CertificateAuthorityFactory
from pycertauthority.CertificateUtils import CertificateUtils


def get_datetime_from_block(start_time, block) -> datetime.datetime:
    if "years" in block.keys():
        start_time = start_time + datetime.timedelta(days=365*block['years'])
    if "days" in block.keys():
        start_time = start_time + datetime.timedelta(days=block['days'])
    if "hours" in block.keys():
        start_time = start_time + datetime.timedelta(hours=block['hours'])
    if "minutes" in block.keys():
        start_time = start_time + datetime.timedelta(minutes=block['minutes'])
    if "seconds" in block.keys():
        start_time = start_time + datetime.timedelta(minutes=block['seconds'])
    return start_time

def get_subject_from_block(common_name, block) -> x509.Name:
    elements = [x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, common_name)]
    if block is not None:
        for element in block:
            parts = element.split("=", 2)
            field_name = parts[0]
            field_value = parts[1]
            if field_name == "OU":
                elements.append(x509.NameAttribute(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME, field_value))
            elif field_name == "O":
                elements.append(x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, field_value))
            elif field_name == "C":
                elements.append(x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, field_value))
            elif field_name == "S" or field_name == "ST":
                elements.append(x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, field_value))
            elif field_name == "L":
                elements.append(x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, field_value))
    return x509.Name(elements)

def process(config):
    cas = {}
    certificates = {}

    for ca_name in config['cas'].keys():
        ca_details = config['cas'][ca_name]
        ca = None

        if os.path.exists(f"{ca_name}.crt"):
            logger.debug(f"Located {ca_name}.crt - using certificate for CA {ca_name}")
            ca_certificate = CertificateUtils.read_certificate_from_file(f"{ca_name}.crt")

            private_key = None
            if os.path.exists(f"{ca_name}.key"):
                logger.debug(f"Located {ca_name}.key - using private key for CA {ca_name}")
                private_key = CertificateUtils.read_private_key_from_file(f"{ca_name}.key")
            else:
                logger.warning(f"Unable to locate private key for CA {ca_name}, signing functions will be unavailable")

            signer = None
            if "signed_by" in ca_details.keys():
                if ca_details['signed_by'] in cas.keys():
                    signer = cas[ca_details['signed_by']]
                else:
                    logger.warning(f"Unable to locate CA signer for {ca_name}, looked for {ca_details['signed_by']}")

            ca = CertificateAuthority(ca_certificate, signer, private_key)
        else:
            private_key = None
            request = None

            if os.path.exists(f"{ca_name}.key"):
                logger.debug(f"Located {ca_name}.key - using private key for CA {ca_name}")
                private_key = CertificateUtils.read_private_key_from_file(f"{ca_name}.key")
            else:
                if os.path.exists(f"{ca_name}.csr"):
                    logger.debug(f"Located {ca_name}.csr - using certificate request for CA {ca_name}")
                    request = CertificateUtils.read_certificate_request_from_file(f"{ca_name}.csr")
                else:
                    key_size = 2048
                    if "key_size" in ca_details.keys():
                        key_size = ca_details["key_size"]
                    private_key = CertificateUtils.generate_rsa_private_key(key_size)
                    CertificateUtils.write_private_key_to_file(f"{ca_name}.key", private_key)
                    logger.info(f"Created new private key for CA {ca_name}, size: {key_size}")

            if "common_name" not in ca_details.keys():
                logger.error(f"Failed to create CA {ca_name}, missing parameter common_name!")
                continue

            # New CA
            if 'subject' in ca_details.keys():
                subject_detail = ca_details['subject']
            else:
                subject_detail = None
            subject = get_subject_from_block(ca_details['common_name'], subject_detail)
            expires = None
            if "expires_after" in ca_details.keys():
                expires = get_datetime_from_block(datetime.datetime.now(datetime.UTC), ca_details['expires_after'])

            if "signed_by" in ca_details.keys():
                if ca_details["signed_by"] not in cas:
                    logger.error(f"Failed to create CA {ca_name}, unable to find signing CA {ca_details['signed_by']}!")
                    continue
                signing_ca = cas[ca_details["signed_by"]]
                if private_key is not None:
                    ca = signing_ca.create_intermediate_ca(subject, private_key=private_key, not_valid_after=expires)
                else:
                    ca = signing_ca.create_intermediate_ca_with_request(request, subject, not_valid_after=expires)
                logger.info(
                    f"Created intermediate CA {ca_name}, common name: {ca.get_common_name()}, issuer: {signing_ca.get_common_name()}")
            else:
                # New root CA
                ca = CertificateAuthorityFactory.create_self_signed_ca(subject, private_key=private_key,
                                                                       not_valid_after=expires)
                logger.info(f"Created root CA {ca_name}, common name: {ca.get_common_name()}")

            CertificateUtils.write_certificate_to_file(f"{ca_name}.crt", ca.get_ca_certificate())

        cas[ca_name] = ca
        logger.info(f"Loaded CA {ca_name}, common name: {ca.get_common_name()}, has key: {ca.has_private_key()}")

    for cert_name in config['certificates'].keys():
        cert_details = config['certificates'][cert_name]

        if os.path.exists(f"{cert_name}.crt"):
            certificate = CertificateUtils.read_certificate_from_file(f"{cert_name}.crt")

            if 'subject' in cert_details.keys():
                subject_detail = cert_details['subject']
            else:
                subject_detail = None
            subject = get_subject_from_block(cert_details['common_name'], subject_detail)

            if certificate.subject == subject:
                if certificate.not_valid_after_utc > datetime.datetime.now(datetime.UTC):
                    logger.info(f"Skipping certificate {cert_name}, as it already exists and is not expired")
                    continue
                else:
                    logger.warning(f"Certificate {cert_name} exists, but is expired.  Will be re-generated.")
            else:
                logger.warning(f"Certificate {cert_name} exists, but subject has changed.  Will be re-generated.")

        expires = None
        if "expires_after" in cert_details.keys():
            expires = get_datetime_from_block(datetime.datetime.now(datetime.UTC), cert_details['expires_after'])

        request = None
        if os.path.exists(f"{cert_name}.csr"):
            logger.debug(f"Located {cert_name}.csr - using signing request for cert {cert_name}")
            request = CertificateUtils.read_certificate_request_from_file(f"{cert_name}.csr")
        else:
            private_key = None
            if os.path.exists(f"{cert_name}.key"):
                logger.debug(f"Located {cert_name}.key - using private key for certificate {cert_name}")
                private_key = CertificateUtils.read_private_key_from_file(f"{cert_name}.key")
            else:
                key_size = 2048
                if "key_size" in cert_details.keys():
                    key_size = cert_details["key_size"]
                private_key = CertificateUtils.generate_rsa_private_key(key_size)
                CertificateUtils.write_private_key_to_file(f"{cert_name}.key", private_key)
                logger.info(f"Created new private key for certificate {cert_name}, size: {key_size}")

            if "common_name" not in cert_details.keys():
                logger.error(f"Failed to create certificate request {cert_name}, missing parameter common_name!")
                continue

            if 'subject' in cert_details.keys():
                subject_detail = cert_details['subject']
            else:
                subject_detail = None
            subject = get_subject_from_block(cert_details['common_name'], subject_detail)

            request = CertificateUtils.generate_certificate_request(private_key, subject)
            CertificateUtils.write_certificate_request_to_file(f"{cert_name}.csr", request)
            logger.info(f"Created new certificate request for certificate {cert_name}")

        if "signed_by" not in cert_details.keys():
            logger.error(f"Failed to create certificate {cert_name}, missing parameter signed_by!")
            continue

        if cert_details["signed_by"] not in cas:
            logger.error(
                f"Failed to create certificate {cert_name}, unable to find signing CA {cert_details['signed_by']}!")
            continue

        signing_ca = cas[cert_details['signed_by']]
        if 'subject' in cert_details.keys():
            subject_detail = cert_details['subject']
        else:
            subject_detail = None
        subject = get_subject_from_block(request.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,
                                         subject_detail)

        sans = None
        if 'sans' in cert_details.keys():
            sans = []
            sans_raw = cert_details['sans']
            for san in sans_raw:
                sans.append(x509.DNSName(san))

        certificate = signing_ca.sign_request(request, subject=subject, subject_alternative_names=sans,
                                              not_valid_after=expires)
        CertificateUtils.write_certificate_to_file(f"{cert_name}.crt", certificate)
        certificate_cn = certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        certificates[cert_name] = certificate
        logger.info(
            f"Created certificate {cert_name}, common name: {certificate_cn}, issuer: {signing_ca.get_common_name()}")
    return True

def process_yaml(
        file_path: Annotated[str, typer.Argument(help="Path to the YAML file to process")] = "pkicompose.yaml"
):
    if not os.path.exists(file_path):
        logger.error(f"The specified YAML file {file_path} does not exist.")
        return False

    with open(file_path) as stream:
        config = yaml.safe_load(stream)
        return process(config)