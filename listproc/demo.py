#!/usr/bin/env python

import tyrell.spec as S
from tyrell.enumerator import SmtEnumerator, ExhaustiveEnumerator, RandomEnumerator
from tyrell.decider import Example, ExampleConstraintDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

from listproc_util import *
from interpreter import ToyInterpreter
import dataset

logger = get_logger('tyrell')
logger.setLevel('DEBUG')

def get_samples_of_type(sample_type):
    if sample_type == ("Int",):
        return (0, 1, 2, 4, 9)
    if sample_type == ("Int", "Int"):
        return ((0, 0), (1, 4), (3, 2), (4, 12), (9, 2))
    if sample_type == ("List",)):
        return ([0, 1, 8, 3], [1], [12, 3, 8, 1], [9, 8, 7, 2])

    assert False

def do_make_ioset(sample_type, prog):
    ret = []

    for s in get_samples_of_type(sample_type):
        interpreter = ToyInterpreter()
        ret.append(
            Example(input=s, output=interpreter.eval(prog, s)),
        )
    
    return tuple(ret)

def do_make_progs(progtype, n, depth_bound):
    spec = parse_spec_with_progspec('grammar.tyrell', *progtype)

    ret = []

    #enumer = ExhaustiveEnumerator(spec, max_depth=depth_bound)
    enumer = RandomEnumerator(spec, max_depth=depth_bound)
    #enumer = SmtEnumerator(spec, depth=depth_bound, loc=loc)

    prog = enumer.next()
    while prog is not None and len(ret) < n:
        ret.append(prog)
        prog = enumer.next()
        
    return ret

def do_synthesize(progtype, examples):
    logger.info('Parsing Spec...')
    spec = parse_spec_with_progspec('grammar.tyrell', *progtype)
    logger.info('Parsing succeeded')

    logger.info('Building synthesizer...')
    
    depth_bound = 4
    loc_max = 10

    #input0 = [[1,2], [3,4]]
#
    #interpreter = ToyInterpreter()
    #logger.info('Executing program on inputs {}...'.format(input0))
    #out_value = interpreter.eval(prog, input0)
    #print(out_value)
#
    #return None
    for loc in range(1, loc_max):
        synthesizer = Synthesizer(
            # enumerator=SmtEnumerator(spec, depth=3, loc=1), # plus(@param1, @param0) / plus(@param0, @param1)
            # enumerator=SmtEnumerator(spec, depth=4, loc=3), # plus(plus(@param0, const(_apple_)), @param1)
            enumerator=SmtEnumerator(spec, depth=depth_bound, loc=loc), # plus(plus(@param0, const(_apple_)), @param1)
            decider=ExampleConstraintDecider(
                spec=spec,
                interpreter=ToyInterpreter(),
                examples=examples,
            )
        )
        logger.info('Synthesizing programs...')

        prog = synthesizer.synthesize()
        if prog is not None:
            logger.info('Solution found: {}'.format(prog))
            return prog
        else:
            logger.info(f'Solution not found at LOC {loc}!')

def dataset_synthesize(subdomain, problem):
    typespec, progs = dataset.subdomains[subdomain]
    return do_synthesize(typespec, progs[problem])

def there_and_back_again(progtype, prog):
    there = do_make_ioset(progtype[0], prog)
    back_again = do_synthesize(progtype, there)

    print(prog)
    print(back_again)
    print(there)

list2_int_progs = do_make_progs((("Int", "Int"), "Int"), 20, 4)

for p in list2_int_progs:
    print(p)

there_and_back_again((("Int", "Int"), "Int"), list2_int_progs[0])

#dataset_synthesize("bool_bool", "const_false")
#dataset_synthesize("int2_int", "plus")
#dataset_synthesize("list2_int", "deepcoder_demo")
#dataset_synthesize("str2_str", "demo_string_enumerator")
#dataset_synthesize("str_str", "prepend_apple")
#dataset_synthesize("bool2_bool", "and")