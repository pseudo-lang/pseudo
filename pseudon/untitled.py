# int Int
# float Float
# boolean Boolean
# str String
# [2] List<Int>
# {2: 2.0} Dict<Int, Float>
# [] List
# {} Dict

V = '_' # we don't really typecheck or care for a lot of the arg types, so just use this
_ = ()

# for template types as list, dict @t is the type of list arg and @k, @v of dict args
TYPED_API = {
	# methods
	'len': 	[(V), 'Int'],
	'str':  [(V), 'String'],
	'int':  [(V), 'Int'],
	'repr': [(V), 'String'],

	'Int#+': [_, 'Int'],
	'Int#-': [_, 'Int'],
	'Int#/': [_, 'Int'],
	'Int#**': [_, 'Int'],
	'Int#*': [_, 'Int'],
	'Int#%': [_, 'Int'],

	'Float#+': [_, 'Float'],
	'Float#-': [_, 'Float'],
	'Float#/': [_, 'Float'],
	'Float#**': [_, 'Float'],
	'Float#*': [_, 'Float'],

	'Boolean#and': [_, 'Boolean'],
	'Boolean#or': [_, 'Boolean'],

	'Null#and': [_, 'Boolean'],
	'Null#or': [_, 'Boolean'],

	'List#push':       [_, 'Null'],
	'List#pop':        [_, '@t'],
	'List#insert':     [_, 'Null'],
	'List#remove': 	   [_, 'Null'],
	'List#remove_at':  [_, 'Null'],
	'List#length':     [_, 'Int'],
	'List#concat_one': [_, 'List<@t>'],
	'List#concat':     [_, 'List<@t>'],

	'List#map':		   [('Function<@t,@a>'), 'List<@a>'],
	'List#filter': 	   [('Function<@t,Boolean>'), 'List<@t>'],
	'List#reduce':     [('Function<@u, @t, @u>', '@u'), '@u'],

	'Dict#keys': 	   [_, 'List<@k>'],
	'Dict#values':     [_, 'List<@v>']
}
