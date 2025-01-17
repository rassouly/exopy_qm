from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *


class QuantumMachine(object):
    def __init__(self, connection_info):
        self.connection_info = connection_info

        port = ""
        if self.connection_info["gateway_port"] is not None and self.connection_info["gateway_port"] != "":
            port = self.connection_info["gateway_port"]

        ip = ""
        if self.connection_info["gateway_ip"] is not None and self.connection_info["gateway_ip"] != "":
            ip = self.connection_info["gateway_ip"]

        if ip != "" and port != "":
            self.qmm = QuantumMachinesManager(host=ip, port=port)
        else:
            self.qmm = QuantumMachinesManager()

        self.qmObj = None
        self.job = None

    def connect(self):
        """
        Already connected in the constructor
        :return:
        """
        pass

    def connected(self):
        """Return whether or not commands can be sent to the instrument
        """
        try:
            print(self.qmObj.list_controllers())
        except Exception:
            return False

        return True

    def close_connection(self):
        if self.qmObj:
            self.qmObj.close()

    def set_config(self, config):
        self.qmObj = self.qmm.open_qm(config)

    def execute_program(self, prog, duration_limit, data_limit):
        self.job = self.qmObj.execute(prog, duration_limit=duration_limit, data_limit=data_limit, force_execution=True)

    def resume(self):
        self.job.resume()

    def set_output_dc_offset_by_qe(self, element, input, offset):
        self.qmObj.set_output_dc_offset_by_element(element, input, offset)

    def set_input_dc_offset_by_qe(self, element, output, offset):
        self.qmObj.set_input_dc_offset_by_element(element, output, offset)

    def get_results(self):
        return self.job.get_results()

    def set_io_values(self, io1_value, io2_value):
        self.qmObj.set_io_values(io1_value, io2_value)

    def get_io_values(self):
        return self.qmObj.get_io_values()

    def set_mixer_correction(self, mixer, intermediate_frequency, lo_frequency, values):
        self.qmObj.set_mixer_correction(mixer, intermediate_frequency, lo_frequency, values)

    def set_intermediate_frequency(self, qe, intermediate_frequency):
        self.qmObj.set_intermediate_frequency(qe, intermediate_frequency)

    def set_digital_delay(self, qe, digital_input, delay):
        self.qmObj.set_digital_delay(qe, digital_input, delay)

    def set_digital_buffer(self, qe, digital_input, buffer):
        self.qmObj.set_digital_buffer(qe, digital_input, buffer)
