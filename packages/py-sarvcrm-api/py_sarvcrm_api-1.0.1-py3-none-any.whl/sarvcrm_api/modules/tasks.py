from ._base import SarvModule
from ._mixins import UrlMixins

class Tasks(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Tasks'
    _label_en = 'Tasks'
    _label_pr = 'وظایف'