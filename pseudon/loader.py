import types
import yaml
from pseudon_tree import Node

COMMANDS = {
    'py': lambda filename: ['pseudon-python', filename],
    'rb': lambda filename: ['pseudon-ruby', filename],
    'php': lambda filename: ['pseudon-php', filename],
    'js': lambda filename: ['pseudon-javascript', filename]
}


def load_input(filename, call_command):
    extension, _, base = filename.rpartition('.')
    with open(filename) as f:
        source = f.read()
    if extension == 'yaml':
        intermediate_code = source
    else:
        call_command(COMMANDS[extension](filename))
        with open('%s.pseudon.yaml' % base, 'r') as f:
            intermediate_code = f.read()
        call_command(['rm', '%s.pseudon.yaml' % base])
    intermediate_code = yaml.load(intermediate_code)
    return convert_to_syntax_tree(intermediate_code)


def convert_to_syntax_tree(tree):
    if isinstance(tree, dict) and 'type' in tree:
        return Node(tree['type'], {k: convert_to_syntax_tree(v) for k, v in tree.items() if k != 'type'})
    elif isinstance(tree, dict):
        return {k: convert_to_syntax_tree(v) for k, v in tree.items()}
    elif isinstance(tree, list):
        return [convert_to_syntax_tree(v) for v in tree]
    else:
        return tree
