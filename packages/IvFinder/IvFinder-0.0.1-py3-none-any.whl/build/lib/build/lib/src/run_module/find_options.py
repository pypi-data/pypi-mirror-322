import os

def find_advanced_options(command, args):

    advanced_options = args.advanced_options
    if command in advanced_options:
        return advanced_options[command]
    else:
        return None