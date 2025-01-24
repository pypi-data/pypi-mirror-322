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
class bstack1111lllll_opy_:
    def __init__(self, handler):
        self._1ll11l11ll1_opy_ = None
        self.handler = handler
        self._1ll11l1l111_opy_ = self.bstack1ll11l11lll_opy_()
        self.patch()
    def patch(self):
        self._1ll11l11ll1_opy_ = self._1ll11l1l111_opy_.execute
        self._1ll11l1l111_opy_.execute = self.bstack1ll11l11l1l_opy_()
    def bstack1ll11l11l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1ll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦᛠ"), driver_command, None, this, args)
            response = self._1ll11l11ll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1ll1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦᛡ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11l1l111_opy_.execute = self._1ll11l11ll1_opy_
    @staticmethod
    def bstack1ll11l11lll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver