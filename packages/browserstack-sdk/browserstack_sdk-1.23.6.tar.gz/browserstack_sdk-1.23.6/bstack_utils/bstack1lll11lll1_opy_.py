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
from browserstack_sdk.bstack1l1l11ll11_opy_ import bstack1l11lllll1_opy_
from browserstack_sdk.bstack11l11ll111_opy_ import RobotHandler
def bstack11111ll1l_opy_(framework):
    if framework.lower() == bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᎇ"):
        return bstack1l11lllll1_opy_.version()
    elif framework.lower() == bstack1l1ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᎈ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1ll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᎉ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1ll1l_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᎊ")