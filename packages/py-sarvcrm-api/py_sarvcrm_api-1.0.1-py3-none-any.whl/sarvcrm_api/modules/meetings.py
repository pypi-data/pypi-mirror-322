from ._base import SarvModule
from ._mixins import UrlMixins

class Meetings(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Meetings'
    _label_en = 'Meetings'
    _label_pr = 'جلسات'