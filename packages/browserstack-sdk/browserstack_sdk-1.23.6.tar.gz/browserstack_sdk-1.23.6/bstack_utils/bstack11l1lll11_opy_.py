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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11111lll11_opy_, bstack11111l11ll_opy_
import tempfile
import json
bstack1lll1l1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭ᖐ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1ll1l_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᖑ"),
      datefmt=bstack1l1ll1l_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨᖒ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11ll111_opy_():
  global bstack1lll1l1111l_opy_
  if os.path.exists(bstack1lll1l1111l_opy_):
    os.remove(bstack1lll1l1111l_opy_)
def bstack11ll1111l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l11l11111_opy_(config, log_level):
  bstack1lll1l11l11_opy_ = log_level
  if bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᖓ") in config and config[bstack1l1ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᖔ")] in bstack11111lll11_opy_:
    bstack1lll1l11l11_opy_ = bstack11111lll11_opy_[config[bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᖕ")]]
  if config.get(bstack1l1ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᖖ"), False):
    logging.getLogger().setLevel(bstack1lll1l11l11_opy_)
    return bstack1lll1l11l11_opy_
  global bstack1lll1l1111l_opy_
  bstack11ll1111l1_opy_()
  bstack1lll11ll1l1_opy_ = logging.Formatter(
    fmt=bstack1l1ll1l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᖗ"),
    datefmt=bstack1l1ll1l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧᖘ")
  )
  bstack1lll11ll1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lll1l1111l_opy_)
  file_handler.setFormatter(bstack1lll11ll1l1_opy_)
  bstack1lll11ll1ll_opy_.setFormatter(bstack1lll11ll1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lll11ll1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1ll1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨᖙ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lll11ll1ll_opy_.setLevel(bstack1lll1l11l11_opy_)
  logging.getLogger().addHandler(bstack1lll11ll1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lll1l11l11_opy_
def bstack1lll1l11l1l_opy_(config):
  try:
    bstack1lll1l111l1_opy_ = set(bstack11111l11ll_opy_)
    bstack1lll11lllll_opy_ = bstack1l1ll1l_opy_ (u"ࠧࠨᖚ")
    with open(bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᖛ")) as bstack1lll11lll11_opy_:
      bstack1lll11lll1l_opy_ = bstack1lll11lll11_opy_.read()
      bstack1lll11lllll_opy_ = re.sub(bstack1l1ll1l_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪᖜ"), bstack1l1ll1l_opy_ (u"ࠪࠫᖝ"), bstack1lll11lll1l_opy_, flags=re.M)
      bstack1lll11lllll_opy_ = re.sub(
        bstack1l1ll1l_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧᖞ") + bstack1l1ll1l_opy_ (u"ࠬࢂࠧᖟ").join(bstack1lll1l111l1_opy_) + bstack1l1ll1l_opy_ (u"࠭ࠩ࠯ࠬࠧࠫᖠ"),
        bstack1l1ll1l_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᖡ"),
        bstack1lll11lllll_opy_, flags=re.M | re.I
      )
    def bstack1lll1l111ll_opy_(dic):
      bstack1lll1l11111_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lll1l111l1_opy_:
          bstack1lll1l11111_opy_[key] = bstack1l1ll1l_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᖢ")
        else:
          if isinstance(value, dict):
            bstack1lll1l11111_opy_[key] = bstack1lll1l111ll_opy_(value)
          else:
            bstack1lll1l11111_opy_[key] = value
      return bstack1lll1l11111_opy_
    bstack1lll1l11111_opy_ = bstack1lll1l111ll_opy_(config)
    return {
      bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬᖣ"): bstack1lll11lllll_opy_,
      bstack1l1ll1l_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᖤ"): json.dumps(bstack1lll1l11111_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll111lll1_opy_(config):
  global bstack1lll1l1111l_opy_
  try:
    if config.get(bstack1l1ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᖥ"), False):
      return
    uuid = os.getenv(bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᖦ"))
    if not uuid or uuid == bstack1l1ll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᖧ"):
      return
    bstack1lll11ll11l_opy_ = [bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᖨ"), bstack1l1ll1l_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᖩ"), bstack1l1ll1l_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᖪ"), bstack1lll1l1111l_opy_]
    bstack11ll1111l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᖫ") + uuid + bstack1l1ll1l_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᖬ"))
    with tarfile.open(output_file, bstack1l1ll1l_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᖭ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lll11ll11l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lll1l11l1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lll11llll1_opy_ = data.encode()
        tarinfo.size = len(bstack1lll11llll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lll11llll1_opy_))
    bstack1l11lll11_opy_ = MultipartEncoder(
      fields= {
        bstack1l1ll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᖮ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1ll1l_opy_ (u"ࠧࡳࡤࠪᖯ")), bstack1l1ll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᖰ")),
        bstack1l1ll1l_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᖱ"): uuid
      }
    )
    response = requests.post(
      bstack1l1ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᖲ"),
      data=bstack1l11lll11_opy_,
      headers={bstack1l1ll1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᖳ"): bstack1l11lll11_opy_.content_type},
      auth=(config[bstack1l1ll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᖴ")], config[bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᖵ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1ll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭ᖶ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧᖷ") + str(e))
  finally:
    try:
      bstack1lll11ll111_opy_()
    except:
      pass