"""test ShieldsLink class"""

from cimd.classes.shields_link import ShieldsLink


def test_shields_link() -> None:
    """Test shields link creation"""
    minimal = ShieldsLink(message="hello")
    assert str(minimal) == minimal.to_string()
    message = ShieldsLink(label="hello", message="there")
    assert str(message) == "https://img.shields.io/badge/hello-there-blue"
    logo = ShieldsLink(label="hello", message="there", logo="trivy")
    assert str(logo) == "https://img.shields.io/badge/hello-there-blue?logo=trivy"
    red = ShieldsLink(label="hello", message="there", logo="trivy", color="red")
    assert str(red) == "https://img.shields.io/badge/hello-there-red?logo=trivy"
    with_dash = ShieldsLink(label="hel-lo", message="th-ere", logo="tri-vy")
    assert str(with_dash) == "https://img.shields.io/badge/hel--lo-th--ere-blue?logo=tri-vy"
    with_base = ShieldsLink(
        label="hello", message="there", logo="trivy", color="red", base="https://example.org/"
    )
    assert str(with_base) == "https://example.org/hello-there-red?logo=trivy"
    assert str(with_base) == with_base.to_string()
