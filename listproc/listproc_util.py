
import tyrell.spec.do_parse as do_parse
import string
import random
import types

def parse_spec_with_progspec(file_path, arg_types, ret_type):
    '''
    Parse Tyrell spec from an input file path.
    May raise either ``ParseError`` or ``ParseTreeProcessingError``.
    '''
    with open(file_path, 'r') as f:
        spec_str = f.read()
    
    progname = "progname"    
    progstr = "program " + progname + "(" + (", ".join(arg_types)) + ") -> " + ret_type + ";"
    print(progstr)

    spec_str2 = spec_str.replace("[[PROGSPEC]]", progstr)

    return do_parse.parse(spec_str2)

# common utils
function_types = set([
	types.BuiltinFunctionType,
	types.BuiltinMethodType,
	types.FunctionType,
	types.LambdaType,
	types.MethodType,
])

def type_checker(actual, expect):
	na = len(actual)
	ne = len(expect)
	if na!=ne:
		return False
	for i in range(na):
		if type(expect[i])==set:
			# need to match anyone
			# so in this DSL, the "set" type is not avaiable
			# since it's used here as special type
			if not actual[i] in expect[i]:
				return False
		elif actual[i]!=expect[i]:
			# need to match exactly
			return False
	return True
