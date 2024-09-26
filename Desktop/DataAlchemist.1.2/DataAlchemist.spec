# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['src\\start.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icon/*.ico', 'assets/icon'),
	('lib/tkinterDnD/*', 'tkinterDnD'), 
    	('lib/tkinterdnd2/*', 'tkinterdnd2'), 
    	('lib/pandas/*', 'pandas'),
    	('lib/matplotlib/*', 'matplotlib'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DataAlchemist',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)