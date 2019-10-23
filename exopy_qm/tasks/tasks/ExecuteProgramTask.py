import importlib

from exopy.tasks.api import InstrumentTask
from atom.api import Unicode, Long, Typed
import sys

from exopy_qm.utils.dynamic_importer import *


class ExecuteProgramTask(InstrumentTask):
    """ Executes a qua program.
    """
    path_to_program_file = Unicode().tag(pref=True)
    duration_limit = Long(default=int(1000)).tag(pref=True)
    data_limit = Long(default=int(20000)).tag(pref=True)
    
    #: Dictionary containing all the parameters used in the program
    parameters = Typed(dict).tag(pref=True)

    #: Dictionary containing the comments for the parameters used in the program
    comments = Typed(dict).tag(pref=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def _post_setattr_path_to_program_file(self, old, new):
        self.comments = {}

        if new:
            try:
                importlib.invalidate_caches()
                directory = get_directory_from_path(self.path_to_program_file)
                module_name = get_module_name_from_path(self.path_to_program_file)

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
                print('Program cannot be loaded from {}\n'.format(new))
                self.parameters = {}


    def perform(self):
        directory = get_directory_from_path(self.path_to_program_file)
        module_name = get_module_name_from_path(self.path_to_program_file)

        sys.path.append(directory)

        module_with_program = importlib.import_module(module_name)
        module_with_program = importlib.reload(module_with_program)
        
        # Convert all the parameters to floats
        params = {}
        for i in self.parameters:
            params[i] = float(self.parameters[i])

        program_to_execute = module_with_program.get_prog(params)

        self.driver.execute_program(program_to_execute, self.duration_limit, self.data_limit)
