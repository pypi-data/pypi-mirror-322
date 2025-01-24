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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack111l111l11_opy_ as bstack111l1l1l11_opy_, EVENTS
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1ll1ll1ll_opy_
from bstack_utils.helper import bstack1l1lll1l1_opy_, bstack11l111l1l1_opy_, bstack1lll1ll11_opy_, bstack111l1l11l1_opy_, \
  bstack1111lll11l_opy_, bstack1ll1ll11l1_opy_, get_host_info, bstack111l1l1ll1_opy_, bstack11ll1111ll_opy_, bstack11l111ll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11l1lll11_opy_ import get_logger
from bstack_utils.bstack11lll1l1ll_opy_ import bstack111l1ll11l_opy_
logger = get_logger(__name__)
bstack11lll1l1ll_opy_ = bstack111l1ll11l_opy_()
@bstack11l111ll1l_opy_(class_method=False)
def _111l1111l1_opy_(driver, bstack111ll1l1l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1ll1l_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩྞ"): caps.get(bstack1l1ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨྟ"), None),
        bstack1l1ll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧྠ"): bstack111ll1l1l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧྡ"), None),
        bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫྡྷ"): caps.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫྣ"), None),
        bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩྤ"): caps.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩྥ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ྦ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨྦྷ"), None) is None or os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩྨ")] == bstack1l1ll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥྩ"):
        return False
    return True
def bstack1111lll111_opy_(config):
  return config.get(bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ྪ"), False) or any([p.get(bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧྫ"), False) == True for p in config.get(bstack1l1ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫྫྷ"), [])])
def bstack1l1l1l11_opy_(config, bstack11lll11l1_opy_):
  try:
    if not bstack1lll1ll11_opy_(config):
      return False
    bstack111l1l111l_opy_ = config.get(bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩྭ"), False)
    if int(bstack11lll11l1_opy_) < len(config.get(bstack1l1ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ྮ"), [])) and config[bstack1l1ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧྯ")][bstack11lll11l1_opy_]:
      bstack1111llllll_opy_ = config[bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨྰ")][bstack11lll11l1_opy_].get(bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ྱ"), None)
    else:
      bstack1111llllll_opy_ = config.get(bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧྲ"), None)
    if bstack1111llllll_opy_ != None:
      bstack111l1l111l_opy_ = bstack1111llllll_opy_
    bstack111l1l11ll_opy_ = os.getenv(bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ླ")) is not None and len(os.getenv(bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧྴ"))) > 0 and os.getenv(bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨྵ")) != bstack1l1ll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩྶ")
    return bstack111l1l111l_opy_ and bstack111l1l11ll_opy_
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬྷ") + str(error))
  return False
def bstack11ll1l1ll1_opy_(test_tags):
  bstack1111lllll1_opy_ = os.getenv(bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧྸ"))
  if bstack1111lllll1_opy_ is None:
    return True
  bstack1111lllll1_opy_ = json.loads(bstack1111lllll1_opy_)
  try:
    include_tags = bstack1111lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬྐྵ")] if bstack1l1ll1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ྺ") in bstack1111lllll1_opy_ and isinstance(bstack1111lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧྻ")], list) else []
    exclude_tags = bstack1111lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨྼ")] if bstack1l1ll1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ྽") in bstack1111lllll1_opy_ and isinstance(bstack1111lllll1_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ྾")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ྿") + str(error))
  return False
