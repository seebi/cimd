"""test ShieldsLink class"""

from cimd.classes.shields_link import ShieldsLink


def test_minimal() -> None:
    """Test shields link creation"""
    minimal = ShieldsLink(message="hello")
    assert str(minimal) == minimal.to_string()


def test_with_label() -> None:
    """Test shields link creation - with label"""
    with_label = ShieldsLink(label="hello", message="there")
    assert str(with_label) == "https://img.shields.io/badge/hello-there-blue"


def test_with_logo() -> None:
    """Test shields link creation - with logo"""
    logo = ShieldsLink(label="hello", message="there", logo="trivy")
    assert str(logo) == "https://img.shields.io/badge/hello-there-blue?logo=trivy"


def test_with_color() -> None:
    """Test shields link creation - with color"""
    red = ShieldsLink(label="hello", message="there", logo="trivy", color="red")
    assert str(red) == "https://img.shields.io/badge/hello-there-red?logo=trivy"


def test_with_base() -> None:
    """Test shields link creation - with different deployment base"""
    with_base = ShieldsLink(
        label="hello", message="there", logo="trivy", color="red", base="https://example.org/"
    )
    assert str(with_base) == "https://example.org/hello-there-red?logo=trivy"
    assert str(with_base) == with_base.to_string()


def test_with_special_chars() -> None:
    """Test shields link creation - with special chars"""
    with_dash = ShieldsLink(label="hel-lo", message="th-ere", logo="tri-vy")
    assert str(with_dash) == "https://img.shields.io/badge/hel--lo-th--ere-blue?logo=tri-vy"
    with_percent = ShieldsLink(label="hello", message="there %")
    assert str(with_percent) == "https://img.shields.io/badge/hello-there%20%25-blue"
    with_umlaut = ShieldsLink(label="hellö", message="there")
    assert str(with_umlaut) == "https://img.shields.io/badge/hell%C3%B6-there-blue"
