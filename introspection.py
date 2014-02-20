#!/usr/bin/env python

import inspect
import os
import sys

import django

import pkgutil

RESULTS = []


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

def try_to_find(module, string_to_find):

    prefix = module.__name__ + "."
    try:
        class_names = list_classes(sys.modules[module.__name__])
        
        if string_to_find in class_names:
            return prefix + string_to_find

        function_names = list_functions(sys.modules[module.__name__])

        if string_to_find in function_names:
            return prefix + string_to_find

    except ImportError:
        pass

# this is the package we are inspecting -- for example 'django' from stdlib
def get_submodules_of_module(module_name, class_to_find):

    module = __import__(module_name, fromlist="dummy")
    prefix = module.__name__ + "."

    print('Processing module ' + module.__name__)
    
    result = try_to_find(module, class_to_find)
    
    if result:
        return result

    try:
        submodules = [modname for importer, modname, ispkg in pkgutil.iter_modules(module.__path__, prefix)]

        print('Submodules of ' + module_name + ' are : ' + ' '.join(submodules))

        for submodule in submodules:
            result = get_submodules_of_module(submodule, class_to_find)

            if result:
                RESULTS.append(result)

    except AttributeError:
        print('End path for ' + module.__name__)
    except Exception, e:
        print('We have to manage this exception')
        print(str(e))

    return result

if __name__ == '__main__':

    module_name = 'django'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dummy_settings'

    cont = True

    result = get_submodules_of_module(module_name, sys.argv[1])

    if RESULTS:
        print('Result found : ' + " ".join(RESULTS))
    else:
        print('No result found')

