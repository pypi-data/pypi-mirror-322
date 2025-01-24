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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack111l1lllll_opy_ as bstack11l11ll1_opy_
from browserstack_sdk.bstack1l111111l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1ll1lll_opy_
class bstack1l11lllll1_opy_:
    def __init__(self, args, logger, bstack111ll1lll1_opy_, bstack111ll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll1lll1_opy_ = bstack111ll1lll1_opy_
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1lll1ll1_opy_ = []
        self.bstack111ll111ll_opy_ = None
        self.bstack11ll1l11ll_opy_ = []
        self.bstack111lll1111_opy_ = self.bstack1l1l1ll11_opy_()
        self.bstack1ll1ll11_opy_ = -1
    def bstack1ll1lllll1_opy_(self, bstack111ll1l11l_opy_):
        self.parse_args()
        self.bstack111ll1l111_opy_()
        self.bstack111ll11l11_opy_(bstack111ll1l11l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111ll111l1_opy_():
        import importlib
        if getattr(importlib, bstack1l1ll1l_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫཹ"), False):
            bstack111ll1llll_opy_ = importlib.find_loader(bstack1l1ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ེࠩ"))
        else:
            bstack111ll1llll_opy_ = importlib.util.find_spec(bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ཻࠪ"))
    def bstack111ll1111l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1ll11_opy_ = -1
        if self.bstack111ll11l1l_opy_ and bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ོࠩ") in self.bstack111ll1lll1_opy_:
            self.bstack1ll1ll11_opy_ = int(self.bstack111ll1lll1_opy_[bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ཽࠪ")])
        try:
            bstack111ll11ll1_opy_ = [bstack1l1ll1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ཾ"), bstack1l1ll1l_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨཿ"), bstack1l1ll1l_opy_ (u"࠭࠭ࡱྀࠩ")]
            if self.bstack1ll1ll11_opy_ >= 0:
                bstack111ll11ll1_opy_.extend([bstack1l1ll1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨཱྀ"), bstack1l1ll1l_opy_ (u"ࠨ࠯ࡱࠫྂ")])
            for arg in bstack111ll11ll1_opy_:
                self.bstack111ll1111l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111ll1l111_opy_(self):
        bstack111ll111ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111ll111ll_opy_ = bstack111ll111ll_opy_
        return bstack111ll111ll_opy_
    def bstack1lllllllll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111ll111l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1ll1lll_opy_)
    def bstack111ll11l11_opy_(self, bstack111ll1l11l_opy_):
        bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
        if bstack111ll1l11l_opy_:
            self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ྃ"))
            self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠪࡘࡷࡻࡥࠨ྄"))
        if bstack111111111_opy_.bstack111ll1l1ll_opy_():
            self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ྅"))
            self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"࡚ࠬࡲࡶࡧࠪ྆"))
        self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"࠭࠭ࡱࠩ྇"))
        self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬྈ"))
        self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪྉ"))
        self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩྊ"))
        if self.bstack1ll1ll11_opy_ > 1:
            self.bstack111ll111ll_opy_.append(bstack1l1ll1l_opy_ (u"ࠪ࠱ࡳ࠭ྋ"))
            self.bstack111ll111ll_opy_.append(str(self.bstack1ll1ll11_opy_))
    def bstack111ll11111_opy_(self):
        bstack11ll1l11ll_opy_ = []
        for spec in self.bstack1l1lll1ll1_opy_:
            bstack1111ll1l_opy_ = [spec]
            bstack1111ll1l_opy_ += self.bstack111ll111ll_opy_
            bstack11ll1l11ll_opy_.append(bstack1111ll1l_opy_)
        self.bstack11ll1l11ll_opy_ = bstack11ll1l11ll_opy_
        return bstack11ll1l11ll_opy_
    def bstack1l1l1ll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111lll1111_opy_ = True
            return True
        except Exception as e:
            self.bstack111lll1111_opy_ = False
        return self.bstack111lll1111_opy_
    def bstack11ll11111l_opy_(self, bstack111ll11lll_opy_, bstack1ll1lllll1_opy_):
        bstack1ll1lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫྌ")] = self.bstack111ll1lll1_opy_
        multiprocessing.set_start_method(bstack1l1ll1l_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫྍ"))
        bstack11llll11l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1ll1l_opy_ = manager.list()
        if bstack1l1ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩྎ") in self.bstack111ll1lll1_opy_:
            for index, platform in enumerate(self.bstack111ll1lll1_opy_[bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪྏ")]):
                bstack11llll11l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111ll11lll_opy_,
                                                            args=(self.bstack111ll111ll_opy_, bstack1ll1lllll1_opy_, bstack1lll1ll1l_opy_)))
            bstack111ll1ll11_opy_ = len(self.bstack111ll1lll1_opy_[bstack1l1ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫྐ")])
        else:
            bstack11llll11l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111ll11lll_opy_,
                                                        args=(self.bstack111ll111ll_opy_, bstack1ll1lllll1_opy_, bstack1lll1ll1l_opy_)))
            bstack111ll1ll11_opy_ = 1
        i = 0
        for t in bstack11llll11l_opy_:
            os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩྑ")] = str(i)
            if bstack1l1ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ྒ") in self.bstack111ll1lll1_opy_:
                os.environ[bstack1l1ll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬྒྷ")] = json.dumps(self.bstack111ll1lll1_opy_[bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨྔ")][i % bstack111ll1ll11_opy_])
            i += 1
            t.start()
        for t in bstack11llll11l_opy_:
            t.join()
        return list(bstack1lll1ll1l_opy_)
    @staticmethod
    def bstack1ll11llll1_opy_(driver, bstack111ll1l1l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪྕ"), None)
        if item and getattr(item, bstack1l1ll1l_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩྖ"), None) and not getattr(item, bstack1l1ll1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪྗ"), False):
            logger.info(
                bstack1l1ll1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣ྘"))
            bstack111ll1ll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l11ll1_opy_.bstack1ll1lll111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)