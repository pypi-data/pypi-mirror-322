from ._base import SarvModule
from ._mixins import UrlMixins

class Calls(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Calls'
    _label_en = 'Calls'
    _label_pr = 'تماس ها'