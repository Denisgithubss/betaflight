#!/usr/bin/env python3

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[3]
OSD_ELEMENTS = ROOT / "src/main/osd/osd_elements.c"
OSD_CORE = ROOT / "src/main/osd/osd.c"
OSD_HEADER = ROOT / "src/main/osd/osd.h"
CMS_MENU = ROOT / "src/main/cms/cms_menu_osd.c"
CLI_SETTINGS = ROOT / "src/main/cli/settings.c"
HAKRC_TARGET = ROOT / "src/config/configs/HAKRCF722V2_ATR3000/config.c"
MATEK_TARGET = ROOT / "src/config/configs/MATEKF405TE_SD/config.c"


def fail(message: str) -> None:
    print(f"SEC1 audit failed: {message}", file=sys.stderr)
    sys.exit(1)


def extract_function_body(source: str, function_name: str) -> str:
    match = re.search(rf"static void {function_name}\(.*?\)\n\{{", source, re.S)
    if not match:
        fail(f"function {function_name} not found")

    start = match.end()
    depth = 1
    pos = start
    while pos < len(source) and depth:
        char = source[pos]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        pos += 1

    if depth != 0:
        fail(f"function {function_name} body is not balanced")

    return source[start:pos - 1]


def main() -> None:
    source = OSD_ELEMENTS.read_text()
    osd_core = OSD_CORE.read_text()
    osd_header = OSD_HEADER.read_text()
    cms_menu = CMS_MENU.read_text()
    cli_settings = CLI_SETTINGS.read_text()
    hakrc_target = HAKRC_TARGET.read_text()
    matek_target = MATEK_TARGET.read_text()
    sec1_body = extract_function_body(source, "osdElementSec1Tag")
    build_body = extract_function_body(source, "osdBuildSec1TagVisual")

    if 'static const char sec1VisualPattern[] = "101011010110";' not in source:
        fail('SEC1 pattern must remain exactly "101011010110"')

    if "SYM_PB_FULL" not in build_body:
        fail("SEC1 visual builder must use SYM_PB_FULL for 1 bits")

    if "SYM_PB_EMPTY" not in build_body:
        fail("SEC1 visual builder must use SYM_PB_EMPTY for 0 bits")

    if "SYM_BLANK" in build_body:
        fail("SEC1 visual builder must not use SYM_BLANK")

    forbidden_calls = (
        "displayWrite(",
        "displayWriteChar(",
        "osdDisplayWrite(",
        "osdDisplayWriteChar(",
    )
    if any(call in sec1_body for call in forbidden_calls):
        fail("SEC1 renderer must not bypass normal OSD item positioning")

    if "element->buff" not in sec1_body:
        fail("SEC1 renderer must populate element->buff for the common OSD renderer")

    if "osdBuildSec1TagVisual();" not in sec1_body:
        fail("SEC1 renderer must build the visual pattern through the shared helper")

    forbidden_tokens = (
        "SEC1:",
        "SYNC",
        "HEADER",
        "sec1Header",
        "sec1Sync",
        "prefix",
    )
    if any(token in build_body for token in forbidden_tokens):
        fail("SEC1 visual builder must not add text/header/sync/prefix content")

    if 'osdElementConfig->item_pos[OSD_SEC1_TAG]           = OSD_POS(2, 1);' not in osd_core:
        fail("SEC1 default position must be OSD_POS(2, 1)")

    if "element->item_pos[OSD_SEC1_TAG] = OSD_PROFILE_1_FLAG | OSD_POS(2, 1);" not in hakrc_target:
        fail("HAKRCF722V2_ATR3000 must keep SEC1 default at OSD_POS(2, 1)")

    if "element->item_pos[OSD_SEC1_TAG] = OSD_PROFILE_1_FLAG | OSD_POS(2, 1);" not in matek_target:
        fail("MATEKF405TE_SD must keep SEC1 default at OSD_POS(2, 1)")

    if osd_header.count("OSD_SEC1_TAG") != 1:
        fail("only one OSD_SEC1_TAG item may exist in osd.h")

    if source.count("[OSD_SEC1_TAG]") != 1:
        fail("only one SEC1 renderer mapping may exist in osd_elements.c")

    if cms_menu.count('"SEC1 TAG"') != 1:
        fail("CMS must expose exactly one SEC1 TAG item")

    if cli_settings.count('"osd_sec1_tag_pos"') != 1:
        fail("CLI must expose exactly one osd_sec1_tag_pos setting")

    print("SEC1 audit passed")


if __name__ == "__main__":
    main()