def bstack111l11l111_opy_(config, bstack111l11ll11_opy_, bstack111l1ll111_opy_, bstack1111lll1l1_opy_):
  bstack111l1l1111_opy_ = bstack111l1l11l1_opy_(config)
  bstack111l11ll1l_opy_ = bstack1111lll11l_opy_(config)
  if bstack111l1l1111_opy_ is None or bstack111l11ll1l_opy_ is None:
    logger.error(bstack1l1ll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ࿀"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ࿁"), bstack1l1ll1l_opy_ (u"ࠩࡾࢁࠬ࿂")))
    data = {
        bstack1l1ll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࿃"): config[bstack1l1ll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ࿄")],
        bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿅"): config.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ࿆ࠩ"), os.path.basename(os.getcwd())),
        bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪ࿇"): bstack1l1lll1l1_opy_(),
        bstack1l1ll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭࿈"): config.get(bstack1l1ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ࿉"), bstack1l1ll1l_opy_ (u"ࠪࠫ࿊")),
        bstack1l1ll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ࿋"): {
            bstack1l1ll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ࿌"): bstack111l11ll11_opy_,
            bstack1l1ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ࿍"): bstack111l1ll111_opy_,
            bstack1l1ll1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ࿎"): __version__,
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ࿏"): bstack1l1ll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ࿐"),
            bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ࿑"): bstack1l1ll1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭࿒"),
            bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ࿓"): bstack1111lll1l1_opy_
        },
        bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ࿔"): settings,
        bstack1l1ll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨ࿕"): bstack111l1l1ll1_opy_(),
        bstack1l1ll1l_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨ࿖"): bstack1ll1ll11l1_opy_(),
        bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫ࿗"): get_host_info(),
        bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ࿘"): bstack1lll1ll11_opy_(config)
    }
    headers = {
        bstack1l1ll1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ࿙"): bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ࿚"),
    }
    config = {
        bstack1l1ll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ࿛"): (bstack111l1l1111_opy_, bstack111l11ll1l_opy_),
        bstack1l1ll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ࿜"): headers
    }
    response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭࿝"), bstack111l1l1l11_opy_ + bstack1l1ll1l_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩ࿞"), data, config)
    bstack111l111111_opy_ = response.json()
    if bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ࿟")]:
      parsed = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ࿠"), bstack1l1ll1l_opy_ (u"ࠬࢁࡽࠨ࿡")))
      parsed[bstack1l1ll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ࿢")] = bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬ࿣")][bstack1l1ll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ࿤")]
      os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ࿥")] = json.dumps(parsed)
      bstack1ll1ll1ll_opy_.bstack111l1111ll_opy_(bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨ࿦")][bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ࿧")])
      bstack1ll1ll1ll_opy_.bstack111l111l1l_opy_(bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪ࿨")][bstack1l1ll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ࿩")])
      bstack1ll1ll1ll_opy_.store()
      return bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬ࿪")][bstack1l1ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭࿫")], bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡧࡥࡹࡧࠧ࿬")][bstack1l1ll1l_opy_ (u"ࠪ࡭ࡩ࠭࿭")]
    else:
      logger.error(bstack1l1ll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬ࿮") + bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿯")])
      if bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿰")] == bstack1l1ll1l_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩ࿱"):
        for bstack1111llll1l_opy_ in bstack111l111111_opy_[bstack1l1ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ࿲")]:
          logger.error(bstack1111llll1l_opy_[bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿳")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1ll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦ࿴") +  str(error))
    return None, None
def bstack111l11lll1_opy_():
  if os.getenv(bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ࿵")) is None:
    return {
        bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿶"): bstack1l1ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ࿷"),
        bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿸"): bstack1l1ll1l_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧ࿹")
    }
  data = {bstack1l1ll1l_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪ࿺"): bstack1l1lll1l1_opy_()}
  headers = {
      bstack1l1ll1l_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ࿻"): bstack1l1ll1l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬ࿼") + os.getenv(bstack1l1ll1l_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥ࿽")),
      bstack1l1ll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ࿾"): bstack1l1ll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ࿿")
  }
  response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"ࠨࡒࡘࡘࠬက"), bstack111l1l1l11_opy_ + bstack1l1ll1l_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫခ"), data, { bstack1l1ll1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫဂ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1ll1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧဃ") + bstack11l111l1l1_opy_().isoformat() + bstack1l1ll1l_opy_ (u"ࠬࡠࠧင"))
      return {bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭စ"): bstack1l1ll1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨဆ"), bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဇ"): bstack1l1ll1l_opy_ (u"ࠩࠪဈ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1ll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨဉ") + str(error))
    return {
        bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫည"): bstack1l1ll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫဋ"),
        bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဌ"): str(error)
    }
