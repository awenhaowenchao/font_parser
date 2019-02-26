#!/usr/bin/python
#coding=utf-8

import io
import requests
from fontTools.ttLib import TTFont
from parser.font_parser import FontParser

SAMPLE_FONT_URL = ' https://static.yximgs.com/udata/pkg/kuaishou-front-end-live/fontscn_qw2f1m1o.ttf'
SAMPLE_FONT_MAPPING = {
    'uniABCB': '4',
    'uniACCD': '3',
    'uniACDA': '0',
    'uniAEFF': '8',
    'uniAFBB': '6',
    'uniBDCA': '1',
    'uniBDCC': '5',
    'uniBFEF': '9',
    'uniCCAA': '2',
    'uniCFBA': '7',
}

class KuaishouFontParser(FontParser):
    def __init__(self, name='kuaishou'):
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
        return KuaishouFont(url, self.glyphs_mapping)


class KuaishouFont:

    def __init__(self, url, mapping):
        self._url = url
        self._glyphs = None
        #unicode-escape形式的mapping
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
        li = []
        new_data = (list(map(lambda x: x.encode('unicode_escape'), codes)))
        for i in new_data:
            if len(str(i)) > 5:
                num = self._glyphs_ru[str(i)[3:-1]]
                li.append(str(num))
            else:
                li.append(str(i)[2:-1])
        res = ''.join(li)
        return res

if __name__ == '__main__':
    parser = KuaishouFontParser()
    font = parser.load('https://static.yximgs.com/udata/pkg/kuaishou-front-end-live/fontscn_h57yip2q.ttf')
    font.normalize('붪.곭w')