from os.path import abspath, isfile

template_paths = dict()

def register_template(name: str, path: str) -> bool:
    template_abs_path = abspath(path)
    if isfile(template_abs_path):
        template_paths[name] = template_abs_path
    else:
        print(f"ERROR: Template at path '{template_abs_path}' not found.")

def get_template_path(name: str):
    return template_paths[name]

