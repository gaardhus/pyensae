"""
@brief      test log(time=2s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""


import sys
import os
import unittest
import warnings
from pyquickhelper.loghelper import fLOG


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.pyensae.languages.antlr_grammar_use import get_parser_lexer, get_tree_string, parse_code
from src.pyensae.languages.antlr_grammar_build import build_grammar
import src.pyensae.languages.antlr_grammar_use as source_parser


class TestParseCode (unittest.TestCase):

    def test_build_parser_extra(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        try:
            clparser, cllexer = get_parser_lexer("language")
            return
        except ImportError:
            pass

        folder = os.path.dirname(source_parser.__file__)

        for lang in ["language"]:
            gr = os.path.join(folder, lang + ".g4")
            if not os.path.exists(gr):
                warnings.warn("'{0}' does not exists.".format(gr))
                continue
            build_grammar(lang, fLOG=fLOG)

    def test_extra(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        code = """
        example of the language
        """
        try:
            from src.pyensae.languages.LanguageLexer import LanguageLexer
            from src.pyensae.languages.LanguageParser import LanguageParser
        except ImportError:
            return

        parser = parse_code(code, LanguageParser, LanguageLexer)
        tree = parser.parse()
        st = get_tree_string(tree, parser)
        fLOG(st.replace("\\n", "\n"))
        assert len(st) > 0


if __name__ == "__main__":
    unittest.main()
