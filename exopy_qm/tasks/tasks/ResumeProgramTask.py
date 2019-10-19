from exopy.tasks.api import (InstrumentTask)
from atom.api import Float, Unicode, Str, set_default
from qm.qua import *


class ResumeProgramTask(InstrumentTask):
    """ Resumes a paused program.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def perform(self):
        self.driver.resume()
