#!/usr/bin/python3

from dataclasses import dataclass
import io
import subprocess
import sys

UPS_NAME = 'apc'
SMTP_HOSTNAME = 'in-v3.mailjet.com'
PATH_SMTP_CLI_CONFIG = '/opt/smtp-cli/smtp-cli.conf'


@dataclass
class Info:
    battery_level: int
    status: set[str]


@dataclass
class Email:
    from_name: str
    from_address: str
    to_name: str
    to_address: str
    host: str
    username: str
    password: str
    subject: str = ''
    body: str = ''


def get_upsc_info(field: str):
    result = subprocess.run(
        ['upsc', UPS_NAME, field],
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def collect_info() -> Info:
    return Info(
        battery_level=int(get_upsc_info('battery.charge')),
        status=set(get_upsc_info('ups.status').split(' ')),
    )


def parse_env_file(file: io.TextIOWrapper) -> dict[str, str]:
    config = {}
    for line in file:
        name, value = line.split('=', 1)
        config[name] = value.strip(" \t\n\r\"'")
    return config


def build_email(event: str, info: Info) -> Email:
    # Parse config
    with open(PATH_SMTP_CLI_CONFIG, 'rt') as f:
        config = parse_env_file(f)

    # Get subject and body
    if event == 'onbatt':
        subject = "UPS running on battery"
        message = "UPS is running on battery since 60 seconds."
    elif event == 'online':
        subject = "UPS power restored"
        message = "UPS is running on mains again."
    elif event == 'commbad':
        subject = "UPS connection broken"
        message = "Unable to contact UPS since 60 seconds."
    elif event == 'commok':
        subject = "UPS connection restored"
        message = "Contact with UPS has been restored."
    elif event == 'lowbatt':
        subject = "UPS BATTERY CRITICAL"
        message = "Battery level of UPS is critically low!"
    elif event == 'fsd':
        subject = "UPS FSD FLAG SET"
        message = "FSD flag has been set. Preparing for shutdown ..."
    elif event == 'shutdown':
        subject = "UPS SHUTDOWN"
        message = "Host is shutting down due to UPS."
    elif event == 'replbatt':
        subject = "Replace UPS battery"
        message = "The battery of the UPS should be replaced."
    elif event == 'nocomm':
        subject = "Unable to contact UPS"
        message = "The UPS cannot be contacted for monitoring."
    elif event == 'noparent':
        subject = "upsmon parent process crashed"
        message = "The upsmon parent process crashed. Shutdown is impossible!"
    elif event == 'test':  # For debugging/testing
        subject = "Test for upssched-cmd"
        message = "Request received to perform test run"
    else:
        subject = "Unknown UPS command received"
        message = f"I received an unknown UPS command: {event}"
    status = list(info.status)
    status.sort()
    body = f"{message}\n\nINFO:\n- level: {info.battery_level}/100\n- status: {' '.join(status)}"

    # Build email
    return Email(
        from_name=config['FROM_NAME'],
        from_address=config['FROM_EMAIL'],
        to_name=config['TO_EMAIL'],
        to_address=config['TO_EMAIL'],
        host=SMTP_HOSTNAME,
        username=config['USERNAME'],
        password=config['PASSWORD'],
        subject=subject,
        body=body,
    )


def main():
    # Send email
    email = build_email(sys.argv[1], collect_info())
    subprocess.run(
        [
            '/opt/smtp-cli/smtp-cli',
            '--from-name', email.from_name,
            '--from-address', email.from_address,
            '--to-name', email.to_name,
            '--to-address', email.to_address,
            '--host', email.host,
            '--username', email.username,
            '--password', email.password,
            '--subject', email.subject,
        ],
        input=email.body,
        capture_output=True,
        check=True,
        text=True,
    )


if __name__ == '__main__':
    main()
