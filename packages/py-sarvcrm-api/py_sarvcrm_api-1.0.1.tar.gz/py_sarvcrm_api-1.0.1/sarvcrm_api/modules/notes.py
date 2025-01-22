from ._base import SarvModule
from ._mixins import UrlMixins

class Notes(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Notes'
    _label_en = 'Notes'
    _label_pr = 'یادداشت ها'