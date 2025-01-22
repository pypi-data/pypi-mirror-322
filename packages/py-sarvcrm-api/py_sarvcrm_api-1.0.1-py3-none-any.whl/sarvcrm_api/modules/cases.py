from ._base import SarvModule
from ._mixins import UrlMixins

class Cases(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Cases'
    _label_en = 'Cases'
    _label_pr = 'سرویس ها'