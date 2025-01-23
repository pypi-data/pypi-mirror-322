from typing import Optional

from injector import singleton

from griff.services.uniqid.generator.uniqid_generator import UniqIdGenerator


@singleton
class FakeUniqIdGenerator(UniqIdGenerator):
    def __init__(self, start_id=1):
        self._start = 0
        self._start = start_id - 1
        self._session = {"default": self._start}

    def next_id(self, name: Optional[str] = None) -> str:
        if name is None:
            name = "default"
        if name not in self._session:
            name_length = len(self._sanitize_name(name))
            start_length = len(str(self._start))
            total_length = 10 + name_length + start_length
            if total_length > 26:
                raise ValueError(
                    f"Uniq Id will be too long {total_length} > 26, reduce start_id "
                    f"({self._start}={start_length}) or name ({name}={name_length})"
                )
            self._session[name] = self._start

        self._session[name] += 1
        return self._format_id(name)

    def reset(self, start_id: int = 1):
        self._start = start_id - 1
        self._session = {"default": self._start}

    def _format_id(self, name: str) -> str:
        if name == "default":
            return f"FAKEULID{self._session[name]:>018}"

        postfix = self._sanitize_name(name)
        pad = 16 - len(postfix)
        id = f"FAKEULID-{postfix}-{self._session[name]:>0{pad}}"
        # noinspection Assert
        assert len(id) == 26, f"id length must be 26, got {len(id)}"
        return id

    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.replace("_", "").upper()
