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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111l1l11l1_opy_, bstack1111lll11l_opy_, bstack11ll1111ll_opy_, bstack11l111ll1l_opy_, bstack1lllll1lll1_opy_, bstack1lllllll11l_opy_, bstack1llll1l11ll_opy_, bstack1l1lll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll11ll11l1_opy_ import bstack1ll11ll1111_opy_
import bstack_utils.bstack1l1ll11ll1_opy_ as bstack1l11llll1_opy_
from bstack_utils.bstack11l1lll111_opy_ import bstack11llll1111_opy_
import bstack_utils.bstack111l1lllll_opy_ as bstack11l11ll1_opy_
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1ll1ll1ll_opy_
from bstack_utils.bstack11l1lll11l_opy_ import bstack11l11l1l11_opy_
bstack1ll111111l1_opy_ = bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ᝕")
logger = logging.getLogger(__name__)
class bstack1llllll11_opy_:
    bstack1ll11ll11l1_opy_ = None
    bs_config = None
    bstack1lllll1ll1_opy_ = None
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11111ll1l1_opy_, stage=STAGE.SINGLE)
    def launch(cls, bs_config, bstack1lllll1ll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1lllll1ll1_opy_ = bstack1lllll1ll1_opy_
        try:
            cls.bstack1l1llll1ll1_opy_()
            bstack111l1l1111_opy_ = bstack111l1l11l1_opy_(bs_config)
            bstack111l11ll1l_opy_ = bstack1111lll11l_opy_(bs_config)
            data = bstack1l11llll1_opy_.bstack1l1lllllll1_opy_(bs_config, bstack1lllll1ll1_opy_)
            config = {
                bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺࡨࠨ᝖"): (bstack111l1l1111_opy_, bstack111l11ll1l_opy_),
                bstack1l1ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᝗"): cls.default_headers()
            }
            response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪ᝘"), cls.request_url(bstack1l1ll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠷࠵ࡢࡶ࡫࡯ࡨࡸ࠭᝙")), data, config)
            if response.status_code != 200:
                bstack1l1lll1llll_opy_ = response.json()
                if bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ᝚")] == False:
                    cls.bstack1l1llll1lll_opy_(bstack1l1lll1llll_opy_)
                    return
                cls.bstack1l1llll1111_opy_(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᝛")])
                cls.bstack1ll111111ll_opy_(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᝜")])
                return None
            bstack1ll1111l111_opy_ = cls.bstack1l1llll1l1l_opy_(response)
            return bstack1ll1111l111_opy_
        except Exception as error:
            logger.error(bstack1l1ll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣ᝝").format(str(error)))
            return None
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def stop(cls, bstack1l1llll11ll_opy_=None):
        if not bstack11llll1111_opy_.on() and not bstack11l11ll1_opy_.on():
            return
        if os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ᝞")) == bstack1l1ll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᝟") or os.environ.get(bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᝠ")) == bstack1l1ll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᝡ"):
            logger.error(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᝢ"))
            return {
                bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᝣ"): bstack1l1ll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᝤ"),
                bstack1l1ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᝥ"): bstack1l1ll1l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪᝦ")
            }
        try:
            cls.bstack1ll11ll11l1_opy_.shutdown()
            data = {
                bstack1l1ll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᝧ"): bstack1l1lll1l1_opy_()
            }
            if not bstack1l1llll11ll_opy_ is None:
                data[bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫᝨ")] = [{
                    bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᝩ"): bstack1l1ll1l_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧᝪ"),
                    bstack1l1ll1l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪᝫ"): bstack1l1llll11ll_opy_
                }]
            config = {
                bstack1l1ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᝬ"): cls.default_headers()
            }
            bstack1llll11111l_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭᝭").format(os.environ[bstack1l1ll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦᝮ")])
            bstack1ll1111l11l_opy_ = cls.request_url(bstack1llll11111l_opy_)
            response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"ࠧࡑࡗࡗࠫᝯ"), bstack1ll1111l11l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1ll1l_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢᝰ"))
        except Exception as error:
            logger.error(bstack1l1ll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨ᝱") + str(error))
            return {
                bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝲ"): bstack1l1ll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᝳ"),
                bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᝴"): str(error)
            }
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def bstack1l1llll1l1l_opy_(cls, response):
        bstack1l1lll1llll_opy_ = response.json()
        bstack1ll1111l111_opy_ = {}
        if bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"࠭ࡪࡸࡶࠪ᝵")) is None:
            os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ᝶")] = bstack1l1ll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭᝷")
        else:
            os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ᝸")] = bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"ࠪ࡮ࡼࡺࠧ᝹"), bstack1l1ll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ᝺"))
        os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᝻")] = bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ᝼"), bstack1l1ll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ᝽"))
        if bstack11llll1111_opy_.bstack1l1lllll1ll_opy_(cls.bs_config, cls.bstack1lllll1ll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ᝾"), bstack1l1ll1l_opy_ (u"ࠩࠪ᝿"))) is True:
            bstack1ll11111l11_opy_, bstack11l11l1ll_opy_, bstack1ll11111lll_opy_ = cls.bstack1l1llllllll_opy_(bstack1l1lll1llll_opy_)
            if bstack1ll11111l11_opy_ != None and bstack11l11l1ll_opy_ != None:
                bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪក")] = {
                    bstack1l1ll1l_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧខ"): bstack1ll11111l11_opy_,
                    bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧគ"): bstack11l11l1ll_opy_,
                    bstack1l1ll1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪឃ"): bstack1ll11111lll_opy_
                }
            else:
                bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧង")] = {}
        else:
            bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨច")] = {}
        if bstack11l11ll1_opy_.bstack1111lll111_opy_(cls.bs_config) is True:
            bstack1l1lllll111_opy_, bstack11l11l1ll_opy_ = cls.bstack1ll1111ll11_opy_(bstack1l1lll1llll_opy_)
            if bstack1l1lllll111_opy_ != None and bstack11l11l1ll_opy_ != None:
                bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩឆ")] = {
                    bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧជ"): bstack1l1lllll111_opy_,
                    bstack1l1ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ឈ"): bstack11l11l1ll_opy_,
                }
            else:
                bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬញ")] = {}
        else:
            bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ដ")] = {}
        if bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧឋ")].get(bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪឌ")) != None or bstack1ll1111l111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩឍ")].get(bstack1l1ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬណ")) != None:
            cls.bstack1ll11111111_opy_(bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"ࠫ࡯ࡽࡴࠨត")), bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧថ")))
        return bstack1ll1111l111_opy_
    @classmethod
    def bstack1l1llllllll_opy_(cls, bstack1l1lll1llll_opy_):
        if bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ទ")) == None:
            cls.bstack1l1llll1111_opy_()
            return [None, None, None]
        if bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧធ")][bstack1l1ll1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩន")] != True:
            cls.bstack1l1llll1111_opy_(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩប")])
            return [None, None, None]
        logger.debug(bstack1l1ll1l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧផ"))
        os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪព")] = bstack1l1ll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪភ")
        if bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"࠭ࡪࡸࡶࠪម")):
            os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨយ")] = bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨ࡬ࡺࡸࠬរ")]
            os.environ[bstack1l1ll1l_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ល")] = json.dumps({
                bstack1l1ll1l_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬវ"): bstack111l1l11l1_opy_(cls.bs_config),
                bstack1l1ll1l_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ឝ"): bstack1111lll11l_opy_(cls.bs_config)
            })
        if bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧឞ")):
            os.environ[bstack1l1ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬស")] = bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩហ")]
        if bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨឡ")].get(bstack1l1ll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪអ"), {}).get(bstack1l1ll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧឣ")):
            os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬឤ")] = str(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬឥ")][bstack1l1ll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧឦ")][bstack1l1ll1l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫឧ")])
        return [bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨ࡬ࡺࡸࠬឨ")], bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫឩ")], os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫឪ")]]
    @classmethod
    def bstack1ll1111ll11_opy_(cls, bstack1l1lll1llll_opy_):
        if bstack1l1lll1llll_opy_.get(bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫឫ")) == None:
            cls.bstack1ll111111ll_opy_()
            return [None, None]
        if bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬឬ")][bstack1l1ll1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧឭ")] != True:
            cls.bstack1ll111111ll_opy_(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧឮ")])
            return [None, None]
        if bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨឯ")].get(bstack1l1ll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪឰ")):
            logger.debug(bstack1l1ll1l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧឱ"))
            parsed = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬឲ"), bstack1l1ll1l_opy_ (u"ࠬࢁࡽࠨឳ")))
            capabilities = bstack1l11llll1_opy_.bstack1ll1111l1ll_opy_(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭឴")][bstack1l1ll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ឵")][bstack1l1ll1l_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧា")], bstack1l1ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧិ"), bstack1l1ll1l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩី"))
            bstack1l1lllll111_opy_ = capabilities[bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩឹ")]
            os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪឺ")] = bstack1l1lllll111_opy_
            parsed[bstack1l1ll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧុ")] = capabilities[bstack1l1ll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨូ")]
            os.environ[bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩួ")] = json.dumps(parsed)
            scripts = bstack1l11llll1_opy_.bstack1ll1111l1ll_opy_(bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩើ")][bstack1l1ll1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫឿ")][bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬៀ")], bstack1l1ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪេ"), bstack1l1ll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧែ"))
            bstack1ll1ll1ll_opy_.bstack111l1111ll_opy_(scripts)
            commands = bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧៃ")][bstack1l1ll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩោ")][bstack1l1ll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪៅ")].get(bstack1l1ll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬំ"))
            bstack1ll1ll1ll_opy_.bstack111l111l1l_opy_(commands)
            bstack1ll1ll1ll_opy_.store()
        return [bstack1l1lllll111_opy_, bstack1l1lll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ះ")]]
    @classmethod
    def bstack1l1llll1111_opy_(cls, response=None):
        os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪៈ")] = bstack1l1ll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ៉")
        os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭៊")] = bstack1l1ll1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ់")
        os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ៌")] = bstack1l1ll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ៍")
        os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬ៎")] = bstack1l1ll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ៏")
        os.environ[bstack1l1ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ័")] = bstack1l1ll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ៑")
        os.environ[bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔ្ࠩ")] = bstack1l1ll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢ៓")
        cls.bstack1l1llll1lll_opy_(response, bstack1l1ll1l_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ។"))
        return [None, None, None]
    @classmethod
    def bstack1ll111111ll_opy_(cls, response=None):
        os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ៕")] = bstack1l1ll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ៖")
        os.environ[bstack1l1ll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫៗ")] = bstack1l1ll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ៘")
        os.environ[bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ៙")] = bstack1l1ll1l_opy_ (u"ࠩࡱࡹࡱࡲࠧ៚")
        cls.bstack1l1llll1lll_opy_(response, bstack1l1ll1l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ៛"))
        return [None, None, None]
    @classmethod
    def bstack1ll11111111_opy_(cls, bstack1ll11111l1l_opy_, bstack11l11l1ll_opy_):
        os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬៜ")] = bstack1ll11111l1l_opy_
        os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ៝")] = bstack11l11l1ll_opy_
    @classmethod
    def bstack1l1llll1lll_opy_(cls, response=None, product=bstack1l1ll1l_opy_ (u"ࠨࠢ៞")):
        if response == None:
            logger.error(product + bstack1l1ll1l_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤ៟"))
        for error in response[bstack1l1ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ០")]:
            bstack1llll1ll1ll_opy_ = error[bstack1l1ll1l_opy_ (u"ࠩ࡮ࡩࡾ࠭១")]
            error_message = error[bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ២")]
            if error_message:
                if bstack1llll1ll1ll_opy_ == bstack1l1ll1l_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥ៣"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨ៤") + product + bstack1l1ll1l_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ៥"))
    @classmethod
    def bstack1l1llll1ll1_opy_(cls):
        if cls.bstack1ll11ll11l1_opy_ is not None:
            return
        cls.bstack1ll11ll11l1_opy_ = bstack1ll11ll1111_opy_(cls.bstack1l1llll11l1_opy_)
        cls.bstack1ll11ll11l1_opy_.start()
    @classmethod
    def bstack111lllll1l_opy_(cls):
        if cls.bstack1ll11ll11l1_opy_ is None:
            return
        cls.bstack1ll11ll11l1_opy_.shutdown()
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def bstack1l1llll11l1_opy_(cls, bstack11l11ll1l1_opy_, bstack1l1llll1l11_opy_=bstack1l1ll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭៦")):
        config = {
            bstack1l1ll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ៧"): cls.default_headers()
        }
        logger.debug(bstack1l1ll1l_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤ៨").format(bstack1l1ll1l_opy_ (u"ࠪ࠰ࠥ࠭៩").join([event[bstack1l1ll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ៪")] for event in bstack11l11ll1l1_opy_])))
        response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪ៫"), cls.request_url(bstack1l1llll1l11_opy_), bstack11l11ll1l1_opy_, config)
        bstack111l111111_opy_ = response.json()
    @classmethod
    def bstack1llll1ll11_opy_(cls, bstack11l11ll1l1_opy_, bstack1l1llll1l11_opy_=bstack1l1ll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ៬")):
        logger.debug(bstack1l1ll1l_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ៭").format(bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ៮")]))
        if not bstack1l11llll1_opy_.bstack1ll1111l1l1_opy_(bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭៯")]):
            logger.debug(bstack1l1ll1l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ៰").format(bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ៱")]))
            return
        bstack1l11ll1l11_opy_ = bstack1l11llll1_opy_.bstack1l1lllll11l_opy_(bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ៲")], bstack11l11ll1l1_opy_.get(bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ៳")))
        if bstack1l11ll1l11_opy_ != None:
            if bstack11l11ll1l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ៴")) != None:
                bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ៵")][bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ៶")] = bstack1l11ll1l11_opy_
            else:
                bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ៷")] = bstack1l11ll1l11_opy_
        if bstack1l1llll1l11_opy_ == bstack1l1ll1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ៸"):
            cls.bstack1l1llll1ll1_opy_()
            logger.debug(bstack1l1ll1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ៹").format(bstack11l11ll1l1_opy_[bstack1l1ll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ៺")]))
            cls.bstack1ll11ll11l1_opy_.add(bstack11l11ll1l1_opy_)
        elif bstack1l1llll1l11_opy_ == bstack1l1ll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ៻"):
            cls.bstack1l1llll11l1_opy_([bstack11l11ll1l1_opy_], bstack1l1llll1l11_opy_)
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def bstack1ll111lll1_opy_(cls, bstack11l11lllll_opy_):
        bstack1l1llll111l_opy_ = []
        for log in bstack11l11lllll_opy_:
            bstack1l1lllll1l1_opy_ = {
                bstack1l1ll1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭៼"): bstack1l1ll1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫ៽"),
                bstack1l1ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៾"): log[bstack1l1ll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ៿")],
                bstack1l1ll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᠀"): log[bstack1l1ll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ᠁")],
                bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ᠂"): {},
                bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᠃"): log[bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᠄")],
            }
            if bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᠅") in log:
                bstack1l1lllll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᠆")] = log[bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᠇")]
            elif bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᠈") in log:
                bstack1l1lllll1l1_opy_[bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᠉")] = log[bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᠊")]
            bstack1l1llll111l_opy_.append(bstack1l1lllll1l1_opy_)
        cls.bstack1llll1ll11_opy_({
            bstack1l1ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᠋"): bstack1l1ll1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᠌"),
            bstack1l1ll1l_opy_ (u"ࠫࡱࡵࡧࡴࠩ᠍"): bstack1l1llll111l_opy_
        })
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def bstack1ll11111ll1_opy_(cls, steps):
        bstack1l1llllll11_opy_ = []
        for step in steps:
            bstack1ll1111111l_opy_ = {
                bstack1l1ll1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᠎"): bstack1l1ll1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ᠏"),
                bstack1l1ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᠐"): step[bstack1l1ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᠑")],
                bstack1l1ll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᠒"): step[bstack1l1ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᠓")],
                bstack1l1ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᠔"): step[bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᠕")],
                bstack1l1ll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ᠖"): step[bstack1l1ll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ᠗")]
            }
            if bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᠘") in step:
                bstack1ll1111111l_opy_[bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᠙")] = step[bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᠚")]
            elif bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᠛") in step:
                bstack1ll1111111l_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᠜")] = step[bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᠝")]
            bstack1l1llllll11_opy_.append(bstack1ll1111111l_opy_)
        cls.bstack1llll1ll11_opy_({
            bstack1l1ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ᠞"): bstack1l1ll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ᠟"),
            bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᠠ"): bstack1l1llllll11_opy_
        })
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def bstack11l11111_opy_(cls, screenshot):
        cls.bstack1llll1ll11_opy_({
            bstack1l1ll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᠡ"): bstack1l1ll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᠢ"),
            bstack1l1ll1l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᠣ"): [{
                bstack1l1ll1l_opy_ (u"࠭࡫ࡪࡰࡧࠫᠤ"): bstack1l1ll1l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩᠥ"),
                bstack1l1ll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᠦ"): datetime.datetime.utcnow().isoformat() + bstack1l1ll1l_opy_ (u"ࠩ࡝ࠫᠧ"),
                bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᠨ"): screenshot[bstack1l1ll1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᠩ")],
                bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᠪ"): screenshot[bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᠫ")]
            }]
        }, bstack1l1llll1l11_opy_=bstack1l1ll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᠬ"))
    @classmethod
    @bstack11l111ll1l_opy_(class_method=True)
    def bstack1ll11l1111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1llll1ll11_opy_({
            bstack1l1ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᠭ"): bstack1l1ll1l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᠮ"),
            bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᠯ"): {
                bstack1l1ll1l_opy_ (u"ࠦࡺࡻࡩࡥࠤᠰ"): cls.current_test_uuid(),
                bstack1l1ll1l_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦᠱ"): cls.bstack11l1ll1l1l_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1ll1ll1_opy_(cls, event: str, bstack11l11ll1l1_opy_: bstack11l11l1l11_opy_):
        bstack111llll11l_opy_ = {
            bstack1l1ll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᠲ"): event,
            bstack11l11ll1l1_opy_.bstack11l11l11ll_opy_(): bstack11l11ll1l1_opy_.bstack11l111ll11_opy_(event)
        }
        cls.bstack1llll1ll11_opy_(bstack111llll11l_opy_)
        result = getattr(bstack11l11ll1l1_opy_, bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᠳ"), None)
        if event == bstack1l1ll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᠴ"):
            threading.current_thread().bstackTestMeta = {bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᠵ"): bstack1l1ll1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᠶ")}
        elif event == bstack1l1ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᠷ"):
            threading.current_thread().bstackTestMeta = {bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᠸ"): getattr(result, bstack1l1ll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᠹ"), bstack1l1ll1l_opy_ (u"ࠧࠨᠺ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᠻ"), None) is None or os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᠼ")] == bstack1l1ll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᠽ")) and (os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᠾ"), None) is None or os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᠿ")] == bstack1l1ll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᡀ")):
            return False
        return True
    @staticmethod
    def bstack1l1llllll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llllll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1ll1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᡁ"): bstack1l1ll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᡂ"),
            bstack1l1ll1l_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᡃ"): bstack1l1ll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᡄ")
        }
        if os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᡅ"), None):
            headers[bstack1l1ll1l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᡆ")] = bstack1l1ll1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᡇ").format(os.environ[bstack1l1ll1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣᡈ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1ll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᡉ").format(bstack1ll111111l1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᡊ"), None)
    @staticmethod
    def bstack11l1ll1l1l_opy_(driver):
        return {
            bstack1lllll1lll1_opy_(): bstack1lllllll11l_opy_(driver)
        }
    @staticmethod
    def bstack1ll1111ll1l_opy_(exception_info, report):
        return [{bstack1l1ll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᡋ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111l1llll1_opy_(typename):
        if bstack1l1ll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᡌ") in typename:
            return bstack1l1ll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᡍ")
        return bstack1l1ll1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᡎ")