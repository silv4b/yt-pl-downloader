from app.core.utils import sanitize_filename


def test_sanitize_filename_removes_accents():
    assert sanitize_filename("café") == "cafe"


def test_sanitize_filename_removes_special_chars():
    assert sanitize_filename("video<name>.txt") == "videonametxt"


def test_sanitize_filename_replaces_spaces():
    assert sanitize_filename("my video title") == "my_video_title"


def test_sanitize_filename_strips_underscores():
    assert sanitize_filename("__video__") == "video"


def test_sanitize_filename_preserves_alphanumeric():
    assert sanitize_filename("Video123") == "Video123"
