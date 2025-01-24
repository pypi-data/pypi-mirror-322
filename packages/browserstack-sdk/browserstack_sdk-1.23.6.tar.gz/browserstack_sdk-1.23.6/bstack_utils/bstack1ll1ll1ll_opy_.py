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
class bstack1111ll1l11_opy_(object):
  bstack1l1111111_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1l_opy_ (u"ࠨࢀࠪၔ")), bstack1l1ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩၕ"))
  bstack1111ll11ll_opy_ = os.path.join(bstack1l1111111_opy_, bstack1l1ll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪၖ"))
  bstack1111ll1ll1_opy_ = None
  perform_scan = None
  bstack111l11ll_opy_ = None
  bstack11ll11l1l1_opy_ = None
  bstack111l111ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1ll1l_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭ၗ")):
      cls.instance = super(bstack1111ll1l11_opy_, cls).__new__(cls)
      cls.instance.bstack1111ll11l1_opy_()
    return cls.instance
  def bstack1111ll11l1_opy_(self):
    try:
      with open(self.bstack1111ll11ll_opy_, bstack1l1ll1l_opy_ (u"ࠬࡸࠧၘ")) as bstack1l11ll1l1l_opy_:
        bstack1111ll1l1l_opy_ = bstack1l11ll1l1l_opy_.read()
        data = json.loads(bstack1111ll1l1l_opy_)
        if bstack1l1ll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨၙ") in data:
          self.bstack111l111l1l_opy_(data[bstack1l1ll1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩၚ")])
        if bstack1l1ll1l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩၛ") in data:
          self.bstack111l1111ll_opy_(data[bstack1l1ll1l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪၜ")])
    except:
      pass
  def bstack111l1111ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l1ll1l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨၝ")]
      self.bstack111l11ll_opy_ = scripts[bstack1l1ll1l_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨၞ")]
      self.bstack11ll11l1l1_opy_ = scripts[bstack1l1ll1l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩၟ")]
      self.bstack111l111ll1_opy_ = scripts[bstack1l1ll1l_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫၠ")]
  def bstack111l111l1l_opy_(self, bstack1111ll1ll1_opy_):
    if bstack1111ll1ll1_opy_ != None and len(bstack1111ll1ll1_opy_) != 0:
      self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
  def store(self):
    try:
      with open(self.bstack1111ll11ll_opy_, bstack1l1ll1l_opy_ (u"ࠧࡸࠩၡ")) as file:
        json.dump({
          bstack1l1ll1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥၢ"): self.bstack1111ll1ll1_opy_,
          bstack1l1ll1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥၣ"): {
            bstack1l1ll1l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣၤ"): self.perform_scan,
            bstack1l1ll1l_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣၥ"): self.bstack111l11ll_opy_,
            bstack1l1ll1l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤၦ"): self.bstack11ll11l1l1_opy_,
            bstack1l1ll1l_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦၧ"): self.bstack111l111ll1_opy_
          }
        }, file)
    except:
      pass
  def bstack1l1l11lll1_opy_(self, bstack1111ll111l_opy_):
    try:
      return any(command.get(bstack1l1ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬၨ")) == bstack1111ll111l_opy_ for command in self.bstack1111ll1ll1_opy_)
    except:
      return False
bstack1ll1ll1ll_opy_ = bstack1111ll1l11_opy_()