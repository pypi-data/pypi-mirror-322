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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llllllll1l_opy_, bstack1l11lll1ll_opy_, bstack1ll111111l_opy_, bstack1l1l1lllll_opy_, \
    bstack1111111111_opy_
from bstack_utils.measure import measure
def bstack11lll1111l_opy_(bstack1ll11l11l11_opy_):
    for driver in bstack1ll11l11l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111l1llll_opy_, stage=STAGE.SINGLE)
def bstack1l1llll11_opy_(driver, status, reason=bstack1l1ll1l_opy_ (u"࠭ࠧᛢ")):
    bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
    if bstack111111111_opy_.bstack111ll1l1ll_opy_():
        return
    bstack1l1l1l11ll_opy_ = bstack11l1l1ll_opy_(bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᛣ"), bstack1l1ll1l_opy_ (u"ࠨࠩᛤ"), status, reason, bstack1l1ll1l_opy_ (u"ࠩࠪᛥ"), bstack1l1ll1l_opy_ (u"ࠪࠫᛦ"))
    driver.execute_script(bstack1l1l1l11ll_opy_)
@measure(event_name=EVENTS.bstack111l1llll_opy_, stage=STAGE.SINGLE)
def bstack1lll1l1l1l_opy_(page, status, reason=bstack1l1ll1l_opy_ (u"ࠫࠬᛧ")):
    try:
        if page is None:
            return
        bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
        if bstack111111111_opy_.bstack111ll1l1ll_opy_():
            return
        bstack1l1l1l11ll_opy_ = bstack11l1l1ll_opy_(bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᛨ"), bstack1l1ll1l_opy_ (u"࠭ࠧᛩ"), status, reason, bstack1l1ll1l_opy_ (u"ࠧࠨᛪ"), bstack1l1ll1l_opy_ (u"ࠨࠩ᛫"))
        page.evaluate(bstack1l1ll1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ᛬"), bstack1l1l1l11ll_opy_)
    except Exception as e:
        print(bstack1l1ll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣ᛭"), e)
def bstack11l1l1ll_opy_(type, name, status, reason, bstack1l1111l111_opy_, bstack11111l11_opy_):
    bstack1l111l1111_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᛮ"): type,
        bstack1l1ll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛯ"): {}
    }
    if type == bstack1l1ll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᛰ"):
        bstack1l111l1111_opy_[bstack1l1ll1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᛱ")][bstack1l1ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᛲ")] = bstack1l1111l111_opy_
        bstack1l111l1111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᛳ")][bstack1l1ll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᛴ")] = json.dumps(str(bstack11111l11_opy_))
    if type == bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᛵ"):
        bstack1l111l1111_opy_[bstack1l1ll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛶ")][bstack1l1ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᛷ")] = name
    if type == bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᛸ"):
        bstack1l111l1111_opy_[bstack1l1ll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᛹")][bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᛺")] = status
        if status == bstack1l1ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᛻") and str(reason) != bstack1l1ll1l_opy_ (u"ࠦࠧ᛼"):
            bstack1l111l1111_opy_[bstack1l1ll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᛽")][bstack1l1ll1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭᛾")] = json.dumps(str(reason))
    bstack1l11l11lll_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ᛿").format(json.dumps(bstack1l111l1111_opy_))
    return bstack1l11l11lll_opy_
def bstack111llll1l_opy_(url, config, logger, bstack111ll11l_opy_=False):
    hostname = bstack1l11lll1ll_opy_(url)
    is_private = bstack1l1l1lllll_opy_(hostname)
    try:
        if is_private or bstack111ll11l_opy_:
            file_path = bstack1llllllll1l_opy_(bstack1l1ll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᜀ"), bstack1l1ll1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᜁ"), logger)
            if os.environ.get(bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᜂ")) and eval(
                    os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᜃ"))):
                return
            if (bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᜄ") in config and not config[bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᜅ")]):
                os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᜆ")] = str(True)
                bstack1ll11l111l1_opy_ = {bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᜇ"): hostname}
                bstack1111111111_opy_(bstack1l1ll1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᜈ"), bstack1l1ll1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᜉ"), bstack1ll11l111l1_opy_, logger)
    except Exception as e:
        pass
def bstack11ll111l1l_opy_(caps, bstack1ll11l111ll_opy_):
    if bstack1l1ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᜊ") in caps:
        caps[bstack1l1ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜋ")][bstack1l1ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᜌ")] = True
        if bstack1ll11l111ll_opy_:
            caps[bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᜍ")][bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᜎ")] = bstack1ll11l111ll_opy_
    else:
        caps[bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᜏ")] = True
        if bstack1ll11l111ll_opy_:
            caps[bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᜐ")] = bstack1ll11l111ll_opy_
def bstack1ll11lllll1_opy_(bstack11l11llll1_opy_):
    bstack1ll11l1111l_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᜑ"), bstack1l1ll1l_opy_ (u"ࠬ࠭ᜒ"))
    if bstack1ll11l1111l_opy_ == bstack1l1ll1l_opy_ (u"࠭ࠧᜓ") or bstack1ll11l1111l_opy_ == bstack1l1ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ᜔"):
        threading.current_thread().testStatus = bstack11l11llll1_opy_
    else:
        if bstack11l11llll1_opy_ == bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᜕"):
            threading.current_thread().testStatus = bstack11l11llll1_opy_