# Cocotbext BUS Base
### Provides base of methods for bus extensions

![image](docs/manual/img/AFRL.png)

---

   author: Jay Convertino   
   
   date: 2025.03.26
   
   details:
   
   license: MIT   
   
---

### Version
#### Current
  - V0.0.0 - initial release

#### Previous
  - none

### DOCUMENTATION
  For detailed usage information, please navigate to one of the following sources. They are the same, just in a different format.

  - [cocotbext_busbase.pdf](docs/manual/cocotbext_busbase.pdf)
  - [github page](https://johnathan-convertino-afrl.github.io/cocotbext-up/)

### DEPENDENCIES
#### Build
  - cocotb (python)

### COMPONENTS

  - cocotbext = Contains all of the various uP drivers by version.
  - docs = Contains all documents on how to use the core in PDF, and HTML formats.
  - tests = Contains test code to verify drivers and monitors.

```bash
├── cocotbext
│   └── busbase
│       ├── busbase.py
│       ├── __init__.py
│       └── version.py
├── docs
│   ├── index.html
│   └── manual
│       ├── cocotbext-busbase.html
│       ├── config
│       │   ├── Comments.txt
│       │   ├── Languages.txt
│       │   ├── Project.txt
│       │   └── Working Data
│       │       ├── CodeDB.nd
│       │       ├── Comments.nd
│       │       ├── Files.nd
│       │       ├── Languages.nd
│       │       ├── Output
│       │       │   ├── BuildState.nd
│       │       │   ├── Config.nd
│       │       │   └── SearchIndex.nd
│       │       ├── Parser.nd
│       │       └── Project.nd
│       ├── css
│       │   └── custom_font_l2h.css
│       ├── html
│       ├── img
│       │   ├── AFRL.png
│       │   └── diagrams
│       ├── makefile
│       ├── makefiles
│       │   ├── makefuselatex.mk
│       │   ├── makehtml.mk
│       │   └── makepdf.mk
│       ├── py
│       │   └── gen_fusesoc_latex_info.py
│       └── src
│           ├── common.tex
│           ├── fusesoc
│           ├── html.tex
│           └── pdf.tex
├── LICENSE.md
├── MANIFEST.in
├── README.md
├── setup.cfg
├── setup.py
└── tests
    └── busbase
        ├── Makefile
        ├── test.py
        └── test.v

```
