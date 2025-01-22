import json
from pathlib import Path
from typing import Dict


class Translator:

    def __init__(self, dictionary: Dict) -> None:
        self._dictionary: Dict = dictionary

    @classmethod
    def from_json_file(cls, path: str):
        return cls(json.loads(Path(path).read_text(encoding='utf8')))

    def set_dictionary(self, dictionary: Dict):
        self._dictionary = dictionary

    def exists(self, phrase: str) -> bool:
        return self._dictionary.get(phrase) is not None

    def translate(self, phrase: str, nested: bool = False, **kwargs):
        translation: str = ""
        if nested:
            dict_copy = self._dictionary
            for key in phrase.split('.'):
                val  = dict_copy.get(key)
                if isinstance(val, str):
                    translation = val
                    break
                else:
                    dict_copy = val
        else:
            translation = self._dictionary.get(phrase) if phrase in self._dictionary else phrase
        return translation if len(kwargs) == 0 else translation.format(**kwargs)
