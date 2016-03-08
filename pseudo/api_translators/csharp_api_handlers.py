from pseudo.pseudo_tree import Node, call, method_call, local, typename, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

def expand_slice(receiver, from_, to, pseudo_type=None):
    return method_call(method_call(receiver, 'Take', [to], pseudo_type), 'Drop', [from_], pseudo_type)

class Display(NormalLeakingNode):
	def as_expression(self):
		return [Node('static_call',
					receiver=typename('Console', 'Library'),
					message='WriteLine',
					args=[arg],
					pseudo_type='Void')
				for arg
				in self.args], None
