from ._base import SarvModule
from ._mixins import UrlMixins

class Campaigns(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Campaigns'
    _label_en = 'Campaigns'
    _label_pr = 'کمپین ها'