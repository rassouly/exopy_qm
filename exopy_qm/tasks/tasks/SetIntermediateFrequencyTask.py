from exopy.tasks.api import (InstrumentTask)
from atom.api import Float, Unicode, Str, set_default


class SetIntermediateFrequencyTask(InstrumentTask):
    """ Sets the intermediate frequency of the given element.
    """
    element = Unicode().tag(pref=True)
    intermediate_frequency = Float().tag(pref=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def perform(self):
        self.driver.set_intermediate_frequency(self.element, self.intermediate_frequency)
