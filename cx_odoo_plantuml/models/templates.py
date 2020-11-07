# Templates used to build UML structure

MODULE_PREFIX = "!define Root(name,desc) class name as \"desc\" << (R,magenta) >>\n" \
                "!define App(name,desc) class name as \"desc\" << (A,orange) >>\n" \
                "!define Module(name,desc) class name as \"desc\" << (M,grey) >>\n" \
                "!define tech_name(x) <b>x</b>\n" \
                "!define installed(x) <color:green><i>x</i></color>\n" \
                "!define not_installed(x) <color:red><i>x</i></color>\n" \
                "!define free(x) <color:green><i>x</i></color>\n" \
                "!define paid(x) <color:magenta><i>x - paid!</i></color>\n" \
                "!define ee(x) <color:magenta><i>x</i></color>\n" \
                "!define version(x) x\n" \
                "!define author(x) x\n" \
                "hide methods"

MODULE_TEMPLATE = '{}({}, "{}") {{\n' \
                  '    {}\n' \
                  '    {}\n' \
                  '    version({}) {}\n' \
                  '    {}\n' \
                  '}}'

RELATION_TEMPLATE = '{} --> {}'
MAX_NAME_LEN = 20
MAX_NAME_WORDS = 4

MODEL_PREFIX = "!define Model(name,desc) class name as \"desc\" << (M,#FFAAAA) >>\n" \
               "!define TransientModel(name,desc) class name as \"desc\" << (T,magenta) >>\n" \
               "!define AbstractModel(name,desc) class name as \"desc\" << (T,green) >>\n" \
               "hide methods"

MODEL_TEMPLATE = "{}({}, \"{}\") {{\n" \
                 "{} \n" \
                 " }}"

PACKAGE_NEW = 'package "%s" {\n'
PACKAGE_INHERITED = 'package "%s" {\n'




