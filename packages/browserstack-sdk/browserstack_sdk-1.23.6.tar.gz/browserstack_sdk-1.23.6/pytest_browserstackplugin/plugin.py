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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11lll1l1ll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll1l11ll_opy_, bstack1l1lllllll_opy_, update, bstack11lllll1l1_opy_,
                                       bstack1lll111111_opy_, bstack1l1l1l1ll_opy_, bstack11llllll11_opy_, bstack11ll11ll_opy_,
                                       bstack1ll1111l_opy_, bstack1l11111l1_opy_, bstack1lll1lll1_opy_, bstack1l1l11l111_opy_,
                                       bstack1l11l1l1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11llll_opy_)
from browserstack_sdk.bstack1l1l11ll11_opy_ import bstack1l11lllll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11l1lll11_opy_
from bstack_utils.capture import bstack11l1l1l1ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1lll11_opy_, bstack111lllll_opy_, bstack1ll1llllll_opy_, \
    bstack1lll11l1l_opy_
from bstack_utils.helper import bstack1ll111111l_opy_, bstack111111l111_opy_, bstack11l111l1l1_opy_, bstack1l1l1ll11l_opy_, bstack1lll1lll1l1_opy_, bstack1l1lll1l1_opy_, \
    bstack111111ll11_opy_, \
    bstack1llll1llll1_opy_, bstack11l1l11l_opy_, bstack11l1l1ll1_opy_, bstack1lllll11ll1_opy_, bstack1l1ll111ll_opy_, Notset, \
    bstack1l111111ll_opy_, bstack1llll1lllll_opy_, bstack1llll1ll111_opy_, Result, bstack1lllll1ll11_opy_, bstack1lllll1l1ll_opy_, bstack11l111ll1l_opy_, \
    bstack11llll1l_opy_, bstack1ll1l1llll_opy_, bstack1ll11l1ll1_opy_, bstack1llllll1lll_opy_
from bstack_utils.bstack1lll1ll11l1_opy_ import bstack1lll1l11ll1_opy_
from bstack_utils.messages import bstack1lll1ll1l1_opy_, bstack11lllll1ll_opy_, bstack1l1l1ll1_opy_, bstack1ll1l11l1l_opy_, bstack1l1ll1lll_opy_, \
    bstack1ll1111l1_opy_, bstack1l1l11l11_opy_, bstack1l1ll1l111_opy_, bstack1lll1l111_opy_, bstack11ll1lll11_opy_, \
    bstack1l1ll1l1l1_opy_, bstack1l11ll111l_opy_
from bstack_utils.proxy import bstack11lll1ll_opy_, bstack11l11l1l1_opy_
from bstack_utils.bstack1llllllll_opy_ import bstack1ll1l111111_opy_, bstack1ll11lll11l_opy_, bstack1ll11llllll_opy_, bstack1ll11lll1ll_opy_, \
    bstack1ll11lll1l1_opy_, bstack1ll11ll1ll1_opy_, bstack1ll1l1111l1_opy_, bstack111l111ll_opy_, bstack1ll11llll1l_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1111lllll_opy_
from bstack_utils.bstack11lll1ll1l_opy_ import bstack11l1l1ll_opy_, bstack111llll1l_opy_, bstack11ll111l1l_opy_, \
    bstack1l1llll11_opy_, bstack1lll1l1l1l_opy_
