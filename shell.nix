# Intent:
#   This nix file specifies a suitable environment for building our docs.
#   It shall not be mis-used to actually *execute* the building of our docs.
#   Building of docs is the responsibility of {make, forge or some build.sh}.
#
# How:
#   Nix is not used everywhere (yet!), so for now, we rely on the lowest common denominator: pip.
#   Why pip?
#     1. familiarity: everybody and their grandma knows pip
#     2. pip has **lots** of python packages - many too obscure for Nix to bother with
#     3. some python packages are very fast-moving, so putting these in docker is maintenance - let pip deal with it
#     4. pip requirements.txt is declarative
#     5. pip is idempotent (though impure)
#
#   But pip has some issues:
#     a. pip installs to global shared space: either local user or system-wide
#     b. conflicts with already-installed versions can occur
#     c. pip wants to update/mutate itself
#
#   Thus a normal pip installation is fragile and non-reproducible.
#   To solve this, we use make a virtualenv **within** the workspace, just for documentation.
#   virtualenv prevents clobbering between logically-separate python-installations.
#
# This nix file just specifies how such a pip-virtualenv can be made.
# If you have nix, you can get that environment.
# If you don't have nix, you can read this file and do similar stuff.


# Lock all nix-package versions to that which is released atomically together
with (import (builtins.fetchTarball {
  # Release '22.05' is a tag which points to ce6aa13369b667ac2542593170993504932eb836
  url = "https://github.com/nixos/nixpkgs/tarball/22.05";
  # This hash is git-agnostic so nix can detect if the git-tag changes
  sha256 = "0d643wp3l77hv2pmg2fi7vyxn4rwy0iyr8djcw1h5x72315ck9ik";
}) {});

# Alternative to fetchTarball, we can fetchGit (but fetchGit is slower):
#   with (import (builtins.fetchGit {
#     url = "https://github.com/nixos/nixpkgs/";
#     ref = "refs/tags/22.05";
#     rev = "ce6aa13369b667ac2542593170993504932eb836";
#   }) {});

mkShell {

  buildInputs = [
    git
    xorg.xorgserver  # drawio requires an X. Xvfb is part of this
    doxygen
    graphviz
    drawio

    # Keep python-dependencies in pip-land with venv insulation padding
    python39
    python39Packages.pip
    python39Packages.virtualenv

    # LaTeX needed for PDF output -- massive!
    (texlive.combine { inherit (texlive) scheme-medium latexmk cmap fncychap wrapfig capt-of framed upquote needspace tabulary varwidth titlesec; })
  ];


  # The folder containing this nix file, i.e. <workspace>/git/doc
  # wdh_doc_folder = builtins.toString ./.;

  # Output artifacts: Generated HTML documentation
  obj_output_folder = builtins.toString ../obj/doc;

  # Ephemeral cache for required python packages
  obj_venv_folder   = builtins.toString ../obj/venv;


  shellHook = ''
   trap 'echo "\$ $BASH_COMMAND"' DEBUG  # Print commands below, but less noisy than 'set -x' does

   # nix-shell preserves $PWD from calling shell, but we want to be in doc folder here
   # cd $doc_folder || exit 1

   # Ensure folders exist
   mkdir -p $obj_output_folder $obj_temp_folder

   # Let pip install into a virtual environment just for documentation
   virtualenv --quiet $obj_venv_folder
   source $obj_venv_folder/bin/activate   # Exports VIRTUAL_ENV

   # Annoyingly, venv's activate only exports PATH but not PYTHONPATH
   export PYTHONPATH=$VIRTUAL_ENV/lib/python3.9/site-packages:$PYTHONPATH

   # Finally install into the venv
   # TODO: Turn this into a nix package so we can avoid running pip every time
   export PIP_DISABLE_PIP_VERSION_CHECK=1
   pip install --quiet -r requirements.txt

   trap - DEBUG  # Don't print commands anymore
  '';
}
