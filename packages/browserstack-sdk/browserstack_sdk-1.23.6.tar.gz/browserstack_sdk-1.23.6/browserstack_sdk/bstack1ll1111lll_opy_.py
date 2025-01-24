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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l111ll1l1_opy_ = {}
        bstack11l1llllll_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂูࠩ"), bstack1l1ll1l_opy_ (u"ฺࠩࠪ"))
        if not bstack11l1llllll_opy_:
            return bstack1l111ll1l1_opy_
        try:
            bstack11l1lllll1_opy_ = json.loads(bstack11l1llllll_opy_)
            if bstack1l1ll1l_opy_ (u"ࠥࡳࡸࠨ฻") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠦࡴࡹࠢ฼")] = bstack11l1lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠧࡵࡳࠣ฽")]
            if bstack1l1ll1l_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ฾") in bstack11l1lllll1_opy_ or bstack1l1ll1l_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ฿") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦเ")] = bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨแ"), bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨโ")))
            if bstack1l1ll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧใ") in bstack11l1lllll1_opy_ or bstack1l1ll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥไ") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦๅ")] = bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣๆ"), bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ็")))
            if bstack1l1ll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱ่ࠦ") in bstack11l1lllll1_opy_ or bstack1l1ll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱ้ࠦ") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ๊ࠧ")] = bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴ๋ࠢ"), bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ์")))
            if bstack1l1ll1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢํ") in bstack11l1lllll1_opy_ or bstack1l1ll1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧ๎") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ๏")] = bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ๐"), bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ๑")))
            if bstack1l1ll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ๒") in bstack11l1lllll1_opy_ or bstack1l1ll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ๓") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ๔")] = bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ๕"), bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ๖")))
            if bstack1l1ll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ๗") in bstack11l1lllll1_opy_ or bstack1l1ll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ๘") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ๙")] = bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ๚"), bstack11l1lllll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ๛")))
            if bstack1l1ll1l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ๜") in bstack11l1lllll1_opy_:
                bstack1l111ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ๝")] = bstack11l1lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ๞")]
        except Exception as error:
            logger.error(bstack1l1ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥ๟") +  str(error))
        return bstack1l111ll1l1_opy_