from bstack_utils.bstack11l1lll11l_opy_ import bstack11l1l11ll1_opy_
from bstack_utils.bstack11l1lll111_opy_ import bstack11llll1111_opy_
import bstack_utils.bstack111l1lllll_opy_ as bstack11l11ll1_opy_
from bstack_utils.bstack11l1l11lll_opy_ import bstack1llllll11_opy_
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1ll1ll1ll_opy_
from browserstack_sdk.__init__ import bstack11ll1lll1_opy_
bstack1lllllll1_opy_ = None
bstack1l1111ll1l_opy_ = None
bstack1l1ll11l_opy_ = None
bstack11llll1lll_opy_ = None
bstack1ll1l1ll11_opy_ = None
bstack11111llll_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack11ll1ll11l_opy_ = None
bstack11llll1ll1_opy_ = None
bstack1l1llll1l1_opy_ = None
bstack1llll111l_opy_ = None
bstack111lllll1_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack11111l111_opy_ = bstack1l1ll1l_opy_ (u"ࠪࠫ᢭")
CONFIG = {}
bstack111l11l1_opy_ = False
bstack1ll11lll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࠬ᢮")
bstack111ll1ll_opy_ = bstack1l1ll1l_opy_ (u"ࠬ࠭᢯")
bstack1l1l11111_opy_ = False
bstack11l1l1111_opy_ = []
bstack1lllll1l1l_opy_ = bstack1l1lll11_opy_
bstack1l1ll11ll1l_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᢰ")
bstack11l11ll1l_opy_ = {}
bstack1ll1ll1l_opy_ = None
bstack11ll1111l_opy_ = False
logger = bstack11l1lll11_opy_.get_logger(__name__, bstack1lllll1l1l_opy_)
store = {
    bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᢱ"): []
}
bstack1l1ll11l11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l111l11l_opy_ = {}
current_test_uuid = None
def bstack1llllllll1_opy_(page, bstack1l11l1ll1l_opy_):
    try:
        page.evaluate(bstack1l1ll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᢲ"),
                      bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᢳ") + json.dumps(
                          bstack1l11l1ll1l_opy_) + bstack1l1ll1l_opy_ (u"ࠥࢁࢂࠨᢴ"))
    except Exception as e:
        print(bstack1l1ll1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᢵ"), e)
def bstack111lll1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1ll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᢶ"), bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫᢷ") + json.dumps(
            message) + bstack1l1ll1l_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪᢸ") + json.dumps(level) + bstack1l1ll1l_opy_ (u"ࠨࡿࢀࠫᢹ"))
    except Exception as e:
        print(bstack1l1ll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧᢺ"), e)
def pytest_configure(config):
    bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
    config.args = bstack11llll1111_opy_.bstack1l1lll111ll_opy_(config.args)
    bstack111111111_opy_.bstack11111ll11_opy_(bstack1ll11l1ll1_opy_(config.getoption(bstack1l1ll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᢻ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1l1ll1l1l1l_opy_ = item.config.getoption(bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᢼ"))
    plugins = item.config.getoption(bstack1l1ll1l_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᢽ"))
    report = outcome.get_result()
    bstack1l1ll11ll11_opy_(item, call, report)
    if bstack1l1ll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᢾ") not in plugins or bstack1l1ll111ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1ll1l_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᢿ"), None)
    page = getattr(item, bstack1l1ll1l_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᣀ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1l1ll11lll1_opy_(item, report, summary, bstack1l1ll1l1l1l_opy_)
    if (page is not None):
        bstack1l1ll1l111l_opy_(item, report, summary, bstack1l1ll1l1l1l_opy_)
def bstack1l1ll11lll1_opy_(item, report, summary, bstack1l1ll1l1l1l_opy_):
    if report.when == bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᣁ") and report.skipped:
        bstack1ll11llll1l_opy_(report)
    if report.when in [bstack1l1ll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᣂ"), bstack1l1ll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᣃ")]:
        return
    if not bstack1lll1lll1l1_opy_():
        return
    try:
        if (str(bstack1l1ll1l1l1l_opy_).lower() != bstack1l1ll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᣄ")):
            item._driver.execute_script(
                bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᣅ") + json.dumps(
                    report.nodeid) + bstack1l1ll1l_opy_ (u"ࠧࡾࡿࠪᣆ"))
        os.environ[bstack1l1ll1l_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᣇ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1ll1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᣈ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᣉ")))
    bstack1ll11ll111_opy_ = bstack1l1ll1l_opy_ (u"ࠦࠧᣊ")
    bstack1ll11llll1l_opy_(report)
    if not passed:
        try:
            bstack1ll11ll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1ll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᣋ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11ll111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1ll1l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᣌ")))
        bstack1ll11ll111_opy_ = bstack1l1ll1l_opy_ (u"ࠢࠣᣍ")
        if not passed:
            try:
                bstack1ll11ll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1ll1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᣎ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11ll111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᣏ")
                    + json.dumps(bstack1l1ll1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦᣐ"))
                    + bstack1l1ll1l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᣑ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᣒ")
                    + json.dumps(str(bstack1ll11ll111_opy_))
                    + bstack1l1ll1l_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᣓ")
                )
        except Exception as e:
            summary.append(bstack1l1ll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧᣔ").format(e))
def bstack1l1ll111ll1_opy_(test_name, error_message):
    try:
        bstack1l1ll111l11_opy_ = []
        bstack11lll11l1_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᣕ"), bstack1l1ll1l_opy_ (u"ࠩ࠳ࠫᣖ"))
        bstack1l1ll1ll11_opy_ = {bstack1l1ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᣗ"): test_name, bstack1l1ll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᣘ"): error_message, bstack1l1ll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᣙ"): bstack11lll11l1_opy_}
        bstack1l1ll1lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᣚ"))
        if os.path.exists(bstack1l1ll1lll11_opy_):
            with open(bstack1l1ll1lll11_opy_) as f:
                bstack1l1ll111l11_opy_ = json.load(f)
        bstack1l1ll111l11_opy_.append(bstack1l1ll1ll11_opy_)
        with open(bstack1l1ll1lll11_opy_, bstack1l1ll1l_opy_ (u"ࠧࡸࠩᣛ")) as f:
            json.dump(bstack1l1ll111l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᣜ") + str(e))
def bstack1l1ll1l111l_opy_(item, report, summary, bstack1l1ll1l1l1l_opy_):
    if report.when in [bstack1l1ll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᣝ"), bstack1l1ll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᣞ")]:
        return
    if (str(bstack1l1ll1l1l1l_opy_).lower() != bstack1l1ll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᣟ")):
        bstack1llllllll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll1l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᣠ")))
    bstack1ll11ll111_opy_ = bstack1l1ll1l_opy_ (u"ࠨࠢᣡ")
    bstack1ll11llll1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll11ll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1ll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᣢ").format(e)
                )
        try:
            if passed:
                bstack1lll1l1l1l_opy_(getattr(item, bstack1l1ll1l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᣣ"), None), bstack1l1ll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᣤ"))
            else:
                error_message = bstack1l1ll1l_opy_ (u"ࠪࠫᣥ")
                if bstack1ll11ll111_opy_:
                    bstack111lll1l1_opy_(item._page, str(bstack1ll11ll111_opy_), bstack1l1ll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᣦ"))
                    bstack1lll1l1l1l_opy_(getattr(item, bstack1l1ll1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᣧ"), None), bstack1l1ll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᣨ"), str(bstack1ll11ll111_opy_))
                    error_message = str(bstack1ll11ll111_opy_)
                else:
                    bstack1lll1l1l1l_opy_(getattr(item, bstack1l1ll1l_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᣩ"), None), bstack1l1ll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᣪ"))
                bstack1l1ll111ll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1ll1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨᣫ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l1ll1l_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᣬ"), default=bstack1l1ll1l_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᣭ"), help=bstack1l1ll1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᣮ"))
    parser.addoption(bstack1l1ll1l_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᣯ"), default=bstack1l1ll1l_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᣰ"), help=bstack1l1ll1l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᣱ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1ll1l_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦᣲ"), action=bstack1l1ll1l_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤᣳ"), default=bstack1l1ll1l_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᣴ"),
                         help=bstack1l1ll1l_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᣵ"))
def bstack11l1l1llll_opy_(log):
    if not (log[bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᣶")] and log[bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᣷")].strip()):
        return
    active = bstack11l1ll11l1_opy_()
    log = {
        bstack1l1ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᣸"): log[bstack1l1ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᣹")],
        bstack1l1ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᣺"): bstack11l111l1l1_opy_().isoformat() + bstack1l1ll1l_opy_ (u"ࠫ࡟࠭᣻"),
        bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᣼"): log[bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᣽")],
    }
    if active:
        if active[bstack1l1ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ᣾")] == bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭᣿"):
            log[bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᤀ")] = active[bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᤁ")]
        elif active[bstack1l1ll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᤂ")] == bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᤃ"):
            log[bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᤄ")] = active[bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᤅ")]
    bstack1llllll11_opy_.bstack1ll111lll1_opy_([log])
def bstack11l1ll11l1_opy_():
    if len(store[bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᤆ")]) > 0 and store[bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᤇ")][-1]:
        return {
            bstack1l1ll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᤈ"): bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᤉ"),
            bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᤊ"): store[bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᤋ")][-1]
        }
    if store.get(bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᤌ"), None):
        return {
            bstack1l1ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᤍ"): bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺࠧᤎ"),
            bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᤏ"): store[bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᤐ")]
        }
    return None
