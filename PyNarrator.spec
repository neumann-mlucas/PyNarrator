# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['pynarrator/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('dialog', 'dialog'),
        ('translated_dialog', 'translated_dialog'),
        ('img', 'img'),
        ('save', 'save')],
    hiddenimports=[],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PyNarrator',
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
