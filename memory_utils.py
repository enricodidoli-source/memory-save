import os
import pickle
import gc
import sys
import ctypes
import matplotlib.pyplot as plt
from IPython import get_ipython
import shutil

def clear_RAM(variables_names=None, clear_all=False)
    plt.close('all')
    ipython = get_ipython()

    if variables_names
        for var_name in variables_names
            if var_name is not None and ipython is not None
                if var_name in ipython.user_ns
                    ipython.user_ns.pop(var_name, None)

    if clear_all
        try
            ctypes.CDLL('libc.so.6').malloc_trim(0)
        except Exception
            pass

        try
            import tensorflow as tf
            tf.keras.backend.clear_session()
        except ImportError
            pass

        if hasattr(sys, 'last_traceback')
            sys.last_type, sys.last_value, sys.last_traceback = None, None, None

        if ipython is not None
            try
                ipython.user_ns.pop('_', None)
                ipython.user_ns.pop('__', None)
                ipython.user_ns.pop('___', None)
                ipython.user_ns['_ih'].clear()
                ipython.user_ns['_oh'].clear()
            except Exception
                pass

    gc.collect()


class MemorySave()
    def __init__(self, base_dir str)
        self.base_dir = os.path.join(base_dir, 'temp_var')
        self.variable_dict = {}
        os.makedirs(self.base_dir, exist_ok=True)

    def save_and_clear(self,  variables list, variables_names list, custom_dir str = None, clear = True, force = False)
        if custom_dir is not None
            save_dir = os.path.join(custom_dir, 'temp_var')
            os.makedirs(save_dir, exist_ok=True)
        else
            save_dir = self.base_dir

        for var, var_name in zip(variables, variables_names)

            if var_name in self.variable_dict and not force ### force the save
                print(f'Variable {var_name} already saved in memory. (Use force = True to overwrite)')
            else
                file_path = os.path.join(save_dir, f{var_name}.pkl)

                with open(file_path, 'wb') as f
                    pickle.dump(var, f)

                self.variable_dict[var_name] = save_dir

        if clear
            clear_RAM(variables_names=variables_names)


    def load_variables(self, variables_names list)
        variables = []
        for var_name in variables_names
            if var_name not in self.variable_dict
                raise ValueError(f'Variable {var_name} not found in memory')


            file_path = os.path.join(self.variable_dict[var_name], f{var_name}.pkl)

            with open(file_path, 'rb') as f
                var = pickle.load(f)
            variables.append(var)
        return tuple(variables)


    def show_vars(self)
        if not self.variable_dict
            print(No variables saved.)
            return
        for name, path in self.variable_dict.items()
            print(f - {name} {path})

    def is_var(self, variables_names list)
        results = {}
        for var_name in variables_names
            results[var_name] = self.variable_dict.get(var_name, False)
        return results

    def remove_var(self, variables_names list)
        for var_name in variables_names
            if var_name in self.variable_dict

                save_dir = self.variable_dict[var_name]
                file_path = os.path.join(save_dir, f{var_name}.pkl)
                
                if os.path.exists(file_path)
                    os.remove(file_path)
                
                self.variable_dict.pop(var_name)
    
    def close(self)
        if os.path.exists(self.base_dir)
            shutil.rmtree(self.base_dir)
        
        self.variable_dict.clear()
        print(fFolder {self.base_dir} deleted.)
