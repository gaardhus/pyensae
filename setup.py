# -*- coding: utf-8 -*-
import sys
import os
from distutils.core import setup
from setuptools import find_packages

#########
# settings
#########

project_var_name = "pyensae"
sversion = "1.2"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = "HISTORY.rst"
requirements = None

KEYWORDS = project_var_name + ', ENSAE, sqllite, database, teachings'
DESCRIPTION = """Helpers for teaching purposes (includes sqllite helpers)"""
CLASSIFIERS = [
    'Programming Language :: Python :: %d' % sys.version_info[0],
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]

#######
# data
#######

packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {project_var_name + ".subproject": ["*.tohelp"],
                project_var_name + ".languages": ["*.g4", "*.tokens"], }

############
# functions
############


def is_local():
    file = os.path.abspath(__file__).replace("\\", "/").lower()
    if "/temp/" in file and "pip-" in file:
        return False
    for cname in {"bdist_msi", "build27", "build_script", "build_sphinx", "build_ext",
                  "bdist_wheel", "bdist_egg", "bdist_wininst", "clean_pyd", "clean_space",
                  "copy27", "copy_dist", "local_pypi", "notebook", "publish", "publish_doc",
                  "register", "unittests", "unittests_LONG", "unittests_SKIP", "unittests_GUI",
                  "run27", "sdist", "setupdep", "test_local_pypi", "upload_docs", "setup_hook",
                  "copy_sphinx", "write_version", "lab"}:
        if cname in sys.argv:
            try:
                import_pyquickhelper()
            except ImportError:
                return False
            return True
    else:
        return False

    return False


def ask_help():
    return "--help" in sys.argv or "--help-commands" in sys.argv


def import_pyquickhelper():
    try:
        import pyquickhelper
    except ImportError:
        sys.path.append(
            os.path.normpath(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "pyquickhelper",
                        "src"))))
        try:
            import pyquickhelper
        except ImportError as e:
            message = "Module pyquickhelper is needed to build the documentation ({0}), not found in path {1} - current {2}".format(
                sys.executable,
                sys.path[-1],
                os.getcwd())
            raise ImportError(message) from e
    return pyquickhelper


def verbose():
    print("---------------------------------")
    print("package_dir =", package_dir)
    print("packages    =", packages)
    print("package_data=", package_data)
    print("current     =", os.path.abspath(os.getcwd()))
    print("---------------------------------")

##########
# version
##########


if is_local() and not ask_help():
    def write_version():
        pyquickhelper = import_pyquickhelper()
        from pyquickhelper.pycode import write_version_for_setup
        return write_version_for_setup(__file__)

    if sys.version_info[0] != 2:
        write_version()

    versiontxt = os.path.join(os.path.dirname(__file__), "version.txt")
    if os.path.exists(versiontxt):
        with open(versiontxt, "r") as f:
            lines = f.readlines()
        subversion = "." + lines[0].strip("\r\n ")
        if subversion == ".0":
            raise Exception("Subversion is wrong: '{0}'.".format(subversion))
    else:
        raise FileNotFoundError(versiontxt)
else:
    # when the module is installed, no commit number is displayed
    subversion = ""

if "upload" in sys.argv and not subversion and not ask_help():
    # avoid uploading with a wrong subversion number
    try:
        import pyquickhelper
        pyq = True
    except ImportError:
        pyq = False
    raise Exception(
        "subversion is empty, cannot upload, is_local()={0}, pyquickhelper={1}".format(is_local(), pyq))

##############
# common part
##############

if os.path.exists(readme):
    if sys.version_info[0] == 2:
        from codecs import open
    with open(readme, "r", encoding='utf-8-sig') as f:
        long_description = f.read()
else:
    long_description = ""
if os.path.exists(history):
    if sys.version_info[0] == 2:
        from codecs import open
    with open(history, "r", encoding='utf-8-sig') as f:
        long_description += f.read()

