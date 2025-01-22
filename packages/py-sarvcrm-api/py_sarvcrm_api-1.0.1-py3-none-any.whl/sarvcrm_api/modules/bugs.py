from ._base import SarvModule
from ._mixins import UrlMixins

class Bugs(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Bugs'
    _label_en = 'Bug Tracker'
    _label_pr = 'پیگیری ایرادهای محصول'