def bstack1ll1l1l1ll_opy_(caps, options, desired_capabilities={}):
  try:
    bstack111l11llll_opy_ = caps.get(bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨဍ"), {}).get(bstack1l1ll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬဎ"), caps.get(bstack1l1ll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩဏ"), bstack1l1ll1l_opy_ (u"ࠪࠫတ")))
    if bstack111l11llll_opy_:
      logger.warn(bstack1l1ll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣထ"))
      return False
    if options:
      bstack111l111lll_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack111l111lll_opy_ = desired_capabilities
    else:
      bstack111l111lll_opy_ = {}
    browser = caps.get(bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪဒ"), bstack1l1ll1l_opy_ (u"࠭ࠧဓ")).lower() or bstack111l111lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬန"), bstack1l1ll1l_opy_ (u"ࠨࠩပ")).lower()
    if browser != bstack1l1ll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩဖ"):
      logger.warn(bstack1l1ll1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨဗ"))
      return False
    browser_version = caps.get(bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬဘ")) or caps.get(bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧမ")) or bstack111l111lll_opy_.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧယ")) or bstack111l111lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨရ"), {}).get(bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩလ")) or bstack111l111lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪဝ"), {}).get(bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬသ"))
    if browser_version and browser_version != bstack1l1ll1l_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫဟ") and int(browser_version.split(bstack1l1ll1l_opy_ (u"ࠬ࠴ࠧဠ"))[0]) <= 98:
      logger.warn(bstack1l1ll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ࠦအ"))
      return False
    if not options:
      bstack111l1ll1l1_opy_ = caps.get(bstack1l1ll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬဢ")) or bstack111l111lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ဣ"), {})
      if bstack1l1ll1l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ဤ") in bstack111l1ll1l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨဥ"), []):
        logger.warn(bstack1l1ll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨဦ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢဧ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack111l11l1l1_opy_ = config.get(bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ဨ"), {})
    bstack111l11l1l1_opy_[bstack1l1ll1l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪဩ")] = os.getenv(bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ဪ"))
    bstack111l11l1ll_opy_ = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪါ"), bstack1l1ll1l_opy_ (u"ࠪࡿࢂ࠭ာ"))).get(bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬိ"))
    caps[bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬီ")] = True
    if bstack1l1ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧု") in caps:
      caps[bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨူ")][bstack1l1ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨေ")] = bstack111l11l1l1_opy_
      caps[bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪဲ")][bstack1l1ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪဳ")][bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬဴ")] = bstack111l11l1ll_opy_
    else:
      caps[bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫဵ")] = bstack111l11l1l1_opy_
      caps[bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬံ")][bstack1l1ll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ့")] = bstack111l11l1ll_opy_
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤး") +  str(error))
def bstack1l111l11ll_opy_(driver, bstack1111llll11_opy_):
  try:
    setattr(driver, bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯္ࠩ"), True)
    session = driver.session_id
    if session:
      bstack111l1l1lll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111l1l1lll_opy_ = False
      bstack111l1l1lll_opy_ = url.scheme in [bstack1l1ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ်ࠣ"), bstack1l1ll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥျ")]
      if bstack111l1l1lll_opy_:
        if bstack1111llll11_opy_:
          logger.info(bstack1l1ll1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧြ"))
      return bstack1111llll11_opy_
  except Exception as e:
    logger.error(bstack1l1ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤွ") + str(e))
    return False
def bstack1ll1lll111_opy_(driver, name, path):
  try:
    bstack111l1l1l1l_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧှ"): threading.current_thread().current_test_uuid,
        bstack1l1ll1l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ဿ"): os.environ.get(bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ၀"), bstack1l1ll1l_opy_ (u"ࠪࠫ၁")),
        bstack1l1ll1l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨ၂"): os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭၃"), bstack1l1ll1l_opy_ (u"࠭ࠧ၄"))
    }
    bstack111l11111l_opy_ = bstack11lll1l1ll_opy_.bstack1111ll1lll_opy_(EVENTS.bstack11l11llll_opy_.value)
    bstack11lll1l1ll_opy_.mark(bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ၅"))
    logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ၆"))
    try:
      logger.debug(driver.execute_async_script(bstack1ll1ll1ll_opy_.perform_scan, {bstack1l1ll1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ၇"): name}))
      bstack11lll1l1ll_opy_.end(bstack111l11111l_opy_, bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ၈"), bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ၉"), True, None)
    except Exception as error:
      bstack11lll1l1ll_opy_.end(bstack111l11111l_opy_, bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ၊"), bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ။"), False, str(error))
    bstack111l11111l_opy_ = bstack11lll1l1ll_opy_.bstack1111ll1lll_opy_(EVENTS.bstack1111lll1ll_opy_.value)
    bstack11lll1l1ll_opy_.mark(bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ၌"))
    try:
      logger.debug(driver.execute_async_script(bstack1ll1ll1ll_opy_.bstack111l111ll1_opy_, bstack111l1l1l1l_opy_))
      bstack11lll1l1ll_opy_.end(bstack111l11111l_opy_, bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ၍"), bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ၎"),True, None)
    except Exception as error:
      bstack11lll1l1ll_opy_.end(bstack111l11111l_opy_, bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ၏"), bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤၐ"),False, str(error))
    logger.info(bstack1l1ll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣၑ"))
  except Exception as bstack111l11l11l_opy_:
    logger.error(bstack1l1ll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣၒ") + str(path) + bstack1l1ll1l_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤၓ") + str(bstack111l11l11l_opy_))