# beijing fushengji rewrite


<a href="https://pypi.org/project/beijing_fushengji/">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/beijing_fushengji">
</a>

北京浮生记重制版

Rewrite [beijing fushengji][url] using Qt.

[url]: https://github.com/chrisguo/beijing_fushengji

Features:
 - all dialogs are reproduced.
 - support sounds.
 - Support Autosave.
 - Support both English and Simplified Chinese.


![main](https://github.com/soda92/beijing_fushengji_rewrite/raw/main/main.png)
![main_en](https://github.com/soda92/beijing_fushengji_rewrite/raw/main/main-en.png)

## Install package From PYPI

```
pip install -U beijing_fushengji
```

Run:

`beijing-fushengji`

## Run locally

1. Clone repo
1. install [uv](https://docs.astral.sh/uv/)
1. run `uv sync`, then activate the virtual environment
1. run `tools/compile_all.py`
1. Start app with `entry.py`

## Design Forms

Run `tools/design.py`

## Translation

Run `tools/translate.py`

## Other considerations

On debian, you need to install some dependencies first. see `debian_deps.sh`.

On linux with fcitx, need to copy some libs for `Linguist` translator to support Chinese. see `enable-pyside-fcitx.sh`.
