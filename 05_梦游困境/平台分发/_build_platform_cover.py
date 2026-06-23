# -*- coding: utf-8 -*-
"""第 5 期《梦游困境》抖音/快手图文 9:16 信息流封面生成器。
复用系列设计 token（字体/配色），文字进上方负空间、不压原图主体（嗦粉案教训）。
用法：py _build_platform_cover.py 依赖：pip install Pillow
产物：梦游困境_抖音快手封面_9x16.png（1080×1920）。
"""
import os
from PIL import Image, ImageDraw, ImageFont

SRC = "../梦游困境_原图.png"
OUT = "梦游困境_抖音快手封面_9x16.png"

# 信息流钩子文案（制造知识缺口：题面俩词、多数人只做一个）
KICKER = "PROMPT BATTLE 当日冠军 · 第 5 期"
TITLE1 = "题目有俩词"
TITLE2 = "多数人只做一个"
SUB    = "「梦游困境」别画梦游的人，画“出不去”"
CTA    = "↘ 完整 prompt + 四层拆解 在后面"

# ===== 设计系统（对齐系列母版）=====
W, H = 1080, 1920
MARGIN = 88
BG    = (244, 238, 230)
INK   = (47, 45, 42)
MUTED = (140, 132, 121)
HAIR  = (213, 203, 190)
ACCENT = (198, 138, 51)   # 系列 trans 黄（困境层色）

FONTS = r"C:/Windows/Fonts"
def _f(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)
def msyh(s):  return _f("msyh.ttc", s)
def msyhb(s): return _f("msyhbd.ttc", s)
def deng(s):  return _f("Dengl.ttf", s)
def dengb(s): return _f("Dengb.ttf", s)

def tracked(d, xy, s, fnt, fill, tracking=0, center_w=None):
    x, y = xy
    widths = [d.textlength(ch, font=fnt) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1) if s else 0
    if center_w is not None:
        x = (center_w - total) / 2
    for ch, wch in zip(s, widths):
        d.text((x, y), ch, font=fnt, fill=fill); x += wch + tracking
    return total

def rounded(im, r):
    im = im.convert("RGBA")
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=r, fill=255)
    im.putalpha(m); return im

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)

    # 顶部系列标
    tracked(d, (0, 70), "目标是成为 PROMPT 大师", deng(30), MUTED, tracking=6, center_w=W)

    # kicker（小标·强调名次身份）
    tracked(d, (0, 138), KICKER, dengb(34), ACCENT, tracking=2, center_w=W)

    # 大标题钩子（两行，进上方负空间）
    tracked(d, (0, 200), TITLE1, msyhb(104), INK, tracking=4, center_w=W)
    tracked(d, (0, 322), TITLE2, msyhb(104), INK, tracking=4, center_w=W)

    # 副标题
    tracked(d, (0, 462), SUB, deng(40), MUTED, tracking=1, center_w=W)

    # 原图（居中，宽度撑满边距内，3:4 竖图自然放在中下部）
    src = Image.open(os.path.join(here, SRC)).convert("RGB")
    box_w = W - MARGIN * 2
    box_h = int(box_w * src.size[1] / src.size[0])
    top = 548
    src = rounded(src.resize((box_w, box_h), Image.LANCZOS), 24)
    x = (W - box_w) // 2
    d.rounded_rectangle([x-2, top-2, x+box_w+2, top+box_h+2], radius=26, outline=HAIR, width=3)
    c.paste(src, (x, top), src)
    img_bottom = top + box_h

    # 底部 CTA 带
    cta_y = max(img_bottom + 46, H - 150)
    d.rounded_rectangle([MARGIN, cta_y, W-MARGIN, cta_y+88], radius=20, fill=ACCENT)
    tracked(d, (0, cta_y+24), CTA, msyhb(38), (250, 246, 240), tracking=1, center_w=W)

    c.save(os.path.join(here, OUT), quality=95)
    print("saved", OUT, "| img_bottom=", img_bottom, "| cta_y=", cta_y, "(需 cta_y+88 <", H, ")")

if __name__ == "__main__":
    main()
