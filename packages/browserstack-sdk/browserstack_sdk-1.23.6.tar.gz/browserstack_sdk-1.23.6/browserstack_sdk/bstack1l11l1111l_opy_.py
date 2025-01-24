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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1lll11l_opy_ import bstack11l1ll1l11_opy_, bstack11l1l11ll1_opy_
from bstack_utils.bstack11l1lll111_opy_ import bstack11llll1111_opy_
from bstack_utils.helper import bstack1ll111111l_opy_, bstack1l1lll1l1_opy_, Result
from bstack_utils.bstack11l1l11lll_opy_ import bstack1llllll11_opy_
from bstack_utils.capture import bstack11l1l1l1ll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l11l1111l_opy_:
    def __init__(self):
        self.bstack11l1l1ll11_opy_ = bstack11l1l1l1ll_opy_(self.bstack11l1l1llll_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1l1llll_opy_(log):
        if not (log[bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭๠")] and log[bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๡")].strip()):
            return
        active = bstack11llll1111_opy_.bstack11l1ll11l1_opy_()
        log = {
            bstack1l1ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭๢"): log[bstack1l1ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ๣")],
            bstack1l1ll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ๤"): bstack1l1lll1l1_opy_(),
            bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๥"): log[bstack1l1ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๦")],
        }
        if active:
            if active[bstack1l1ll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ๧")] == bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ๨"):
                log[bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ๩")] = active[bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ๪")]
            elif active[bstack1l1ll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๫")] == bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࠨ๬"):
                log[bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ๭")] = active[bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ๮")]
        bstack1llllll11_opy_.bstack1ll111lll1_opy_([log])
    def start_test(self, attrs):
        bstack11l1llll1l_opy_ = uuid4().__str__()
        self.tests[bstack11l1llll1l_opy_] = {}
        self.bstack11l1l1ll11_opy_.start()
        driver = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ๯"), None)
        bstack11l1lll11l_opy_ = bstack11l1l11ll1_opy_(
            name=attrs.scenario.name,
            uuid=bstack11l1llll1l_opy_,
            bstack11l1lll1ll_opy_=bstack1l1lll1l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l1ll1l_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ๰"),
            framework=bstack1l1ll1l_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨ๱"),
            scope=[attrs.feature.name],
            bstack11l1l11l1l_opy_=bstack1llllll11_opy_.bstack11l1ll1l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11l1llll1l_opy_][bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ๲")] = bstack11l1lll11l_opy_
        threading.current_thread().current_test_uuid = bstack11l1llll1l_opy_
        bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ๳"), bstack11l1lll11l_opy_)
    def end_test(self, attrs):
        bstack11l1ll1lll_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ๴"): attrs.feature.name,
            bstack1l1ll1l_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥ๵"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1lll11l_opy_ = self.tests[current_test_uuid][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ๶")]
        meta = {
            bstack1l1ll1l_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣ๷"): bstack11l1ll1lll_opy_,
            bstack1l1ll1l_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢ๸"): bstack11l1lll11l_opy_.meta.get(bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ๹"), []),
            bstack1l1ll1l_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ๺"): {
                bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ๻"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1lll11l_opy_.bstack11l1l111l1_opy_(meta)
        bstack11l1lll11l_opy_.bstack11l1l1l111_opy_(bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ๼"), []))
        bstack11l1l1l1l1_opy_, exception = self._11l1l111ll_opy_(attrs)
        bstack11l1lll1l1_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1ll1111_opy_=[bstack11l1l1l1l1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ๽")].stop(time=bstack1l1lll1l1_opy_(), duration=int(attrs.duration)*1000, result=bstack11l1lll1l1_opy_)
        bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ๾"), self.tests[threading.current_thread().current_test_uuid][bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ๿")])
    def bstack11l1ll1l1_opy_(self, attrs):
        bstack11l1l1l11l_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠩ࡬ࡨࠬ຀"): uuid4().__str__(),
            bstack1l1ll1l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫກ"): attrs.keyword,
            bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫຂ"): [],
            bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡹࡶࠪ຃"): attrs.name,
            bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪຄ"): bstack1l1lll1l1_opy_(),
            bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ຅"): bstack1l1ll1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩຆ"),
            bstack1l1ll1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧງ"): bstack1l1ll1l_opy_ (u"ࠪࠫຈ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຉ")].add_step(bstack11l1l1l11l_opy_)
        threading.current_thread().current_step_uuid = bstack11l1l1l11l_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨຊ")]
    def bstack11llllll_opy_(self, attrs):
        current_test_id = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ຋"), None)
        current_step_uuid = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫຌ"), None)
        bstack11l1l1l1l1_opy_, exception = self._11l1l111ll_opy_(attrs)
        bstack11l1lll1l1_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1ll1111_opy_=[bstack11l1l1l1l1_opy_])
        self.tests[current_test_id][bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫຍ")].bstack11l1l1ll1l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l1lll1l1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack111l1ll11_opy_(self, name, attrs):
        try:
            bstack11l1l1lll1_opy_ = uuid4().__str__()
            self.tests[bstack11l1l1lll1_opy_] = {}
            self.bstack11l1l1ll11_opy_.start()
            scopes = []
            driver = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨຎ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l1ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨຏ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l1l1lll1_opy_)
            if name in [bstack1l1ll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣຐ"), bstack1l1ll1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣຑ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l1ll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢຒ"), bstack1l1ll1l_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢຓ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l1ll1l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩດ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l1ll1l11_opy_(
                name=name,
                uuid=bstack11l1l1lll1_opy_,
                bstack11l1lll1ll_opy_=bstack1l1lll1l1_opy_(),
                file_path=file_path,
                framework=bstack1l1ll1l_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤຕ"),
                bstack11l1l11l1l_opy_=bstack1llllll11_opy_.bstack11l1ll1l1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l1ll1l_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦຖ"),
                hook_type=name
            )
            self.tests[bstack11l1l1lll1_opy_][bstack1l1ll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢທ")] = hook_data
            current_test_id = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤຘ"), None)
            if current_test_id:
                hook_data.bstack11l1ll111l_opy_(current_test_id)
            if name == bstack1l1ll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥນ"):
                threading.current_thread().before_all_hook_uuid = bstack11l1l1lll1_opy_
            threading.current_thread().current_hook_uuid = bstack11l1l1lll1_opy_
            bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠣບ"), hook_data)
        except Exception as e:
            logger.debug(bstack1l1ll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹࠢປ"), name, e)
    def bstack1l11l1ll1_opy_(self, attrs):
        bstack11l1l11l11_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ຜ"), None)
        hook_data = self.tests[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ຝ")]
        status = bstack1l1ll1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦພ")
        exception = None
        bstack11l1l1l1l1_opy_ = None
        if hook_data.name == bstack1l1ll1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣຟ"):
            self.bstack11l1l1ll11_opy_.reset()
            bstack11l1llll11_opy_ = self.tests[bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ຠ"), None)][bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪມ")].result.result
            if bstack11l1llll11_opy_ == bstack1l1ll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣຢ"):
                if attrs.hook_failures == 1:
                    status = bstack1l1ll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤຣ")
                elif attrs.hook_failures == 2:
                    status = bstack1l1ll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ຤")
            elif attrs.bstack11l1ll11ll_opy_:
                status = bstack1l1ll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦລ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l1ll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ຦") and attrs.hook_failures == 1:
                status = bstack1l1ll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨວ")
            elif hasattr(attrs, bstack1l1ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧຨ")) and attrs.error_message:
                status = bstack1l1ll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣຩ")
            bstack11l1l1l1l1_opy_, exception = self._11l1l111ll_opy_(attrs)
        bstack11l1lll1l1_opy_ = Result(result=status, exception=exception, bstack11l1ll1111_opy_=[bstack11l1l1l1l1_opy_])
        hook_data.stop(time=bstack1l1lll1l1_opy_(), duration=0, result=bstack11l1lll1l1_opy_)
        bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫສ"), self.tests[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ຫ")])
        threading.current_thread().current_hook_uuid = None
    def _11l1l111ll_opy_(self, attrs):
        try:
            import traceback
            bstack11ll11ll11_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l1l1l1l1_opy_ = bstack11ll11ll11_opy_[-1] if bstack11ll11ll11_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l1ll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣຬ"))
            bstack11l1l1l1l1_opy_ = None
            exception = None
        return bstack11l1l1l1l1_opy_, exception