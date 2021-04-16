
python -m venv %~dp0 %
call Scripts\activate.bat
pip install keyboard colorama mutagen pyglet
cls
python %~dp0\game.py %