bstack11l1l1ll11_opy_ = bstack11l1l1l1ll_opy_(bstack11l1l1llll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1l1ll111lll_opy_ = True
        bstack11l1111l_opy_ = bstack11l11ll1_opy_.bstack11ll1l1ll1_opy_(bstack1llll1llll1_opy_(item.own_markers))
        item._a11y_test_case = bstack11l1111l_opy_
        if bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᤑ"), None):
            driver = getattr(item, bstack1l1ll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᤒ"), None)
            item._a11y_started = bstack11l11ll1_opy_.bstack1l111l11ll_opy_(driver, bstack11l1111l_opy_)
        if not bstack1llllll11_opy_.on() or bstack1l1ll11ll1l_opy_ != bstack1l1ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᤓ"):
            return
        global current_test_uuid, bstack11l1l1ll11_opy_
        bstack11l1l1ll11_opy_.start()
        bstack111lll11l1_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᤔ"): uuid4().__str__(),
            bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᤕ"): bstack11l111l1l1_opy_().isoformat() + bstack1l1ll1l_opy_ (u"ࠪ࡞ࠬᤖ")
        }
        current_test_uuid = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᤗ")]
        store[bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᤘ")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᤙ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l111l11l_opy_[item.nodeid] = {**_11l111l11l_opy_[item.nodeid], **bstack111lll11l1_opy_}
        bstack1l1ll111111_opy_(item, _11l111l11l_opy_[item.nodeid], bstack1l1ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᤚ"))
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪᤛ"), str(err))
def pytest_runtest_setup(item):
    global bstack1l1ll11l11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1lllll11ll1_opy_():
        atexit.register(bstack11lll1111l_opy_)
        if not bstack1l1ll11l11l_opy_:
            try:
                bstack1l1ll1l1111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1llllll1lll_opy_():
                    bstack1l1ll1l1111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1l1ll1l1111_opy_:
                    signal.signal(s, bstack1l1l1llllll_opy_)
                bstack1l1ll11l11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1ll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥᤜ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1l111111_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᤝ")
    try:
        if not bstack1llllll11_opy_.on():
            return
        bstack11l1l1ll11_opy_.start()
        uuid = uuid4().__str__()
        bstack111lll11l1_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᤞ"): uuid,
            bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᤟"): bstack11l111l1l1_opy_().isoformat() + bstack1l1ll1l_opy_ (u"࡚࠭ࠨᤠ"),
            bstack1l1ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᤡ"): bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᤢ"),
            bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᤣ"): bstack1l1ll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᤤ"),
            bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᤥ"): bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᤦ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᤧ")] = item
        store[bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᤨ")] = [uuid]
        if not _11l111l11l_opy_.get(item.nodeid, None):
            _11l111l11l_opy_[item.nodeid] = {bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᤩ"): [], bstack1l1ll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᤪ"): []}
        _11l111l11l_opy_[item.nodeid][bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᤫ")].append(bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᤬")])
        _11l111l11l_opy_[item.nodeid + bstack1l1ll1l_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ᤭")] = bstack111lll11l1_opy_
        bstack1l1ll1ll1ll_opy_(item, bstack111lll11l1_opy_, bstack1l1ll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ᤮"))
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ᤯"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11l11ll1l_opy_
        bstack11lll11l1_opy_ = 0
        if bstack1l1l11111_opy_ is True:
            bstack11lll11l1_opy_ = int(os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᤰ")))
        if bstack1ll11l1l1_opy_.bstack1l1ll1l1_opy_() == bstack1l1ll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᤱ"):
            if bstack1ll11l1l1_opy_.bstack11ll1l1l_opy_() == bstack1l1ll1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᤲ"):
                bstack1l1ll11111l_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᤳ"), None)
                bstack111111l1_opy_ = bstack1l1ll11111l_opy_ + bstack1l1ll1l_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᤴ")
                driver = getattr(item, bstack1l1ll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᤵ"), None)
                bstack1llll1l11_opy_ = getattr(item, bstack1l1ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᤶ"), None)
                bstack11ll11l1_opy_ = getattr(item, bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᤷ"), None)
                PercySDK.screenshot(driver, bstack111111l1_opy_, bstack1llll1l11_opy_=bstack1llll1l11_opy_, bstack11ll11l1_opy_=bstack11ll11l1_opy_, bstack1ll111ll1_opy_=bstack11lll11l1_opy_)
        if getattr(item, bstack1l1ll1l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩᤸ"), False):
            bstack1l11lllll1_opy_.bstack1ll11llll1_opy_(getattr(item, bstack1l1ll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵ᤹ࠫ"), None), bstack11l11ll1l_opy_, logger, item)
        if not bstack1llllll11_opy_.on():
            return
        bstack111lll11l1_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᤺"): uuid4().__str__(),
            bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵ᤻ࠩ"): bstack11l111l1l1_opy_().isoformat() + bstack1l1ll1l_opy_ (u"࡚࠭ࠨ᤼"),
            bstack1l1ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ᤽"): bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭᤾"),
            bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᤿"): bstack1l1ll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ᥀"),
            bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ᥁"): bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ᥂")
        }
        _11l111l11l_opy_[item.nodeid + bstack1l1ll1l_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ᥃")] = bstack111lll11l1_opy_
        bstack1l1ll1ll1ll_opy_(item, bstack111lll11l1_opy_, bstack1l1ll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᥄"))
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ᥅"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1llllll11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1ll11lll1ll_opy_(fixturedef.argname):
        store[bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ᥆")] = request.node
    elif bstack1ll11lll1l1_opy_(fixturedef.argname):
        store[bstack1l1ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ᥇")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l1ll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᥈"): fixturedef.argname,
            bstack1l1ll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᥉"): bstack111111ll11_opy_(outcome),
            bstack1l1ll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ᥊"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᥋")]
        if not _11l111l11l_opy_.get(current_test_item.nodeid, None):
            _11l111l11l_opy_[current_test_item.nodeid] = {bstack1l1ll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ᥌"): []}
        _11l111l11l_opy_[current_test_item.nodeid][bstack1l1ll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ᥍")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭᥎"), str(err))
if bstack1l1ll111ll_opy_() and bstack1llllll11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l111l11l_opy_[request.node.nodeid][bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ᥏")].bstack11l1ll1l1_opy_(id(step))
        except Exception as err:
            print(bstack1l1ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪᥐ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l111l11l_opy_[request.node.nodeid][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᥑ")].bstack11l1l1ll1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1ll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᥒ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11l1lll11l_opy_: bstack11l1l11ll1_opy_ = _11l111l11l_opy_[request.node.nodeid][bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᥓ")]
            bstack11l1lll11l_opy_.bstack11l1l1ll1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1ll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᥔ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1l1ll11ll1l_opy_
        try:
            if not bstack1llllll11_opy_.on() or bstack1l1ll11ll1l_opy_ != bstack1l1ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᥕ"):
                return
            global bstack11l1l1ll11_opy_
            bstack11l1l1ll11_opy_.start()
            driver = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᥖ"), None)
            if not _11l111l11l_opy_.get(request.node.nodeid, None):
                _11l111l11l_opy_[request.node.nodeid] = {}
            bstack11l1lll11l_opy_ = bstack11l1l11ll1_opy_.bstack1ll1111llll_opy_(
                scenario, feature, request.node,
                name=bstack1ll11ll1ll1_opy_(request.node, scenario),
                bstack11l1lll1ll_opy_=bstack1l1lll1l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1ll1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᥗ"),
                tags=bstack1ll1l1111l1_opy_(feature, scenario),
                bstack11l1l11l1l_opy_=bstack1llllll11_opy_.bstack11l1ll1l1l_opy_(driver) if driver and driver.session_id else {}
            )
            _11l111l11l_opy_[request.node.nodeid][bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᥘ")] = bstack11l1lll11l_opy_
            bstack1l1ll11l1l1_opy_(bstack11l1lll11l_opy_.uuid)
            bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᥙ"), bstack11l1lll11l_opy_)
        except Exception as err:
            print(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪᥚ"), str(err))
def bstack1l1ll11llll_opy_(bstack11l1l1lll1_opy_):
    if bstack11l1l1lll1_opy_ in store[bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᥛ")]:
        store[bstack1l1ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᥜ")].remove(bstack11l1l1lll1_opy_)
def bstack1l1ll11l1l1_opy_(bstack11l1llll1l_opy_):
    store[bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᥝ")] = bstack11l1llll1l_opy_
    threading.current_thread().current_test_uuid = bstack11l1llll1l_opy_
@bstack1llllll11_opy_.bstack1l1llllll1l_opy_
def bstack1l1ll11ll11_opy_(item, call, report):
    logger.debug(bstack1l1ll1l_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧᥞ"))
    global bstack1l1ll11ll1l_opy_
    bstack11llllll1l_opy_ = bstack1l1lll1l1_opy_()
    if hasattr(report, bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡱࡳࠫᥟ")):
        bstack11llllll1l_opy_ = bstack1lllll1ll11_opy_(report.stop)
    elif hasattr(report, bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ᥠ")):
        bstack11llllll1l_opy_ = bstack1lllll1ll11_opy_(report.start)
    try:
        if getattr(report, bstack1l1ll1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᥡ"), bstack1l1ll1l_opy_ (u"ࠩࠪᥢ")) == bstack1l1ll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᥣ"):
            bstack11l1l1ll11_opy_.reset()
        if getattr(report, bstack1l1ll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᥤ"), bstack1l1ll1l_opy_ (u"ࠬ࠭ᥥ")) == bstack1l1ll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᥦ"):
            logger.debug(bstack1l1ll1l_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩᥧ").format(getattr(report, bstack1l1ll1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᥨ"), bstack1l1ll1l_opy_ (u"ࠩࠪᥩ")).__str__(), bstack1l1ll11ll1l_opy_))
            if bstack1l1ll11ll1l_opy_ == bstack1l1ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᥪ"):
                _11l111l11l_opy_[item.nodeid][bstack1l1ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᥫ")] = bstack11llllll1l_opy_
                bstack1l1ll111111_opy_(item, _11l111l11l_opy_[item.nodeid], bstack1l1ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᥬ"), report, call)
                store[bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᥭ")] = None
            elif bstack1l1ll11ll1l_opy_ == bstack1l1ll1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ᥮"):
                bstack11l1lll11l_opy_ = _11l111l11l_opy_[item.nodeid][bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ᥯")]
                bstack11l1lll11l_opy_.set(hooks=_11l111l11l_opy_[item.nodeid].get(bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᥰ"), []))
                exception, bstack11l1ll1111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1ll1111_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩᥱ"), bstack1l1ll1l_opy_ (u"ࠫࠬᥲ"))]
                bstack11l1lll11l_opy_.stop(time=bstack11llllll1l_opy_, result=Result(result=getattr(report, bstack1l1ll1l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᥳ"), bstack1l1ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᥴ")), exception=exception, bstack11l1ll1111_opy_=bstack11l1ll1111_opy_))
                bstack1llllll11_opy_.bstack11l1ll1ll1_opy_(bstack1l1ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ᥵"), _11l111l11l_opy_[item.nodeid][bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ᥶")])
        elif getattr(report, bstack1l1ll1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ᥷"), bstack1l1ll1l_opy_ (u"ࠪࠫ᥸")) in [bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ᥹"), bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ᥺")]:
            logger.debug(bstack1l1ll1l_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ᥻").format(getattr(report, bstack1l1ll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬ᥼"), bstack1l1ll1l_opy_ (u"ࠨࠩ᥽")).__str__(), bstack1l1ll11ll1l_opy_))
            bstack11l1l11l11_opy_ = item.nodeid + bstack1l1ll1l_opy_ (u"ࠩ࠰ࠫ᥾") + getattr(report, bstack1l1ll1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ᥿"), bstack1l1ll1l_opy_ (u"ࠫࠬᦀ"))
            if getattr(report, bstack1l1ll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᦁ"), False):
                hook_type = bstack1l1ll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᦂ") if getattr(report, bstack1l1ll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬᦃ"), bstack1l1ll1l_opy_ (u"ࠨࠩᦄ")) == bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᦅ") else bstack1l1ll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᦆ")
                _11l111l11l_opy_[bstack11l1l11l11_opy_] = {
                    bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᦇ"): uuid4().__str__(),
                    bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᦈ"): bstack11llllll1l_opy_,
                    bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᦉ"): hook_type
                }
            _11l111l11l_opy_[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᦊ")] = bstack11llllll1l_opy_
            bstack1l1ll11llll_opy_(_11l111l11l_opy_[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦋ")])
            bstack1l1ll1ll1ll_opy_(item, _11l111l11l_opy_[bstack11l1l11l11_opy_], bstack1l1ll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᦌ"), report, call)
            if getattr(report, bstack1l1ll1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᦍ"), bstack1l1ll1l_opy_ (u"ࠫࠬᦎ")) == bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᦏ"):
                if getattr(report, bstack1l1ll1l_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᦐ"), bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᦑ")) == bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᦒ"):
                    bstack111lll11l1_opy_ = {
                        bstack1l1ll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᦓ"): uuid4().__str__(),
                        bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᦔ"): bstack1l1lll1l1_opy_(),
                        bstack1l1ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦕ"): bstack1l1lll1l1_opy_()
                    }
                    _11l111l11l_opy_[item.nodeid] = {**_11l111l11l_opy_[item.nodeid], **bstack111lll11l1_opy_}
                    bstack1l1ll111111_opy_(item, _11l111l11l_opy_[item.nodeid], bstack1l1ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᦖ"))
                    bstack1l1ll111111_opy_(item, _11l111l11l_opy_[item.nodeid], bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᦗ"), report, call)
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬᦘ"), str(err))
def bstack1l1ll1l1lll_opy_(test, bstack111lll11l1_opy_, result=None, call=None, bstack1ll1l11ll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l1lll11l_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦙ"): bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᦚ")],
        bstack1l1ll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᦛ"): bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᦜ"),
        bstack1l1ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᦝ"): test.name,
        bstack1l1ll1l_opy_ (u"࠭ࡢࡰࡦࡼࠫᦞ"): {
            bstack1l1ll1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᦟ"): bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᦠ"),
            bstack1l1ll1l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᦡ"): inspect.getsource(test.obj)
        },
        bstack1l1ll1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᦢ"): test.name,
        bstack1l1ll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᦣ"): test.name,
        bstack1l1ll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᦤ"): bstack11llll1111_opy_.bstack11l1111l1l_opy_(test),
        bstack1l1ll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᦥ"): file_path,
        bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᦦ"): file_path,
        bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᦧ"): bstack1l1ll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᦨ"),
        bstack1l1ll1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᦩ"): file_path,
        bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᦪ"): bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᦫ")],
        bstack1l1ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᦬"): bstack1l1ll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ᦭"),
        bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ᦮"): {
            bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭᦯"): test.nodeid
        },
        bstack1l1ll1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᦰ"): bstack1llll1llll1_opy_(test.own_markers)
    }
    if bstack1ll1l11ll1_opy_ in [bstack1l1ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᦱ"), bstack1l1ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᦲ")]:
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡶࡤࠫᦳ")] = {
            bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᦴ"): bstack111lll11l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᦵ"), [])
        }
    if bstack1ll1l11ll1_opy_ == bstack1l1ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᦶ"):
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᦷ")] = bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᦸ")
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᦹ")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᦺ")]
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᦻ")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᦼ")]
    if result:
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᦽ")] = result.outcome
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᦾ")] = result.duration * 1000
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦿ")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᧀ")]
        if result.failed:
            bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᧁ")] = bstack1llllll11_opy_.bstack111l1llll1_opy_(call.excinfo.typename)
            bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᧂ")] = bstack1llllll11_opy_.bstack1ll1111ll1l_opy_(call.excinfo, result)
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᧃ")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᧄ")]
    if outcome:
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᧅ")] = bstack111111ll11_opy_(outcome)
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᧆ")] = 0
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᧇ")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᧈ")]
        if bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᧉ")] == bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᧊"):
            bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᧋")] = bstack1l1ll1l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ᧌")  # bstack1l1l1lllll1_opy_
            bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᧍")] = [{bstack1l1ll1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ᧎"): [bstack1l1ll1l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ᧏")]}]
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᧐")] = bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᧑")]
    return bstack11l1lll11l_opy_
def bstack1l1ll1l1ll1_opy_(test, bstack11l1l11111_opy_, bstack1ll1l11ll1_opy_, result, call, outcome, bstack1l1ll1l11ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᧒")]
    hook_name = bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭᧓")]
    hook_data = {
        bstack1l1ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᧔"): bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ᧕")],
        bstack1l1ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ᧖"): bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᧗"),
        bstack1l1ll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᧘"): bstack1l1ll1l_opy_ (u"ࠩࡾࢁࠬ᧙").format(bstack1ll11lll11l_opy_(hook_name)),
        bstack1l1ll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨ᧚"): {
            bstack1l1ll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ᧛"): bstack1l1ll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᧜"),
            bstack1l1ll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫ᧝"): None
        },
        bstack1l1ll1l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭᧞"): test.name,
        bstack1l1ll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ᧟"): bstack11llll1111_opy_.bstack11l1111l1l_opy_(test, hook_name),
        bstack1l1ll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᧠"): file_path,
        bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ᧡"): file_path,
        bstack1l1ll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᧢"): bstack1l1ll1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭᧣"),
        bstack1l1ll1l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ᧤"): file_path,
        bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᧥"): bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᧦")],
        bstack1l1ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ᧧"): bstack1l1ll1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ᧨") if bstack1l1ll11ll1l_opy_ == bstack1l1ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ᧩") else bstack1l1ll1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ᧪"),
        bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ᧫"): hook_type
    }
    bstack1ll11l11111_opy_ = bstack11l11ll1ll_opy_(_11l111l11l_opy_.get(test.nodeid, None))
    if bstack1ll11l11111_opy_:
        hook_data[bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ᧬")] = bstack1ll11l11111_opy_
    if result:
        hook_data[bstack1l1ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᧭")] = result.outcome
        hook_data[bstack1l1ll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ᧮")] = result.duration * 1000
        hook_data[bstack1l1ll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᧯")] = bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᧰")]
        if result.failed:
            hook_data[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ᧱")] = bstack1llllll11_opy_.bstack111l1llll1_opy_(call.excinfo.typename)
            hook_data[bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᧲")] = bstack1llllll11_opy_.bstack1ll1111ll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᧳")] = bstack111111ll11_opy_(outcome)
        hook_data[bstack1l1ll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᧴")] = 100
        hook_data[bstack1l1ll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᧵")] = bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᧶")]
        if hook_data[bstack1l1ll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᧷")] == bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᧸"):
            hook_data[bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ᧹")] = bstack1l1ll1l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ᧺")  # bstack1l1l1lllll1_opy_
            hook_data[bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᧻")] = [{bstack1l1ll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ᧼"): [bstack1l1ll1l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ᧽")]}]
    if bstack1l1ll1l11ll_opy_:
        hook_data[bstack1l1ll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᧾")] = bstack1l1ll1l11ll_opy_.result
        hook_data[bstack1l1ll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭᧿")] = bstack1llll1lllll_opy_(bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᨀ")], bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᨁ")])
        hook_data[bstack1l1ll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᨂ")] = bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᨃ")]
        if hook_data[bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᨄ")] == bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᨅ"):
            hook_data[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᨆ")] = bstack1llllll11_opy_.bstack111l1llll1_opy_(bstack1l1ll1l11ll_opy_.exception_type)
            hook_data[bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᨇ")] = [{bstack1l1ll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᨈ"): bstack1llll1ll111_opy_(bstack1l1ll1l11ll_opy_.exception)}]
    return hook_data
def bstack1l1ll111111_opy_(test, bstack111lll11l1_opy_, bstack1ll1l11ll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬᨉ").format(bstack1ll1l11ll1_opy_))
    bstack11l1lll11l_opy_ = bstack1l1ll1l1lll_opy_(test, bstack111lll11l1_opy_, result, call, bstack1ll1l11ll1_opy_, outcome)
    driver = getattr(test, bstack1l1ll1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᨊ"), None)
    if bstack1ll1l11ll1_opy_ == bstack1l1ll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᨋ") and driver:
        bstack11l1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᨌ")] = bstack1llllll11_opy_.bstack11l1ll1l1l_opy_(driver)
    if bstack1ll1l11ll1_opy_ == bstack1l1ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᨍ"):
        bstack1ll1l11ll1_opy_ = bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᨎ")
    bstack111llll11l_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᨏ"): bstack1ll1l11ll1_opy_,
        bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᨐ"): bstack11l1lll11l_opy_
    }
    bstack1llllll11_opy_.bstack1llll1ll11_opy_(bstack111llll11l_opy_)
    if bstack1ll1l11ll1_opy_ == bstack1l1ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᨑ"):
        threading.current_thread().bstackTestMeta = {bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᨒ"): bstack1l1ll1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᨓ")}
    elif bstack1ll1l11ll1_opy_ == bstack1l1ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᨔ"):
        threading.current_thread().bstackTestMeta = {bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᨕ"): getattr(result, bstack1l1ll1l_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᨖ"), bstack1l1ll1l_opy_ (u"ࠨࠩᨗ"))}
