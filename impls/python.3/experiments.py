from core import str_, pr_str_
from mal_types import make_string

a = make_string(r'" \" \n \\ "')

print(a)

assert str_(a) == " \" \n \\ ", str_(a)
assert pr_str_(a) == "\" \\\" \\n \\\\ \"", pr_str_(a)
