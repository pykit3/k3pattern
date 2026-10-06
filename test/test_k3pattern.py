import os
import random
import unittest

import k3ut

import k3pattern

dd = k3ut.dd

this_base = os.path.dirname(__file__)


def _rand_str(rnd):
    return "".join(rnd.choice("ab") for _ in range(rnd.randint(0, 3)))


def _vary(rnd, base):
    # Cut the tail or change values, but keep the element type at each position.
    rst = []
    for elt in base:
        if rnd.random() < 0.15:
            break
        if rnd.random() < 0.7:
            rst.append(elt)
        elif isinstance(elt, str):
            rst.append(_rand_str(rnd))
        else:
            rst.append(_vary(rnd, elt))
    return tuple(rst)


class TestK3pattern(unittest.TestCase):
    def test_common_prefix_invalid_arg(self):
        cases = (
            (1, []),
            ("a", 1),
            ("a", True),
            ("a", ("a",)),
            (
                (
                    "a",
                    (),
                ),
                (
                    "a",
                    2,
                ),
            ),
        )

        for a, b in cases:
            dd("wrong type: ", repr(a), " ", repr(b))
            self.assertRaises(TypeError, k3pattern.common_prefix, a, b)

    def test_common_prefix(self):
        cases = (
            (
                "abc",
                "abc",
            ),
            (
                "",
                "",
                "",
            ),
            (
                (),
                (),
                (),
                (),
            ),
            (
                "abc",
                "ab",
                "ab",
            ),
            (
                "ab",
                "abd",
                "ab",
            ),
            (
                "abc",
                "abd",
                "ab",
            ),
            (
                "abc",
                "def",
                "",
            ),
            (
                "abc",
                "",
                "",
            ),
            (
                "",
                "def",
                "",
            ),
            (
                "abc",
                "abd",
                "ag",
                "a",
            ),
            (
                "abc",
                "abd",
                "ag",
                "yz",
                "",
            ),
            (
                (
                    1,
                    2,
                ),
                (
                    1,
                    3,
                ),
                (1,),
            ),
            (
                (
                    1,
                    2,
                ),
                (
                    2,
                    3,
                ),
                (),
            ),
            (
                (
                    1,
                    2,
                    "abc",
                ),
                (
                    1,
                    2,
                    "abd",
                ),
                (
                    1,
                    2,
                    "ab",
                ),
            ),
            (
                (
                    1,
                    2,
                    "abc",
                ),
                (
                    1,
                    2,
                    "xyz",
                ),
                (
                    1,
                    2,
                ),
            ),
            (
                (
                    1,
                    2,
                    (5, 6),
                ),
                (
                    1,
                    2,
                    (5, 7),
                ),
                (
                    1,
                    2,
                    (5,),
                ),
            ),
            (
                (
                    "abc",
                    "45",
                ),
                ("abc", "46", "xyz"),
                (
                    "abc",
                    "4",
                ),
            ),
            (
                ("abc", ("45", "xyz"), 3),
                ("abc", ("45", "xz"), 5),
                ("abc", ("45", "x-"), 5),
                (
                    "abc",
                    ("45", "x"),
                ),
            ),
            (
                ("abc", ("45", "xyz"), 3),
                ("abc", ("45", "xz"), 5),
                (
                    "abc",
                    ("x",),
                ),
                ("abc",),
            ),
            (
                [1, 2, 3],
                [1, 2, 4],
                [1, 2],
            ),
        )

        for args in cases:
            expected = args[-1]
            args = args[:-1]

            dd("input: ", args, "expected: ", expected)
            rst = k3pattern.common_prefix(*args)
            dd("rst: ", rst)

            self.assertEqual(expected, rst)

    def test_common_prefix_no_recursive(self):
        cases = (
            (
                ("abc", ("45", "xyz"), 3),
                ("abc", ("45", "xz"), 5),
                ("abc", ("45", "x-"), 5),
                ("abc",),
            ),
            (
                "abc",
                "abd",
                "ag",
                "a",
            ),
            (
                (1, 2, "abc"),
                (1, 2, "abd"),
                (1, 2),
            ),
        )

        for args in cases:
            expected = args[-1]
            args = args[:-1]

            dd("input: ", args, "expected: ", expected)
            rst = k3pattern.common_prefix(*args, recursive=False)
            dd("rst: ", rst)

            self.assertEqual(expected, rst)

    def test_common_prefix_nested_type_mismatch(self):
        cases = (
            (("x", ("a", 1)), ("x", ("a", "b"))),
            ((1, (2, ("a", 3))), (1, (2, ("a", "b")))),
            (("x", ("a", [1])), ("x", ("a", (1,)))),
            ([1, [2, "a"]], [1, [2, 3]]),
        )

        for a, b in cases:
            dd("wrong nested type: ", repr(a), " ", repr(b))
            self.assertRaises(TypeError, k3pattern.common_prefix, a, b)

    def test_common_prefix_random_tuples_of_str(self):
        # Reference model: the common elements, then the common prefix of the
        # first differing str elements if it is not empty.
        rnd = random.Random(0)

        for _ in range(1000):
            base = tuple(_rand_str(rnd) for _ in range(4))
            inputs = [_vary(rnd, base) for _ in range(rnd.randint(1, 4))]

            flat = os.path.commonprefix(inputs)
            k = len(flat)
            expected = flat
            if all(k < len(x) for x in inputs):
                tail = os.path.commonprefix([x[k] for x in inputs])
                if tail:
                    expected = flat + (tail,)

            rst = k3pattern.common_prefix(*inputs)
            self.assertEqual(expected, rst, inputs)

            rst = k3pattern.common_prefix(*inputs, recursive=False)
            self.assertEqual(flat, rst, inputs)

    def test_common_prefix_random_nested(self):
        # The result is a common prefix of every input, whatever the input order.
        rnd = random.Random(0)

        for _ in range(1000):
            base = tuple(_rand_str(rnd) if rnd.random() < 0.5 else (_rand_str(rnd), _rand_str(rnd)) for _ in range(4))
            inputs = [_vary(rnd, base) for _ in range(rnd.randint(1, 4))]
            rst = k3pattern.common_prefix(*inputs)

            rnd.shuffle(inputs)
            shuffled_rst = k3pattern.common_prefix(*inputs)
            self.assertEqual(rst, shuffled_rst, inputs)

            for x in inputs:
                prefix_of_x = k3pattern.common_prefix(rst, x)
                self.assertEqual(rst, prefix_of_x, (rst, x))
