# coding: UTF-8
import sys
bstack11ll11l_opy_ = sys.version_info [0] == 2
bstack1ll1l11_opy_ = 2048
bstack11llll_opy_ = 7
def bstack1l1ll1l_opy_ (bstack11ll1l_opy_):
    global bstack1ll1ll1_opy_
    bstack1111111_opy_ = ord (bstack11ll1l_opy_ [-1])
    bstack1lll111_opy_ = bstack11ll1l_opy_ [:-1]
    bstack1l111l_opy_ = bstack1111111_opy_ % len (bstack1lll111_opy_)
    bstack11ll1l1_opy_ = bstack1lll111_opy_ [:bstack1l111l_opy_] + bstack1lll111_opy_ [bstack1l111l_opy_:]
    if bstack11ll11l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l11_opy_ - (bstack1lllll1_opy_ + bstack1111111_opy_) % bstack11llll_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11ll1l1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l11_opy_ - (bstack1lllll1_opy_ + bstack1111111_opy_) % bstack11llll_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11ll1l1_opy_)])
    return eval (bstack1llll1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1llll111ll1_opy_
from browserstack_sdk.bstack1l1l11ll11_opy_ import bstack1l11lllll1_opy_
def _1lll1l1l1ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lll1l11ll1_opy_:
    def __init__(self, handler):
        self._1lll1l1ll1l_opy_ = {}
        self._1lll1ll1111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l11lllll1_opy_.version()
        if bstack1llll111ll1_opy_(pytest_version, bstack1l1ll1l_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᕥ")) >= 0:
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᕦ")] = Module._register_setup_function_fixture
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᕧ")] = Module._register_setup_module_fixture
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᕨ")] = Class._register_setup_class_fixture
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᕩ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᕪ"))
            Module._register_setup_module_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᕫ"))
            Class._register_setup_class_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᕬ"))
            Class._register_setup_method_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᕭ"))
        else:
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᕮ")] = Module._inject_setup_function_fixture
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᕯ")] = Module._inject_setup_module_fixture
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᕰ")] = Class._inject_setup_class_fixture
            self._1lll1l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᕱ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᕲ"))
            Module._inject_setup_module_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᕳ"))
            Class._inject_setup_class_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᕴ"))
            Class._inject_setup_method_fixture = self.bstack1lll1ll1l11_opy_(bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᕵ"))
    def bstack1lll1ll1ll1_opy_(self, bstack1lll1l1l11l_opy_, hook_type):
        bstack1lll1l1ll11_opy_ = id(bstack1lll1l1l11l_opy_.__class__)
        if (bstack1lll1l1ll11_opy_, hook_type) in self._1lll1ll1111_opy_:
            return
        meth = getattr(bstack1lll1l1l11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lll1ll1111_opy_[(bstack1lll1l1ll11_opy_, hook_type)] = meth
            setattr(bstack1lll1l1l11l_opy_, hook_type, self.bstack1lll1l1l1l1_opy_(hook_type, bstack1lll1l1ll11_opy_))
    def bstack1lll1l1lll1_opy_(self, instance, bstack1lll1ll11ll_opy_):
        if bstack1lll1ll11ll_opy_ == bstack1l1ll1l_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᕶ"):
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᕷ"))
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᕸ"))
        if bstack1lll1ll11ll_opy_ == bstack1l1ll1l_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᕹ"):
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᕺ"))
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᕻ"))
        if bstack1lll1ll11ll_opy_ == bstack1l1ll1l_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᕼ"):
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᕽ"))
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᕾ"))
        if bstack1lll1ll11ll_opy_ == bstack1l1ll1l_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᕿ"):
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᖀ"))
            self.bstack1lll1ll1ll1_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᖁ"))
    @staticmethod
    def bstack1lll1ll1l1l_opy_(hook_type, func, args):
        if hook_type in [bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᖂ"), bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᖃ")]:
            _1lll1l1l1ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lll1l1l1l1_opy_(self, hook_type, bstack1lll1l1ll11_opy_):
        def bstack1lll1l1l111_opy_(arg=None):
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᖄ"))
            result = None
            try:
                bstack1lll1ll111l_opy_ = self._1lll1ll1111_opy_[(bstack1lll1l1ll11_opy_, hook_type)]
                self.bstack1lll1ll1l1l_opy_(hook_type, bstack1lll1ll111l_opy_, (arg,))
                result = Result(result=bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᖅ"))
            except Exception as e:
                result = Result(result=bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᖆ"), exception=e)
                self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᖇ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᖈ"), result)
        def bstack1lll1l11lll_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᖉ"))
            result = None
            exception = None
            try:
                self.bstack1lll1ll1l1l_opy_(hook_type, self._1lll1ll1111_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᖊ"))
            except Exception as e:
                result = Result(result=bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᖋ"), exception=e)
                self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᖌ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᖍ"), result)
        if hook_type in [bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᖎ"), bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᖏ")]:
            return bstack1lll1l11lll_opy_
        return bstack1lll1l1l111_opy_
    def bstack1lll1ll1l11_opy_(self, bstack1lll1ll11ll_opy_):
        def bstack1lll1l1llll_opy_(this, *args, **kwargs):
            self.bstack1lll1l1lll1_opy_(this, bstack1lll1ll11ll_opy_)
            self._1lll1l1ll1l_opy_[bstack1lll1ll11ll_opy_](this, *args, **kwargs)
        return bstack1lll1l1llll_opy_