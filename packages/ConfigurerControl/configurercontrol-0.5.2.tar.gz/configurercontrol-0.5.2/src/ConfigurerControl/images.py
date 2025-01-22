from typing import Literal, TypeAlias
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageTk
import logging
from DLMS_SPODES.cosem_interface_classes import cosem_interface_class as ic
from DLMS_SPODES.config_parser import get_values


conf = {
    "path": "./Themes",
    "theme": "light",
    "icons": {
        "size": [20, 20]
    }
}


if toml_val := get_values("CONTROL", "themes"):
    conf.update(toml_val)
else:
    logging.warning("VIEW, ObjectList not find in config file")

if not (t_path := Path(F"{conf["path"]}/{conf["theme"]}")).exists():
    if not (themes := Path(F"{conf["path"]}")).exists():
        raise RuntimeError(F"themes folder: {themes.absolute()} not was find")
    if len(tmp := tuple(themes.iterdir())) == 0:
        raise RuntimeError("no one themes was find")
    else:
        t_path = tmp[0]  # choice first theme
        logging.warning(F"choice first theme: {t_path}")


DEFAULT = Image.new('RGB', (100, 100), 'white')
font = ImageFont.load_default(size=50)
pencil = ImageDraw.Draw(DEFAULT)
pencil.text(
    (50, 90),
    '?',
    anchor="ms",
    font=ImageFont.load_default(size=100),
    fill='red'
)


def get_image(name: str) -> Image:
    path = t_path / name
    if not path.is_file():
        logging.error(F"not find {name} image in {t_path}")
        return DEFAULT
    else:
        return Image.open(path)


def get_tk_image(img: Image) -> ImageTk:
    return ImageTk.PhotoImage(img.resize(conf["icons"]["size"]))


ActionName = Literal[
    "activate",
    "receive",
    "recv_all",
    "send",
    "stop",
    "delete",
    "change",
    "plus",
    "target",
    "back",
    "group_select",
    "folder_tree",
    "lupe",
    "ascii_hex",
    "lock_view",
    "cycle",
    "load_file",
    "sync"
]
StatusName = Literal[
    "relay_off",
    "relay_on"
]
EventName = Literal[
    "exchange",
    "ready",
    "no_transport",
    "connected",
    "read",
    "no_port",
    "timeout",
    "no_access",
    "fingerprint",
    "stop",
    "handle_stop",
    "execute_error",
    "yellow_bagel",
    "version_error",
    "unknown"
]
IconName = Literal[
    ic.Name,
    EventName,
    ActionName,
    StatusName
]
Icons: TypeAlias = dict[IconName, ImageTk]
images: dict[IconName, Image] = {name: get_image(F"{name}.png") for name in IconName.__args__}
