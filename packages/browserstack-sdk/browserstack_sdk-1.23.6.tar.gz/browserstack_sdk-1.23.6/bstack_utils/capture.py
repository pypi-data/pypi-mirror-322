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
import builtins
import logging
class bstack11l1l1l1ll_opy_:
    def __init__(self, handler):
        self._1111l1l1ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111ll1111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1ll1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨၲ"), bstack1l1ll1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪၳ"), bstack1l1ll1l_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ၴ"), bstack1l1ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬၵ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l1llll_opy_
        self._1111l1lll1_opy_()
    def _1111l1llll_opy_(self, *args, **kwargs):
        self._1111l1l1ll_opy_(*args, **kwargs)
        message = bstack1l1ll1l_opy_ (u"ࠧࠡࠩၶ").join(map(str, args)) + bstack1l1ll1l_opy_ (u"ࠨ࡞ࡱࠫၷ")
        self._log_message(bstack1l1ll1l_opy_ (u"ࠩࡌࡒࡋࡕࠧၸ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩၹ"): level, bstack1l1ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬၺ"): msg})
    def _1111l1lll1_opy_(self):
        for level, bstack1111l1ll11_opy_ in self._1111ll1111_opy_.items():
            setattr(logging, level, self._1111l1ll1l_opy_(level, bstack1111l1ll11_opy_))
    def _1111l1ll1l_opy_(self, level, bstack1111l1ll11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111l1ll11_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111l1l1ll_opy_
        for level, bstack1111l1ll11_opy_ in self._1111ll1111_opy_.items():
            setattr(logging, level, bstack1111l1ll11_opy_)