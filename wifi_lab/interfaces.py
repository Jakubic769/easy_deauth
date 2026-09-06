import subprocess


def run_command(command):
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def list_wifi_interfaces():
    output = run_command(["iw", "dev"])
    return [
        line.strip().split()[1]
        for line in output.splitlines()
        if line.strip().startswith("Interface ")
    ]


def enable_monitor_mode(interface):
    run_command(["sudo", "ip", "link", "set", interface, "down"])
    run_command(["sudo", "iw", "dev", interface, "set", "type", "monitor"])
    run_command(["sudo", "ip", "link", "set", interface, "up"])
    return interface


def restore_managed_mode(interface):
    run_command(["sudo", "ip", "link", "set", interface, "down"])
    run_command(["sudo", "iw", "dev", interface, "set", "type", "managed"])
    run_command(["sudo", "ip", "link", "set", interface, "up"])
