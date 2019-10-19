from exopy.tasks.api import (InstrumentTask, validators)
from atom.api import Float, Unicode, Str, set_default
from qm.qua import *
import numbers
EMPTY_REAL = validators.SkipEmpty(types=numbers.Real)
EMPTY_INT = validators.SkipEmpty(types=numbers.Integral)


class SetInputDcOffsetByQeTask(InstrumentTask):
    """ Sets the input dc offset of the given element and port by the given offset value.
    """
    element = Unicode().tag(pref=True)
    output = Unicode().tag(pref=True)
    offset = Unicode().tag(pref=True, feval=EMPTY_REAL)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def perform(self):
        offset = self.format_and_eval_string(self.offset)
        self.driver.set_input_dc_offset_by_qe(self.element, self.output, float(offset))
