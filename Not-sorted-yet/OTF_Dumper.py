#Used in the amat_eursctf 2024
from fontTools.ttLib import TTFont

def dump_otf(file_path):
    font = TTFont(file_path)
    font.saveXML("output.xml")

dump_otf("agile-rut.otf")

#<LigatureSet glyph="a">
#components="m,a,t,e,u,r,s,c,t,f,braceleft, ....... , braceright" glyph="lig.j.u.s.t.a.n.a.m.e.o.k.xxxxxxxxx.xxxx.x.xxxxxxxxxx.x.x.x.xxxxxxxxxx.xxx.xxxxxxxxxx.x.x.x.x.xxxxxxxxxx.x.x.x.x.xxxxxxxxxx.x.x.x.xxxxxxxxxx.x.x.x.x.x.xxxx.xxxxxxxxxx.xxxxx.xxxxx.xxxxx.xxxxxxxxxx"/>