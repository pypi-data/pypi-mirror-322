import argparse
import logging
import os
import subprocess # nosec B404
import tempfile
import time


class QMIManager:
    def __init__(self, device="/dev/cdc-wdm0"):
        self.device = device
        self.logger = logging.getLogger(__name__)

    def qmicli_command(self, *args):
        """Execute qmicli command with given arguments."""
        command = ["qmicli", "-d", self.device] + list(args)
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True) # nosec B603
            self.logger.debug(f"qmicli output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"qmicli command failed: {e.stderr}")
        time.sleep(1)

    def wait_for_process(self, seconds):
        """Wait for a process to finish."""
        time.sleep(seconds)

    def disable_interface(self, interface):
        """Disable a network interface."""
        try:
            subprocess.run(["ip", "link", "set", interface, "down"], check=True) # nosec B603, B607
            self.logger.info(f"Disabled interface {interface}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to disable interface {interface}: {e}")

    def enable_raw_ip_mode(self, interface):
        """Enable raw IP mode."""
        raw_ip_path = f"/sys/class/net/{interface}/qmi/raw_ip"
        try:
            with open(raw_ip_path, "w") as f:
                f.write("Y")
            self.logger.info(f"Enabled raw IP mode for {interface}")
        except IOError as e:
            self.logger.error(f"Failed to enable raw IP mode: {e}")

    def enable_interface(self, interface):
        """Enable a network interface."""
        try:
            subprocess.run(["ip", "link", "set", interface, "up"], check=True) # nosec B603, B607
            self.logger.info(f"Enabled interface {interface}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to enable interface {interface}: {e}")

    def start_qmi_network(self):
        """Start the QMI network."""
        state_file = os.path.join(tempfile.gettempdir(), f"qmi-network-state-{os.path.basename(self.device)}")
        if os.path.exists(state_file):
            try:
                os.remove(state_file)
                self.logger.info(f"Removed previous QMI state file: {state_file}")
            except OSError as e:
                self.logger.warning(f"Failed to remove QMI state file: {e}")
                self.logger.warning(f"Failed to remove QMI state file: {e}")

        try:
            subprocess.run(["qmi-network", self.device, "start"], check=True) # nosec B603, B607
            self.logger.info("QMI network started successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start QMI network: {e}")

    def configure_interface(self, interface):
        """Configure network interface using udhcpc."""
        try:
            subprocess.run(["udhcpc", "-q", "-f", "-i", interface], check=True) # nosec B603, B607
            self.logger.info(f"Interface {interface} configured via DHCP")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to configure interface via DHCP: {e}")

    def source_env(self, script_path):
        """Source an environment script and update current environment."""
        if not os.path.exists(script_path):
            self.logger.error(f"Environment script not found: {script_path}")
            return False

        try:
            # Execute the script and capture its output
            command = ["/bin/bash", "-c", f"source {script_path} && env"]
            output = subprocess.check_output(command, text=True) # nosec B603

            # Parse and update environment variables
            for line in output.splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

            self.logger.info(f"Successfully sourced environment from {script_path}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to source environment script: {e}")
            return False

    def execute(self):
        """Execute the sequence of commands."""
        self.logger.info("Starting QMI initialization sequence...")
        self.wait_for_process(5)
        self.qmicli_command("--dms-get-operating-mode")
        self.qmicli_command("--nas-get-signal-strength")
        self.disable_interface("wwan0")
        self.enable_raw_ip_mode("wwan0")
        self.enable_interface("wwan0")
        self.qmicli_command("--wda-get-data-format")
        self.qmicli_command("--wds-start-network=ip-type=4,apn=etisalat.ae")
        self.start_qmi_network()
        self.wait_for_process(1)
        self.configure_interface("wwan0")
        self.wait_for_process(2)
        config_path = "/usr/local/bin/utm/config/ussp_config.sh"
        if not self.source_env(config_path):
            self.logger.error("Failed to initialize environment variables")

        self.wait_for_process(10)
        self.logger.info("QMI initialization sequence completed")


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Manage QMI device.")
    parser.add_argument(
        "-d",
        "--device",
        default="/dev/cdc-wdm0",
        help="Specify the QMI device (default: /dev/cdc-wdm0)",
    )
    args = parser.parse_args()

    qmi_manager = QMIManager(device=args.device)
    qmi_manager.execute()


if __name__ == "__main__":
    main()
