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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11l1lll11_opy_ import get_logger
from bstack_utils.bstack11lll1l1ll_opy_ import bstack111l1ll11l_opy_
bstack11lll1l1ll_opy_ = bstack111l1ll11l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l111l1l1l_opy_: Optional[str] = None):
    bstack1l1ll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᖸ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack111l11111l_opy_: str = bstack11lll1l1ll_opy_.bstack1111ll1lll_opy_(label)
            start_mark: str = label + bstack1l1ll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᖹ")
            end_mark: str = label + bstack1l1ll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᖺ")
            result = None
            try:
                if stage.value == STAGE.bstack111ll1l1l_opy_.value:
                    bstack11lll1l1ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack11lll1l1ll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l111l1l1l_opy_)
                elif stage.value == STAGE.SINGLE.value:
                    start_mark: str = bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᖻ")
                    end_mark: str = bstack111l11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᖼ")
                    bstack11lll1l1ll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack11lll1l1ll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l111l1l1l_opy_)
            except Exception as e:
                bstack11lll1l1ll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l111l1l1l_opy_)
            return result
        return wrapper
    return decorator