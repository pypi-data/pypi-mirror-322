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
import re
from enum import Enum
bstack1l1l1ll111_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬႀ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࠨႁ"),
  bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨႂ"): bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡱࡥࡺࠩႃ"),
  bstack1l1ll1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪႄ"): bstack1l1ll1l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬႅ"),
  bstack1l1ll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩႆ"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪႇ"),
  bstack1l1ll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩႈ"): bstack1l1ll1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹ࠭ႉ"),
  bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩႊ"): bstack1l1ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭ႋ"),
  bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ႌ"): bstack1l1ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ႍࠧ"),
  bstack1l1ll1l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩႎ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨࠩႏ"),
  bstack1l1ll1l_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪ႐"): bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡵࡲࡰࡪ࠭႑"),
  bstack1l1ll1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬ႒"): bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬ႓"),
  bstack1l1ll1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭႔"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭႕"),
  bstack1l1ll1l_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪ႖"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡻ࡯ࡤࡦࡱࠪ႗"),
  bstack1l1ll1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ႘"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ႙"),
  bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨႚ"): bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨႛ"),
  bstack1l1ll1l_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨႜ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨႝ"),
  bstack1l1ll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ႞"): bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ႟"),
  bstack1l1ll1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩႠ"): bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪႡ"),
  bstack1l1ll1l_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨႢ"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨႣ"),
  bstack1l1ll1l_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩႤ"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩႥ"),
  bstack1l1ll1l_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭Ⴆ"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭Ⴇ"),
  bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪႨ"): bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡲࡩࡑࡥࡺࡵࠪႩ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬႪ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬႫ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫႬ"): bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡶࠫႭ"),
  bstack1l1ll1l_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨႮ"): bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡨࡦࡥࡨ࡮ࡥࠨႯ"),
  bstack1l1ll1l_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪႰ"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪႱ"),
  bstack1l1ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧႲ"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧႳ"),
  bstack1l1ll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪႴ"): bstack1l1ll1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧႵ"),
  bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬႶ"): bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧႷ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪႸ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫႹ"),
  bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬႺ"): bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬႻ"),
  bstack1l1ll1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨႼ"): bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨႽ"),
  bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨႾ"): bstack1l1ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫႿ"),
  bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭Ⴠ"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭Ⴡ"),
  bstack1l1ll1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭Ⴢ"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡰࡷࡵࡧࡪ࠭Ⴣ"),
  bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪჄ"): bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪჅ"),
  bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬ჆"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡏࡣࡰࡩࠬჇ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨ჈"): bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨ჉"),
  bstack1l1ll1l_opy_ (u"ࠧࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫ჊"): bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴ࡫ࡰࡓࡵࡺࡩࡰࡰࡶࠫ჋"),
  bstack1l1ll1l_opy_ (u"ࠩࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧ჌"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡴࡱࡵࡡࡥࡏࡨࡨ࡮ࡧࠧჍ"),
  bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ჎"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ჏"),
  bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨა"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨბ")
}
bstack1111l11111_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠨࡱࡶࠫგ"),
  bstack1l1ll1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬდ"),
  bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬე"),
  bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩვ"),
  bstack1l1ll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩზ"),
  bstack1l1ll1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪთ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧი"),
]
bstack1ll11111l_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪკ"): [bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪლ"), bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡏࡃࡐࡉࠬმ")],
  bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧნ"): bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨო"),
  bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩპ"): bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠪჟ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭რ"): bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠧს"),
  bstack1l1ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬტ"): bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭უ"),
  bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬფ"): bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒࡓࡠࡒࡈࡖࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧქ"),
  bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫღ"): bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭ყ"),
  bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭შ"): bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧჩ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡶࡰࠨც"): [bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡖࡐࡠࡋࡇࠫძ"), bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࠩწ")],
  bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩჭ"): bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡑࡕࡇࡍࡇ࡙ࡉࡑ࠭ხ"),
  bstack1l1ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ჯ"): bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ჰ"),
  bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨჱ"): bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡒࡆࡘࡋࡒࡗࡃࡅࡍࡑࡏࡔ࡚ࠩჲ"),
  bstack1l1ll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪჳ"): bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡖࡔࡅࡓࡘࡉࡁࡍࡇࠪჴ")
}
bstack1l11111l11_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪჵ"): [bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫჶ"), bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫჷ")],
  bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧჸ"): [bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨჹ"), bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨჺ")],
  bstack1l1ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ჻"): bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪჼ"),
  bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧჽ"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧჾ"),
  bstack1l1ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ჿ"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᄀ"),
  bstack1l1ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᄁ"): [bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪᄂ"), bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᄃ")],
  bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᄄ"): bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᄅ"),
  bstack1l1ll1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᄆ"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᄇ"),
  bstack1l1ll1l_opy_ (u"࠭ࡡࡱࡲࠪᄈ"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪᄉ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᄊ"): bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᄋ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄌ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄍ")
}
bstack1ll1l1l1l_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᄎ"): bstack1l1ll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᄏ"),
  bstack1l1ll1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᄐ"): [bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᄑ"), bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᄒ")],
  bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᄓ"): bstack1l1ll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᄔ"),
  bstack1l1ll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᄕ"): bstack1l1ll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᄖ"),
  bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᄗ"): [bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᄘ"), bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᄙ")],
  bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᄚ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᄛ"),
  bstack1l1ll1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩᄜ"): bstack1l1ll1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫᄝ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᄞ"): [bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᄟ"), bstack1l1ll1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᄠ")],
  bstack1l1ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᄡ"): [bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬᄢ"), bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬᄣ")]
}
bstack1111lll1_opy_ = [
  bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᄤ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᄥ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᄦ"),
  bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩᄧ"),
  bstack1l1ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᄨ"),
  bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩᄩ"),
  bstack1l1ll1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᄪ"),
  bstack1l1ll1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᄫ"),
  bstack1l1ll1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᄬ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᄭ"),
  bstack1l1ll1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᄮ"),
  bstack1l1ll1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᄯ"),
]
bstack111l1l11l_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᄰ"),
  bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᄱ"),
  bstack1l1ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᄲ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᄳ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄴ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᄵ"),
  bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᄶ"),
  bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᄷ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᄸ"),
  bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᄹ"),
  bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᄺ"),
  bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᄻ"),
  bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬᄼ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄽ"),
  bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄾ"),
  bstack1l1ll1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩᄿ"),
  bstack1l1ll1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬᅀ"),
  bstack1l1ll1l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭ᅁ"),
  bstack1l1ll1l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧᅂ"),
  bstack1l1ll1l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨᅃ"),
  bstack1l1ll1l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩᅄ"),
  bstack1l1ll1l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪᅅ"),
  bstack1l1ll1l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫᅆ"),
  bstack1l1ll1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬᅇ"),
  bstack1l1ll1l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭ᅈ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᅉ"),
  bstack1l1ll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᅊ"),
  bstack1l1ll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᅋ"),
  bstack1l1ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᅌ"),
  bstack1l1ll1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᅍ"),
  bstack1l1ll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᅎ")
]
bstack1111l11l11_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬᅏ"),
  bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᅐ"),
  bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᅑ"),
  bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᅒ"),
  bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪᅓ"),
  bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᅔ"),
  bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨᅕ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᅖ"),
  bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᅗ"),
  bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᅘ"),
  bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᅙ"),
  bstack1l1ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᅚ"),
  bstack1l1ll1l_opy_ (u"ࠬࡵࡳࠨᅛ"),
  bstack1l1ll1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᅜ"),
  bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᅝ"),
  bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪᅞ"),
  bstack1l1ll1l_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩᅟ"),
  bstack1l1ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬᅠ"),
  bstack1l1ll1l_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬᅡ"),
  bstack1l1ll1l_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩᅢ"),
  bstack1l1ll1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᅣ"),
  bstack1l1ll1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᅤ"),
  bstack1l1ll1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧᅥ"),
  bstack1l1ll1l_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᅦ"),
  bstack1l1ll1l_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫᅧ"),
  bstack1l1ll1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᅨ"),
  bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᅩ"),
  bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧᅪ"),
  bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫᅫ"),
  bstack1l1ll1l_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬᅬ"),
  bstack1l1ll1l_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫᅭ"),
  bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᅮ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫᅯ"),
  bstack1l1ll1l_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫᅰ"),
  bstack1l1ll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᅱ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᅲ"),
  bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲࠬᅳ"),
  bstack1l1ll1l_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩࠪᅴ"),
  bstack1l1ll1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩᅵ"),
  bstack1l1ll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨᅶ"),
  bstack1l1ll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪࠧᅷ"),
  bstack1l1ll1l_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨᅸ"),
  bstack1l1ll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭ᅹ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭ᅺ"),
  bstack1l1ll1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᅻ"),
  bstack1l1ll1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨᅼ"),
  bstack1l1ll1l_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩᅽ"),
  bstack1l1ll1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᅾ"),
  bstack1l1ll1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪᅿ"),
  bstack1l1ll1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩᆀ"),
  bstack1l1ll1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩᆁ"),
  bstack1l1ll1l_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪᆂ"),
  bstack1l1ll1l_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫᆃ"),
  bstack1l1ll1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪᆄ"),
  bstack1l1ll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪᆅ"),
  bstack1l1ll1l_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ᆆ"),
  bstack1l1ll1l_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࠩᆇ"),
  bstack1l1ll1l_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ᆈ"),
  bstack1l1ll1l_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧᆉ"),
  bstack1l1ll1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫᆊ"),
  bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫᆋ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ᆌ"),
  bstack1l1ll1l_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷ࠭ᆍ"),
  bstack1l1ll1l_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧᆎ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧᆏ"),
  bstack1l1ll1l_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩᆐ"),
  bstack1l1ll1l_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫᆑ"),
  bstack1l1ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧᆒ"),
  bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯ࠩᆓ"),
  bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᆔ"),
  bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࠪᆕ"),
  bstack1l1ll1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࠬᆖ"),
  bstack1l1ll1l_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩᆗ"),
  bstack1l1ll1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫᆘ"),
  bstack1l1ll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᆙ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡯ࡥࠨᆚ"),
  bstack1l1ll1l_opy_ (u"࠭ࡥࡥࡩࡨࠫᆛ"),
  bstack1l1ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᆜ"),
  bstack1l1ll1l_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࠧᆝ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫᆞ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫᆟ"),
  bstack1l1ll1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪᆠ"),
  bstack1l1ll1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨᆡ"),
  bstack1l1ll1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩᆢ"),
  bstack1l1ll1l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᆣ"),
  bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨᆤ"),
  bstack1l1ll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᆥ"),
  bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᆦ"),
  bstack1l1ll1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬᆧ"),
  bstack1l1ll1l_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡎࡵࡳࡅࡧࡹ࡭ࡨ࡫ࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᆨ"),
  bstack1l1ll1l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡵࡥ࡫ࡲࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ᆩ"),
  bstack1l1ll1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡱࡲ࡯ࡩࡕࡧࡹࠨᆪ"),
  bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᆫ"),
  bstack1l1ll1l_opy_ (u"ࠩࡺࡨ࡮ࡵࡓࡦࡴࡹ࡭ࡨ࡫ࠧᆬ"),
  bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᆭ"),
  bstack1l1ll1l_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸࡈࡸ࡯ࡴࡵࡖ࡭ࡹ࡫ࡔࡳࡣࡦ࡯࡮ࡴࡧࠨᆮ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡮ࡩࡨࡪࡆࡳࡳࡺࡲࡢࡵࡷࠫᆯ"),
  bstack1l1ll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡖࡲࡦࡨࡨࡶࡪࡴࡣࡦࡵࠪᆰ"),
  bstack1l1ll1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪᆱ"),
  bstack1l1ll1l_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬᆲ"),
  bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧᆳ"),
  bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬᆴ"),
  bstack1l1ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᆵ"),
  bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᆶ"),
  bstack1l1ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᆷ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᆸ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫᆹ"),
  bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨᆺ"),
  bstack1l1ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᆻ"),
  bstack1l1ll1l_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧᆼ")
]
bstack11l1ll11_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠬࡼࠧᆽ"): bstack1l1ll1l_opy_ (u"࠭ࡶࠨᆾ"),
  bstack1l1ll1l_opy_ (u"ࠧࡧࠩᆿ"): bstack1l1ll1l_opy_ (u"ࠨࡨࠪᇀ"),
  bstack1l1ll1l_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨᇁ"): bstack1l1ll1l_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᇂ"),
  bstack1l1ll1l_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪᇃ"): bstack1l1ll1l_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫᇄ"),
  bstack1l1ll1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪᇅ"): bstack1l1ll1l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᇆ"),
  bstack1l1ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᇇ"): bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬᇈ"),
  bstack1l1ll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᇉ"): bstack1l1ll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᇊ"),
  bstack1l1ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᇋ"): bstack1l1ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᇌ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᇍ"): bstack1l1ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᇎ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪᇏ"): bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫᇐ"),
  bstack1l1ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬᇑ"): bstack1l1ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᇒ"),
  bstack1l1ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᇓ"): bstack1l1ll1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᇔ"),
  bstack1l1ll1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᇕ"): bstack1l1ll1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫᇖ"),
  bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᇗ"): bstack1l1ll1l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᇘ"),
  bstack1l1ll1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᇙ"): bstack1l1ll1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨᇚ"),
  bstack1l1ll1l_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫᇛ"): bstack1l1ll1l_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᇜ"),
  bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪᇝ"): bstack1l1ll1l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᇞ"),
  bstack1l1ll1l_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᇟ"): bstack1l1ll1l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᇠ"),
  bstack1l1ll1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᇡ"): bstack1l1ll1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᇢ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩᇣ"): bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪᇤ"),
  bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᇥ"): bstack1l1ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᇦ"),
  bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࠲ࡸࡥࡱࡧࡤࡸࡪࡸࠧᇧ"): bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡱࡧࡤࡸࡪࡸࠧᇨ")
}
bstack1111l111ll_opy_ = bstack1l1ll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩ࡬ࡸ࡭ࡻࡢ࠯ࡥࡲࡱ࠴ࡶࡥࡳࡥࡼ࠳ࡨࡲࡩ࠰ࡴࡨࡰࡪࡧࡳࡦࡵ࠲ࡰࡦࡺࡥࡴࡶ࠲ࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᇩ")
bstack111111llll_opy_ = bstack1l1ll1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠰ࡪࡨࡥࡱࡺࡨࡤࡪࡨࡧࡰࠨᇪ")
bstack11l1ll111_opy_ = bstack1l1ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡩࡩࡹ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡷࡪࡴࡤࡠࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧᇫ")
bstack1111l1l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡼࡪ࠯ࡩࡷࡥࠫᇬ")
bstack1l1lll1111_opy_ = bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠧᇭ")
bstack1lll11ll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠩᇮ")
bstack11111lll11_opy_ = {
  bstack1l1ll1l_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨᇯ"): 50,
  bstack1l1ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᇰ"): 40,
  bstack1l1ll1l_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᇱ"): 30,
  bstack1l1ll1l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᇲ"): 20,
  bstack1l1ll1l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᇳ"): 10
}
bstack1l1lll11_opy_ = bstack11111lll11_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᇴ")]
bstack1l1111l1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᇵ")
bstack1lll1l1ll1_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᇶ")
bstack1l11l11l_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᇷ")
bstack1lll11l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᇸ")
bstack1l1ll1lll_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧᇹ")
bstack11111lllll_opy_ = [bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᇺ"), bstack1l1ll1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫᇻ")]
bstack1111l1111l_opy_ = [bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᇼ"), bstack1l1ll1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨᇽ")]
bstack1l1lll11ll_opy_ = re.compile(bstack1l1ll1l_opy_ (u"ࠧ࡟࡝࡟ࡠࡼ࠳࡝ࠬ࠼࠱࠮ࠩ࠭ᇾ"))
bstack1l1l1111_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩᇿ"),
  bstack1l1ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫሀ"),
  bstack1l1ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧሁ"),
  bstack1l1ll1l_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨሂ"),
  bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡱࠩሃ"),
  bstack1l1ll1l_opy_ (u"࠭ࡵࡥ࡫ࡧࠫሄ"),
  bstack1l1ll1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩህ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨሆ"),
  bstack1l1ll1l_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧሇ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨለ"),
  bstack1l1ll1l_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬሉ"), bstack1l1ll1l_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨሊ"),
  bstack1l1ll1l_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩላ"),
  bstack1l1ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭ሌ"),
  bstack1l1ll1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬል"),
  bstack1l1ll1l_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬሎ"),
  bstack1l1ll1l_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫሏ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩሐ"), bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩሑ"), bstack1l1ll1l_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨሒ"), bstack1l1ll1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨሓ"), bstack1l1ll1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪሔ"),
  bstack1l1ll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧሕ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧሖ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭ሗ"), bstack1l1ll1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩመ"),
  bstack1l1ll1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫሙ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨሚ"),
  bstack1l1ll1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧማ"),
  bstack1l1ll1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪሜ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨም"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡼࡤࠨሞ"), bstack1l1ll1l_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨሟ"), bstack1l1ll1l_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨሠ"), bstack1l1ll1l_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨሡ"),
  bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ሢ"), bstack1l1ll1l_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨሣ"), bstack1l1ll1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭ሤ"),
  bstack1l1ll1l_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭ሥ"), bstack1l1ll1l_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪሦ"),
  bstack1l1ll1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨሧ"), bstack1l1ll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪረ"), bstack1l1ll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭ሩ"), bstack1l1ll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫሪ"), bstack1l1ll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧራ"),
  bstack1l1ll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧሬ"), bstack1l1ll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩር"),
  bstack1l1ll1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨሮ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬሯ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧሰ"), bstack1l1ll1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪሱ"), bstack1l1ll1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨሲ"), bstack1l1ll1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧሳ"),
  bstack1l1ll1l_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪሴ"),
  bstack1l1ll1l_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨስ"), bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧሶ"),
  bstack1l1ll1l_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨሷ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫሸ"),
  bstack1l1ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬሹ"),
  bstack1l1ll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫሺ"),
  bstack1l1ll1l_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭ሻ"),
  bstack1l1ll1l_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬሼ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨሽ"),
  bstack1l1ll1l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧሾ"),
  bstack1l1ll1l_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ሿ"),
  bstack1l1ll1l_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧቀ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬቁ"),
  bstack1l1ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫቂ"),
  bstack1l1ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪቃ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧቄ"),
  bstack1l1ll1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ቅ"),
  bstack1l1ll1l_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭ቆ"),
  bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪቇ"),
  bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨቈ"), bstack1l1ll1l_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩ቉"), bstack1l1ll1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩቊ"),
  bstack1l1ll1l_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫቋ"),
  bstack1l1ll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬቌ"),
  bstack1l1ll1l_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫቍ"),
  bstack1l1ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬ቎"),
  bstack1l1ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ቏"),
  bstack1l1ll1l_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩቐ"),
  bstack1l1ll1l_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩቑ"), bstack1l1ll1l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ቒ"), bstack1l1ll1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫቓ"),
  bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩቔ"),
  bstack1l1ll1l_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫቕ"),
  bstack1l1ll1l_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ቖ"),
  bstack1l1ll1l_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ቗"),
  bstack1l1ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩቘ"), bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭቙"),
  bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫቚ"), bstack1l1ll1l_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ቛ"),
  bstack1l1ll1l_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪቜ"),
  bstack1l1ll1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪቝ"),
  bstack1l1ll1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨ቞"), bstack1l1ll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪ቟"), bstack1l1ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫበ"), bstack1l1ll1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨቡ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩቢ"),
  bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫባ"),
  bstack1l1ll1l_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧቤ"),
  bstack1l1ll1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬብ"),
  bstack1l1ll1l_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪቦ"),
  bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩቧ"),
  bstack1l1ll1l_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩቨ"), bstack1l1ll1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪቩ"),
  bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭ቪ"),
  bstack1l1ll1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫቫ"),
  bstack1l1ll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ቬ"),
  bstack1l1ll1l_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭ቭ"),
  bstack1l1ll1l_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩቮ"),
  bstack1l1ll1l_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫቯ"),
  bstack1l1ll1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪተ"),
  bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫቱ"),
  bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫቲ"),
  bstack1l1ll1l_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪታ"),
  bstack1l1ll1l_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫቴ"),
  bstack1l1ll1l_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭ት"),
  bstack1l1ll1l_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧቶ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫቷ"),
  bstack1l1ll1l_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬቸ"),
  bstack1l1ll1l_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧቹ"),
  bstack1l1ll1l_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ቺ"),
  bstack1l1ll1l_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧቻ"),
  bstack1l1ll1l_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫቼ"),
  bstack1l1ll1l_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧች"),
  bstack1l1ll1l_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬቾ"),
  bstack1l1ll1l_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ቿ"), bstack1l1ll1l_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫኀ"),
  bstack1l1ll1l_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩኁ"), bstack1l1ll1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧኂ"),
  bstack1l1ll1l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬኃ"),
  bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫኄ"),
  bstack1l1ll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫኅ"),
  bstack1l1ll1l_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧኆ"), bstack1l1ll1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧኇ"),
  bstack1l1ll1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨኈ"),
  bstack1l1ll1l_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫ኉"),
  bstack1l1ll1l_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧኊ"),
  bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩኋ"),
  bstack1l1ll1l_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫኌ"),
  bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ኍ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩ኎"),
  bstack1l1ll1l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫ኏"),
  bstack1l1ll1l_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨነ"),
  bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭ኑ"), bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬኒ"),
  bstack1l1ll1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩና"),
  bstack1l1ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡍࡩࡒ࡯ࡤࡣࡷࡳࡷࡇࡵࡵࡱࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳ࠭ኔ")
]
bstack11ll11ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪን")
bstack111l11l1l_opy_ = [bstack1l1ll1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪኖ"), bstack1l1ll1l_opy_ (u"࠭࠮ࡢࡣࡥࠫኗ"), bstack1l1ll1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬኘ")]
bstack11l111l11_opy_ = [bstack1l1ll1l_opy_ (u"ࠨ࡫ࡧࠫኙ"), bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧኚ"), bstack1l1ll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ኛ"), bstack1l1ll1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪኜ")]
bstack1ll11lll1_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬኝ"): bstack1l1ll1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫኞ"),
  bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨኟ"): bstack1l1ll1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭አ"),
  bstack1l1ll1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧኡ"): bstack1l1ll1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫኢ"),
  bstack1l1ll1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧኣ"): bstack1l1ll1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫኤ"),
  bstack1l1ll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭እ"): bstack1l1ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨኦ")
}
bstack1ll1ll1111_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ኧ"),
  bstack1l1ll1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧከ"),
  bstack1l1ll1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫኩ"),
  bstack1l1ll1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኪ"),
  bstack1l1ll1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ካ"),
]
bstack1l1l1llll_opy_ = bstack111l1l11l_opy_ + bstack1111l11l11_opy_ + bstack1l1l1111_opy_
bstack1lllll11l_opy_ = [
  bstack1l1ll1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫኬ"),
  bstack1l1ll1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨክ"),
  bstack1l1ll1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧኮ"),
  bstack1l1ll1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧኯ"),
  bstack1l1ll1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩኰ"),
  bstack1l1ll1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪ኱"),
  bstack1l1ll1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫኲ"),
  bstack1l1ll1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩኳ")
]
bstack11111l1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨኴ")
bstack1111l1lll_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧኵ")
bstack1l11l1ll_opy_ = [ bstack1l1ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ኶") ]
bstack11ll1lllll_opy_ = [ bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ኷") ]
bstack11l1llll1_opy_ = [bstack1l1ll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨኸ")]
bstack1l1l11l1_opy_ = [ bstack1l1ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬኹ") ]
bstack1ll111111_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨኺ")
bstack1llllll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪኻ")
bstack1llllll11l_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬኼ")
bstack111lllll_opy_ = bstack1l1ll1l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨኽ")
bstack1ll1llllll_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧኾ"),
  bstack1l1ll1l_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫ኿"),
  bstack1l1ll1l_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭ዀ"),
  bstack1l1ll1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈࠬ዁"),
  bstack1l1ll1l_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫዂ"),
  bstack1l1ll1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩዃ"),
  bstack1l1ll1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩዄ"),
  bstack1l1ll1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬዅ"),
  bstack1l1ll1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭዆"),
  bstack1l1ll1l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭዇"),
  bstack1l1ll1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧወ"),
  bstack1l1ll1l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭ዉ"),
  bstack1l1ll1l_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫዊ"),
  bstack1l1ll1l_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪዋ"),
  bstack1l1ll1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧዌ"),
  bstack1l1ll1l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫው"),
  bstack1l1ll1l_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨዎ"),
  bstack1l1ll1l_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ዏ"),
  bstack1l1ll1l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨዐ"),
  bstack1l1ll1l_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧዑ"),
  bstack1l1ll1l_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨዒ"),
]
bstack11lll1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨዓ")
bstack11l111ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1l_opy_ (u"ࠫࢃ࠭ዔ")), bstack1l1ll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬዕ"), bstack1l1ll1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬዖ"))
bstack111l111l11_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡩࠨ዗")
bstack11111l1lll_opy_ = [ bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨዘ"), bstack1l1ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨዙ"), bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩዚ"), bstack1l1ll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫዛ")]
bstack111lll11_opy_ = [ bstack1l1ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬዜ"), bstack1l1ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬዝ"), bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ዞ"), bstack1l1ll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨዟ") ]
bstack111lll1ll1_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧዠ"): bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪዡ"),
  bstack1l1ll1l_opy_ (u"ࠫࡋࡇࡉࡍࠩዢ"): bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬዣ"),
  bstack1l1ll1l_opy_ (u"࠭ࡓࡌࡋࡓࠫዤ"): bstack1l1ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨዥ")
}
bstack11lll1lll1_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠣࡩࡨࡸࠧዦ"),
  bstack1l1ll1l_opy_ (u"ࠤࡪࡳࡇࡧࡣ࡬ࠤዧ"),
  bstack1l1ll1l_opy_ (u"ࠥ࡫ࡴࡌ࡯ࡳࡹࡤࡶࡩࠨየ"),
  bstack1l1ll1l_opy_ (u"ࠦࡷ࡫ࡦࡳࡧࡶ࡬ࠧዩ"),
  bstack1l1ll1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦዪ"),
  bstack1l1ll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥያ"),
  bstack1l1ll1l_opy_ (u"ࠢࡴࡷࡥࡱ࡮ࡺࡅ࡭ࡧࡰࡩࡳࡺࠢዬ"),
  bstack1l1ll1l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧይ"),
  bstack1l1ll1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧዮ"),
  bstack1l1ll1l_opy_ (u"ࠥࡧࡱ࡫ࡡࡳࡇ࡯ࡩࡲ࡫࡮ࡵࠤዯ"),
  bstack1l1ll1l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࡷࠧደ"),
  bstack1l1ll1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠧዱ"),
  bstack1l1ll1l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡁࡴࡻࡱࡧࡘࡩࡲࡪࡲࡷࠦዲ"),
  bstack1l1ll1l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨዳ"),
  bstack1l1ll1l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨዴ"),
  bstack1l1ll1l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡗࡳࡺࡩࡨࡂࡥࡷ࡭ࡴࡴࠢድ"),
  bstack1l1ll1l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡑࡺࡲࡴࡪࡖࡲࡹࡨ࡮ࠢዶ"),
  bstack1l1ll1l_opy_ (u"ࠦࡸ࡮ࡡ࡬ࡧࠥዷ"),
  bstack1l1ll1l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࡅࡵࡶࠢዸ")
]
bstack111111lll1_opy_ = [
  bstack1l1ll1l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧዹ"),
  bstack1l1ll1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦዺ"),
  bstack1l1ll1l_opy_ (u"ࠣࡣࡸࡸࡴࠨዻ"),
  bstack1l1ll1l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤዼ"),
  bstack1l1ll1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧዽ")
]
bstack1lll1lll1l_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥዾ"): [bstack1l1ll1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦዿ")],
  bstack1l1ll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጀ"): [bstack1l1ll1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦጁ")],
  bstack1l1ll1l_opy_ (u"ࠣࡣࡸࡸࡴࠨጂ"): [bstack1l1ll1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨጃ"), bstack1l1ll1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨጄ"), bstack1l1ll1l_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣጅ"), bstack1l1ll1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦጆ")],
  bstack1l1ll1l_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨጇ"): [bstack1l1ll1l_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢገ")],
  bstack1l1ll1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥጉ"): [bstack1l1ll1l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦጊ")],
}
bstack1111l11lll_opy_ = {
  bstack1l1ll1l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤጋ"): bstack1l1ll1l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥጌ"),
  bstack1l1ll1l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤግ"): bstack1l1ll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጎ"),
  bstack1l1ll1l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦጏ"): bstack1l1ll1l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥጐ"),
  bstack1l1ll1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧ጑"): bstack1l1ll1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧጒ"),
  bstack1l1ll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨጓ"): bstack1l1ll1l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢጔ")
}
bstack111lll1l11_opy_ = {
  bstack1l1ll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪጕ"): bstack1l1ll1l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡓࡦࡶࡸࡴࠬ጖"),
  bstack1l1ll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ጗"): bstack1l1ll1l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪጘ"),
  bstack1l1ll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨጙ"): bstack1l1ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡖࡩࡹࡻࡰࠨጚ"),
  bstack1l1ll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩጛ"): bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ጜ")
}
bstack1111l111l1_opy_ = 65536
bstack1111l11l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠧ࠯࠰࠱࡟࡙ࡘࡕࡏࡅࡄࡘࡊࡊ࡝ࠨጝ")
bstack11111l11ll_opy_ = [
      bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪጞ"), bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬጟ"), bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ጠ"), bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨጡ"), bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧጢ"),
      bstack1l1ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩጣ"), bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪጤ"), bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩጥ"), bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪጦ"),
      bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጧ"), bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጨ"), bstack1l1ll1l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨጩ")
    ]
