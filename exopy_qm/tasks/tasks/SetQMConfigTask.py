import importlib

from exopy.tasks.api import InstrumentTask
from atom.api import Unicode, Typed
import sys

from exopy_qm.utils.dynamic_importer import *


class SetQMConfigTask(InstrumentTask):
    """ Updates the QM config.

    """

    #: String containing the path to a file with 2 functions
    #: get_parameters() and get_config(params)
    path_to_config_file = Unicode().tag(pref=True)

    #: Dictionary containing all the parameters used in the configuration
    parameters = Typed(dict).tag(pref=True)

    #: Dictionary containing the comments for the parameters used in the configuration
    comments = Typed(dict).tag(pref=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _post_setattr_path_to_config_file(self, old, new):
        self.comments = {}

        if new:
            try:
                importlib.invalidate_caches()
                directory = get_directory_from_path(self.path_to_config_file)
                module_name = get_module_name_from_path(self.path_to_config_file)

                sys.path.append(directory)

                module_with_config = importlib.import_module(module_name)
                module_with_config = importlib.reload(module_with_config)

                params = module_with_config.get_parameters()

                tmp = {}  # Temporary dict to avoid updating the view needlessly
                # find the default values and comments
                for i in params:
                    if len(params[i]) == 1:
                        if i not in self.parameters:
                            tmp[i] = str(params[i])
                        else:
                            tmp[i] = self.parameters[i]
                        self.comments = ''
                    else:
                        if i not in self.parameters:
                            tmp[i] = str(params[i][0])
                        else:
                            tmp[i] = self.parameters[i]
                        self.comments[i] = str(params[i][1])
                self.parameters = tmp

            except:
                print('Config cannot be loaded from {}\n'.format(new))
                self.parameters = {}

    def perform(self):
        directory = get_directory_from_path(self.path_to_config_file)
        module_name = get_module_name_from_path(self.path_to_config_file)

        sys.path.append(directory)

        module_with_config = importlib.import_module(module_name)
        module_with_config = importlib.reload(module_with_config)

        # Convert all the parameters to floats
        params = {}
        for i in self.parameters:
            params[i] = float(self.format_and_eval_string(self.parameters[i]))

        config_to_apply = module_with_config.get_config(params)

        self.driver.set_config(config_to_apply)
