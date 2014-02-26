#!/usr/bin/env python

import inspect
import os
import pkgutil
import sys


def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    return [func.__name__ for func in mod.__dict__.itervalues()
            if is_mod_function(mod, func)]


def is_mod_class(mod, klass):
    return inspect.isclass(klass) and inspect.getmodule(klass) == mod


def list_classes(mod):
    return [klass.__name__ for klass in mod.__dict__.itervalues()
            if is_mod_class(mod, klass)]


class DjangoImportSeeker(object):

    def __init__(self, string_to_find=None, package=None):

        self.string_to_find = string_to_find
        self.package = package

    def process_seek(self):

        self.results = []
        self.get_submodules_of_module(self.package)
        return self.results

    def try_to_find(self, module):

        prefix = module.__name__ + "."
        try:
            class_names = list_classes(sys.modules[module.__name__])

            if self.string_to_find in class_names:
                return prefix + self.string_to_find

            function_names = list_functions(sys.modules[module.__name__])

            if self.string_to_find in function_names:
                return prefix + self.string_to_find

        except ImportError:
            pass

    # this is the package we are inspecting -- for example 'django' from stdlib
    def get_submodules_of_module(self, module_name):

        module = __import__(module_name, fromlist="dummy")
        prefix = module.__name__ + "."

        result = self.try_to_find(module)

        if result:
            self.results.append(result)

        try:
            submodules = [modname for importer, modname, ispkg in
                          pkgutil.iter_modules(module.__path__, prefix)]

            for submodule in submodules:
                self.get_submodules_of_module(submodule)

        except AttributeError:
            pass
        except Exception, e:
            pass


if __name__ == '__main__':

    module_name = 'django'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dummy_settings'

    dis = DjangoImportSeeker(sys.argv[1], module_name)
    results_found = dis.process_seek()

    if results_found:
        print('>>> ' + " ".join(results_found))
    else:
        print('No result found')
