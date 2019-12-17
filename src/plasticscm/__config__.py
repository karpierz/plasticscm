# Copyright (c) 2019-2019 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib/


def make_config(cfg_name):
    import sys
    import os.path
    from runpy import run_path
    fglobals = sys._getframe(1).f_globals
    fglobals.pop("make_config", None)
    cfg_path = os.path.join(os.path.dirname(fglobals["__file__"]), cfg_name)
    cfg_dict = ({k: v for k, v in run_path(cfg_path).items() if not k.startswith("__")}
                if os.path.isfile(cfg_path) else {})
    fglobals.update(cfg_dict)
    fglobals.pop("__builtins__", None)
    fglobals.pop("__cached__",   None)
    fglobals["__all__"] = tuple(cfg_dict.keys())


make_config("plasticscm.cfg")
