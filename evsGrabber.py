from metavision_core.event_io.raw_reader import initiate_device
from metavision_core.event_io import EventsIterator
from metavision_sdk_core import PeriodicFrameGenerationAlgorithm

class CameraController:
    def __init__(self):
        self.device = initiate_device("")
        self.delta_t = 1E3
        self.fps = 10
        self.bias_diff_on = 0
        self.bias_diff_off = 0
        self.bias_interface = self.device.get_i_ll_biases()
        self.mv_iterator = None
        self.event_frame_gen = None

    def update_settings(self, delta_t=None, fps=None, bias_diff_on=None, bias_diff_off=None):
        if delta_t is not None:
            self.delta_t = delta_t
        if fps is not None:
            self.fps = fps
        if bias_diff_on is not None:
            self.bias_diff_on = bias_diff_on
            self.bias_interface.set("bias_diff_on", bias_diff_on)
        if bias_diff_off is not None:
            self.bias_diff_off = bias_diff_off
            self.bias_interface.set("bias_diff_off", bias_diff_off)

    def get_frame_generator(self):
        self.mv_iterator = EventsIterator.from_device(device=self.device, delta_t=self.delta_t)
        height, width = self.mv_iterator.get_size()
        self.event_frame_gen = PeriodicFrameGenerationAlgorithm(sensor_width=width, sensor_height=height, fps=self.fps)
        return self.event_frame_gen

camera_controller = CameraController()
