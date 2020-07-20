#!/usr/local/bin/python3

import argparse
import cairosvg
import os
from svgpathtools import svg2paths

from html.parser import HTMLParser

template = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg
  style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns="http://www.w3.org/2000/svg"
  version="1.1">
  <defs/>
  <g id="{}">
   <path d="{}"/>
  </g>
</svg>
"""
class SFSymbolParser(HTMLParser):

    def __init__(self, symbol):
        super(SFSymbolParser, self).__init__()
        self.regM = False
        self.pathText = 'none'
        self.symbolName = symbol

    def handle_starttag(self, tag, attrs):
        if tag == 'g' and attrs[0][0] == 'id' and attrs[0][1] == self.symbolName:
            self.regM = True
        if tag == 'path' and self.regM:
            self.pathText = attrs[0][1]

    def handle_endtag(self, tag):
        if tag == 'g':
            self.regM = False


parser = argparse.ArgumentParser(description='Convert an SFSymbol file type to pdf or png.')
parser.add_argument("src", nargs = "?", help='Path to SFSymbol file')
parser.add_argument("dest", nargs = '?', help='Path to save converted file. Include name but not format extension.')
parser.add_argument("--style", nargs = "?", default='Regular-M', help='The specific style to use for export. Default is Regular-M')
parser.add_argument("--type", choices = ["pdf", "png"], default='pdf')
parser.add_argument("--png_size", type=int, nargs = "?", default='48', help='Used for png type, size of 1x image. 2x and 3x will be scaled.')
args = parser.parse_args()

sfSymbolFile = open(args.src, 'r')

parser = SFSymbolParser(args.symbol)
parser.feed(sfSymbolFile.read())

# print(template.format(args.symbol, parser.pathText))
svg_text = template.format(args.symbol, parser.pathText)
output = open('temp.svg', 'w')
output.write(svg_text)
output.close()
sfSymbolFile.close()

paths, attributes = svg2paths('temp.svg')
mypath = paths[0]

xmin, xmax, ymin, ymax = mypath.bbox()
x = xmin
y = ymin
width = xmax - xmin
height = ymax - ymin

svg_split_text = svg_text.split('<svg', 1)
svg_with_view_box = '{}<svg\nviewBox="{} {} {} {}"{}'.format(svg_split_text[0], x, y, width, height, svg_split_text[1])

if args.type == "pdf":
    cairosvg.svg2pdf(bytestring=svg_with_view_box.encode('utf-8'), write_to='{}.pdf'.format(args.dest))
elif args.type == "png":
    # Create 1x, 2x and 3x images
    atOnex = args.png_size
    atTwox = atOnex * 2
    atThreex = atOnex * 3
    cairosvg.svg2png(bytestring=svg_with_view_box.encode('utf-8'), parent_width=atOnex, parent_height=atOnex, write_to='{}@1x.png'.format(args.dest))
    cairosvg.svg2png(bytestring=svg_with_view_box.encode('utf-8'), parent_width=atTwox, parent_height=atTwox,
                     write_to='{}@2x.png'.format(args.dest))
    cairosvg.svg2png(bytestring=svg_with_view_box.encode('utf-8'), parent_width=atThreex, parent_height=atThreex,
                     write_to='{}@3x.png'.format(args.dest))

os.remove('temp.svg')
