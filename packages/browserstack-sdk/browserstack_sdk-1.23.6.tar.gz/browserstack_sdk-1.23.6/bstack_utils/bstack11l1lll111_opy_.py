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
import os
import threading
from bstack_utils.helper import bstack1ll11l1ll1_opy_
from bstack_utils.constants import bstack11111l1lll_opy_, EVENTS, STAGE
from bstack_utils.bstack11l1lll11_opy_ import get_logger
logger = get_logger(__name__)
class bstack11llll1111_opy_:
    bstack1ll11ll11l1_opy_ = None
    @classmethod
    def bstack1ll111l1l_opy_(cls):
        if cls.on():
            logger.info(
                bstack1l1ll1l_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᢍ").format(os.environ[bstack1l1ll1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᢎ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᢏ"), None) is None or os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᢐ")] == bstack1l1ll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᢑ"):
            return False
        return True
    @classmethod
    def bstack1l1lll11l1l_opy_(cls, bs_config, framework=bstack1l1ll1l_opy_ (u"ࠦࠧᢒ")):
        bstack1l1lll11111_opy_ = False
        for fw in bstack11111l1lll_opy_:
            if fw in framework:
                bstack1l1lll11111_opy_ = True
        return bstack1ll11l1ll1_opy_(bs_config.get(bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᢓ"), bstack1l1lll11111_opy_))
    @classmethod
    def bstack1l1lll111l1_opy_(cls, framework):
        return framework in bstack11111l1lll_opy_
    @classmethod
    def bstack1l1lllll1ll_opy_(cls, bs_config, framework):
        return cls.bstack1l1lll11l1l_opy_(bs_config, framework) is True and cls.bstack1l1lll111l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᢔ"), None)
    @staticmethod
    def bstack11l1ll11l1_opy_():
        if getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᢕ"), None):
            return {
                bstack1l1ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᢖ"): bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺࠧᢗ"),
                bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᢘ"): getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᢙ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᢚ"), None):
            return {
                bstack1l1ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᢛ"): bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᢜ"),
                bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᢝ"): getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᢞ"), None)
            }
        return None
    @staticmethod
    def bstack1l1ll1llll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11llll1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1111l1l_opy_(test, hook_name=None):
        bstack1l1ll1lllll_opy_ = test.parent
        if hook_name in [bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᢟ"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᢠ"), bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᢡ"), bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᢢ")]:
            bstack1l1ll1lllll_opy_ = test
        scope = []
        while bstack1l1ll1lllll_opy_ is not None:
            scope.append(bstack1l1ll1lllll_opy_.name)
            bstack1l1ll1lllll_opy_ = bstack1l1ll1lllll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l1ll1lll1l_opy_(hook_type):
        if hook_type == bstack1l1ll1l_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᢣ"):
            return bstack1l1ll1l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᢤ")
        elif hook_type == bstack1l1ll1l_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᢥ"):
            return bstack1l1ll1l_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᢦ")
    @staticmethod
    def bstack1l1lll111ll_opy_(bstack1l1lll1ll1_opy_):
        try:
            if not bstack11llll1111_opy_.on():
                return bstack1l1lll1ll1_opy_
            if os.environ.get(bstack1l1ll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᢧ"), None) == bstack1l1ll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᢨ"):
                tests = os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕᢩࠥ"), None)
                if tests is None or tests == bstack1l1ll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᢪ"):
                    return bstack1l1lll1ll1_opy_
                bstack1l1lll1ll1_opy_ = tests.split(bstack1l1ll1l_opy_ (u"ࠨ࠮ࠪ᢫"))
                return bstack1l1lll1ll1_opy_
        except Exception as exc:
            logger.debug(bstack1l1lll1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࡾࡷࡹࡸࠨࡦࡺࡦ࠭ࢂࠨ᢬"))
        return bstack1l1lll1ll1_opy_