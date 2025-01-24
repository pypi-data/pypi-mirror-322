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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11111l1ll1_opy_, bstack1lllll11l_opy_, bstack1l1lll1111_opy_, bstack1111l1l1l_opy_,
                                    bstack1111l111l1_opy_, bstack1111l11l1l_opy_, bstack11111l11ll_opy_, bstack11111l1111_opy_)
from bstack_utils.messages import bstack1ll1lll1ll_opy_, bstack1ll1111l1_opy_
from bstack_utils.proxy import bstack11l1lllll_opy_, bstack11lll1ll_opy_
bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
logger = logging.getLogger(__name__)
def bstack111l1l11l1_opy_(config):
    return config[bstack1l1ll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᎋ")]
def bstack1111lll11l_opy_(config):
    return config[bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᎌ")]
def bstack1llll1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1lll1lllll1_opy_(obj):
    values = []
    bstack1lllll11111_opy_ = re.compile(bstack1l1ll1l_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᎍ"), re.I)
    for key in obj.keys():
        if bstack1lllll11111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1lll1ll1lll_opy_(config):
    tags = []
    tags.extend(bstack1lll1lllll1_opy_(os.environ))
    tags.extend(bstack1lll1lllll1_opy_(config))
    return tags
def bstack1llll1llll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llllll11l1_opy_(bstack1lllll11l1l_opy_):
    if not bstack1lllll11l1l_opy_:
        return bstack1l1ll1l_opy_ (u"ࠨࠩᎎ")
    return bstack1l1ll1l_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᎏ").format(bstack1lllll11l1l_opy_.name, bstack1lllll11l1l_opy_.email)
def bstack111l1l1ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111111l1ll_opy_ = repo.common_dir
        info = {
            bstack1l1ll1l_opy_ (u"ࠥࡷ࡭ࡧࠢ᎐"): repo.head.commit.hexsha,
            bstack1l1ll1l_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢ᎑"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧ᎒"): repo.active_branch.name,
            bstack1l1ll1l_opy_ (u"ࠨࡴࡢࡩࠥ᎓"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1ll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥ᎔"): bstack1llllll11l1_opy_(repo.head.commit.committer),
            bstack1l1ll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤ᎕"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1ll1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤ᎖"): bstack1llllll11l1_opy_(repo.head.commit.author),
            bstack1l1ll1l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣ᎗"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1ll1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ᎘"): repo.head.commit.message,
            bstack1l1ll1l_opy_ (u"ࠧࡸ࡯ࡰࡶࠥ᎙"): repo.git.rev_parse(bstack1l1ll1l_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣ᎚")),
            bstack1l1ll1l_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ᎛"): bstack111111l1ll_opy_,
            bstack1l1ll1l_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ᎜"): subprocess.check_output([bstack1l1ll1l_opy_ (u"ࠤࡪ࡭ࡹࠨ᎝"), bstack1l1ll1l_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨ᎞"), bstack1l1ll1l_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢ᎟")]).strip().decode(
                bstack1l1ll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᎠ")),
            bstack1l1ll1l_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᎡ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1ll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᎢ"): repo.git.rev_list(
                bstack1l1ll1l_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣᎣ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llll1lll11_opy_ = []
        for remote in remotes:
            bstack1llllll1111_opy_ = {
                bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎤ"): remote.name,
                bstack1l1ll1l_opy_ (u"ࠥࡹࡷࡲࠢᎥ"): remote.url,
            }
            bstack1llll1lll11_opy_.append(bstack1llllll1111_opy_)
        bstack1lll1lll11l_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᎦ"): bstack1l1ll1l_opy_ (u"ࠧ࡭ࡩࡵࠤᎧ"),
            **info,
            bstack1l1ll1l_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢᎨ"): bstack1llll1lll11_opy_
        }
        bstack1lll1lll11l_opy_ = bstack1llll1l111l_opy_(bstack1lll1lll11l_opy_)
        return bstack1lll1lll11l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᎩ").format(err))
        return {}
def bstack1llll1l111l_opy_(bstack1lll1lll11l_opy_):
    bstack1llll1lll1l_opy_ = bstack111111l1l1_opy_(bstack1lll1lll11l_opy_)
    if bstack1llll1lll1l_opy_ and bstack1llll1lll1l_opy_ > bstack1111l111l1_opy_:
        bstack1llll1l1lll_opy_ = bstack1llll1lll1l_opy_ - bstack1111l111l1_opy_
        bstack1lllllll1ll_opy_ = bstack1lllllllll1_opy_(bstack1lll1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᎪ")], bstack1llll1l1lll_opy_)
        bstack1lll1lll11l_opy_[bstack1l1ll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᎫ")] = bstack1lllllll1ll_opy_
        logger.info(bstack1l1ll1l_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧᎬ")
                    .format(bstack111111l1l1_opy_(bstack1lll1lll11l_opy_) / 1024))
    return bstack1lll1lll11l_opy_
def bstack111111l1l1_opy_(bstack1l111l1ll_opy_):
    try:
        if bstack1l111l1ll_opy_:
            bstack1lll1lll1ll_opy_ = json.dumps(bstack1l111l1ll_opy_)
            bstack1lllllll1l1_opy_ = sys.getsizeof(bstack1lll1lll1ll_opy_)
            return bstack1lllllll1l1_opy_
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦᎭ").format(e))
    return -1
def bstack1lllllllll1_opy_(field, bstack1111111lll_opy_):
    try:
        bstack1llll1l1l1l_opy_ = len(bytes(bstack1111l11l1l_opy_, bstack1l1ll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᎮ")))
        bstack1llllll111l_opy_ = bytes(field, bstack1l1ll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᎯ"))
        bstack11111111ll_opy_ = len(bstack1llllll111l_opy_)
        bstack1lllll111ll_opy_ = ceil(bstack11111111ll_opy_ - bstack1111111lll_opy_ - bstack1llll1l1l1l_opy_)
        if bstack1lllll111ll_opy_ > 0:
            bstack1llll1111ll_opy_ = bstack1llllll111l_opy_[:bstack1lllll111ll_opy_].decode(bstack1l1ll1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ꮀ"), errors=bstack1l1ll1l_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨᎱ")) + bstack1111l11l1l_opy_
            return bstack1llll1111ll_opy_
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢᎲ").format(e))
    return field
def bstack1ll1ll11l1_opy_():
    env = os.environ
    if (bstack1l1ll1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᎳ") in env and len(env[bstack1l1ll1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᎴ")]) > 0) or (
            bstack1l1ll1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᎵ") in env and len(env[bstack1l1ll1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᎶ")]) > 0):
        return {
            bstack1l1ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᎷ"): bstack1l1ll1l_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤᎸ"),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᎹ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᎺ")),
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎻ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢᎼ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎽ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᎾ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡌࠦᎿ")) == bstack1l1ll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᏀ") and bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧᏁ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏂ"): bstack1l1ll1l_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢᏃ"),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᏄ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᏅ")),
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᏆ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨᏇ")),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᏈ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢᏉ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡉࠣᏊ")) == bstack1l1ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᏋ") and bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢᏌ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᏍ"): bstack1l1ll1l_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧᏎ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏏ"): env.get(bstack1l1ll1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦᏐ")),
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏑ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᏒ")),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏓ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᏔ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡍࠧᏕ")) == bstack1l1ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᏖ") and env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧᏗ")) == bstack1l1ll1l_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢᏘ"):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏙ"): bstack1l1ll1l_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᏚ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᏛ"): None,
            bstack1l1ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏜ"): None,
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᏝ"): None
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᏞ")) and env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᏟ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏠ"): bstack1l1ll1l_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᏡ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᏢ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᏣ")),
            bstack1l1ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏤ"): None,
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏥ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᏦ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡊࠤᏧ")) == bstack1l1ll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᏨ") and bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᏩ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏪ"): bstack1l1ll1l_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᏫ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᏬ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᏭ")),
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᏮ"): None,
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏯ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᏰ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡍࠧᏱ")) == bstack1l1ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᏲ") and bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᏳ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏴ"): bstack1l1ll1l_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᏵ"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᏶"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢ᏷")),
            bstack1l1ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏸ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᏹ")),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏺ"): env.get(bstack1l1ll1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᏻ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡊࠤᏼ")) == bstack1l1ll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᏽ") and bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦ᏾"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᏿"): bstack1l1ll1l_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥ᐀"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᐁ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᐂ")),
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐃ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᐄ")),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐅ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᐆ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡎࠨᐇ")) == bstack1l1ll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᐈ") and bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᐉ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐊ"): bstack1l1ll1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᐋ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐌ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᐍ")),
            bstack1l1ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᐎ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᐏ")) or env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᐐ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐑ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᐒ"))
        }
    if bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᐓ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᐔ"): bstack1l1ll1l_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᐕ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᐖ"): bstack1l1ll1l_opy_ (u"ࠧࢁࡽࡼࡿࠥᐗ").format(env.get(bstack1l1ll1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᐘ")), env.get(bstack1l1ll1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᐙ"))),
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐚ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᐛ")),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐜ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᐝ"))
        }
    if bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᐞ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐟ"): bstack1l1ll1l_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᐠ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐡ"): bstack1l1ll1l_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᐢ").format(env.get(bstack1l1ll1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᐣ")), env.get(bstack1l1ll1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᐤ")), env.get(bstack1l1ll1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᐥ")), env.get(bstack1l1ll1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᐦ"))),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᐧ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᐨ")),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᐩ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᐪ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᐫ")) and env.get(bstack1l1ll1l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᐬ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐭ"): bstack1l1ll1l_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᐮ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐯ"): bstack1l1ll1l_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᐰ").format(env.get(bstack1l1ll1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᐱ")), env.get(bstack1l1ll1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᐲ")), env.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᐳ"))),
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐴ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᐵ")),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐶ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᐷ"))
        }
    if any([env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᐸ")), env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᐹ")), env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᐺ"))]):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐻ"): bstack1l1ll1l_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᐼ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐽ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᐾ")),
            bstack1l1ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᐿ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᑀ")),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᑁ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᑂ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᑃ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᑄ"): bstack1l1ll1l_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᑅ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᑆ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᑇ")),
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᑈ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᑉ")),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᑊ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᑋ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᑌ")) or env.get(bstack1l1ll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᑍ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᑎ"): bstack1l1ll1l_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨᑏ"),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᑐ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᑑ")),
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᑒ"): bstack1l1ll1l_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤᑓ") if env.get(bstack1l1ll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᑔ")) else None,
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᑕ"): env.get(bstack1l1ll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥᑖ"))
        }
    if any([env.get(bstack1l1ll1l_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦᑗ")), env.get(bstack1l1ll1l_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᑘ")), env.get(bstack1l1ll1l_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᑙ"))]):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᑚ"): bstack1l1ll1l_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᑛ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᑜ"): None,
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᑝ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᑞ")),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᑟ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᑠ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᑡ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᑢ"): bstack1l1ll1l_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᑣ"),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᑤ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᑥ")),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᑦ"): bstack1l1ll1l_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᑧ").format(env.get(bstack1l1ll1l_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᑨ"))) if env.get(bstack1l1ll1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨᑩ")) else None,
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᑪ"): env.get(bstack1l1ll1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᑫ"))
        }
    if bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢᑬ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᑭ"): bstack1l1ll1l_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤᑮ"),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᑯ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢᑰ")),
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᑱ"): env.get(bstack1l1ll1l_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣᑲ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᑳ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᑴ"))
        }
    if bstack1ll11l1ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤᑵ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᑶ"): bstack1l1ll1l_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦᑷ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᑸ"): bstack1l1ll1l_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᑹ").format(env.get(bstack1l1ll1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪᑺ")), env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫᑻ")), env.get(bstack1l1ll1l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨᑼ"))),
            bstack1l1ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᑽ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧᑾ")),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᑿ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᒀ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡊࠤᒁ")) == bstack1l1ll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᒂ") and env.get(bstack1l1ll1l_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᒃ")) == bstack1l1ll1l_opy_ (u"ࠤ࠴ࠦᒄ"):
        return {
            bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᒅ"): bstack1l1ll1l_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᒆ"),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᒇ"): bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᒈ").format(env.get(bstack1l1ll1l_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫᒉ"))),
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᒊ"): None,
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᒋ"): None,
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᒌ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᒍ"): bstack1l1ll1l_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢᒎ"),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᒏ"): None,
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᒐ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤᒑ")),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᒒ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᒓ"))
        }
    if any([env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᒔ")), env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᒕ")), env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᒖ")), env.get(bstack1l1ll1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᒗ"))]):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᒘ"): bstack1l1ll1l_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᒙ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᒚ"): None,
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᒛ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᒜ")) or None,
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᒝ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᒞ"), 0)
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᒟ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒠ"): bstack1l1ll1l_opy_ (u"ࠥࡋࡴࡉࡄࠣᒡ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᒢ"): None,
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᒣ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᒤ")),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᒥ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᒦ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᒧ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᒨ"): bstack1l1ll1l_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢᒩ"),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᒪ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᒫ")),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᒬ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᒭ")),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᒮ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᒯ"))
        }
    return {bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᒰ"): None}
def get_host_info():
    return {
        bstack1l1ll1l_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢᒱ"): platform.node(),
        bstack1l1ll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣᒲ"): platform.system(),
        bstack1l1ll1l_opy_ (u"ࠢࡵࡻࡳࡩࠧᒳ"): platform.machine(),
        bstack1l1ll1l_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᒴ"): platform.version(),
        bstack1l1ll1l_opy_ (u"ࠤࡤࡶࡨ࡮ࠢᒵ"): platform.architecture()[0]
    }
def bstack1l1l1ll11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1lllll1lll1_opy_():
    if bstack111111111_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᒶ")):
        return bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᒷ")
    return bstack1l1ll1l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫᒸ")
def bstack1lllllll11l_opy_(driver):
    info = {
        bstack1l1ll1l_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᒹ"): driver.capabilities,
        bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᒺ"): driver.session_id,
        bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᒻ"): driver.capabilities.get(bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᒼ"), None),
        bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᒽ"): driver.capabilities.get(bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᒾ"), None),
        bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᒿ"): driver.capabilities.get(bstack1l1ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᓀ"), None),
    }
    if bstack1lllll1lll1_opy_() == bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᓁ"):
        if bstack11llll1l1_opy_():
            info[bstack1l1ll1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᓂ")] = bstack1l1ll1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᓃ")
        elif driver.capabilities.get(bstack1l1ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᓄ"), {}).get(bstack1l1ll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᓅ"), False):
            info[bstack1l1ll1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᓆ")] = bstack1l1ll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᓇ")
        else:
            info[bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᓈ")] = bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᓉ")
    return info
