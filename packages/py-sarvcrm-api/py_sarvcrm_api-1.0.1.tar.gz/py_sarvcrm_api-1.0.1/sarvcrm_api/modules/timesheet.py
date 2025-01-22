from ._base import SarvModule
from ._mixins import UrlMixins

class Timesheet(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Timesheet'
    _label_en = 'Timesheet'
    _label_pr = 'تایم شیت'