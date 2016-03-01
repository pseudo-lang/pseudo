# base generator with common functionality
import re
from pseudon.pseudon_tree import Node
from pseudon.code_generator_dsl import Placeholder, Newline, Action, Function, SubTemplate, Offset, INTERNAL_WHITESPACE

class CodeGenerator:
    '''
    options:
      indent: the size of indent, example: python - 4, ruby - 2
      spaces: use spaces if true, tabs if false
    '''

    def __init__(self, indent=None, use_spaces=None):
        if indent: self.indent = indent 
        if use_spaces: self.use_spaces = use_spaces
        # always init them in classes
        symbol = ' ' if use_spaces else '\t'
        self._single_indent = symbol * (self.indent)
        self._parsed_templates = {k: self._parse_template(v, k) for k, v in self.templates.items()}

    def safe_single(self, node, indent):
        if "'" in node.value:
            if '"' in node.value:
                s = "'%s'" % node.value.replace("'", "\\'")
            else:
                s = '"%s"' % node.value
        else:
            s = "'%s'" % node.value
        return '%s%s' % (self.offset(indent), s)

    def safe_double(self, node, indent):
        if '"' in node.value:
            if "'" in node.value:
                s = '"%s"' % node.value.replace('"', '\\"')
            else:
                s = "'%s'" % node.value
        else:
            s = '"%s"' % node.value
        return '%s%s' % (self.offset(indent), s)


    def generate(self, tree):
        '''
        generates code based on templates and gen functions
        defined in the <x> lang generator
        '''
        return self._generate_node(tree, 0)

    def action_join(self, expanded, separator, depth):
        return separator.join(expanded)

    def _generate_node(self, node, depth=0):
        if not isinstance(node, Node):
            return node
        elif node.type in self._parsed_templates:
            return self._generate_from_template(self._parsed_templates[node.type], node, depth)
        elif hasattr(self, 'generate_%s' % node.type):
            return getattr(self, 'generate_%s' % node.type)(node, depth)
        else:
            raise NotImplementedError("no action for %s" % node.type)

    def _generate_from_template(self, template, node, depth):
        expanded = []
        for i, element in enumerate(template):
            if isinstance(element, str):
                expanded.append(element)
            elif isinstance(element, Whitespace):
                if expanded.is_offset:
                    expanded.append(self._single_indent * depth)
                else:
                    expanded.append(' ')
            elif isinstance(element, Newline):
                expanded.append('\n')
            elif hasattr(element, 'expand'):
                expanded.append(element.expand(self, node, depth))
            elif callable(element):
                expanded.append(element(self, node, depth))

        return ''.join(expanded)

    def _parse_template(self, code, label):
        '''
        Pare smart indented templates

        Takes a template a returns a list of sub-templates, taking in account
        the indentation of the original code based on the first line indentation(0)
        Special treatment of whitespace: returns special Offset and INTERNAL_WHITESPACE, so the generation can be configurable
        It auto detects the indentation width used, as the indent of the first indented line 
        >>> indented("""
          def %<code>
            e = 
            %<code2>
          """) 
        ['def', INTERNAL_WHITESPACE, Placeholder('code', 0), NEWLINE,
          Offset(1),'e', INTERNAL_WHITESPACE, '=', NEWLINE,
          Placeholder('code2', 1), NEWLINE]
        '''

        if not isinstance(code, str):
            return []
        lines = code.split('\n')
        parsed = []
        if len(lines) == 1:
            i = re.match(r'^( +)', lines[0])
            indent_size = len(i.group()) if i else 0
            indent = 1 if i else 0
            actual = lines
        else:
            base = len(re.match(r'^( *)', lines[1]).group())
            rebased = [line[base:] for line in lines]
            for line in rebased:
                i = re.match(r'^( +)', line)
                if i:
                    indent_size = len(i.group())
                    break
            else:
                indent_size = 0
            actual = rebased[1:]

        for line in actual:
            j = re.match(r'^( +)', line)
            indent = len(j.group()) // indent_size if j else 0
            if indent:
                parsed.append(Offset(indent))
            in_placeholder = False
            in_action = False
            in_args = False
            in_string_arg = False
            in_double_arg = False
            c = int(indent * indent_size)
            m = c
            placeholder = ''
            while m < len(line):
                # print(m, line[m], 'place:', in_placeholder, 'act:', in_action, 'a:', in_args, 's:', in_string_arg, yaml.dump(parsed))
                f = line[m]
                next_f = line[m + 1] if m < len(line) - 1 else None
                if f == '%' and not in_placeholder and next_f == '<':
                    m += 2
                    in_placeholder = True
                    placeholder = ''
                    continue
                elif f == ':' and in_placeholder:
                    m += 1
                    in_placeholder = False
                    in_action = True
                    action = ''
                    continue
                elif f == ' ' and in_placeholder:
                    m += 1
                    continue
                elif f == ' ' and in_action:
                    m += 1
                    in_action = False
                    in_args = True
                    args = ['']
                    continue
                elif f == ' ' and (in_string_arg or in_double_arg):
                    args[-1] += f
                    m += 1
                    continue
                elif f == ' ' and in_args:
                    m += 1
                    args.append('')
                    continue
                elif f == '\'' and in_args:
                    m += 1
                    if in_string_arg:
                        in_string_arg = False
                        args[-1] += f
                    elif in_double_arg:
                        args[-1] += f
                    else:
                        in_string_arg = True
                    
                    continue
                elif f == '"' and in_args:
                    m += 1
                    if in_double_arg:
                        in_double_arg = False
                        args[-1] += f
                    elif in_string_arg:
                        args[-1] += f
                    else:
                        in_string_arg = True

                    continue
                elif f == '>' and in_args and not in_string_arg and not in_double_arg:
                    m += 1
                    if args[-1] == '':
                        args = args[:-1]
                    args = [arg[:-1] if arg[-1] == '\'' else int(arg) for arg in args]
                    in_args = False
                    parsed.append(Action(placeholder, action, args))
                    continue
                elif f == '>' and in_action:
                    m += 1
                    in_action = False
                    parsed.append(Action(placeholder, action, []))
                elif f == '>' and in_placeholder:
                    m += 1
                    q = None
                    if placeholder[0] == '#':
                        q = Function(placeholder[1:])
                    elif placeholder[0] == '.':
                        q = SubTemplate(label, placeholder[1:])
                    else:
                        q = Placeholder(placeholder)
                    in_placeholder = False
                    parsed.append(q)
                elif f == ' ':
                    m += 1
                    parsed.append(INTERNAL_WHITESPACE)
                elif in_placeholder:
                    m += 1
                    placeholder += f
                elif in_action:
                    m += 1
                    action += f
                elif in_args:
                    m += 1
                    args[-1] += f
                else:
                    m += 1
                    if parsed and isinstance(parsed[-1], str):
                        parsed[-1] += f
                    else: 
                        parsed.append(f)
        return parsed

    def _offset(self, depth):
        return self._single_indent * (self.indent * depth)