def bstack11llll1l1_opy_():
    if bstack111111111_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᓊ")):
        return True
    if bstack1ll11l1ll1_opy_(os.environ.get(bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᓋ"), None)):
        return True
    return False
def bstack11ll1111ll_opy_(bstack1llll1l11l1_opy_, url, data, config):
    headers = config.get(bstack1l1ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᓌ"), None)
    proxies = bstack11l1lllll_opy_(config, url)
    auth = config.get(bstack1l1ll1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᓍ"), None)
    response = requests.request(
            bstack1llll1l11l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack111l1111l_opy_(bstack1l11l1lll1_opy_, size):
    bstack11l11l1l_opy_ = []
    while len(bstack1l11l1lll1_opy_) > size:
        bstack11lll11lll_opy_ = bstack1l11l1lll1_opy_[:size]
        bstack11l11l1l_opy_.append(bstack11lll11lll_opy_)
        bstack1l11l1lll1_opy_ = bstack1l11l1lll1_opy_[size:]
    bstack11l11l1l_opy_.append(bstack1l11l1lll1_opy_)
    return bstack11l11l1l_opy_
def bstack1llll1l11ll_opy_(message, bstack1lllll1l1l1_opy_=False):
    os.write(1, bytes(message, bstack1l1ll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᓎ")))
    os.write(1, bytes(bstack1l1ll1l_opy_ (u"ࠧ࡝ࡰࠪᓏ"), bstack1l1ll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᓐ")))
    if bstack1lllll1l1l1_opy_:
        with open(bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨᓑ") + os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᓒ")] + bstack1l1ll1l_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩᓓ"), bstack1l1ll1l_opy_ (u"ࠬࡧࠧᓔ")) as f:
            f.write(message + bstack1l1ll1l_opy_ (u"࠭࡜࡯ࠩᓕ"))
def bstack1lll1lll1l1_opy_():
    return os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᓖ")].lower() == bstack1l1ll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᓗ")
def bstack1111111l1_opy_(bstack1llll11111l_opy_):
    return bstack1l1ll1l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᓘ").format(bstack11111l1ll1_opy_, bstack1llll11111l_opy_)
def bstack1l1lll1l1_opy_():
    return bstack11l111l1l1_opy_().replace(tzinfo=None).isoformat() + bstack1l1ll1l_opy_ (u"ࠪ࡞ࠬᓙ")
def bstack1llll1lllll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1ll1l_opy_ (u"ࠫ࡟࠭ᓚ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1ll1l_opy_ (u"ࠬࡠࠧᓛ")))).total_seconds() * 1000
def bstack1lllll1ll11_opy_(timestamp):
    return bstack111111l111_opy_(timestamp).isoformat() + bstack1l1ll1l_opy_ (u"࡚࠭ࠨᓜ")
def bstack1llllll1ll1_opy_(bstack111111l11l_opy_):
    date_format = bstack1l1ll1l_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬᓝ")
    bstack1llllll1l1l_opy_ = datetime.datetime.strptime(bstack111111l11l_opy_, date_format)
    return bstack1llllll1l1l_opy_.isoformat() + bstack1l1ll1l_opy_ (u"ࠨ࡜ࠪᓞ")
def bstack111111ll11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᓟ")
    else:
        return bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᓠ")
def bstack1ll11l1ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1ll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᓡ")
def bstack1llll1111l1_opy_(val):
    return val.__str__().lower() == bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᓢ")
def bstack11l111ll1l_opy_(bstack1llll1ll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1llll1ll1ll_opy_ as e:
                print(bstack1l1ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᓣ").format(func.__name__, bstack1llll1ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llll1l1l11_opy_(bstack1llll11l11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llll11l11l_opy_(cls, *args, **kwargs)
            except bstack1llll1ll1ll_opy_ as e:
                print(bstack1l1ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᓤ").format(bstack1llll11l11l_opy_.__name__, bstack1llll1ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llll1l1l11_opy_
    else:
        return decorator
def bstack1lll1ll11_opy_(bstack111ll1lll1_opy_):
    if bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᓥ") in bstack111ll1lll1_opy_ and bstack1llll1111l1_opy_(bstack111ll1lll1_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓦ")]):
        return False
    if bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᓧ") in bstack111ll1lll1_opy_ and bstack1llll1111l1_opy_(bstack111ll1lll1_opy_[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓨ")]):
        return False
    return True
def bstack1l1ll111ll_opy_():
    try:
        from pytest_bdd import reporting
        bstack1lll1llllll_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᓩ"), None)
        return bstack1lll1llllll_opy_ is None or bstack1lll1llllll_opy_ == bstack1l1ll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᓪ")
    except Exception as e:
        return False
def bstack11l1l1ll1_opy_(hub_url, CONFIG):
    if bstack11l1l11l_opy_() <= version.parse(bstack1l1ll1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᓫ")):
        if hub_url != bstack1l1ll1l_opy_ (u"ࠨࠩᓬ"):
            return bstack1l1ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᓭ") + hub_url + bstack1l1ll1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᓮ")
        return bstack1l1lll1111_opy_
    if hub_url != bstack1l1ll1l_opy_ (u"ࠫࠬᓯ"):
        return bstack1l1ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᓰ") + hub_url + bstack1l1ll1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᓱ")
    return bstack1111l1l1l_opy_
def bstack1lllll11ll1_opy_():
    return isinstance(os.getenv(bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᓲ")), str)
def bstack1l11lll1ll_opy_(url):
    return urlparse(url).hostname
def bstack1l1l1lllll_opy_(hostname):
    for bstack11ll11l111_opy_ in bstack1lllll11l_opy_:
        regex = re.compile(bstack11ll11l111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llllllll1l_opy_(bstack1111111l1l_opy_, file_name, logger):
    bstack1l1111111_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1l_opy_ (u"ࠨࢀࠪᓳ")), bstack1111111l1l_opy_)
    try:
        if not os.path.exists(bstack1l1111111_opy_):
            os.makedirs(bstack1l1111111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1ll1l_opy_ (u"ࠩࢁࠫᓴ")), bstack1111111l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1ll1l_opy_ (u"ࠪࡻࠬᓵ")):
                pass
            with open(file_path, bstack1l1ll1l_opy_ (u"ࠦࡼ࠱ࠢᓶ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1lll1ll_opy_.format(str(e)))
def bstack1111111111_opy_(file_name, key, value, logger):
    file_path = bstack1llllllll1l_opy_(bstack1l1ll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᓷ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11ll11ll_opy_ = json.load(open(file_path, bstack1l1ll1l_opy_ (u"࠭ࡲࡣࠩᓸ")))
        else:
            bstack1l11ll11ll_opy_ = {}
        bstack1l11ll11ll_opy_[key] = value
        with open(file_path, bstack1l1ll1l_opy_ (u"ࠢࡸ࠭ࠥᓹ")) as outfile:
            json.dump(bstack1l11ll11ll_opy_, outfile)
def bstack1lllll1111_opy_(file_name, logger):
    file_path = bstack1llllllll1l_opy_(bstack1l1ll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᓺ"), file_name, logger)
    bstack1l11ll11ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1ll1l_opy_ (u"ࠩࡵࠫᓻ")) as bstack1l11ll1l1l_opy_:
            bstack1l11ll11ll_opy_ = json.load(bstack1l11ll1l1l_opy_)
    return bstack1l11ll11ll_opy_
def bstack11l11111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᓼ") + file_path + bstack1l1ll1l_opy_ (u"ࠫࠥ࠭ᓽ") + str(e))
def bstack11l1l11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1ll1l_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᓾ")
def bstack1l111111ll_opy_(config):
    if bstack1l1ll1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᓿ") in config:
        del (config[bstack1l1ll1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᔀ")])
        return False
    if bstack11l1l11l_opy_() < version.parse(bstack1l1ll1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᔁ")):
        return False
    if bstack11l1l11l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᔂ")):
        return True
    if bstack1l1ll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᔃ") in config and config[bstack1l1ll1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᔄ")] is False:
        return False
    else:
        return True
def bstack11lll11l1l_opy_(args_list, bstack1lllll1ll1l_opy_):
    index = -1
    for value in bstack1lllll1ll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l1ll1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l1ll1111_opy_ = bstack11l1ll1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᔅ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᔆ"), exception=exception)
    def bstack111l1llll1_opy_(self):
        if self.result != bstack1l1ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᔇ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1ll1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᔈ") in self.exception_type:
            return bstack1l1ll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᔉ")
        return bstack1l1ll1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᔊ")
    def bstack1llll11ll11_opy_(self):
        if self.result != bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᔋ"):
            return None
        if self.bstack11l1ll1111_opy_:
            return self.bstack11l1ll1111_opy_
        return bstack1llll1ll111_opy_(self.exception)
def bstack1llll1ll111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1lllll1l1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll111111l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11l1l1l1_opy_(config, logger):
    try:
        import playwright
        bstack1lllll1l111_opy_ = playwright.__file__
        bstack1llllllll11_opy_ = os.path.split(bstack1lllll1l111_opy_)
        bstack1lll1llll1l_opy_ = bstack1llllllll11_opy_[0] + bstack1l1ll1l_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᔌ")
        os.environ[bstack1l1ll1l_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᔍ")] = bstack11lll1ll_opy_(config)
        with open(bstack1lll1llll1l_opy_, bstack1l1ll1l_opy_ (u"ࠧࡳࠩᔎ")) as f:
            bstack1l111llll_opy_ = f.read()
            bstack1llllllllll_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᔏ")
            bstack1lll1lll111_opy_ = bstack1l111llll_opy_.find(bstack1llllllllll_opy_)
            if bstack1lll1lll111_opy_ == -1:
              process = subprocess.Popen(bstack1l1ll1l_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᔐ"), shell=True, cwd=bstack1llllllll11_opy_[0])
              process.wait()
              bstack1lllll11l11_opy_ = bstack1l1ll1l_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᔑ")
              bstack1llll111lll_opy_ = bstack1l1ll1l_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᔒ")
              bstack1lllll1llll_opy_ = bstack1l111llll_opy_.replace(bstack1lllll11l11_opy_, bstack1llll111lll_opy_)
              with open(bstack1lll1llll1l_opy_, bstack1l1ll1l_opy_ (u"ࠬࡽࠧᔓ")) as f:
                f.write(bstack1lllll1llll_opy_)
    except Exception as e:
        logger.error(bstack1ll1111l1_opy_.format(str(e)))
def bstack1lll11111l_opy_():
  try:
    bstack1lllll1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᔔ"))
    bstack1llll11llll_opy_ = []
    if os.path.exists(bstack1lllll1111l_opy_):
      with open(bstack1lllll1111l_opy_) as f:
        bstack1llll11llll_opy_ = json.load(f)
      os.remove(bstack1lllll1111l_opy_)
    return bstack1llll11llll_opy_
  except:
    pass
  return []
def bstack11llll1l_opy_(bstack1lll1llll1_opy_):
  try:
    bstack1llll11llll_opy_ = []
    bstack1lllll1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᔕ"))
    if os.path.exists(bstack1lllll1111l_opy_):
      with open(bstack1lllll1111l_opy_) as f:
        bstack1llll11llll_opy_ = json.load(f)
    bstack1llll11llll_opy_.append(bstack1lll1llll1_opy_)
    with open(bstack1lllll1111l_opy_, bstack1l1ll1l_opy_ (u"ࠨࡹࠪᔖ")) as f:
        json.dump(bstack1llll11llll_opy_, f)
  except:
    pass
def bstack1ll1l1llll_opy_(logger, bstack1llll11l1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1ll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᔗ"), bstack1l1ll1l_opy_ (u"ࠪࠫᔘ"))
    if test_name == bstack1l1ll1l_opy_ (u"ࠫࠬᔙ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᔚ"), bstack1l1ll1l_opy_ (u"࠭ࠧᔛ"))
    bstack1llll1ll11l_opy_ = bstack1l1ll1l_opy_ (u"ࠧ࠭ࠢࠪᔜ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llll11l1ll_opy_:
        bstack11lll11l1_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᔝ"), bstack1l1ll1l_opy_ (u"ࠩ࠳ࠫᔞ"))
        bstack1l1ll1ll11_opy_ = {bstack1l1ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᔟ"): test_name, bstack1l1ll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᔠ"): bstack1llll1ll11l_opy_, bstack1l1ll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᔡ"): bstack11lll11l1_opy_}
        bstack1lllll11lll_opy_ = []
        bstack1lllll111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᔢ"))
        if os.path.exists(bstack1lllll111l1_opy_):
            with open(bstack1lllll111l1_opy_) as f:
                bstack1lllll11lll_opy_ = json.load(f)
        bstack1lllll11lll_opy_.append(bstack1l1ll1ll11_opy_)
        with open(bstack1lllll111l1_opy_, bstack1l1ll1l_opy_ (u"ࠧࡸࠩᔣ")) as f:
            json.dump(bstack1lllll11lll_opy_, f)
    else:
        bstack1l1ll1ll11_opy_ = {bstack1l1ll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᔤ"): test_name, bstack1l1ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᔥ"): bstack1llll1ll11l_opy_, bstack1l1ll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᔦ"): str(multiprocessing.current_process().name)}
        if bstack1l1ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᔧ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1ll1ll11_opy_)
  except Exception as e:
      logger.warn(bstack1l1ll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᔨ").format(e))
def bstack1l1ll1llll_opy_(error_message, test_name, index, logger):
  try:
    bstack1llll11ll1l_opy_ = []
    bstack1l1ll1ll11_opy_ = {bstack1l1ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᔩ"): test_name, bstack1l1ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᔪ"): error_message, bstack1l1ll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᔫ"): index}
    bstack1llll11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᔬ"))
    if os.path.exists(bstack1llll11lll1_opy_):
        with open(bstack1llll11lll1_opy_) as f:
            bstack1llll11ll1l_opy_ = json.load(f)
    bstack1llll11ll1l_opy_.append(bstack1l1ll1ll11_opy_)
    with open(bstack1llll11lll1_opy_, bstack1l1ll1l_opy_ (u"ࠪࡻࠬᔭ")) as f:
        json.dump(bstack1llll11ll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1ll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᔮ").format(e))
def bstack1l1lllll1_opy_(bstack111l1l1l_opy_, name, logger):
  try:
    bstack1l1ll1ll11_opy_ = {bstack1l1ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᔯ"): name, bstack1l1ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᔰ"): bstack111l1l1l_opy_, bstack1l1ll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᔱ"): str(threading.current_thread()._name)}
    return bstack1l1ll1ll11_opy_
  except Exception as e:
    logger.warn(bstack1l1ll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᔲ").format(e))
  return
def bstack1llllll1lll_opy_():
    return platform.system() == bstack1l1ll1l_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᔳ")
def bstack11l1llll_opy_(bstack1llll11l111_opy_, config, logger):
    bstack1lllllll111_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llll11l111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᔴ").format(e))
    return bstack1lllllll111_opy_
def bstack1llll111ll1_opy_(bstack1llll111111_opy_, bstack1llll1ll1l1_opy_):
    bstack1llll1l1111_opy_ = version.parse(bstack1llll111111_opy_)
    bstack1llll111l1l_opy_ = version.parse(bstack1llll1ll1l1_opy_)
    if bstack1llll1l1111_opy_ > bstack1llll111l1l_opy_:
        return 1
    elif bstack1llll1l1111_opy_ < bstack1llll111l1l_opy_:
        return -1
    else:
        return 0
def bstack11l111l1l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111111l111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111111ll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll1ll1l11_opy_(options, framework, bstack1l11ll1l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1ll1l_opy_ (u"ࠫ࡬࡫ࡴࠨᔵ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l111lll11_opy_ = caps.get(bstack1l1ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᔶ"))
    bstack1llll1l1ll1_opy_ = True
    bstack1ll111l1l1_opy_ = os.environ[bstack1l1ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᔷ")]
    if bstack1llll1111l1_opy_(caps.get(bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᔸ"))) or bstack1llll1111l1_opy_(caps.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᔹ"))):
        bstack1llll1l1ll1_opy_ = False
    if bstack1l111111ll_opy_({bstack1l1ll1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᔺ"): bstack1llll1l1ll1_opy_}):
        bstack1l111lll11_opy_ = bstack1l111lll11_opy_ or {}
        bstack1l111lll11_opy_[bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᔻ")] = bstack1111111ll1_opy_(framework)
        bstack1l111lll11_opy_[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᔼ")] = bstack1lll1lll1l1_opy_()
        bstack1l111lll11_opy_[bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᔽ")] = bstack1ll111l1l1_opy_
        bstack1l111lll11_opy_[bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᔾ")] = bstack1l11ll1l11_opy_
        if getattr(options, bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᔿ"), None):
            options.set_capability(bstack1l1ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᕀ"), bstack1l111lll11_opy_)
        else:
            options[bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᕁ")] = bstack1l111lll11_opy_
    else:
        if getattr(options, bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫᕂ"), None):
            options.set_capability(bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᕃ"), bstack1111111ll1_opy_(framework))
            options.set_capability(bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᕄ"), bstack1lll1lll1l1_opy_())
            options.set_capability(bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᕅ"), bstack1ll111l1l1_opy_)
            options.set_capability(bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᕆ"), bstack1l11ll1l11_opy_)
        else:
            options[bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᕇ")] = bstack1111111ll1_opy_(framework)
            options[bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᕈ")] = bstack1lll1lll1l1_opy_()
            options[bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᕉ")] = bstack1ll111l1l1_opy_
            options[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᕊ")] = bstack1l11ll1l11_opy_
    return options
def bstack1llll11l1l1_opy_(bstack111111111l_opy_, framework):
    bstack1l11ll1l11_opy_ = bstack111111111_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢᕋ"))
    if bstack111111111l_opy_ and len(bstack111111111l_opy_.split(bstack1l1ll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᕌ"))) > 1:
        ws_url = bstack111111111l_opy_.split(bstack1l1ll1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᕍ"))[0]
        if bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᕎ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lllll1l11l_opy_ = json.loads(urllib.parse.unquote(bstack111111111l_opy_.split(bstack1l1ll1l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᕏ"))[1]))
            bstack1lllll1l11l_opy_ = bstack1lllll1l11l_opy_ or {}
            bstack1ll111l1l1_opy_ = os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᕐ")]
            bstack1lllll1l11l_opy_[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᕑ")] = str(framework) + str(__version__)
            bstack1lllll1l11l_opy_[bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᕒ")] = bstack1lll1lll1l1_opy_()
            bstack1lllll1l11l_opy_[bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᕓ")] = bstack1ll111l1l1_opy_
            bstack1lllll1l11l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᕔ")] = bstack1l11ll1l11_opy_
            bstack111111111l_opy_ = bstack111111111l_opy_.split(bstack1l1ll1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᕕ"))[0] + bstack1l1ll1l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᕖ") + urllib.parse.quote(json.dumps(bstack1lllll1l11l_opy_))
    return bstack111111111l_opy_
def bstack1l111ll11l_opy_():
    global bstack1l1ll1l11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1ll1l11_opy_ = BrowserType.connect
    return bstack1l1ll1l11_opy_
def bstack111l1lll1_opy_(framework_name):
    global bstack11111l111_opy_
    bstack11111l111_opy_ = framework_name
    return framework_name
def bstack1l111ll1_opy_(self, *args, **kwargs):
    global bstack1l1ll1l11_opy_
    try:
        global bstack11111l111_opy_
        if bstack1l1ll1l_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᕗ") in kwargs:
            kwargs[bstack1l1ll1l_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᕘ")] = bstack1llll11l1l1_opy_(
                kwargs.get(bstack1l1ll1l_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᕙ"), None),
                bstack11111l111_opy_
            )
    except Exception as e:
        logger.error(bstack1l1ll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨᕚ").format(str(e)))
    return bstack1l1ll1l11_opy_(self, *args, **kwargs)
def bstack1llll111l11_opy_(bstack1lll1llll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1lllll_opy_(bstack1lll1llll11_opy_, bstack1l1ll1l_opy_ (u"ࠢࠣᕛ"))
        if proxies and proxies.get(bstack1l1ll1l_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᕜ")):
            parsed_url = urlparse(proxies.get(bstack1l1ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᕝ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1ll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᕞ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1ll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᕟ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᕠ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᕡ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1l111l11_opy_(bstack1lll1llll11_opy_):
    bstack1111111l11_opy_ = {
        bstack11111l1111_opy_[bstack1llllll1l11_opy_]: bstack1lll1llll11_opy_[bstack1llllll1l11_opy_]
        for bstack1llllll1l11_opy_ in bstack1lll1llll11_opy_
        if bstack1llllll1l11_opy_ in bstack11111l1111_opy_
    }
    bstack1111111l11_opy_[bstack1l1ll1l_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢᕢ")] = bstack1llll111l11_opy_(bstack1lll1llll11_opy_, bstack111111111_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᕣ")))
    bstack11111111l1_opy_ = [element.lower() for element in bstack11111l11ll_opy_]
    bstack1llllll11ll_opy_(bstack1111111l11_opy_, bstack11111111l1_opy_)
    return bstack1111111l11_opy_
def bstack1llllll11ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1ll1l_opy_ (u"ࠤ࠭࠮࠯࠰ࠢᕤ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1llllll11ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1llllll11ll_opy_(item, keys)