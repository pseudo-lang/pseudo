import types
import yaml
from pseudo.pseudo_tree import Node

def load_input(filename):
    try:
        with open(filename) as f:
            intermediate_code = f.read()
    except (OSError, IOError) as e:
        print("something's wrong with %s" % filename)
        exit(1)
    return intermediate_code

def as_tree(intermediate_code):
    intermediate_code = yaml.load(intermediate_code)
    return convert_to_syntax_tree(intermediate_code)

def convert_to_syntax_tree(tree):
    if isinstance(tree, dict) and 'type' in tree:
        return Node(tree['type'], **{k: convert_to_syntax_tree(v) for k, v in tree.items() if k != 'type'})
    elif isinstance(tree, dict):
        return {k: convert_to_syntax_tree(v) for k, v in tree.items()}
    elif isinstance(tree, list):
        return [convert_to_syntax_tree(v) for v in tree]
    else:
        return tree
