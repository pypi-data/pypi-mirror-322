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
import datetime
import threading
from bstack_utils.helper import bstack111l1l1ll1_opy_, bstack1ll1ll11l1_opy_, get_host_info, bstack1lll1ll1lll_opy_, \
 bstack1lll1ll11_opy_, bstack1ll111111l_opy_, bstack11l111ll1l_opy_, bstack1llll1l11ll_opy_, bstack1l1lll1l1_opy_
import bstack_utils.bstack111l1lllll_opy_ as bstack11l11ll1_opy_
from bstack_utils.bstack11l1lll111_opy_ import bstack11llll1111_opy_
from bstack_utils.percy import bstack1ll11l1l1_opy_
from bstack_utils.config import Config
bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll11l1l1_opy_()
@bstack11l111ll1l_opy_(class_method=False)
def bstack1l1lllllll1_opy_(bs_config, bstack1lllll1ll1_opy_):
  try:
    data = {
        bstack1l1ll1l_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧᡏ"): bstack1l1ll1l_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ᡐ"),
        bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨᡑ"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᡒ"), bstack1l1ll1l_opy_ (u"ࠫࠬᡓ")),
        bstack1l1ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᡔ"): bs_config.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᡕ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᡖ"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᡗ")),
        bstack1l1ll1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᡘ"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᡙ"), bstack1l1ll1l_opy_ (u"ࠫࠬᡚ")),
        bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᡛ"): bstack1l1lll1l1_opy_(),
        bstack1l1ll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫᡜ"): bstack1lll1ll1lll_opy_(bs_config),
        bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪᡝ"): get_host_info(),
        bstack1l1ll1l_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩᡞ"): bstack1ll1ll11l1_opy_(),
        bstack1l1ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᡟ"): os.environ.get(bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᡠ")),
        bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩᡡ"): os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪᡢ"), False),
        bstack1l1ll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨᡣ"): bstack111l1l1ll1_opy_(),
        bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᡤ"): bstack1l1lll1ll11_opy_(),
        bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬᡥ"): bstack1l1lll1l111_opy_(bstack1lllll1ll1_opy_),
        bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᡦ"): bstack1lll11ll_opy_(bs_config, bstack1lllll1ll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᡧ"), bstack1l1ll1l_opy_ (u"ࠫࠬᡨ"))),
        bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᡩ"): bstack1lll1ll11_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᡪ").format(str(error)))
    return None
def bstack1l1lll1l111_opy_(framework):
  return {
    bstack1l1ll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᡫ"): framework.get(bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᡬ"), bstack1l1ll1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᡭ")),
    bstack1l1ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᡮ"): framework.get(bstack1l1ll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᡯ")),
    bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᡰ"): framework.get(bstack1l1ll1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᡱ")),
    bstack1l1ll1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᡲ"): bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᡳ"),
    bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᡴ"): framework.get(bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᡵ"))
  }
def bstack1lll11ll_opy_(bs_config, framework):
  bstack1llll1llll_opy_ = False
  bstack11lllll11_opy_ = False
  bstack1l1lll1ll1l_opy_ = False
  if bstack1l1ll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᡶ") in bs_config:
    bstack1l1lll1ll1l_opy_ = True
  elif bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡱࠩᡷ") in bs_config:
    bstack1llll1llll_opy_ = True
  else:
    bstack11lllll11_opy_ = True
  bstack1l11ll1l11_opy_ = {
    bstack1l1ll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᡸ"): bstack11llll1111_opy_.bstack1l1lll11l1l_opy_(bs_config, framework),
    bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᡹"): bstack11l11ll1_opy_.bstack1111lll111_opy_(bs_config),
    bstack1l1ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᡺"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᡻"), False),
    bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᡼"): bstack11lllll11_opy_,
    bstack1l1ll1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ᡽"): bstack1llll1llll_opy_,
    bstack1l1ll1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ᡾"): bstack1l1lll1ll1l_opy_
  }
  return bstack1l11ll1l11_opy_
@bstack11l111ll1l_opy_(class_method=False)
def bstack1l1lll1ll11_opy_():
  try:
    bstack1l1lll1lll1_opy_ = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᡿"), bstack1l1ll1l_opy_ (u"ࠧࡼࡿࠪᢀ")))
    return {
        bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᢁ"): bstack1l1lll1lll1_opy_
    }
  except Exception as error:
    logger.error(bstack1l1ll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣᢂ").format(str(error)))
    return {}
def bstack1ll1111l1ll_opy_(array, bstack1l1lll11lll_opy_, bstack1l1lll1l1ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1l1lll11lll_opy_]
    result[key] = o[bstack1l1lll1l1ll_opy_]
  return result
def bstack1ll1111l1l1_opy_(bstack1ll1l11ll1_opy_=bstack1l1ll1l_opy_ (u"ࠪࠫᢃ")):
  bstack1l1lll11l11_opy_ = bstack11l11ll1_opy_.on()
  bstack1l1lll1l1l1_opy_ = bstack11llll1111_opy_.on()
  bstack1l1lll11ll1_opy_ = percy.bstack1l1ll1l1_opy_()
  if bstack1l1lll11ll1_opy_ and not bstack1l1lll1l1l1_opy_ and not bstack1l1lll11l11_opy_:
    return bstack1ll1l11ll1_opy_ not in [bstack1l1ll1l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᢄ"), bstack1l1ll1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᢅ")]
  elif bstack1l1lll11l11_opy_ and not bstack1l1lll1l1l1_opy_:
    return bstack1ll1l11ll1_opy_ not in [bstack1l1ll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᢆ"), bstack1l1ll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᢇ"), bstack1l1ll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᢈ")]
  return bstack1l1lll11l11_opy_ or bstack1l1lll1l1l1_opy_ or bstack1l1lll11ll1_opy_
@bstack11l111ll1l_opy_(class_method=False)
def bstack1l1lllll11l_opy_(bstack1ll1l11ll1_opy_, test=None):
  bstack1l1lll1l11l_opy_ = bstack11l11ll1_opy_.on()
  if not bstack1l1lll1l11l_opy_ or bstack1ll1l11ll1_opy_ not in [bstack1l1ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᢉ")] or test == None:
    return None
  return {
    bstack1l1ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᢊ"): bstack1l1lll1l11l_opy_ and bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᢋ"), None) == True and bstack11l11ll1_opy_.bstack11ll1l1ll1_opy_(test[bstack1l1ll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᢌ")])
  }