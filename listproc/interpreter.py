from tyrell.interpreter import PostOrderInterpreter, GeneralError
from listproc_util import *

class ToyInterpreter(PostOrderInterpreter):
    def eval_bool_const(self, node, args):
        if args[0] == "true":
            return True
        elif args[0] == "false":
            return False
        else:
            assert False
    
    def eval_int_const(self, node, args):
        return int(args[0])

    def eval_fn_const(self, node, args):
        # no exception handler
        fn_dict = {
            "pos": self.eval_pos,
            "neg": self.eval_neg,
            "plus": self.eval_plus,
            "minus": self.eval_minus,
            "mul": self.eval_mul,
            "div": self.eval_div,
            "pow": self.eval_pow,
            "gt_zero": self.eval_gt_zero,
            "lt_zero": self.eval_lt_zero,
            "is_even": self.eval_is_even,
            "is_odd": self.eval_is_odd,
        }
        if args[0] in fn_dict:
            return fn_dict[args[0]]
        else:
            raise GeneralError()

    def eval_mfn_const(self, node, args):
        # no exception handler
        fn_dict = {
            "plus": self.meta_plus,
            "minus": self.meta_minus,
            "mul": self.meta_mul,
            "div": self.meta_div,
            "pow": self.meta_pow,
        }
        if args[0] in fn_dict:
            return fn_dict[args[0]](
                self.eval_int_const(None, [args[1]])
            )
        else:
            raise GeneralError()

    def eval_bool_nand(self, node, args):
        return not (args[0] and args[1])

    def eval_str_const(self, node, args):
        return args[0]

    def eval_str_plus(self, node, args):
        return args[0] + args[1]

    # lists

    def eval_head(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            if len(args[0])>0:
                return args[0][0]
            else:
                raise GeneralError()
        else:
            raise GeneralError()

    def eval_last(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            if len(args[0])>0:
                return args[0][-1]
            else:
                raise GeneralError()
        else:
            raise GeneralError()

    def eval_take(self, node, args):
        if type_checker([type(d) for d in args], [int, list]):
            if len(args[1])<=args[0]:
                return args[1]
            else:
                return args[1][:args[0]]
        else:
            raise GeneralError()

    def eval_drop(self, node, args):
        if type_checker([type(d) for d in args], [int, list]):
            if len(args[1])<=args[0]:
                return []
            else:
                return args[1][args[0]:]
        else:
            raise GeneralError()

    def eval_access(self, node, args):
        if type_checker([type(d) for d in args], [int, list]):
            if args[0]<len(args[1]) and args[0]>=0:
                return args[1][args[0]]
            else:
                raise GeneralError()
        else:
            raise GeneralError()

    def eval_minimum(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            if len(args[0])>0:
                return min(args[0])
            else:
                raise GeneralError()
        else:
            raise GeneralError()

    def eval_maximum(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            if len(args[0])>0:
                return max(args[0])
            else:
                raise GeneralError()
        else:
            raise GeneralError()

    def eval_reverse(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            return args[0][::-1]
        else:
            raise GeneralError()

    def eval_sort(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            return sorted(args[0])
        else:
            raise GeneralError()

    def eval_sum(self, node, args):
        if type_checker([type(d) for d in args], [list]):
            return sum(args[0])
        else:
            raise GeneralError()

    def eval_map(self, node, args):
        # call like "fn( [args] )"
        if type_checker([type(d) for d in args], [function_types, list]):
            return [args[0]( node, [d_item] ) for d_item in args[1]]
        else:
            raise GeneralError()

    def eval_filter(self, node, args):
        # call like "fn( [args] )"
        if type_checker([type(d) for d in args], [function_types, list]):
            rel = []
            for d_item in args[1]:
                if args[0]( node, [d_item] ):
                    rel.append(d_item)
            return rel
        else:
            raise GeneralError()

    def eval_count(self, node, args):
        # call like "fn( [args] )"
        if type_checker([type(d) for d in args], [function_types, list]):
            rel = []
            for d_item in args[1]:
                if args[0]( node, [d_item] ):
                    rel.append(d_item)
            return len(rel)
        else:
            raise GeneralError()

    def eval_zipwith(self, node, args):
        # call like "fn( [args] )"
        if type_checker([type(d) for d in args], [function_types, list, list]):
            return [args[0]( node, [x,y] ) for (x,y) in zip(args[1],args[2])]
        else:
            raise GeneralError()

    def eval_scanl1(self, node, args):
        # call like "fn( [args] )"
        if type_checker([type(d) for d in args], [function_types, list]):
            rel = []
            if len(args[1])>0:
                rel.append(args[1][0])
                for i in range(1, len(args[1])):
                    rel.append( args[0]( node, [rel[i-1],args[1][i]] ) )
            return rel
        else:
            raise GeneralError()

    # "metafunction"s


    # ### meta function ### #
    def meta_plus(self, p):
        def fn_plus(node, args):
            if type_checker([type(d) for d in args], [int]):
                return args[0]+p
            else:
                raise GeneralError()
        return fn_plus

    # ### meta function ### #
    def meta_minus(self, p):
        def fn_minus(node, args):
            if type_checker([type(d) for d in args], [int]):
                return args[0]-p
            else:
                raise GeneralError()
        return fn_minus

    # ### meta function ### #
    def meta_mul(self, p):
        def fn_mul(node, args):
            if type_checker([type(d) for d in args], [int]):
                return args[0]*p
            else:
                raise GeneralError()
        return fn_mul

    # ### meta function ### #
    def meta_div(self, p):
        def fn_div(node, args):
            if type_checker([type(d) for d in args], [int]):
                if p==0:
                    raise GeneralError()
                return args[0]//p # truncated version to keep the results in int range
            else:
                raise GeneralError()
        return fn_div

    # ### meta function ### #
    def meta_pow(self, p):
        def fn_pow(node, args):
            if type_checker([type(d) for d in args], [int]):
                if p<0: # do not deal with power<0
                    raise GeneralError()
                if args[0]<=0: # do not deal with base<=0
                    raise GeneralError()
                return args[0]**p
            else:
                raise GeneralError()
        return fn_pow


    # arithmetic

    def eval_pos(self, node, args):
        if type_checker([type(d) for d in args], [int]):
            return args[0]
        else:
            raise GeneralError()

    def eval_neg(self, node, args):
        if type_checker([type(d) for d in args], [int]):
            return -args[0]
        else:
            raise GeneralError()

    def eval_plus(self, node, args):
        if type_checker([type(d) for d in args], [int, int]):
            return args[0]+args[1]
        else:
            raise GeneralError()

    def eval_minus(self, node, args):
        if type_checker([type(d) for d in args], [int, int]):
            return args[0]-args[1]
        else:
            raise GeneralError()

    def eval_mul(self, node, args):
        if type_checker([type(d) for d in args], [int, int]):
            return args[0]*args[1]
        else:
            raise GeneralError()

    def eval_div(self, node, args):
        if type_checker([type(d) for d in args], [int, int]):
            if args[1]==0:
                raise GeneralError()
            return args[0]//args[1] # truncated version to keep the results in int range
        else:
            raise GeneralError()

    def eval_pow(self, node, args):
        if type_checker([type(d) for d in args], [int, int]):
            if args[1]<0: # do not deal with power<0
                raise GeneralError()
            if args[0]<=0: # do not deal with base<=0
                raise GeneralError() 
            return args[0]**args[1]
        else:
            raise GeneralError()

    def eval_gt_zero(self, node, args):
        if type_checker([type(d) for d in args], [int]):
            return args[0]>0
        else:
            raise GeneralError()

    def eval_lt_zero(self, node, args):
        if type_checker([type(d) for d in args], [int]):
            return args[0]<0
        else:
            raise GeneralError()

    def eval_is_even(self, node, args):
        if type_checker([type(d) for d in args], [int]):
            return args[0]%2==0
        else:
            raise GeneralError()

    def eval_is_odd(self, node, args):
        if type_checker([type(d) for d in args], [int]):
            return args[0]%2!=0
        else:
            raise GeneralError()
