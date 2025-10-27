# typer-invoke

[![pypi](https://img.shields.io/pypi/v/typer-invoke.svg)](https://pypi.python.org/pypi/typer-invoke)
[![Project License - MIT](https://img.shields.io/pypi/l/typer-invoke.svg)](https://github.com/joaonc/show_dialog/blob/main/LICENSE.txt)

Simplified invocation of typer apps from any directory.

The idea is that you place typer apps in a directory in your project and then you can invoke them
from any directory.

## Why?
The main use case is for project management that require custom scripts for various tasks.
Wrapping those scripts as typer apps makes them easier to use.
Making typer easier to use makes those scripts even easier to use.

An alternative to:

* [Make](https://www.gnu.org/software/make/manual/make.html)
* [Invoke](https://www.pyinvoke.org/)

### VS Invoke
The main driver for this project is as a replacement for Invoke, which I've been using for
a while and found the following limitations:

* `--help` and `--list` options are clunky, in that they need to be placed right after the `inv`
  command, ex:
  ```
  inv --help some.task
  ```
  Here a more common pattern is used and `--help` acts as both help and list:
  ```
  inv some task --help
  ```
* Lack of support.
  Some issues and features have been piling up for a while, and I'm not sure if they will ever
  be addressed. Seems like [the project](https://github.com/pyinvoke/invoke) has had new development
  recently, though.  
  [Typer](https://typer.tiangolo.com/) is widely used and has a lot of support.

Other advantages (in my opinion):
* Prettier
  Developer experience counts. Other than more common usage patterns, Typer supports
  [rich](https://github.com/Textualize/rich) and Markdown formatting.
* No dot `.` namespace
  Invoke uses a dot `.` namespace for tasks, which is not very common when running scripts.  
  Typer follows a normal CLI pattern. Namespaces are Typer apps and are separated by a space.

Invoke is the inspiration for this project, hence the name `typer-invoke` and keeping the `inv`
command name.
