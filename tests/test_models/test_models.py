from app.models.playlist import PlaylistInfo
from app.models.video import VideoInfo


def test_video_info_creation():
    video = VideoInfo(title="Test", url="https://example.com")
    assert video.title == "Test"
    assert video.url == "https://example.com"
    assert video.uploader is None
    assert video.duration is None


def test_video_info_with_all_fields():
    video = VideoInfo(
        title="Test",
        url="https://example.com",
        uploader="Channel",
        duration=120,
        thumbnail="https://img.example.com",
    )
    assert video.uploader == "Channel"
    assert video.duration == 120


def test_playlist_info_creation():
    playlist = PlaylistInfo(title="My Playlist", url="https://example.com/playlist")
    assert playlist.title == "My Playlist"
    assert playlist.total_videos == 0
    assert playlist.videos == []


def test_playlist_info_with_videos():
    videos = [
        VideoInfo(title="Video 1", url="https://example.com/1"),
        VideoInfo(title="Video 2", url="https://example.com/2"),
    ]
    playlist = PlaylistInfo(title="My Playlist", url="https://example.com/playlist", videos=videos)
    assert playlist.total_videos == 2
    assert playlist.videos[0].title == "Video 1"
