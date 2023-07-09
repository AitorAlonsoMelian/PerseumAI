from pathlib import Path
import frozendict

datas = [(Path(frozendict.__path__[0]) / 'VERSION', 'frozendict')]