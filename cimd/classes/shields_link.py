"""shields.io link"""

from urllib.parse import quote


class ShieldsLink:
    """shields.io link"""

    message: str
    _label: str | None
    color: str
    logo: str | None
    base: str

    def __init__(
        self,
        message: str,
        label: str | None = None,
        color: str = "blue",
        logo: str | None = None,
        base: str = "https://img.shields.io/badge/",
    ):
        """Init a shields.io link

        {base}{label}-{message}-{color}?logo={logo}
        """
        self.label = label if label else None
        self.message = message
        self.color = color
        self.logo = logo
        self.base = base

    @staticmethod
    def _quote_path(value: str) -> str:
        """Replace some chars, then url path quote

        - "_" -> "__"
        - "-" -> "--"

        """
        value = value.replace("_", "__")
        value = value.replace("-", "--")
        value = quote(value, safe="/", encoding=None, errors=None)
        return value  # noqa: RET504

    @property
    def label(self) -> str | None:
        """Optional part: label-message-color"""
        if self._label:
            return self._quote_path(self._label)
        return None

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    def to_string(self) -> str:
        """Create URL string"""
        path = self._quote_path(self.message)
        if self.label:
            path = f"{self.label}-{path}"
        path = f"{path}-{self.color}"
        url = self.base + path
        if self.logo:
            url = f"{url}?logo={self.logo}"
        return url

    def __str__(self) -> str:
        """Create URL string"""
        return self.to_string()
