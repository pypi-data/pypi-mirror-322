from ._base import SarvModule
from ._mixins import UrlMixins

class Opportunities(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Opportunities'
    _label_en = 'Opportunities'
    _label_pr = 'فرصت ها'