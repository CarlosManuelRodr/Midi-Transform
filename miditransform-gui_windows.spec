# -*- mode: python -*-
a = Analysis(['miditransform-gui.pyw'],
             pathex=['C:\\Users\\Carlos\\Documents\\Programacion\\midi-transform'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break

a.datas += [('resources/midi-transform-icon.png', 'resources/midi-transform-icon.png', 'DATA')]
a.datas += [('resources/play.png', 'resources/play.png', 'DATA')]
a.datas += [('resources/stop.png', 'resources/stop.png', 'DATA')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='miditransform-gui.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='resources/midi-transform-icon.ico' )
