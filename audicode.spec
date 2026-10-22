# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller audicode.spec --noconfirm   (see scripts/build_windows.ps1)
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = []
# routes/ and src/ load modules by string name (importlib / __import__)
for pkg in ("routes", "src", "core", "services", "integrations", "mcp_servers", "companion"):
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass
hiddenimports += [
    "uvicorn.logging", "uvicorn.loops", "uvicorn.loops.auto",
    "uvicorn.protocols", "uvicorn.protocols.http", "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets", "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan", "uvicorn.lifespan.on",
    "multipart", "webview", "pythonnet", "clr_loader",
    "sqlalchemy.dialects.sqlite", "tiktoken_ext", "tiktoken_ext.openai_public",
]

datas = [
    ("static", "static"),
    ("skills", "skills"),
    ("data/skills", "data/skills"),
    ("config", "config"),
    ("assets", "assets"),
]
for pkg in ("fastembed", "pyotp", "certifi"):
    try:
        datas += collect_data_files(pkg)
    except Exception:
        pass

a = Analysis(
    ["audicode_desktop.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["pytest", "tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="AudiCode",
    debug=False,
    strip=False,
    upx=False,
    console=False,  # --windowed
    icon="assets/icon.ico",
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="AudiCode")
