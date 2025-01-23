# The Saturday Sessions

Welcome to the The Saturday Sessions, a collection of tutorials and resources designed to
provide exposure to equity-seeking students as part of the Open Seeds Cohort and Digital Research Alliance EDIA
Champions Program.

This guide is intended to lower the barrier to entry so that you can submit your first working jobs
in a variety of fields with minimal tweaks.

## 🌟 Highlights 🌟

This guide has several valuable resources to help you get up to speed:

- **Workflows**: an overview of frequent workflows used with links to relevant software pages

- **Software Pages**: introductions to the various tools referenced in this documentation

- **Tutorials**: walkthroughs for several common workflows/softwares

- **Sample Scripts**: example Python and SLURM scripts

- **Tips**: common issues and their resolutions/work-arounds

## Prerequisites

- **Set up your local machine**: this guide assumes that your local machine
  is setup up with the necessary software already installed (e.g., Hatch, Python, etc.)

- **Set up your cluster account**: some of the tutorials in the guide
  require that you connect to the remote clusters provided by the Alliance. For these
  tutorials, you will need a [valid CCDB account](docs/sources/tutorials/ccdb.md) and to
  set up your remote cluster environment.

## :rocket: Quickstart :rocket:

1. Create a virtual environment in the top-level directory of this project's folder
(in the same directory as this README).

    ```bash
    python3 -m venv .venv
    ```

2. Activate your environment.

    ```bash
    source .venv/bin/activate
    ```

3. Install the required Python dependencies.

    ```bash
    python3 -m pip install .
    ```

4. Pick a tutorial!

## ⚒ Build Webpage ⚒

To view the complete guide as a website, you need to install [mkdocs][mkdocs],
the [Material][material] theme, and [mdx_truly_sane_lists][mdx-truly-sane-lists]
These packages are grouped into the "docs" optional dependency group and can be
installed via:

```bash
pip install '.[docs]'
```

Then run:

```bash
mkdocs build && mkdocs serve
```

Finally, copy the IP address printed to the command line

```bash
...
INFO    -  [09:50:28] Serving on http://127.0.0.1:8000/
...
```

and paste it into your browser!

[mkdocs]: https://www.mkdocs.org/user-guide/
[material]: https://github.com/squidfunk/mkdocs-material
[mdx-truly-sane-lists]: https://github.com/radude/mdx_truly_sane_lists
