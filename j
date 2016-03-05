main
value
apolonia.txt
None
value
local
value
None
None
name
!Node
block:
- !Node
  local: source
  pseudo_type: Void
  type: local_assignment
  value: !Node
    args: []
    message: read
    pseudo_type: null
    receiver: !Node {name: _f, pseudo_type: null,
      type: local}
    type: method_call
  value_type: String
call: !Node
  args:
  - !Node {name: f, pseudo_type: String, type: local}
  - !Node {name: '''r''', type: typename}
  function: !Node {name: open, type: local}
  pseudo_type: null
  type: call
context: _f
type: _with
local
value
name
