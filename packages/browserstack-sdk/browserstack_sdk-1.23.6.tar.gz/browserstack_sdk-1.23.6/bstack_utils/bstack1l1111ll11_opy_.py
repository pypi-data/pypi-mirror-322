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
from collections import deque
from bstack_utils.constants import *
class bstack1l1ll1l1ll_opy_:
    def __init__(self):
        self._1ll1l1lll11_opy_ = deque()
        self._1ll1l1l11l1_opy_ = {}
        self._1ll1l1ll11l_opy_ = False
    def bstack1ll1l1ll1ll_opy_(self, test_name, bstack1ll1l1l1lll_opy_):
        bstack1ll1l1l1l1l_opy_ = self._1ll1l1l11l1_opy_.get(test_name, {})
        return bstack1ll1l1l1l1l_opy_.get(bstack1ll1l1l1lll_opy_, 0)
    def bstack1ll1l1ll1l1_opy_(self, test_name, bstack1ll1l1l1lll_opy_):
        bstack1ll1l1l1l11_opy_ = self.bstack1ll1l1ll1ll_opy_(test_name, bstack1ll1l1l1lll_opy_)
        self.bstack1ll1l1ll111_opy_(test_name, bstack1ll1l1l1lll_opy_)
        return bstack1ll1l1l1l11_opy_
    def bstack1ll1l1ll111_opy_(self, test_name, bstack1ll1l1l1lll_opy_):
        if test_name not in self._1ll1l1l11l1_opy_:
            self._1ll1l1l11l1_opy_[test_name] = {}
        bstack1ll1l1l1l1l_opy_ = self._1ll1l1l11l1_opy_[test_name]
        bstack1ll1l1l1l11_opy_ = bstack1ll1l1l1l1l_opy_.get(bstack1ll1l1l1lll_opy_, 0)
        bstack1ll1l1l1l1l_opy_[bstack1ll1l1l1lll_opy_] = bstack1ll1l1l1l11_opy_ + 1
    def bstack1l11lll1l1_opy_(self, bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_):
        bstack1ll1l1l11ll_opy_ = self.bstack1ll1l1ll1l1_opy_(bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_)
        event_name = bstack1111l11lll_opy_[bstack1ll1l1lll1l_opy_]
        bstack1ll1l1l1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᙷ").format(bstack1ll1l1l1111_opy_, event_name, bstack1ll1l1l11ll_opy_)
        self._1ll1l1lll11_opy_.append(bstack1ll1l1l1ll1_opy_)
    def bstack1l11l1lll_opy_(self):
        return len(self._1ll1l1lll11_opy_) == 0
    def bstack1l11111lll_opy_(self):
        bstack1ll1l1l111l_opy_ = self._1ll1l1lll11_opy_.popleft()
        return bstack1ll1l1l111l_opy_
    def capturing(self):
        return self._1ll1l1ll11l_opy_
    def bstack1llll111_opy_(self):
        self._1ll1l1ll11l_opy_ = True
    def bstack1ll1ll111_opy_(self):
        self._1ll1l1ll11l_opy_ = False