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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l11ll111_opy_ import RobotHandler
from bstack_utils.capture import bstack11l1l1l1ll_opy_
from bstack_utils.bstack11l1lll11l_opy_ import bstack11l11l1l11_opy_, bstack11l1ll1l11_opy_, bstack11l1l11ll1_opy_
from bstack_utils.bstack11l1lll111_opy_ import bstack11llll1111_opy_
from bstack_utils.bstack11l1l11lll_opy_ import bstack1llllll11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll111111l_opy_, bstack1l1lll1l1_opy_, Result, \
    bstack11l111ll1l_opy_, bstack11l111l1l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩອ"): [],
        bstack1l1ll1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬຮ"): [],
        bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫຯ"): []
    }
    bstack111lllll11_opy_ = []
    bstack11l11l1lll_opy_ = []
    @staticmethod
    def bstack11l1l1llll_opy_(log):
        if not (log[bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩະ")] and log[bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪັ")].strip()):
            return
        active = bstack11llll1111_opy_.bstack11l1ll11l1_opy_()
        log = {
            bstack1l1ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩາ"): log[bstack1l1ll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪຳ")],
            bstack1l1ll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨິ"): bstack11l111l1l1_opy_().isoformat() + bstack1l1ll1l_opy_ (u"࡚࠭ࠨີ"),
            bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຶ"): log[bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩື")],
        }
        if active:
            if active[bstack1l1ll1l_opy_ (u"ࠩࡷࡽࡵ࡫ຸࠧ")] == bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨູ"):
                log[bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧ຺ࠫ")] = active[bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬົ")]
            elif active[bstack1l1ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫຼ")] == bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬຽ"):
                log[bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ຾")] = active[bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ຿")]
        bstack1llllll11_opy_.bstack1ll111lll1_opy_([log])
    def __init__(self):
        self.messages = bstack11l1111l11_opy_()
        self._111llll1ll_opy_ = None
        self._11l11l1111_opy_ = None
        self._11l111l11l_opy_ = OrderedDict()
        self.bstack11l1l1ll11_opy_ = bstack11l1l1l1ll_opy_(self.bstack11l1l1llll_opy_)
    @bstack11l111ll1l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111lll1lll_opy_()
        if not self._11l111l11l_opy_.get(attrs.get(bstack1l1ll1l_opy_ (u"ࠪ࡭ࡩ࠭ເ")), None):
            self._11l111l11l_opy_[attrs.get(bstack1l1ll1l_opy_ (u"ࠫ࡮ࡪࠧແ"))] = {}
        bstack11l1l1111l_opy_ = bstack11l1l11ll1_opy_(
                bstack11l1111lll_opy_=attrs.get(bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨໂ")),
                name=name,
                bstack11l1lll1ll_opy_=bstack1l1lll1l1_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1ll1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ໃ")], start=os.getcwd()) if attrs.get(bstack1l1ll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧໄ")) != bstack1l1ll1l_opy_ (u"ࠨࠩ໅") else bstack1l1ll1l_opy_ (u"ࠩࠪໆ"),
                framework=bstack1l1ll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ໇")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1ll1l_opy_ (u"ࠫ࡮ࡪ່ࠧ"), None)
        self._11l111l11l_opy_[attrs.get(bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨ້"))][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢ໊ࠩ")] = bstack11l1l1111l_opy_
    @bstack11l111ll1l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111llllll1_opy_()
        self._11l111111l_opy_(messages)
        for bstack11l11l111l_opy_ in self.bstack111lllll11_opy_:
            bstack11l11l111l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯໋ࠩ")][bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ໌")].extend(self.store[bstack1l1ll1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨໍ")])
            bstack1llllll11_opy_.bstack1llll1ll11_opy_(bstack11l11l111l_opy_)
        self.bstack111lllll11_opy_ = []
        self.store[bstack1l1ll1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ໎")] = []
    @bstack11l111ll1l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l1l1ll11_opy_.start()
        if not self._11l111l11l_opy_.get(attrs.get(bstack1l1ll1l_opy_ (u"ࠫ࡮ࡪࠧ໏")), None):
            self._11l111l11l_opy_[attrs.get(bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨ໐"))] = {}
        driver = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ໑"), None)
        bstack11l1lll11l_opy_ = bstack11l1l11ll1_opy_(
            bstack11l1111lll_opy_=attrs.get(bstack1l1ll1l_opy_ (u"ࠧࡪࡦࠪ໒")),
            name=name,
            bstack11l1lll1ll_opy_=bstack1l1lll1l1_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1ll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໓")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1111l1l_opy_(attrs.get(bstack1l1ll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ໔"), None)),
            framework=bstack1l1ll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ໕"),
            tags=attrs[bstack1l1ll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩ໖")],
            hooks=self.store[bstack1l1ll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ໗")],
            bstack11l1l11l1l_opy_=bstack1llllll11_opy_.bstack11l1ll1l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1ll1l_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣ໘").format(bstack1l1ll1l_opy_ (u"ࠢࠡࠤ໙").join(attrs[bstack1l1ll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭໚")]), name) if attrs[bstack1l1ll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ໛")] else name
        )
        self._11l111l11l_opy_[attrs.get(bstack1l1ll1l_opy_ (u"ࠪ࡭ࡩ࠭ໜ"))][bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧໝ")] = bstack11l1lll11l_opy_
        threading.current_thread().current_test_uuid = bstack11l1lll11l_opy_.bstack11l111lll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨໞ"), None)
        self.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧໟ"), bstack11l1lll11l_opy_)
    @bstack11l111ll1l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l1l1ll11_opy_.reset()
        bstack11l11llll1_opy_ = bstack111lll1ll1_opy_.get(attrs.get(bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ໠")), bstack1l1ll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ໡"))
        self._11l111l11l_opy_[attrs.get(bstack1l1ll1l_opy_ (u"ࠩ࡬ࡨࠬ໢"))][bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໣")].stop(time=bstack1l1lll1l1_opy_(), duration=int(attrs.get(bstack1l1ll1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ໤"), bstack1l1ll1l_opy_ (u"ࠬ࠶ࠧ໥"))), result=Result(result=bstack11l11llll1_opy_, exception=attrs.get(bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໦")), bstack11l1ll1111_opy_=[attrs.get(bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໧"))]))
        self.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ໨"), self._11l111l11l_opy_[attrs.get(bstack1l1ll1l_opy_ (u"ࠩ࡬ࡨࠬ໩"))][bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໪")], True)
        self.store[bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ໫")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l111ll1l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111lll1lll_opy_()
        current_test_id = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ໬"), None)
        bstack111llll111_opy_ = current_test_id if bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ໭"), None) else bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ໮"), None)
        if attrs.get(bstack1l1ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭໯"), bstack1l1ll1l_opy_ (u"ࠩࠪ໰")).lower() in [bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ໱"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭໲")]:
            hook_type = bstack111lll11ll_opy_(attrs.get(bstack1l1ll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ໳")), bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ໴"), None))
            hook_name = bstack1l1ll1l_opy_ (u"ࠧࡼࡿࠪ໵").format(attrs.get(bstack1l1ll1l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ໶"), bstack1l1ll1l_opy_ (u"ࠩࠪ໷")))
            if hook_type in [bstack1l1ll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ໸"), bstack1l1ll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ໹")]:
                hook_name = bstack1l1ll1l_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭໺").format(bstack111lll1l11_opy_.get(hook_type), attrs.get(bstack1l1ll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭໻"), bstack1l1ll1l_opy_ (u"ࠧࠨ໼")))
            bstack11l1l11111_opy_ = bstack11l1ll1l11_opy_(
                bstack11l1111lll_opy_=bstack111llll111_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠯ࠪ໽") + attrs.get(bstack1l1ll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໾"), bstack1l1ll1l_opy_ (u"ࠪࠫ໿")).lower(),
                name=hook_name,
                bstack11l1lll1ll_opy_=bstack1l1lll1l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1ll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫༀ")), start=os.getcwd()),
                framework=bstack1l1ll1l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ༁"),
                tags=attrs[bstack1l1ll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ༂")],
                scope=RobotHandler.bstack11l1111l1l_opy_(attrs.get(bstack1l1ll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ༃"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l1l11111_opy_.bstack11l111lll1_opy_()
            threading.current_thread().current_hook_id = bstack111llll111_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠯ࠪ༄") + attrs.get(bstack1l1ll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ༅"), bstack1l1ll1l_opy_ (u"ࠪࠫ༆")).lower()
            self.store[bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ༇")] = [bstack11l1l11111_opy_.bstack11l111lll1_opy_()]
            if bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ༈"), None):
                self.store[bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ༉")].append(bstack11l1l11111_opy_.bstack11l111lll1_opy_())
            else:
                self.store[bstack1l1ll1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭༊")].append(bstack11l1l11111_opy_.bstack11l111lll1_opy_())
            if bstack111llll111_opy_:
                self._11l111l11l_opy_[bstack111llll111_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠯ࠪ་") + attrs.get(bstack1l1ll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ༌"), bstack1l1ll1l_opy_ (u"ࠪࠫ།")).lower()] = { bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༎"): bstack11l1l11111_opy_ }
            bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭༏"), bstack11l1l11111_opy_)
        else:
            bstack11l1l1l11l_opy_ = {
                bstack1l1ll1l_opy_ (u"࠭ࡩࡥࠩ༐"): uuid4().__str__(),
                bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡻࡸࠬ༑"): bstack1l1ll1l_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ༒").format(attrs.get(bstack1l1ll1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ༓")), attrs.get(bstack1l1ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ༔"), bstack1l1ll1l_opy_ (u"ࠫࠬ༕"))) if attrs.get(bstack1l1ll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ༖"), []) else attrs.get(bstack1l1ll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭༗")),
                bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺ༘ࠧ"): attrs.get(bstack1l1ll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ༙࠭"), []),
                bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭༚"): bstack1l1lll1l1_opy_(),
                bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ༛"): bstack1l1ll1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ༜"),
                bstack1l1ll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ༝"): attrs.get(bstack1l1ll1l_opy_ (u"࠭ࡤࡰࡥࠪ༞"), bstack1l1ll1l_opy_ (u"ࠧࠨ༟"))
            }
            if attrs.get(bstack1l1ll1l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ༠"), bstack1l1ll1l_opy_ (u"ࠩࠪ༡")) != bstack1l1ll1l_opy_ (u"ࠪࠫ༢"):
                bstack11l1l1l11l_opy_[bstack1l1ll1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ༣")] = attrs.get(bstack1l1ll1l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭༤"))
            if not self.bstack11l11l1lll_opy_:
                self._11l111l11l_opy_[self._11l11lll1l_opy_()][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༥")].add_step(bstack11l1l1l11l_opy_)
                threading.current_thread().current_step_uuid = bstack11l1l1l11l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡪࡦࠪ༦")]
            self.bstack11l11l1lll_opy_.append(bstack11l1l1l11l_opy_)
    @bstack11l111ll1l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111llllll1_opy_()
        self._11l111111l_opy_(messages)
        current_test_id = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ༧"), None)
        bstack111llll111_opy_ = current_test_id if current_test_id else bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ༨"), None)
        bstack11l11l11l1_opy_ = bstack111lll1ll1_opy_.get(attrs.get(bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༩")), bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ༪"))
        bstack11l11l1l1l_opy_ = attrs.get(bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༫"))
        if bstack11l11l11l1_opy_ != bstack1l1ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ༬") and not attrs.get(bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༭")) and self._111llll1ll_opy_:
            bstack11l11l1l1l_opy_ = self._111llll1ll_opy_
        bstack11l1lll1l1_opy_ = Result(result=bstack11l11l11l1_opy_, exception=bstack11l11l1l1l_opy_, bstack11l1ll1111_opy_=[bstack11l11l1l1l_opy_])
        if attrs.get(bstack1l1ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭༮"), bstack1l1ll1l_opy_ (u"ࠩࠪ༯")).lower() in [bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ༰"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭༱")]:
            bstack111llll111_opy_ = current_test_id if current_test_id else bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ༲"), None)
            if bstack111llll111_opy_:
                bstack11l1l11l11_opy_ = bstack111llll111_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠭ࠣ༳") + attrs.get(bstack1l1ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ༴"), bstack1l1ll1l_opy_ (u"ࠨ༵ࠩ")).lower()
                self._11l111l11l_opy_[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༶")].stop(time=bstack1l1lll1l1_opy_(), duration=int(attrs.get(bstack1l1ll1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ༷"), bstack1l1ll1l_opy_ (u"ࠫ࠵࠭༸"))), result=bstack11l1lll1l1_opy_)
                bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪ༹ࠧ"), self._11l111l11l_opy_[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༺")])
        else:
            bstack111llll111_opy_ = current_test_id if current_test_id else bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩ༻"), None)
            if bstack111llll111_opy_ and len(self.bstack11l11l1lll_opy_) == 1:
                current_step_uuid = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ༼"), None)
                self._11l111l11l_opy_[bstack111llll111_opy_][bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༽")].bstack11l1l1ll1l_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1ll1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ༾"), bstack1l1ll1l_opy_ (u"ࠫ࠵࠭༿"))), result=bstack11l1lll1l1_opy_)
            else:
                self.bstack111llll1l1_opy_(attrs)
            self.bstack11l11l1lll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪཀ"), bstack1l1ll1l_opy_ (u"࠭࡮ࡰࠩཁ")) == bstack1l1ll1l_opy_ (u"ࠧࡺࡧࡶࠫག"):
                return
            self.messages.push(message)
            bstack11l11lllll_opy_ = []
            if bstack11llll1111_opy_.bstack11l1ll11l1_opy_():
                bstack11l11lllll_opy_.append({
                    bstack1l1ll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫགྷ"): bstack1l1lll1l1_opy_(),
                    bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪང"): message.get(bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཅ")),
                    bstack1l1ll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪཆ"): message.get(bstack1l1ll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫཇ")),
                    **bstack11llll1111_opy_.bstack11l1ll11l1_opy_()
                })
                if len(bstack11l11lllll_opy_) > 0:
                    bstack1llllll11_opy_.bstack1ll111lll1_opy_(bstack11l11lllll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1llllll11_opy_.bstack111lllll1l_opy_()
    def bstack111llll1l1_opy_(self, bstack11l11111l1_opy_):
        if not bstack11llll1111_opy_.bstack11l1ll11l1_opy_():
            return
        kwname = bstack1l1ll1l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬ཈").format(bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧཉ")), bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ཊ"), bstack1l1ll1l_opy_ (u"ࠩࠪཋ"))) if bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨཌ"), []) else bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫཌྷ"))
        error_message = bstack1l1ll1l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦཎ").format(kwname, bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ཏ")), str(bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཐ"))))
        bstack111lll111l_opy_ = bstack1l1ll1l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢད").format(kwname, bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩདྷ")))
        bstack111lll1l1l_opy_ = error_message if bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫན")) else bstack111lll111l_opy_
        bstack11l11lll11_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧཔ"): self.bstack11l11l1lll_opy_[-1].get(bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩཕ"), bstack1l1lll1l1_opy_()),
            bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧབ"): bstack111lll1l1l_opy_,
            bstack1l1ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭བྷ"): bstack1l1ll1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧམ") if bstack11l11111l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩཙ")) == bstack1l1ll1l_opy_ (u"ࠪࡊࡆࡏࡌࠨཚ") else bstack1l1ll1l_opy_ (u"ࠫࡎࡔࡆࡐࠩཛ"),
            **bstack11llll1111_opy_.bstack11l1ll11l1_opy_()
        }
        bstack1llllll11_opy_.bstack1ll111lll1_opy_([bstack11l11lll11_opy_])
    def _11l11lll1l_opy_(self):
        for bstack11l1111lll_opy_ in reversed(self._11l111l11l_opy_):
            bstack111lllllll_opy_ = bstack11l1111lll_opy_
            data = self._11l111l11l_opy_[bstack11l1111lll_opy_][bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཛྷ")]
            if isinstance(data, bstack11l1ll1l11_opy_):
                if not bstack1l1ll1l_opy_ (u"࠭ࡅࡂࡅࡋࠫཝ") in data.bstack11l1111ll1_opy_():
                    return bstack111lllllll_opy_
            else:
                return bstack111lllllll_opy_
    def _11l111111l_opy_(self, messages):
        try:
            bstack11l111llll_opy_ = BuiltIn().get_variable_value(bstack1l1ll1l_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨཞ")) in (bstack11l11l1ll1_opy_.DEBUG, bstack11l11l1ll1_opy_.TRACE)
            for message, bstack11l111l1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩཟ"))
                level = message.get(bstack1l1ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨའ"))
                if level == bstack11l11l1ll1_opy_.FAIL:
                    self._111llll1ll_opy_ = name or self._111llll1ll_opy_
                    self._11l11l1111_opy_ = bstack11l111l1ll_opy_.get(bstack1l1ll1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦཡ")) if bstack11l111llll_opy_ and bstack11l111l1ll_opy_ else self._11l11l1111_opy_
        except:
            pass
    @classmethod
    def bstack11l1ll1ll1_opy_(self, event: str, bstack11l11ll1l1_opy_: bstack11l11l1l11_opy_, bstack11l1111111_opy_=False):
        if event == bstack1l1ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ར"):
            bstack11l11ll1l1_opy_.set(hooks=self.store[bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩལ")])
        if event == bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧཤ"):
            event = bstack1l1ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩཥ")
        if bstack11l1111111_opy_:
            bstack111llll11l_opy_ = {
                bstack1l1ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬས"): event,
                bstack11l11ll1l1_opy_.bstack11l11l11ll_opy_(): bstack11l11ll1l1_opy_.bstack11l111ll11_opy_(event)
            }
            self.bstack111lllll11_opy_.append(bstack111llll11l_opy_)
        else:
            bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(event, bstack11l11ll1l1_opy_)
class bstack11l1111l11_opy_:
    def __init__(self):
        self._11l11111ll_opy_ = []
    def bstack111lll1lll_opy_(self):
        self._11l11111ll_opy_.append([])
    def bstack111llllll1_opy_(self):
        return self._11l11111ll_opy_.pop() if self._11l11111ll_opy_ else list()
    def push(self, message):
        self._11l11111ll_opy_[-1].append(message) if self._11l11111ll_opy_ else self._11l11111ll_opy_.append([message])
class bstack11l11l1ll1_opy_:
    FAIL = bstack1l1ll1l_opy_ (u"ࠩࡉࡅࡎࡒࠧཧ")
    ERROR = bstack1l1ll1l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩཨ")
    WARNING = bstack1l1ll1l_opy_ (u"ࠫ࡜ࡇࡒࡏࠩཀྵ")
    bstack11l111l111_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡏࡎࡇࡑࠪཪ")
    DEBUG = bstack1l1ll1l_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬཫ")
    TRACE = bstack1l1ll1l_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭ཬ")
    bstack11l11ll11l_opy_ = [FAIL, ERROR]
def bstack11l11ll1ll_opy_(bstack111lll11l1_opy_):
    if not bstack111lll11l1_opy_:
        return None
    if bstack111lll11l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ཭"), None):
        return getattr(bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ཮")], bstack1l1ll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ཯"), None)
    return bstack111lll11l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ཰"), None)
def bstack111lll11ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳཱࠫ"), bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨི")]:
        return
    if hook_type.lower() == bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵཱི࠭"):
        if current_test_uuid is None:
            return bstack1l1ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐུࠬ")
        else:
            return bstack1l1ll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎཱུࠧ")
    elif hook_type.lower() == bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬྲྀ"):
        if current_test_uuid is None:
            return bstack1l1ll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧཷ")
        else:
            return bstack1l1ll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩླྀ")