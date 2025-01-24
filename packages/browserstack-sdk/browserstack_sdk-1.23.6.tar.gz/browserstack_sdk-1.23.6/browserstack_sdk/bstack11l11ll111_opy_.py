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
class RobotHandler():
    def __init__(self, args, logger, bstack111ll1lll1_opy_, bstack111ll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll1lll1_opy_ = bstack111ll1lll1_opy_
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1111l1l_opy_(bstack111l1ll1ll_opy_):
        bstack111l1lll11_opy_ = []
        if bstack111l1ll1ll_opy_:
            tokens = str(os.path.basename(bstack111l1ll1ll_opy_)).split(bstack1l1ll1l_opy_ (u"ࠥࡣࠧྙ"))
            camelcase_name = bstack1l1ll1l_opy_ (u"ࠦࠥࠨྚ").join(t.title() for t in tokens)
            suite_name, bstack111l1lll1l_opy_ = os.path.splitext(camelcase_name)
            bstack111l1lll11_opy_.append(suite_name)
        return bstack111l1lll11_opy_
    @staticmethod
    def bstack111l1llll1_opy_(typename):
        if bstack1l1ll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣྛ") in typename:
            return bstack1l1ll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢྜ")
        return bstack1l1ll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣྜྷ")