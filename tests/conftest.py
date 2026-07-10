import pytest


@pytest.fixture(autouse=True)
def _tmp_media(settings, tmp_path):
    """Keep uploaded/seeded files out of the repo's media/ during tests."""
    settings.MEDIA_ROOT = tmp_path / "media"
