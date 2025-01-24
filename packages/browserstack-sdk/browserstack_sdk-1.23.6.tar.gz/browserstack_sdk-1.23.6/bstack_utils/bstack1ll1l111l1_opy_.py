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
import threading
import logging
import bstack_utils.bstack111l1lllll_opy_ as bstack11l11ll1_opy_
from bstack_utils.helper import bstack1ll111111l_opy_
logger = logging.getLogger(__name__)
def bstack111111l11_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l1l11l11l_opy_(context, *args):
    tags = getattr(args[0], bstack1l1ll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ၩ"), [])
    bstack11l1111l_opy_ = bstack11l11ll1_opy_.bstack11ll1l1ll1_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l1111l_opy_
    try:
      bstack111lll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l11_opy_(bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨၪ")) else context.browser
      if bstack111lll1l_opy_ and bstack111lll1l_opy_.session_id and bstack11l1111l_opy_ and bstack1ll111111l_opy_(
              threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩၫ"), None):
          threading.current_thread().isA11yTest = bstack11l11ll1_opy_.bstack1l111l11ll_opy_(bstack111lll1l_opy_, bstack11l1111l_opy_)
    except Exception as e:
       logger.debug(bstack1l1ll1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫၬ").format(str(e)))
def bstack1l1l111l1_opy_(bstack111lll1l_opy_):
    if bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩၭ"), None) and bstack1ll111111l_opy_(
      threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬၮ"), None) and not bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪၯ"), False):
      threading.current_thread().a11y_stop = True
      bstack11l11ll1_opy_.bstack1ll1lll111_opy_(bstack111lll1l_opy_, name=bstack1l1ll1l_opy_ (u"ࠣࠤၰ"), path=bstack1l1ll1l_opy_ (u"ࠤࠥၱ"))