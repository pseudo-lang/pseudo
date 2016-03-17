#!/usr/bin/env python3

import sys
import os
import types
import pseudo
import pseudo.loader
import yaml

USAGE = '''
pseudo <input-filename> <language>

where <language> can be:
  py / python 
  rb / ruby
  js / javascript
  cs / csharp
  go

<input-filename> should be a .pseudo.yaml pseudo ast file
'''


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        exit()

    input_filename = sys.argv[1]
    output_formats = sys.argv[2:]

    intermediate_code = pseudo.loader.load_input(input_filename)
    base, _, ext = input_filename.rpartition('.')
    if ext == 'yaml':
      base = base.partition('.')[0]
    if output_formats[0] == 'intermediate' or output_formats[0] == 'in':
        with open('%s.pseudo.yaml' % base, 'f') as f:
            f.write(intermediate_code)
        exit()

    for format in output_formats:
      if format in pseudo.SUPPORTED_FORMATS:
        output_source = pseudo.generate_from_yaml(intermediate_code, format)
        with open('%s.%s' % (base, pseudo.FILE_EXTENSIONS[format]), 'w') as f:
            f.write(output_source)
      else:
        print('%s is not supported' % format)

if __name__ == '__main__':
    main()
