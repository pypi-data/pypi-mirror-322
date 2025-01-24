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
from filelock import FileLock
import json
import os
import time
import uuid
from typing import Dict, List, Optional
from bstack_utils.constants import bstack11l1ll111_opy_, EVENTS
from bstack_utils.helper import bstack11ll1111ll_opy_, get_host_info, bstack111111111_opy_
from datetime import datetime
from bstack_utils.bstack11l1lll11_opy_ import get_logger
logger = get_logger(__name__)
bstack1ll1l11ll1l_opy_: Dict[str, float] = {}
bstack1ll1l11ll11_opy_: List = []
bstack1lll1l1l1_opy_ = os.path.join(os.getcwd(), bstack1l1ll1l_opy_ (u"ࠬࡲ࡯ࡨࠩᙸ"), bstack1l1ll1l_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩᙹ"))
lock = FileLock(bstack1lll1l1l1_opy_+bstack1l1ll1l_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᙺ"))
class bstack1ll1l11l1l1_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    def __init__(self, duration: float, name: str, start_time: float, bstack1ll1l11l1ll_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1ll1l11l1ll_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1ll1l_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࠤᙻ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
class bstack111l1ll11l_opy_:
    global bstack1ll1l11ll1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1ll1l11ll1l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1ll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᙼ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack111l1ll11l_opy_.mark(end)
            bstack111l1ll11l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1ll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᙽ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1ll1l11ll1l_opy_ or end not in bstack1ll1l11ll1l_opy_:
                logger.debug(bstack1l1ll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨᙾ").format(start,end))
                return
            duration: float = bstack1ll1l11ll1l_opy_[end] - bstack1ll1l11ll1l_opy_[start]
            bstack1ll1l11lll1_opy_: bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_(duration, label, bstack1ll1l11ll1l_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᙿ"), 0), command, test_name, hook_type)
            del bstack1ll1l11ll1l_opy_[start]
            del bstack1ll1l11ll1l_opy_[end]
            bstack111l1ll11l_opy_.bstack1ll1l11llll_opy_(bstack1ll1l11lll1_opy_)
        except Exception as e:
            logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ ").format(e))
    @staticmethod
    def bstack1ll1l11llll_opy_(bstack1ll1l11lll1_opy_):
        os.makedirs(os.path.dirname(bstack1lll1l1l1_opy_)) if not os.path.exists(os.path.dirname(bstack1lll1l1l1_opy_)) else None
        try:
            with lock:
                with open(bstack1lll1l1l1_opy_, bstack1l1ll1l_opy_ (u"ࠢࡳ࠭ࠥᚁ"), encoding=bstack1l1ll1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᚂ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1ll1l11lll1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError:
            with lock:
                with open(bstack1lll1l1l1_opy_, bstack1l1ll1l_opy_ (u"ࠤࡺࠦᚃ"), encoding=bstack1l1ll1l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᚄ")) as file:
                    data = [bstack1ll1l11lll1_opy_.__dict__]
                    json.dump(data, file, indent=4)
    @staticmethod
    def bstack1111ll1lll_opy_(label: str) -> str:
        try:
            return bstack1l1ll1l_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥᚅ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1ll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᚆ").format(e))