if "--verbose" in sys.argv:
    verbose()

if is_local():
    pyquickhelper = import_pyquickhelper()
    logging_function = pyquickhelper.get_fLOG()
    logging_function(OutputPrint=True)
    from pyquickhelper.pycode import process_standard_options_for_setup
    r = process_standard_options_for_setup(
        sys.argv, __file__, project_var_name,
        layout=["html"],
        unittest_modules=["pyquickhelper", "jyquickhelper", "pymyinstall"],
        requirements=["pyquickhelper", "jyquickhelper", "pymyinstall"],
        additional_notebook_path=["pyquickhelper", "jyquickhelper"],
        coverage_options=dict(
            omit=["*Parser.py", "*Listener.py", "*Lexer.py"]),
        fLOG=logging_function, covtoken=("f929c9b3-bf00-4928-906a-b1dc54d5a5d9", "'_UT_36_std' in outfile"))
    if not r and "update_grammars" in sys.argv:
        # expecting python setup.py update_grammars file
        ind = sys.argv.index("update_grammars")
        if len(sys.argv) <= ind:
            raise Exception(
                "expecting a grammar file: python setup.py update_grammars R.g4")
        grammar = sys.argv[ind + 1]
        if not os.path.exists(grammar):
            cdir = os.path.abspath(os.path.dirname(__file__))
            g2 = os.path.join(cdir, "src", "pyensae", "languages", grammar)
            if not os.path.exists(g2):
                raise FileNotFoundError("{0}\n{1}".format(grammar, g2))
            grammar = g2
        try:
            from pyensae.languages import build_grammar
        except ImportError:
            from src.pyensae.languages import build_grammar
        build_grammar(grammar, fLOG=logging_function)
        r = True
    if not r and not ({"bdist_msi", "sdist",
                       "bdist_wheel", "publish", "publish_doc", "register",
                       "upload_docs", "bdist_wininst", "build_ext"} & set(sys.argv)):
        raise Exception("unable to interpret command line: " + str(sys.argv))
else:
    r = False

if ask_help():
    pyquickhelper = import_pyquickhelper()
    from pyquickhelper.pycode import process_standard_options_for_setup_help
    process_standard_options_for_setup_help(sys.argv)

if not r:
    if len(sys.argv) in (1, 2) and sys.argv[-1] in ("--help-commands",):
        pyquickhelper = import_pyquickhelper()
        from pyquickhelper.pycode import process_standard_options_for_setup_help
        process_standard_options_for_setup_help(sys.argv)
    else:
        pyquickhelper = import_pyquickhelper()
    from pyquickhelper.pycode import clean_readme
    long_description = clean_readme(long_description)

    setup(
        name=project_var_name,
        version='%s%s' % (sversion, subversion),
        author='Xavier Dupré',
        author_email='xavier.dupre@gmail.com',
        license="MIT",
        url="http://www.xavierdupre.fr/app/pyensae/helpsphinx/index.html",
        download_url="https://github.com/sdpython/pyensae/",
        description=DESCRIPTION,
        long_description=long_description,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=packages,
        package_dir=package_dir,
        package_data=package_data,
        install_requires=["pyquickhelper>=1.5.2259"],
        extras_require={
            'graph_helper': ['matplotlib', 'blockdiag'],
            'datasource.convert': ['dbread'],
            'datasource.data_velib': ['moviepy'],
            'datasource.linkedin_access': ['python3-linkedin'],
            'finance': ['pandas-datareader'],
            'languages': ['antlr4-python3-runtime'],
            'notebook_helper.folium_helper': ['folium'],
            'notebook_helper.magic_notebook': ['qgrid'],
        },
        entry_points={
            'console_scripts': [
                'file_head = pyensae.cli.head_cli:file_head_cli',
                'file_tail = pyensae.cli.tail_cli:file_tail_cli',
            ]}
    )
