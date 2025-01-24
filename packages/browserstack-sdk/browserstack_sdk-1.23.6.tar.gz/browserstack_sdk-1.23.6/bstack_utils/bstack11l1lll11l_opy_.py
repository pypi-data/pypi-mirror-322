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
from uuid import uuid4
from bstack_utils.helper import bstack1l1lll1l1_opy_, bstack1llll1lllll_opy_
from bstack_utils.bstack1llllllll_opy_ import bstack1ll11ll1l1l_opy_
class bstack11l11l1l11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11l1lll1ll_opy_=None, framework=None, tags=[], scope=[], bstack1ll111llll1_opy_=None, bstack1ll111l11ll_opy_=True, bstack1ll111l1ll1_opy_=None, bstack1ll1l11ll1_opy_=None, result=None, duration=None, bstack11l1111lll_opy_=None, meta={}):
        self.bstack11l1111lll_opy_ = bstack11l1111lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll111l11ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11l1lll1ll_opy_ = bstack11l1lll1ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll111llll1_opy_ = bstack1ll111llll1_opy_
        self.bstack1ll111l1ll1_opy_ = bstack1ll111l1ll1_opy_
        self.bstack1ll1l11ll1_opy_ = bstack1ll1l11ll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l111lll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1l111l1_opy_(self, meta):
        self.meta = meta
    def bstack11l1l1l111_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll111l1l1l_opy_(self):
        bstack1ll111l111l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1ll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᜖"): bstack1ll111l111l_opy_,
            bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ᜗"): bstack1ll111l111l_opy_,
            bstack1l1ll1l_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ᜘"): bstack1ll111l111l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1ll1l_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨ᜙") + key)
            setattr(self, key, val)
    def bstack1ll111l11l1_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᜚"): self.name,
            bstack1l1ll1l_opy_ (u"ࠧࡣࡱࡧࡽࠬ᜛"): {
                bstack1l1ll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭᜜"): bstack1l1ll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ᜝"),
                bstack1l1ll1l_opy_ (u"ࠪࡧࡴࡪࡥࠨ᜞"): self.code
            },
            bstack1l1ll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᜟ"): self.scope,
            bstack1l1ll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᜠ"): self.tags,
            bstack1l1ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᜡ"): self.framework,
            bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᜢ"): self.bstack11l1lll1ll_opy_
        }
    def bstack1ll111ll1ll_opy_(self):
        return {
         bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᜣ"): self.meta
        }
    def bstack1ll111ll11l_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᜤ"): {
                bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᜥ"): self.bstack1ll111llll1_opy_
            }
        }
    def bstack1ll111l1lll_opy_(self, bstack1ll111lll1l_opy_, details):
        step = next(filter(lambda st: st[bstack1l1ll1l_opy_ (u"ࠫ࡮ࡪࠧᜦ")] == bstack1ll111lll1l_opy_, self.meta[bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᜧ")]), None)
        step.update(details)
    def bstack11l1ll1l1_opy_(self, bstack1ll111lll1l_opy_):
        step = next(filter(lambda st: st[bstack1l1ll1l_opy_ (u"࠭ࡩࡥࠩᜨ")] == bstack1ll111lll1l_opy_, self.meta[bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᜩ")]), None)
        step.update({
            bstack1l1ll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜪ"): bstack1l1lll1l1_opy_()
        })
    def bstack11l1l1ll1l_opy_(self, bstack1ll111lll1l_opy_, result, duration=None):
        bstack1ll111l1ll1_opy_ = bstack1l1lll1l1_opy_()
        if bstack1ll111lll1l_opy_ is not None and self.meta.get(bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᜫ")):
            step = next(filter(lambda st: st[bstack1l1ll1l_opy_ (u"ࠪ࡭ࡩ࠭ᜬ")] == bstack1ll111lll1l_opy_, self.meta[bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᜭ")]), None)
            step.update({
                bstack1l1ll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜮ"): bstack1ll111l1ll1_opy_,
                bstack1l1ll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᜯ"): duration if duration else bstack1llll1lllll_opy_(step[bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᜰ")], bstack1ll111l1ll1_opy_),
                bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᜱ"): result.result,
                bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᜲ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1111lll1_opy_):
        if self.meta.get(bstack1l1ll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᜳ")):
            self.meta[bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵ᜴ࠪ")].append(bstack1ll1111lll1_opy_)
        else:
            self.meta[bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᜵")] = [ bstack1ll1111lll1_opy_ ]
    def bstack1ll111lll11_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᜶"): self.bstack11l111lll1_opy_(),
            **self.bstack1ll111l11l1_opy_(),
            **self.bstack1ll111l1l1l_opy_(),
            **self.bstack1ll111ll1ll_opy_()
        }
    def bstack1ll111ll111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᜷"): self.bstack1ll111l1ll1_opy_,
            bstack1l1ll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᜸"): self.duration,
            bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜹"): self.result.result
        }
        if data[bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᜺")] == bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᜻"):
            data[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ᜼")] = self.result.bstack111l1llll1_opy_()
            data[bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᜽")] = [{bstack1l1ll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ᜾"): self.result.bstack1llll11ll11_opy_()}]
        return data
    def bstack1ll111ll1l1_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᜿"): self.bstack11l111lll1_opy_(),
            **self.bstack1ll111l11l1_opy_(),
            **self.bstack1ll111l1l1l_opy_(),
            **self.bstack1ll111ll111_opy_(),
            **self.bstack1ll111ll1ll_opy_()
        }
    def bstack11l111ll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1ll1l_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪᝀ") in event:
            return self.bstack1ll111lll11_opy_()
        elif bstack1l1ll1l_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᝁ") in event:
            return self.bstack1ll111ll1l1_opy_()
    def bstack11l11l11ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll111l1ll1_opy_ = time if time else bstack1l1lll1l1_opy_()
        self.duration = duration if duration else bstack1llll1lllll_opy_(self.bstack11l1lll1ll_opy_, self.bstack1ll111l1ll1_opy_)
        if result:
            self.result = result
class bstack11l1l11ll1_opy_(bstack11l11l1l11_opy_):
    def __init__(self, hooks=[], bstack11l1l11l1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1l11l1l_opy_ = bstack11l1l11l1l_opy_
        super().__init__(*args, **kwargs, bstack1ll1l11ll1_opy_=bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᝂ"))
    @classmethod
    def bstack1ll1111llll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨᝃ"): id(step),
                bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡺࡷࠫᝄ"): step.name,
                bstack1l1ll1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᝅ"): step.keyword,
            })
        return bstack11l1l11ll1_opy_(
            **kwargs,
            meta={
                bstack1l1ll1l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᝆ"): {
                    bstack1l1ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᝇ"): feature.name,
                    bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨᝈ"): feature.filename,
                    bstack1l1ll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᝉ"): feature.description
                },
                bstack1l1ll1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᝊ"): {
                    bstack1l1ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝋ"): scenario.name
                },
                bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᝌ"): steps,
                bstack1l1ll1l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᝍ"): bstack1ll11ll1l1l_opy_(test)
            }
        )
    def bstack1ll111l1111_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᝎ"): self.hooks
        }
    def bstack1ll111l1l11_opy_(self):
        if self.bstack11l1l11l1l_opy_:
            return {
                bstack1l1ll1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᝏ"): self.bstack11l1l11l1l_opy_
            }
        return {}
    def bstack1ll111ll1l1_opy_(self):
        return {
            **super().bstack1ll111ll1l1_opy_(),
            **self.bstack1ll111l1111_opy_()
        }
    def bstack1ll111lll11_opy_(self):
        return {
            **super().bstack1ll111lll11_opy_(),
            **self.bstack1ll111l1l11_opy_()
        }
    def bstack11l11l11ll_opy_(self):
        return bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᝐ")
class bstack11l1ll1l11_opy_(bstack11l11l1l11_opy_):
    def __init__(self, hook_type, *args,bstack11l1l11l1l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11l11111_opy_ = None
        self.bstack11l1l11l1l_opy_ = bstack11l1l11l1l_opy_
        super().__init__(*args, **kwargs, bstack1ll1l11ll1_opy_=bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᝑ"))
    def bstack11l1111ll1_opy_(self):
        return self.hook_type
    def bstack1ll111lllll_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᝒ"): self.hook_type
        }
    def bstack1ll111ll1l1_opy_(self):
        return {
            **super().bstack1ll111ll1l1_opy_(),
            **self.bstack1ll111lllll_opy_()
        }
    def bstack1ll111lll11_opy_(self):
        return {
            **super().bstack1ll111lll11_opy_(),
            bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᝓ"): self.bstack1ll11l11111_opy_,
            **self.bstack1ll111lllll_opy_()
        }
    def bstack11l11l11ll_opy_(self):
        return bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ᝔")
    def bstack11l1ll111l_opy_(self, bstack1ll11l11111_opy_):
        self.bstack1ll11l11111_opy_ = bstack1ll11l11111_opy_