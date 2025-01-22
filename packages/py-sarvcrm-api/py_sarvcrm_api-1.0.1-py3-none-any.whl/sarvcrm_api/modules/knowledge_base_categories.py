from ._base import SarvModule
from ._mixins import UrlMixins

class KnowledgeBaseCategories(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Knowledge_Base_Categories'
    _label_en = 'Knowledge Base Categories'
    _label_pr = 'دسته پایگاه دانش'