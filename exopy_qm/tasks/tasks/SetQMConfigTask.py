import importlib

from exopy.tasks.api import (InstrumentTask)
from atom.api import Unicode
import sys

from exopy_qm.utils.dynamic_importer import *


class SetQMConfigTask(InstrumentTask):
    """ Updates the QM config.
    """
    path_to_config_file = Unicode().tag(pref=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def perform(self):
        directory = get_directory_from_path(self.path_to_program_file)
        module_name = get_module_name_from_path(self.path_to_program_file)

        sys.path.append(directory)

        module_with_program = importlib.import_module(module_name)
        module_with_program = importlib.reload(module_with_program)

        config_to_apply = module_with_program.get_config()

        self.driver.set_config(config_to_apply)