def bstack1l1ll1ll1ll_opy_(test, bstack111lll11l1_opy_, bstack1ll1l11ll1_opy_, result=None, call=None, outcome=None, bstack1l1ll1l11ll_opy_=None):
    logger.debug(bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾᨘࠩ").format(bstack1ll1l11ll1_opy_))
    hook_data = bstack1l1ll1l1ll1_opy_(test, bstack111lll11l1_opy_, bstack1ll1l11ll1_opy_, result, call, outcome, bstack1l1ll1l11ll_opy_)
    bstack111llll11l_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᨙ"): bstack1ll1l11ll1_opy_,
        bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᨚ"): hook_data
    }
    bstack1llllll11_opy_.bstack1llll1ll11_opy_(bstack111llll11l_opy_)
def bstack11l11ll1ll_opy_(bstack111lll11l1_opy_):
    if not bstack111lll11l1_opy_:
        return None
    if bstack111lll11l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᨛ"), None):
        return getattr(bstack111lll11l1_opy_[bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᨜")], bstack1l1ll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᨝"), None)
    return bstack111lll11l1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᨞"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1llllll11_opy_.on():
            return
        places = [bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᨟"), bstack1l1ll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᨠ"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᨡ")]
        bstack11l11lllll_opy_ = []
        for bstack1l1ll1ll11l_opy_ in places:
            records = caplog.get_records(bstack1l1ll1ll11l_opy_)
            bstack1l1ll11l111_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᨢ") if bstack1l1ll1ll11l_opy_ == bstack1l1ll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᨣ") else bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᨤ")
            bstack1l1ll11l1ll_opy_ = request.node.nodeid + (bstack1l1ll1l_opy_ (u"ࠨࠩᨥ") if bstack1l1ll1ll11l_opy_ == bstack1l1ll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᨦ") else bstack1l1ll1l_opy_ (u"ࠪ࠱ࠬᨧ") + bstack1l1ll1ll11l_opy_)
            bstack11l1llll1l_opy_ = bstack11l11ll1ll_opy_(_11l111l11l_opy_.get(bstack1l1ll11l1ll_opy_, None))
            if not bstack11l1llll1l_opy_:
                continue
            for record in records:
                if bstack1lllll1l1ll_opy_(record.message):
                    continue
                bstack11l11lllll_opy_.append({
                    bstack1l1ll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᨨ"): bstack111111l111_opy_(record.created).isoformat() + bstack1l1ll1l_opy_ (u"ࠬࡠࠧᨩ"),
                    bstack1l1ll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᨪ"): record.levelname,
                    bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᨫ"): record.message,
                    bstack1l1ll11l111_opy_: bstack11l1llll1l_opy_
                })
        if len(bstack11l11lllll_opy_) > 0:
            bstack1llllll11_opy_.bstack1ll111lll1_opy_(bstack11l11lllll_opy_)
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᨬ"), str(err))
def bstack1ll111l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11ll1111l_opy_
    bstack1111l111l_opy_ = bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᨭ"), None) and bstack1ll111111l_opy_(
            threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᨮ"), None)
    bstack1ll1l1l1l1_opy_ = getattr(driver, bstack1l1ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᨯ"), None) != None and getattr(driver, bstack1l1ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᨰ"), None) == True
    if sequence == bstack1l1ll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᨱ") and driver != None:
      if not bstack11ll1111l_opy_ and bstack1lll1lll1l1_opy_() and bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨲ") in CONFIG and CONFIG[bstack1l1ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᨳ")] == True and bstack1ll1ll1ll_opy_.bstack1l1l11lll1_opy_(driver_command) and (bstack1ll1l1l1l1_opy_ or bstack1111l111l_opy_) and not bstack1ll11llll_opy_(args):
        try:
          bstack11ll1111l_opy_ = True
          logger.debug(bstack1l1ll1l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫᨴ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1ll1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨᨵ").format(str(err)))
        bstack11ll1111l_opy_ = False
    if sequence == bstack1l1ll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᨶ"):
        if driver_command == bstack1l1ll1l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᨷ"):
            bstack1llllll11_opy_.bstack11l11111_opy_({
                bstack1l1ll1l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᨸ"): response[bstack1l1ll1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᨹ")],
                bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᨺ"): store[bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᨻ")]
            })
