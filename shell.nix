{ pkgs ? import <nixpkgs> { }, ... }:
pkgs.mkShell {
  venvDir = ".venv";

  QT_QPA_PLATFORM = "xcb";

  packages = [ pkgs.python311 pkgs.poetry ];

  shellHook = ''
    export LD_LIBRARY_PATH="${
      pkgs.lib.makeLibraryPath [
        pkgs.libGL
        pkgs.xorg.libX11
        pkgs.xorg.libxcb
        pkgs.xorg.libXext
        pkgs.xorg.libICE
        pkgs.xorg.libSM
        pkgs.glib
      ]
    }:$LD_LIBRARY_PATH"

    python -m venv .venv
    poetry install
  '';
}
