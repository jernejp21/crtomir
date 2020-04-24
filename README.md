# Črtomir ploter

Črtomir is open source CNC plotter. It takes SVG files and produces G-code. For now, only line drawing is supported. You can plot lines and shapes, but cannot fill shapes.

## How to use
### What do I need?
To use this python program, you will need the following SW packages:
- Python (I'm using <a href="https://www.anaconda.com/distribution/">Anaconda Python</a> 3.7 for development and test)
- Pthon packages:
  - <a href="https://pypi.org/project/PyQt5/">PyQt5</a>
  - <a href="https://pypi.org/project/numpy/">Numpy</a>

### How to use?
- Clone or download repository.
- Run the program from command line or terminal `python main.py`


# For developers
To edit GUI, please use Qt Creator or Qt Designer. Use .ui files and generate python code.
To generate python code from .ui files, use **convert_UI_to_Py.bat**. Because I'm testing on Windows, add path to **pyuic5.exe** to environmental variables as **PYUIC**.

If you are using Anaconda python, location is **..\anaconda3\Scripts**.