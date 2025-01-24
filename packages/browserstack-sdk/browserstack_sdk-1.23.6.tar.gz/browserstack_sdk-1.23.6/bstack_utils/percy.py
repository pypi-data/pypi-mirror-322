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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1111111l1_opy_, bstack11ll1111ll_opy_
from bstack_utils.measure import measure
class bstack1ll11l1l1_opy_:
  working_dir = os.getcwd()
  bstack11llll1l1_opy_ = False
  config = {}
  binary_path = bstack1l1ll1l_opy_ (u"ࠨࠩᘄ")
  bstack1ll1ll1l1ll_opy_ = bstack1l1ll1l_opy_ (u"ࠩࠪᘅ")
  bstack1l11l111l1_opy_ = False
  bstack1ll1lll11ll_opy_ = None
  bstack1lll11l111l_opy_ = {}
  bstack1ll1ll11l1l_opy_ = 300
  bstack1ll1lll1lll_opy_ = False
  logger = None
  bstack1ll1l1llll1_opy_ = False
  bstack1l11l111l_opy_ = False
  bstack1ll11l111l_opy_ = None
  bstack1ll1ll1l11l_opy_ = bstack1l1ll1l_opy_ (u"ࠪࠫᘆ")
  bstack1ll1ll1ll1l_opy_ = {
    bstack1l1ll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᘇ") : 1,
    bstack1l1ll1l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᘈ") : 2,
    bstack1l1ll1l_opy_ (u"࠭ࡥࡥࡩࡨࠫᘉ") : 3,
    bstack1l1ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᘊ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1ll111ll_opy_(self):
    bstack1ll1ll1l1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠨࠩᘋ")
    bstack1lll1111111_opy_ = sys.platform
    bstack1lll11111ll_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᘌ")
    if re.match(bstack1l1ll1l_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᘍ"), bstack1lll1111111_opy_) != None:
      bstack1ll1ll1l1l1_opy_ = bstack1111l111ll_opy_ + bstack1l1ll1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᘎ")
      self.bstack1ll1ll1l11l_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡳࡡࡤࠩᘏ")
    elif re.match(bstack1l1ll1l_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᘐ"), bstack1lll1111111_opy_) != None:
      bstack1ll1ll1l1l1_opy_ = bstack1111l111ll_opy_ + bstack1l1ll1l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᘑ")
      bstack1lll11111ll_opy_ = bstack1l1ll1l_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᘒ")
      self.bstack1ll1ll1l11l_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡺ࡭ࡳ࠭ᘓ")
    else:
      bstack1ll1ll1l1l1_opy_ = bstack1111l111ll_opy_ + bstack1l1ll1l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᘔ")
      self.bstack1ll1ll1l11l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᘕ")
    return bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_
  def bstack1ll1lll1111_opy_(self):
    try:
      bstack1lll111111l_opy_ = [os.path.join(expanduser(bstack1l1ll1l_opy_ (u"ࠧࢄࠢᘖ")), bstack1l1ll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᘗ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll111111l_opy_:
        if(self.bstack1lll111l1l1_opy_(path)):
          return path
      raise bstack1l1ll1l_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᘘ")
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᘙ").format(e))
  def bstack1lll111l1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  @measure(event_name=EVENTS.bstack11111l111l_opy_, stage=STAGE.SINGLE)
  def bstack1lll11l1111_opy_(self, bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_):
    try:
      bstack1ll1lll11l1_opy_ = self.bstack1ll1lll1111_opy_()
      bstack1ll1lll1l11_opy_ = os.path.join(bstack1ll1lll11l1_opy_, bstack1l1ll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᘚ"))
      bstack1lll1111ll1_opy_ = os.path.join(bstack1ll1lll11l1_opy_, bstack1lll11111ll_opy_)
      if os.path.exists(bstack1lll1111ll1_opy_):
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᘛ").format(bstack1lll1111ll1_opy_))
        return bstack1lll1111ll1_opy_
      if os.path.exists(bstack1ll1lll1l11_opy_):
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᘜ").format(bstack1ll1lll1l11_opy_))
        return self.bstack1lll1111l11_opy_(bstack1ll1lll1l11_opy_, bstack1lll11111ll_opy_)
      self.logger.info(bstack1l1ll1l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᘝ").format(bstack1ll1ll1l1l1_opy_))
      response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"࠭ࡇࡆࡖࠪᘞ"), bstack1ll1ll1l1l1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1ll1lll1l11_opy_, bstack1l1ll1l_opy_ (u"ࠧࡸࡤࠪᘟ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᘠ").format(bstack1ll1lll1l11_opy_))
        return self.bstack1lll1111l11_opy_(bstack1ll1lll1l11_opy_, bstack1lll11111ll_opy_)
      else:
        raise(bstack1l1ll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᘡ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᘢ").format(e))
  def bstack1ll1ll1l111_opy_(self, bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_):
    try:
      retry = 2
      bstack1lll1111ll1_opy_ = None
      bstack1lll1111l1l_opy_ = False
      while retry > 0:
        bstack1lll1111ll1_opy_ = self.bstack1lll11l1111_opy_(bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_)
        bstack1lll1111l1l_opy_ = self.bstack1lll111lll1_opy_(bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_, bstack1lll1111ll1_opy_)
        if bstack1lll1111l1l_opy_:
          break
        retry -= 1
      return bstack1lll1111ll1_opy_, bstack1lll1111l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᘣ").format(e))
    return bstack1lll1111ll1_opy_, False
  def bstack1lll111lll1_opy_(self, bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_, bstack1lll1111ll1_opy_, bstack1ll1ll11ll1_opy_ = 0):
    if bstack1ll1ll11ll1_opy_ > 1:
      return False
    if bstack1lll1111ll1_opy_ == None or os.path.exists(bstack1lll1111ll1_opy_) == False:
      self.logger.warn(bstack1l1ll1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᘤ"))
      return False
    bstack1ll1lll1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᘥ")
    command = bstack1l1ll1l_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᘦ").format(bstack1lll1111ll1_opy_)
    bstack1ll1ll1ll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1ll1lll1ll1_opy_, bstack1ll1ll1ll11_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᘧ"))
      return False
  def bstack1lll1111l11_opy_(self, bstack1ll1lll1l11_opy_, bstack1lll11111ll_opy_):
    try:
      working_dir = os.path.dirname(bstack1ll1lll1l11_opy_)
      shutil.unpack_archive(bstack1ll1lll1l11_opy_, working_dir)
      bstack1lll1111ll1_opy_ = os.path.join(working_dir, bstack1lll11111ll_opy_)
      os.chmod(bstack1lll1111ll1_opy_, 0o755)
      return bstack1lll1111ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᘨ"))
  def bstack1lll1111lll_opy_(self):
    try:
      bstack1ll1llll11l_opy_ = self.config.get(bstack1l1ll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᘩ"))
      bstack1lll1111lll_opy_ = bstack1ll1llll11l_opy_ or (bstack1ll1llll11l_opy_ is None and self.bstack11llll1l1_opy_)
      if not bstack1lll1111lll_opy_ or self.config.get(bstack1l1ll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᘪ"), None) not in bstack11111l11l1_opy_:
        return False
      self.bstack1l11l111l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᘫ").format(e))
  def bstack1lll111llll_opy_(self):
    try:
      bstack1lll111llll_opy_ = self.bstack1ll1ll111l1_opy_
      return bstack1lll111llll_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᘬ").format(e))
  def init(self, bstack11llll1l1_opy_, config, logger):
    self.bstack11llll1l1_opy_ = bstack11llll1l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll1111lll_opy_():
      return
    self.bstack1lll11l111l_opy_ = config.get(bstack1l1ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘭ"), {})
    self.bstack1ll1ll111l1_opy_ = config.get(bstack1l1ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᘮ"))
    try:
      bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_ = self.bstack1ll1ll111ll_opy_()
      bstack1lll1111ll1_opy_, bstack1lll1111l1l_opy_ = self.bstack1ll1ll1l111_opy_(bstack1ll1ll1l1l1_opy_, bstack1lll11111ll_opy_)
      if bstack1lll1111l1l_opy_:
        self.binary_path = bstack1lll1111ll1_opy_
        thread = Thread(target=self.bstack1lll11111l1_opy_)
        thread.start()
      else:
        self.bstack1ll1l1llll1_opy_ = True
        self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᘯ").format(bstack1lll1111ll1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᘰ").format(e))
  def bstack1ll1lll1l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1ll1l_opy_ (u"ࠫࡱࡵࡧࠨᘱ"), bstack1l1ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᘲ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᘳ").format(logfile))
      self.bstack1ll1ll1l1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᘴ").format(e))
  @measure(event_name=EVENTS.bstack11111ll11l_opy_, stage=STAGE.SINGLE)
  def bstack1lll11111l1_opy_(self):
    bstack1ll1llll1ll_opy_ = self.bstack1ll1ll1llll_opy_()
    if bstack1ll1llll1ll_opy_ == None:
      self.bstack1ll1l1llll1_opy_ = True
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᘵ"))
      return False
    command_args = [bstack1l1ll1l_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᘶ") if self.bstack11llll1l1_opy_ else bstack1l1ll1l_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᘷ")]
    bstack1lll11l11l1_opy_ = self.bstack1ll1ll11111_opy_()
    if bstack1lll11l11l1_opy_ != None:
      command_args.append(bstack1l1ll1l_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᘸ").format(bstack1lll11l11l1_opy_))
    env = os.environ.copy()
    env[bstack1l1ll1l_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᘹ")] = bstack1ll1llll1ll_opy_
    env[bstack1l1ll1l_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᘺ")] = os.environ.get(bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᘻ"), bstack1l1ll1l_opy_ (u"ࠨࠩᘼ"))
    bstack1ll1lllllll_opy_ = [self.binary_path]
    self.bstack1ll1lll1l1l_opy_()
    self.bstack1ll1lll11ll_opy_ = self.bstack1ll1lllll11_opy_(bstack1ll1lllllll_opy_ + command_args, env)
    self.logger.debug(bstack1l1ll1l_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᘽ"))
    bstack1ll1ll11ll1_opy_ = 0
    while self.bstack1ll1lll11ll_opy_.poll() == None:
      bstack1ll1ll11l11_opy_ = self.bstack1ll1ll1111l_opy_()
      if bstack1ll1ll11l11_opy_:
        self.logger.debug(bstack1l1ll1l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᘾ"))
        self.bstack1ll1lll1lll_opy_ = True
        return True
      bstack1ll1ll11ll1_opy_ += 1
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᘿ").format(bstack1ll1ll11ll1_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1ll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᙀ").format(bstack1ll1ll11ll1_opy_))
    self.bstack1ll1l1llll1_opy_ = True
    return False
  def bstack1ll1ll1111l_opy_(self, bstack1ll1ll11ll1_opy_ = 0):
    if bstack1ll1ll11ll1_opy_ > 10:
      return False
    try:
      bstack1ll1l1lllll_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ᙁ"), bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᙂ"))
      bstack1ll1lllll1l_opy_ = bstack1ll1l1lllll_opy_ + bstack111111llll_opy_
      response = requests.get(bstack1ll1lllll1l_opy_)
      data = response.json()
      self.bstack1ll11l111l_opy_ = data.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᙃ"), {}).get(bstack1l1ll1l_opy_ (u"ࠩ࡬ࡨࠬᙄ"), None)
      return True
    except:
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᙅ"))
      return False
  def bstack1ll1ll1llll_opy_(self):
    bstack1ll1llllll1_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡦࡶࡰࠨᙆ") if self.bstack11llll1l1_opy_ else bstack1l1ll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᙇ")
    bstack1lll111l111_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᙈ") if self.config.get(bstack1l1ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᙉ")) is None else True
    bstack1llll11111l_opy_ = bstack1l1ll1l_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᙊ").format(self.config[bstack1l1ll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᙋ")], bstack1ll1llllll1_opy_, bstack1lll111l111_opy_)
    if self.bstack1ll1ll111l1_opy_:
      bstack1llll11111l_opy_ += bstack1l1ll1l_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧᙌ").format(self.bstack1ll1ll111l1_opy_)
    uri = bstack1111111l1_opy_(bstack1llll11111l_opy_)
    try:
      response = bstack11ll1111ll_opy_(bstack1l1ll1l_opy_ (u"ࠫࡌࡋࡔࠨᙍ"), uri, {}, {bstack1l1ll1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᙎ"): (self.config[bstack1l1ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᙏ")], self.config[bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᙐ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l11l111l1_opy_ = data.get(bstack1l1ll1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᙑ"))
        self.bstack1ll1ll111l1_opy_ = data.get(bstack1l1ll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᙒ"))
        os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᙓ")] = str(self.bstack1l11l111l1_opy_)
        os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᙔ")] = str(self.bstack1ll1ll111l1_opy_)
        if bstack1lll111l111_opy_ == bstack1l1ll1l_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᙕ") and str(self.bstack1l11l111l1_opy_).lower() == bstack1l1ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᙖ"):
          self.bstack1l11l111l_opy_ = True
        if bstack1l1ll1l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᙗ") in data:
          return data[bstack1l1ll1l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᙘ")]
        else:
          raise bstack1l1ll1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᙙ").format(data)
      else:
        raise bstack1l1ll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᙚ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᙛ").format(e))
  def bstack1ll1ll11111_opy_(self):
    bstack1lll111ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᙜ"))
    try:
      if bstack1l1ll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᙝ") not in self.bstack1lll11l111l_opy_:
        self.bstack1lll11l111l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᙞ")] = 2
      with open(bstack1lll111ll1l_opy_, bstack1l1ll1l_opy_ (u"ࠨࡹࠪᙟ")) as fp:
        json.dump(self.bstack1lll11l111l_opy_, fp)
      return bstack1lll111ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᙠ").format(e))
  def bstack1ll1lllll11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll1ll1l11l_opy_ == bstack1l1ll1l_opy_ (u"ࠪࡻ࡮ࡴࠧᙡ"):
        bstack1ll1llll111_opy_ = [bstack1l1ll1l_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᙢ"), bstack1l1ll1l_opy_ (u"ࠬ࠵ࡣࠨᙣ")]
        cmd = bstack1ll1llll111_opy_ + cmd
      cmd = bstack1l1ll1l_opy_ (u"࠭ࠠࠨᙤ").join(cmd)
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᙥ").format(cmd))
      with open(self.bstack1ll1ll1l1ll_opy_, bstack1l1ll1l_opy_ (u"ࠣࡣࠥᙦ")) as bstack1lll111l11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll111l11l_opy_, text=True, stderr=bstack1lll111l11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1ll1l1llll1_opy_ = True
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᙧ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1ll1lll1lll_opy_:
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᙨ"))
        cmd = [self.binary_path, bstack1l1ll1l_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᙩ")]
        self.bstack1ll1lllll11_opy_(cmd)
        self.bstack1ll1lll1lll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᙪ").format(cmd, e))
  def bstack1l111llll1_opy_(self):
    if not self.bstack1l11l111l1_opy_:
      return
    try:
      bstack1lll111l1ll_opy_ = 0
      while not self.bstack1ll1lll1lll_opy_ and bstack1lll111l1ll_opy_ < self.bstack1ll1ll11l1l_opy_:
        if self.bstack1ll1l1llll1_opy_:
          self.logger.info(bstack1l1ll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᙫ"))
          return
        time.sleep(1)
        bstack1lll111l1ll_opy_ += 1
      os.environ[bstack1l1ll1l_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᙬ")] = str(self.bstack1ll1ll1lll1_opy_())
      self.logger.info(bstack1l1ll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤ᙭"))
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ᙮").format(e))
  def bstack1ll1ll1lll1_opy_(self):
    if self.bstack11llll1l1_opy_:
      return
    try:
      bstack1ll1llll1l1_opy_ = [platform[bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᙯ")].lower() for platform in self.config.get(bstack1l1ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᙰ"), [])]
      bstack1ll1ll11lll_opy_ = sys.maxsize
      bstack1lll111ll11_opy_ = bstack1l1ll1l_opy_ (u"ࠬ࠭ᙱ")
      for browser in bstack1ll1llll1l1_opy_:
        if browser in self.bstack1ll1ll1ll1l_opy_:
          bstack1ll1lll111l_opy_ = self.bstack1ll1ll1ll1l_opy_[browser]
        if bstack1ll1lll111l_opy_ < bstack1ll1ll11lll_opy_:
          bstack1ll1ll11lll_opy_ = bstack1ll1lll111l_opy_
          bstack1lll111ll11_opy_ = browser
      return bstack1lll111ll11_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᙲ").format(e))
  @classmethod
  def bstack1l1ll1l1_opy_(self):
    return os.getenv(bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᙳ"), bstack1l1ll1l_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᙴ")).lower()
  @classmethod
  def bstack11ll1l1l_opy_(self):
    return os.getenv(bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᙵ"), bstack1l1ll1l_opy_ (u"ࠪࠫᙶ"))