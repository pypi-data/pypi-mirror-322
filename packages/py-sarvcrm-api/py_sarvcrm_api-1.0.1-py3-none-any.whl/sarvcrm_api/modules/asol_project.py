from ._base import SarvModule
from ._mixins import UrlMixins

class AsolProject(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'asol_Project'
    _label_en = 'Project'
    _label_pr = 'پروژه'