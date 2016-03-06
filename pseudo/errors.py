class PseudoError(Exception):
    pass

class PseudoStandardLibraryError(PseudoError):
    pass

class PseudoDSLError(PseudoError):
    pass

class PseudoTypeError(PseudoError):
	pass