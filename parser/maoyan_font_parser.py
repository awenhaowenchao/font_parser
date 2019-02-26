#!/usr/bin/python
#coding=utf-8

import io
import requests
from fontTools.ttLib import TTFont
from parser.font_parser import FontParser

SAMPLE_FONT_URL = 'http://vfile.meituan.net/colorstone/2c8d9a8f5031f26f4e9fe924263e31ce2076.woff'
SAMPLE_FONT_MAPPING = {
    'uniE851': 0,
    'uniEBCF': 1,
    'uniF38E': 2,
    'uniE824': 3,
    'uniEFFE': 4,
    'uniE829': 5,
    'uniEDEE': 6,
    'uniF35D': 7,
    'uniF3C5': 8,
    'uniEE5A': 9
}

class MaoyanFontParser(FontParser):
    def __init__(self, name='maoyan'):
        super().__init__(name)
        self._init_glyphs_mapping()

    def _init_glyphs_mapping(self):
        font = TTFont(io.BytesIO(requests.get(SAMPLE_FONT_URL).content))
        glyph_set = font.getGlyphSet()
        glyphs = glyph_set._glyphs.glyphs
        self.glyphs_mapping = {}
        for uni, number in SAMPLE_FONT_MAPPING.items():
            self.glyphs_mapping[glyphs[uni].data] = number

    def load(self, url):
        return MaoyanFont(url, self.glyphs_mapping)


class MaoyanFont:

    def __init__(self, url, mapping):
        self._url = url
        self._glyphs = None
        # unicode-escape形式的mapping
        self._glyphs_ru = {}
        self.mapping = mapping

    @property
    def glyphs(self):
        if not self._glyphs:
            font = TTFont(io.BytesIO(requests.get(self._url).content))
            glyph_set = font.getGlyphSet()
            self._glyphs = glyph_set._glyphs.glyphs
        return self._glyphs

    def uni_to_number(self, uni):
        return self.mapping[self.glyphs[uni].data]

    def normalize(self, codes):
        for k in self.glyphs.keys():
            if 'uni' in k:
                if self.glyphs[k].data in self.mapping:
                    self._glyphs_ru[k.replace('uni', '\\u').lower()] = self.mapping[self.glyphs[k].data]
        # li = []
        # new_data = (list(map(lambda x: x.encode('unicode_escape'), codes)))
        # for i in new_data:
        #     if len(str(i)) > 5:
        #         num = self._glyphs_ru[str(i)[3:-1]]
        #         li.append(str(num))
        #     else:
        #         li.append(str(i)[2:-1])
        # res = ''.join(li)
        # return res
        number = ''
        for c in codes.split(';'):
            uni = 'uni%s' % c[-4:].upper()
            if uni in self.glyphs:
                number += str(self.uni_to_number(uni))
            else:
                number += c
        return number

if __name__ == '__main__':
    parser = MaoyanFontParser()
    font = parser.load('https://vfile.meituan.net/colorstone/2a9eb2852b2dee19c7720dae4a35c85f2076.woff')
    str1 = '&#xe0b7;&#xe0b7;&#xf6ca;&#xe032;&#xe032;&#xf6ca;'
    font.normalize(str1)