def bstack11lll1111l_opy_():
    global bstack11l1l1111_opy_
    bstack11l1lll11_opy_.bstack11ll1111l1_opy_()
    logging.shutdown()
    bstack1llllll11_opy_.bstack111lllll1l_opy_()
    for driver in bstack11l1l1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l1llllll_opy_(*args):
    global bstack11l1l1111_opy_
    bstack1llllll11_opy_.bstack111lllll1l_opy_()
    for driver in bstack11l1l1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1111lll_opy_, stage=STAGE.SINGLE, bstack1l111l1l1l_opy_=bstack1ll1ll1l_opy_)
def bstack1ll11l1l_opy_(self, *args, **kwargs):
    bstack11llll111l_opy_ = bstack1lllllll1_opy_(self, *args, **kwargs)
    bstack1lll11ll1_opy_ = getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫᨼ"), None)
    if bstack1lll11ll1_opy_ and bstack1lll11ll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᨽ"), bstack1l1ll1l_opy_ (u"ࠬ࠭ᨾ")) == bstack1l1ll1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᨿ"):
        bstack1llllll11_opy_.bstack1ll11l1111_opy_(self)
    return bstack11llll111l_opy_
@measure(event_name=EVENTS.bstack1lllll11_opy_, stage=STAGE.bstack111ll1l1l_opy_, bstack1l111l1l1l_opy_=bstack1ll1ll1l_opy_)
def bstack11lll1ll11_opy_(framework_name):
    from bstack_utils.config import Config
    bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
    if bstack111111111_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫᩀ")):
        return
    bstack111111111_opy_.bstack111l1l111_opy_(bstack1l1ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᩁ"), True)
    global bstack11111l111_opy_
    global bstack111ll1l11_opy_
    bstack11111l111_opy_ = framework_name
    logger.info(bstack1l11ll111l_opy_.format(bstack11111l111_opy_.split(bstack1l1ll1l_opy_ (u"ࠩ࠰ࠫᩂ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1lll1lll1l1_opy_():
            Service.start = bstack11llllll11_opy_
            Service.stop = bstack11ll11ll_opy_
            webdriver.Remote.__init__ = bstack1ll1l1l11_opy_
            webdriver.Remote.get = bstack1l1l1l111_opy_
            if not isinstance(os.getenv(bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᩃ")), str):
                return
            WebDriver.close = bstack1ll1111l_opy_
            WebDriver.quit = bstack1lll11l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1lll1lll1l1_opy_() and bstack1llllll11_opy_.on():
            webdriver.Remote.__init__ = bstack1ll11l1l_opy_
        bstack111ll1l11_opy_ = True
    except Exception as e:
        pass
    bstack11l1111ll_opy_()
    if os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᩄ")):
        bstack111ll1l11_opy_ = eval(os.environ.get(bstack1l1ll1l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᩅ")))
    if not bstack111ll1l11_opy_:
        bstack1lll1lll1_opy_(bstack1l1ll1l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᩆ"), bstack1l1ll1l1l1_opy_)
    if bstack1111l1ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l1ll1ll1l_opy_ = bstack1ll11l11_opy_
        except Exception as e:
            logger.error(bstack1ll1111l1_opy_.format(str(e)))
    if bstack1l1ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᩇ") in str(framework_name).lower():
        if not bstack1lll1lll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1lll111111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l1ll_opy_
            Config.getoption = bstack1l11lllll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll11lllll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l111lll_opy_, stage=STAGE.SINGLE, bstack1l111l1l1l_opy_=bstack1ll1ll1l_opy_)
def bstack1lll11l1_opy_(self):
    global bstack11111l111_opy_
    global bstack11ll11ll1l_opy_
    global bstack1l1111ll1l_opy_
    try:
        if bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᩈ") in bstack11111l111_opy_ and self.session_id != None and bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᩉ"), bstack1l1ll1l_opy_ (u"ࠪࠫᩊ")) != bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᩋ"):
            bstack11ll1llll1_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᩌ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᩍ")
            bstack1ll1l1llll_opy_(logger, True)
            if self != None:
                bstack1l1llll11_opy_(self, bstack11ll1llll1_opy_, bstack1l1ll1l_opy_ (u"ࠧ࠭ࠢࠪᩎ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᩏ"), None)
        if item is not None and bstack1ll111111l_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᩐ"), None):
            bstack1l11lllll1_opy_.bstack1ll11llll1_opy_(self, bstack11l11ll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1ll1l_opy_ (u"ࠪࠫᩑ")
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᩒ") + str(e))
    bstack1l1111ll1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l11l1l1_opy_, stage=STAGE.SINGLE, bstack1l111l1l1l_opy_=bstack1ll1ll1l_opy_)
def bstack1ll1l1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll11ll1l_opy_
    global bstack1ll1ll1l_opy_
    global bstack1l1l11111_opy_
    global bstack11111l111_opy_
    global bstack1lllllll1_opy_
    global bstack11l1l1111_opy_
    global bstack1ll11lll1l_opy_
    global bstack111ll1ll_opy_
    global bstack11l11ll1l_opy_
    CONFIG[bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᩓ")] = str(bstack11111l111_opy_) + str(__version__)
    command_executor = bstack11l1l1ll1_opy_(bstack1ll11lll1l_opy_, CONFIG)
    logger.debug(bstack1ll1l11l1l_opy_.format(command_executor))
    proxy = bstack1l11l1l1l_opy_(CONFIG, proxy)
    bstack11lll11l1_opy_ = 0
    try:
        if bstack1l1l11111_opy_ is True:
            bstack11lll11l1_opy_ = int(os.environ.get(bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᩔ")))
    except:
        bstack11lll11l1_opy_ = 0
    bstack1ll1llll1_opy_ = bstack1lll1l11ll_opy_(CONFIG, bstack11lll11l1_opy_)
    logger.debug(bstack1l1ll1l111_opy_.format(str(bstack1ll1llll1_opy_)))
    bstack11l11ll1l_opy_ = CONFIG.get(bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᩕ"))[bstack11lll11l1_opy_]
    if bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᩖ") in CONFIG and CONFIG[bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᩗ")]:
        bstack11ll111l1l_opy_(bstack1ll1llll1_opy_, bstack111ll1ll_opy_)
    if bstack11l11ll1_opy_.bstack1l1l1l11_opy_(CONFIG, bstack11lll11l1_opy_) and bstack11l11ll1_opy_.bstack1ll1l1l1ll_opy_(bstack1ll1llll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack11l11ll1_opy_.set_capabilities(bstack1ll1llll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll1l111ll_opy_ = bstack1l1lllllll_opy_(desired_capabilities)
        bstack1ll1l111ll_opy_[bstack1l1ll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᩘ")] = bstack1l111111ll_opy_(CONFIG)
        bstack1ll1ll11ll_opy_ = bstack1lll1l11ll_opy_(bstack1ll1l111ll_opy_)
        if bstack1ll1ll11ll_opy_:
            bstack1ll1llll1_opy_ = update(bstack1ll1ll11ll_opy_, bstack1ll1llll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l11111l1_opy_(options, bstack1ll1llll1_opy_)
    if not options:
        options = bstack11lllll1l1_opy_(bstack1ll1llll1_opy_)
    if proxy and bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᩙ")):
        options.proxy(proxy)
    if options and bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᩚ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1l11l_opy_() < version.parse(bstack1l1ll1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᩛ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1llll1_opy_)
    logger.info(bstack1l1l1ll1_opy_)
    bstack11lll1l1ll_opy_.end(EVENTS.bstack1lllll11_opy_.value, EVENTS.bstack1lllll11_opy_.value + bstack1l1ll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᩜ"),
                               EVENTS.bstack1lllll11_opy_.value + bstack1l1ll1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᩝ"), True, None)
    if bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᩞ")):
        bstack1lllllll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ᩟")):
        bstack1lllllll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳᩠ࠫ")):
        bstack1lllllll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lllllll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1lll1llll1_opy_ = bstack1l1ll1l_opy_ (u"ࠬ࠭ᩡ")
        if bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧᩢ")):
            bstack1lll1llll1_opy_ = self.caps.get(bstack1l1ll1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᩣ"))
        else:
            bstack1lll1llll1_opy_ = self.capabilities.get(bstack1l1ll1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᩤ"))
        if bstack1lll1llll1_opy_:
            bstack11llll1l_opy_(bstack1lll1llll1_opy_)
            if bstack11l1l11l_opy_() <= version.parse(bstack1l1ll1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᩥ")):
                self.command_executor._url = bstack1l1ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᩦ") + bstack1ll11lll1l_opy_ + bstack1l1ll1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᩧ")
            else:
                self.command_executor._url = bstack1l1ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᩨ") + bstack1lll1llll1_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᩩ")
            logger.debug(bstack11lllll1ll_opy_.format(bstack1lll1llll1_opy_))
        else:
            logger.debug(bstack1lll1ll1l1_opy_.format(bstack1l1ll1l_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᩪ")))
    except Exception as e:
        logger.debug(bstack1lll1ll1l1_opy_.format(e))
    bstack11ll11ll1l_opy_ = self.session_id
    if bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᩫ") in bstack11111l111_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᩬ"), None)
        if item:
            bstack1l1ll1l1l11_opy_ = getattr(item, bstack1l1ll1l_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᩭ"), False)
            if not getattr(item, bstack1l1ll1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᩮ"), None) and bstack1l1ll1l1l11_opy_:
                setattr(store[bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᩯ")], bstack1l1ll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᩰ"), self)
        bstack1lll11ll1_opy_ = getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨᩱ"), None)
        if bstack1lll11ll1_opy_ and bstack1lll11ll1_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᩲ"), bstack1l1ll1l_opy_ (u"ࠩࠪᩳ")) == bstack1l1ll1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᩴ"):
            bstack1llllll11_opy_.bstack1ll11l1111_opy_(self)
    bstack11l1l1111_opy_.append(self)
    if bstack1l1ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᩵") in CONFIG and bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᩶") in CONFIG[bstack1l1ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᩷")][bstack11lll11l1_opy_]:
        bstack1ll1ll1l_opy_ = CONFIG[bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᩸")][bstack11lll11l1_opy_][bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᩹")]
    logger.debug(bstack11ll1lll11_opy_.format(bstack11ll11ll1l_opy_))
@measure(event_name=EVENTS.bstack1ll11l1l11_opy_, stage=STAGE.SINGLE, bstack1l111l1l1l_opy_=bstack1ll1ll1l_opy_)
def bstack1l1l1l111_opy_(self, url):
    global bstack11llll1ll1_opy_
    global CONFIG
    try:
        bstack111llll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lll1l111_opy_.format(str(err)))
    try:
        bstack11llll1ll1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1ll11l1_opy_ = str(e)
            if any(err_msg in bstack1l1ll11l1_opy_ for err_msg in bstack1ll1llllll_opy_):
                bstack111llll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lll1l111_opy_.format(str(err)))
        raise e
def bstack1111llll_opy_(item, when):
    global bstack111lllll1_opy_
    try:
        bstack111lllll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11lllll_opy_(item, call, rep):
    global bstack1llll1ll1l_opy_
    global bstack11l1l1111_opy_
    name = bstack1l1ll1l_opy_ (u"ࠩࠪ᩺")
    try:
        if rep.when == bstack1l1ll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ᩻"):
            bstack11ll11ll1l_opy_ = threading.current_thread().bstackSessionId
            bstack1l1ll1l1l1l_opy_ = item.config.getoption(bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᩼"))
            try:
                if (str(bstack1l1ll1l1l1l_opy_).lower() != bstack1l1ll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ᩽")):
                    name = str(rep.nodeid)
                    bstack1l1l1l11ll_opy_ = bstack11l1l1ll_opy_(bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᩾"), name, bstack1l1ll1l_opy_ (u"ࠧࠨ᩿"), bstack1l1ll1l_opy_ (u"ࠨࠩ᪀"), bstack1l1ll1l_opy_ (u"ࠩࠪ᪁"), bstack1l1ll1l_opy_ (u"ࠪࠫ᪂"))
                    os.environ[bstack1l1ll1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ᪃")] = name
                    for driver in bstack11l1l1111_opy_:
                        if bstack11ll11ll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1l11ll_opy_)
            except Exception as e:
                logger.debug(bstack1l1ll1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ᪄").format(str(e)))
            try:
                bstack111l111ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᪅"):
                    status = bstack1l1ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᪆") if rep.outcome.lower() == bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᪇") else bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᪈")
                    reason = bstack1l1ll1l_opy_ (u"ࠪࠫ᪉")
                    if status == bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᪊"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1ll1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ᪋") if status == bstack1l1ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᪌") else bstack1l1ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᪍")
                    data = name + bstack1l1ll1l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ᪎") if status == bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᪏") else name + bstack1l1ll1l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭᪐") + reason
                    bstack1l1111111l_opy_ = bstack11l1l1ll_opy_(bstack1l1ll1l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭᪑"), bstack1l1ll1l_opy_ (u"ࠬ࠭᪒"), bstack1l1ll1l_opy_ (u"࠭ࠧ᪓"), bstack1l1ll1l_opy_ (u"ࠧࠨ᪔"), level, data)
                    for driver in bstack11l1l1111_opy_:
                        if bstack11ll11ll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1111111l_opy_)
            except Exception as e:
                logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ᪕").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭᪖").format(str(e)))
    bstack1llll1ll1l_opy_(item, call, rep)
notset = Notset()
def bstack1l11lllll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll111l_opy_
    if str(name).lower() == bstack1l1ll1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ᪗"):
        return bstack1l1ll1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ᪘")
    else:
        return bstack1llll111l_opy_(self, name, default, skip)
def bstack1ll11l11_opy_(self):
    global CONFIG
    global bstack1lll11l1l1_opy_
    try:
        proxy = bstack11lll1ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1ll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ᪙")):
                proxies = bstack11l11l1l1_opy_(proxy, bstack11l1l1ll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll1l1ll_opy_ = proxies.popitem()
                    if bstack1l1ll1l_opy_ (u"ࠨ࠺࠰࠱ࠥ᪚") in bstack1lll1l1ll_opy_:
                        return bstack1lll1l1ll_opy_
                    else:
                        return bstack1l1ll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᪛") + bstack1lll1l1ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1ll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ᪜").format(str(e)))
    return bstack1lll11l1l1_opy_(self)
def bstack1111l1ll_opy_():
    return (bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᪝") in CONFIG or bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᪞") in CONFIG) and bstack1l1l1ll11l_opy_() and bstack11l1l11l_opy_() >= version.parse(
        bstack111lllll_opy_)
def bstack1111l11ll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1ll1l_opy_
    global bstack1l1l11111_opy_
    global bstack11111l111_opy_
    CONFIG[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᪟")] = str(bstack11111l111_opy_) + str(__version__)
    bstack11lll11l1_opy_ = 0
    try:
        if bstack1l1l11111_opy_ is True:
            bstack11lll11l1_opy_ = int(os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᪠")))
    except:
        bstack11lll11l1_opy_ = 0
    CONFIG[bstack1l1ll1l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ᪡")] = True
    bstack1ll1llll1_opy_ = bstack1lll1l11ll_opy_(CONFIG, bstack11lll11l1_opy_)
    logger.debug(bstack1l1ll1l111_opy_.format(str(bstack1ll1llll1_opy_)))
    if CONFIG.get(bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᪢")):
        bstack11ll111l1l_opy_(bstack1ll1llll1_opy_, bstack111ll1ll_opy_)
    if bstack1l1ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᪣") in CONFIG and bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᪤") in CONFIG[bstack1l1ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᪥")][bstack11lll11l1_opy_]:
        bstack1ll1ll1l_opy_ = CONFIG[bstack1l1ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᪦")][bstack11lll11l1_opy_][bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᪧ")]
    import urllib
    import json
    if bstack1l1ll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᪨") in CONFIG and str(CONFIG[bstack1l1ll1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᪩")]).lower() != bstack1l1ll1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ᪪"):
        bstack11lllll11l_opy_ = bstack11ll1lll1_opy_()
        bstack1l1lllll11_opy_ = bstack11lllll11l_opy_ + urllib.parse.quote(json.dumps(bstack1ll1llll1_opy_))
    else:
        bstack1l1lllll11_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ᪫") + urllib.parse.quote(json.dumps(bstack1ll1llll1_opy_))
    browser = self.connect(bstack1l1lllll11_opy_)
    return browser
def bstack11l1111ll_opy_():
    global bstack111ll1l11_opy_
    global bstack11111l111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111ll1_opy_
        if not bstack1lll1lll1l1_opy_():
            global bstack1l1ll1l11_opy_
            if not bstack1l1ll1l11_opy_:
                from bstack_utils.helper import bstack1l111ll11l_opy_, bstack111l1lll1_opy_
                bstack1l1ll1l11_opy_ = bstack1l111ll11l_opy_()
                bstack111l1lll1_opy_(bstack11111l111_opy_)
            BrowserType.connect = bstack1l111ll1_opy_
            return
        BrowserType.launch = bstack1111l11ll_opy_
        bstack111ll1l11_opy_ = True
    except Exception as e:
        pass
def bstack1l1ll1l11l1_opy_():
    global CONFIG
    global bstack111l11l1_opy_
    global bstack1ll11lll1l_opy_
    global bstack111ll1ll_opy_
    global bstack1l1l11111_opy_
    global bstack1lllll1l1l_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ᪬")))
    bstack111l11l1_opy_ = eval(os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ᪭")))
    bstack1ll11lll1l_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ᪮"))
    bstack1l1l11l111_opy_(CONFIG, bstack111l11l1_opy_)
    bstack1lllll1l1l_opy_ = bstack11l1lll11_opy_.bstack1l11l11111_opy_(CONFIG, bstack1lllll1l1l_opy_)
    global bstack1lllllll1_opy_
    global bstack1l1111ll1l_opy_
    global bstack1l1ll11l_opy_
    global bstack11llll1lll_opy_
    global bstack1ll1l1ll11_opy_
    global bstack11111llll_opy_
    global bstack11ll1ll11l_opy_
    global bstack11llll1ll1_opy_
    global bstack1lll11l1l1_opy_
    global bstack1llll111l_opy_
    global bstack111lllll1_opy_
    global bstack1llll1ll1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lllllll1_opy_ = webdriver.Remote.__init__
        bstack1l1111ll1l_opy_ = WebDriver.quit
        bstack11ll1ll11l_opy_ = WebDriver.close
        bstack11llll1ll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᪯") in CONFIG or bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᪰") in CONFIG) and bstack1l1l1ll11l_opy_():
        if bstack11l1l11l_opy_() < version.parse(bstack111lllll_opy_):
            logger.error(bstack1l1l11l11_opy_.format(bstack11l1l11l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1lll11l1l1_opy_ = RemoteConnection._1l1ll1ll1l_opy_
            except Exception as e:
                logger.error(bstack1ll1111l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll111l_opy_ = Config.getoption
        from _pytest import runner
        bstack111lllll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1ll1lll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llll1ll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ᪱"))
    bstack111ll1ll_opy_ = CONFIG.get(bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭᪲"), {}).get(bstack1l1ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᪳"))
    bstack1l1l11111_opy_ = True
    bstack11lll1ll11_opy_(bstack1lll11l1l_opy_)
if (bstack1lllll11ll1_opy_()):
    bstack1l1ll1l11l1_opy_()
@bstack11l111ll1l_opy_(class_method=False)
def bstack1l1ll1111ll_opy_(hook_name, event, bstack1l1ll111l1l_opy_=None):
    if hook_name not in [bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ᪴"), bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯᪵ࠩ"), bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩ᪶ࠬ"), bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦ᪷ࠩ"), bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ᪸࠭"), bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵ᪹ࠪ"), bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥ᪺ࠩ"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᪻")]:
        return
    node = store[bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᪼")]
    if hook_name in [bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩ᪽ࠬ"), bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ᪾")]:
        node = store[bstack1l1ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳᪿࠧ")]
    elif hook_name in [bstack1l1ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹᫀࠧ"), bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ᫁")]:
        node = store[bstack1l1ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ᫂")]
    if event == bstack1l1ll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩ᫃ࠬ"):
        hook_type = bstack1ll11llllll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l1l11111_opy_ = {
            bstack1l1ll1l_opy_ (u"࠭ࡵࡶ࡫ࡧ᫄ࠫ"): uuid,
            bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᫅"): bstack1l1lll1l1_opy_(),
            bstack1l1ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭᫆"): bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᫇"),
            bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᫈"): hook_type,
            bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ᫉"): hook_name
        }
        store[bstack1l1ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥ᫊ࠩ")].append(uuid)
        bstack1l1ll1ll111_opy_ = node.nodeid
        if hook_type == bstack1l1ll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ᫋"):
            if not _11l111l11l_opy_.get(bstack1l1ll1ll111_opy_, None):
                _11l111l11l_opy_[bstack1l1ll1ll111_opy_] = {bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᫌ"): []}
            _11l111l11l_opy_[bstack1l1ll1ll111_opy_][bstack1l1ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᫍ")].append(bstack11l1l11111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᫎ")])
        _11l111l11l_opy_[bstack1l1ll1ll111_opy_ + bstack1l1ll1l_opy_ (u"ࠪ࠱ࠬ᫏") + hook_name] = bstack11l1l11111_opy_
        bstack1l1ll1ll1ll_opy_(node, bstack11l1l11111_opy_, bstack1l1ll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ᫐"))
    elif event == bstack1l1ll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᫑"):
        bstack11l1l11l11_opy_ = node.nodeid + bstack1l1ll1l_opy_ (u"࠭࠭ࠨ᫒") + hook_name
        _11l111l11l_opy_[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᫓")] = bstack1l1lll1l1_opy_()
        bstack1l1ll11llll_opy_(_11l111l11l_opy_[bstack11l1l11l11_opy_][bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᫔")])
        bstack1l1ll1ll1ll_opy_(node, _11l111l11l_opy_[bstack11l1l11l11_opy_], bstack1l1ll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᫕"), bstack1l1ll1l11ll_opy_=bstack1l1ll111l1l_opy_)
def bstack1l1ll1111l1_opy_():
    global bstack1l1ll11ll1l_opy_
    if bstack1l1ll111ll_opy_():
        bstack1l1ll11ll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ᫖")
    else:
        bstack1l1ll11ll1l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᫗")
@bstack1llllll11_opy_.bstack1l1llllll1l_opy_
def bstack1l1ll1ll1l1_opy_():
    bstack1l1ll1111l1_opy_()
    if bstack1l1l1ll11l_opy_():
        bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
        if bstack111111111_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ᫘")):
            return
        bstack1111lllll_opy_(bstack1ll111l1_opy_)
    try:
        bstack1lll1l11ll1_opy_(bstack1l1ll1111ll_opy_)
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ᫙").format(e))
bstack1l1ll1ll1l1_opy_()