bstack11111l1111_opy_= {
  bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪጪ"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫጫ"),
  bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬጬ"): bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ጭ"),
  bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩጮ"): bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨጯ"),
  bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬጰ"): bstack1l1ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ጱ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪጲ"): bstack1l1ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫጳ"),
  bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫጴ"): bstack1l1ll1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬጵ"),
  bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧጶ"): bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨጷ"),
  bstack1l1ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪጸ"): bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫጹ"),
  bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫጺ"): bstack1l1ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬጻ"),
  bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨጼ"): bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩጽ"),
  bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩጾ"): bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪጿ"),
  bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫፀ"): bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬፁ"),
  bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫፂ"): bstack1l1ll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬፃ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨፄ"): bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧፅ"),
  bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨፆ"): bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩፇ"),
  bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬፈ"): bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ፉ"),
  bstack1l1ll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩፊ"): bstack1l1ll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪፋ"),
  bstack1l1ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫፌ"): bstack1l1ll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬፍ"),
  bstack1l1ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪፎ"): bstack1l1ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫፏ"),
  bstack1l1ll1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫፐ"): bstack1l1ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬፑ"),
  bstack1l1ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫፒ"): bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬፓ"),
  bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ፔ"): bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧፕ"),
  bstack1l1ll1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬፖ"): bstack1l1ll1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ፗ"),
  bstack1l1ll1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧፘ"): bstack1l1ll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨፙ"),
  bstack1l1ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬፚ"): bstack1l1ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭፛")
}
bstack11111l11l1_opy_ = [bstack1l1ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ፜"), bstack1l1ll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ፝")]
bstack1l1l111l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠲ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠱ࡹ࠵࠴࡭ࡲࡪࡦࡶ࠳ࠧ፞")
bstack1l11lll111_opy_ = bstack1l1ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬ࡸࡩࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࠤ፟")
bstack111ll1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠭ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨ࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠧ፠")
class EVENTS(Enum):
  bstack11111ll1ll_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡲ࠵࠶ࡿ࠺ࡱࡴ࡬ࡲࡹ࠳ࡢࡶ࡫࡯ࡨࡱ࡯࡮࡬ࠩ፡")
  bstack1lll111ll_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡫ࡡ࡯ࡷࡳࠫ።") # final bstack11111ll111_opy_
  bstack11111lll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡸ࡫࡮ࡥ࡮ࡲ࡫ࡸ࠭፣")
  bstack1l111l1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ࠼ࡳࡶ࡮ࡴࡴ࠮ࡤࡸ࡭ࡱࡪ࡬ࡪࡰ࡮ࠫ፤")
  bstack1l1llll111_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡲࡵ࡭ࡳࡺ࠭ࡣࡷ࡬ࡰࡩࡲࡩ࡯࡭ࠪ፥")
  bstack11111ll1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡵࡧࡶࡸ࡭ࡻࡢࠨ፦")
  bstack11111l111l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡥࡱࡺࡲࡱࡵࡡࡥࠩ፧")
  bstack11lll11ll_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪࡀࡨࡶࡤ࠰ࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠧ፨")
  bstack1111lll1ll_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥ࠶࠷ࡹ࠻ࡵࡤࡺࡪ࠳ࡲࡦࡵࡸࡰࡹࡹࠧ፩")
  bstack11l11llll_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦ࠷࠱ࡺ࠼ࡧࡶ࡮ࡼࡥࡳ࠯ࡳࡩࡷ࡬࡯ࡳ࡯ࡶࡧࡦࡴࠧ፪")
  bstack1ll11lll11_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺࡭ࡱࡦࡥࡱ࠭፫")
  bstack1l111l11_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡧࡰࡱ࠯ࡸࡴࡱࡵࡡࡥࠩ፬")
  bstack1ll11ll1ll_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡦ࡭࠲ࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠨ፭")
  bstack1l1l1ll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡧࡦࡶ࠰ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠰ࡶࡪࡹࡵ࡭ࡶࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬ፮")
  bstack1ll11ll1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤ࠵࠶ࡿ࠺ࡨࡧࡷ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠱ࡷ࡫ࡳࡶ࡮ࡷࡷࠬ፯")
  bstack11111ll11l_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡪࡸࡣࡺࠩ፰")
  SDK_PERCY_SCREENSHOT = bstack1l1ll1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵ࡫ࡲࡤࡻ࠽ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ፱")
  bstack111l1llll_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡵࡷࡥࡹࡻࡳࠨ፲")
  bstack11ll1ll11_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡪࡸࡦ࠲ࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵࠩ፳")
  bstack1111l1l111_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡲࡼࡾ࠳ࡳࡦࡶࡸࡴࠬ፴")
  bstack1lllll11_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡸࡺࡶࠧ፵")
  bstack11111llll1_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡵࡱࡥࡵࡹࡨࡰࡶࠪ፶") # not bstack111111ll1l_opy_ in python
  bstack11l111lll_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡵࡺ࡯ࡴࠨ፷") # used in bstack1111l11ll1_opy_
  bstack1ll11l1l11_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾࡬࡫ࡴࠨ፸") # used in bstack1111l11ll1_opy_
  bstack11111l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵࡧ࡯࠿࡮࡯ࡰ࡭ࠪ፹")
  bstack1lllll1lll_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡶࡶࡲࡱࡦࡺࡥ࠻ࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠧ፺")
  bstack1l1l1l1111_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡶࡩࡸࡹࡩࡰࡰ࠰ࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠧ፻") #
  bstack1l1l1lll1_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡱ࠴࠵ࡾࡀࡤࡳ࡫ࡹࡩࡷ࠳ࡴࡢ࡭ࡨࡗࡨࡸࡥࡦࡰࡖ࡬ࡴࡺࠧ፼")
  bstack1ll11111l1_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡳࡩࡷࡩࡹ࠻ࡣࡸࡸࡴ࠳ࡣࡢࡲࡷࡹࡷ࡫ࠧ፽")
  bstack1llll1l1ll_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡴࡷ࡫࠭ࡵࡧࡶࡸࠬ፾")
  bstack1l1lllll_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡵࡳࡵ࠯ࡷࡩࡸࡺࠧ፿")
  bstack1l1l11l1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶࡲࡦ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᎀ")
  bstack1l1111lll_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᎁ")
  bstack11111l1l11_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢࡷࡷࡳ࠲ࡩࡡࡱࡶࡸࡶࡪ࠭ᎂ")
  bstack11111l1l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣࡸࡸࡴࡳࡡࡵࡧ࠽࡭ࡩࡲࡥ࠮ࡶ࡬ࡱࡪࡵࡵࡵࠩᎃ")
class STAGE(Enum):
  bstack111ll1l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᎄ")
  END = bstack1l1ll1l_opy_ (u"࠭ࡥ࡯ࡦࠪᎅ")
  SINGLE = bstack1l1ll1l_opy_ (u"ࠧࡴ࡫ࡱ࡫ࡱ࡫ࠧᎆ")