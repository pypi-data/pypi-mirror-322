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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll11l1lll_opy_
bstack111111111_opy_ = Config.bstack1l11ll1l_opy_()
def bstack1ll1l1111ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l111l1l_opy_(bstack1ll1l111lll_opy_, bstack1ll1l11l111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l111lll_opy_):
        with open(bstack1ll1l111lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l1111ll_opy_(bstack1ll1l111lll_opy_):
        pac = get_pac(url=bstack1ll1l111lll_opy_)
    else:
        raise Exception(bstack1l1ll1l_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᚇ").format(bstack1ll1l111lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1ll1l_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᚈ"), 80))
        bstack1ll1l11l11l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l11l11l_opy_ = bstack1l1ll1l_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᚉ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l11l111_opy_, bstack1ll1l11l11l_opy_)
    return proxy_url
def bstack111111ll_opy_(config):
    return bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᚊ") in config or bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᚋ") in config
def bstack11lll1ll_opy_(config):
    if not bstack111111ll_opy_(config):
        return
    if config.get(bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᚌ")):
        return config.get(bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᚍ"))
    if config.get(bstack1l1ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᚎ")):
        return config.get(bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᚏ"))
def bstack11l1lllll_opy_(config, bstack1ll1l11l111_opy_):
    proxy = bstack11lll1ll_opy_(config)
    proxies = {}
    if config.get(bstack1l1ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᚐ")) or config.get(bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᚑ")):
        if proxy.endswith(bstack1l1ll1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᚒ")):
            proxies = bstack11l11l1l1_opy_(proxy, bstack1ll1l11l111_opy_)
        else:
            proxies = {
                bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᚓ"): proxy
            }
    bstack111111111_opy_.bstack111l1l111_opy_(bstack1l1ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬᚔ"), proxies)
    return proxies
def bstack11l11l1l1_opy_(bstack1ll1l111lll_opy_, bstack1ll1l11l111_opy_):
    proxies = {}
    global bstack1ll1l111ll1_opy_
    if bstack1l1ll1l_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᚕ") in globals():
        return bstack1ll1l111ll1_opy_
    try:
        proxy = bstack1ll1l111l1l_opy_(bstack1ll1l111lll_opy_, bstack1ll1l11l111_opy_)
        if bstack1l1ll1l_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᚖ") in proxy:
            proxies = {}
        elif bstack1l1ll1l_opy_ (u"ࠣࡊࡗࡘࡕࠨᚗ") in proxy or bstack1l1ll1l_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᚘ") in proxy or bstack1l1ll1l_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᚙ") in proxy:
            bstack1ll1l111l11_opy_ = proxy.split(bstack1l1ll1l_opy_ (u"ࠦࠥࠨᚚ"))
            if bstack1l1ll1l_opy_ (u"ࠧࡀ࠯࠰ࠤ᚛") in bstack1l1ll1l_opy_ (u"ࠨࠢ᚜").join(bstack1ll1l111l11_opy_[1:]):
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᚝"): bstack1l1ll1l_opy_ (u"ࠣࠤ᚞").join(bstack1ll1l111l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ᚟"): str(bstack1ll1l111l11_opy_[0]).lower() + bstack1l1ll1l_opy_ (u"ࠥ࠾࠴࠵ࠢᚠ") + bstack1l1ll1l_opy_ (u"ࠦࠧᚡ").join(bstack1ll1l111l11_opy_[1:])
                }
        elif bstack1l1ll1l_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᚢ") in proxy:
            bstack1ll1l111l11_opy_ = proxy.split(bstack1l1ll1l_opy_ (u"ࠨࠠࠣᚣ"))
            if bstack1l1ll1l_opy_ (u"ࠢ࠻࠱࠲ࠦᚤ") in bstack1l1ll1l_opy_ (u"ࠣࠤᚥ").join(bstack1ll1l111l11_opy_[1:]):
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᚦ"): bstack1l1ll1l_opy_ (u"ࠥࠦᚧ").join(bstack1ll1l111l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᚨ"): bstack1l1ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᚩ") + bstack1l1ll1l_opy_ (u"ࠨࠢᚪ").join(bstack1ll1l111l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᚫ"): proxy
            }
    except Exception as e:
        print(bstack1l1ll1l_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᚬ"), bstack1lll11l1lll_opy_.format(bstack1ll1l111lll_opy_, str(e)))
    bstack1ll1l111ll1_opy_ = proxies
    return proxies