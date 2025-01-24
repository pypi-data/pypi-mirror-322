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
import re
from bstack_utils.bstack11lll1ll1l_opy_ import bstack1ll11lllll1_opy_
def bstack1ll1l11111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᚭ")):
        return bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᚮ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᚯ")):
        return bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᚰ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᚱ")):
        return bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᚲ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᚳ")):
        return bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᚴ")
def bstack1ll11lll111_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᚵ"), fixture_name))
def bstack1ll11lll1ll_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᚶ"), fixture_name))
def bstack1ll11lll1l1_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᚷ"), fixture_name))
def bstack1ll11llll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᚸ")):
        return bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᚹ"), bstack1l1ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᚺ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᚻ")):
        return bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᚼ"), bstack1l1ll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᚽ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᚾ")):
        return bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᚿ"), bstack1l1ll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᛀ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᛁ")):
        return bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᛂ"), bstack1l1ll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᛃ")
    return None, None
def bstack1ll11lll11l_opy_(hook_name):
    if hook_name in [bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᛄ"), bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᛅ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll11llllll_opy_(hook_name):
    if hook_name in [bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᛆ"), bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᛇ")]:
        return bstack1l1ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᛈ")
    elif hook_name in [bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᛉ"), bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᛊ")]:
        return bstack1l1ll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᛋ")
    elif hook_name in [bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᛌ"), bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᛍ")]:
        return bstack1l1ll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᛎ")
    elif hook_name in [bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᛏ"), bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᛐ")]:
        return bstack1l1ll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᛑ")
    return hook_name
def bstack1ll11ll1ll1_opy_(node, scenario):
    if hasattr(node, bstack1l1ll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᛒ")):
        parts = node.nodeid.rsplit(bstack1l1ll1l_opy_ (u"ࠧࡡࠢᛓ"))
        params = parts[-1]
        return bstack1l1ll1l_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᛔ").format(scenario.name, params)
    return scenario.name
def bstack1ll11ll1l1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1ll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᛕ")):
            examples = list(node.callspec.params[bstack1l1ll1l_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᛖ")].values())
        return examples
    except:
        return []
def bstack1ll1l1111l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll11llll1l_opy_(report):
    try:
        status = bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᛗ")
        if report.passed or (report.failed and hasattr(report, bstack1l1ll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᛘ"))):
            status = bstack1l1ll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᛙ")
        elif report.skipped:
            status = bstack1l1ll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᛚ")
        bstack1ll11lllll1_opy_(status)
    except:
        pass
def bstack111l111ll_opy_(status):
    try:
        bstack1ll11ll1lll_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᛛ")
        if status == bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᛜ"):
            bstack1ll11ll1lll_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᛝ")
        elif status == bstack1l1ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᛞ"):
            bstack1ll11ll1lll_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᛟ")
        bstack1ll11lllll1_opy_(bstack1ll11ll1lll_opy_)
    except:
        pass
def bstack1ll1l111111_opy_(item=None, report=None, summary=None, extra=None):
    return