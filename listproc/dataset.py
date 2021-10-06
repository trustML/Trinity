from tyrell.decider import Example

subdomains = {}

subdomains["bool_bool"] = (
    (["Bool"], "Bool"),
    {
        "const_false": [
            Example(input = [True], output = False),
            Example(input = [False], output = False),
        ]
    }
)

subdomains["bool2_bool"] = (
    (["Bool", "Bool"], "Bool"),
    {
        "nand": [
            Example([True, True], False),
            Example([True, False], True),
            Example([False, True], True),
            Example([False, False], True),
        ],
        "and": [
            Example([True, True], True),
            Example([True, False], False),
            Example([False, True], False),
            Example([False, False], False),
        ],
    }
)

subdomains["int2_int"] = (
    (["Int", "Int"], "Int"),
    {
        "plus": [
            Example([0, 0], 0),
            Example([1, 1], 2),
            Example([10, 3], 13),
        ]
    }
)

subdomains["str_str"] = (
    (["Str"], "Str"),
    {
        "identity": [
            Example(input=["a"], output="a"),
        ],
        "prepend_apple": [
            Example(input=["a"], output="_apple_a"),
        ],
    }
)

subdomains["str2_str"] = (
    (["Str", "Str"], "Str"),
    {
        "demo_string_enumerator": [
            Example(input=["a", "b"], output="a_apple_b"),
        ],
    }
)

subdomains["list2_int"] = (
    (["List", "List"], "Int"),
    {
        "deepcoder_demo": [
            Example(input=[ [6,2,4,7,9], [5,3,6,1,0] ], output=27),
        ],
        "head_plus": [
            Example(input=[ [6], [5] ], output=11),
            Example(input=[ [2], [3] ], output=5),
            Example(input=[ [4], [6] ], output=10),
        ],
    }
)