from ._base import SarvModule
from ._mixins import UrlMixins

class Appointments(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Appointments'
    _label_en = 'Appointments'
    _label_pr = 'بازدیدها'