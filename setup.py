from setuptools import setup

APP = ['Egg_Game.py']
DATA_FILES = ['Broke_egg.png',
              'chick.png',
              'coin_sound.wav',
              'Duck.png',
              'egg.png',
              'eggBreak_sound.wav',
              'gameOver_sound.wav',
              'jump_sound.wav']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],  # Add any packages you use, like 'requests'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
