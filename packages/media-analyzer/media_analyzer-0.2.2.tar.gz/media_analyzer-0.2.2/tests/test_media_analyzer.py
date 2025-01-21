from pathlib import Path
from unittest.mock import patch

import pytest

from media_analyzer.data.anaylzer_config import AnalyzerSettings, FullAnalyzerConfig
from media_analyzer.data.interfaces.api_io import InputMedia
from media_analyzer.media_analyzer import MediaAnalyzer


def test_media_analyzer_none_settings() -> None:
    """Test the MediaAnalyzer with no settings."""
    analyzer = MediaAnalyzer()
    assert isinstance(analyzer.config, FullAnalyzerConfig)


@pytest.mark.parametrize(
    ("photo_filename", "expect_gps", "expect_gif"),
    [
        pytest.param("cat_bee.gif", False, True),
        pytest.param("tent.jpg", True, False),
        pytest.param("sunset.jpg", True, False),
        pytest.param("ocr.jpg", False, False),
        pytest.param("face2_b.jpg", False, False),
    ],
)
def test_media_analyzer(
    assets_folder: Path,
    default_config: AnalyzerSettings,
    photo_filename: str,
    expect_gps: bool,
    expect_gif: bool,
) -> None:
    """Test the MediaAnalyzer functionality for images with and without GPS data."""
    mock_caption_text = "A mock caption."
    with patch(
        "media_analyzer.machine_learning.caption.blip_captioner.BlipCaptioner.raw_caption"
    ) as mock_raw_caption:
        mock_raw_caption.return_value = mock_caption_text
        analyzer = MediaAnalyzer(default_config)
        result = analyzer.photo(assets_folder / photo_filename)

    assert len(result.frame_data) == 1

    assert result.image_data.exif is not None
    assert result.image_data.data_url is not None
    assert result.image_data.time is not None

    if expect_gps:
        assert result.image_data.gps is not None
        assert result.image_data.weather is not None
    else:
        assert result.image_data.gps is None
        assert result.image_data.weather is None

    if expect_gif:
        assert result.image_data.exif.gif is not None
    else:
        assert result.image_data.exif.gif is None


def test_video_analysis(assets_folder: Path, default_config: AnalyzerSettings) -> None:
    """Test the MediaAnalyzer functionality for a video."""
    mock_caption_text = "A mock caption."
    with patch(
        "media_analyzer.machine_learning.caption.blip_captioner.BlipCaptioner.raw_caption"
    ) as mock_raw_caption:
        mock_raw_caption.return_value = mock_caption_text
        analyzer = MediaAnalyzer(default_config)
        result = analyzer.analyze(
            InputMedia(
                path=assets_folder / "video" / "car.webm",
                frames=[
                    assets_folder / "video" / "frame1.jpg",
                    assets_folder / "video" / "frame2.jpg",
                ],
            )
        )

    frame_count = 2
    assert len(result.frame_data) == frame_count

    assert result.image_data.exif is not None
    assert result.image_data.exif.matroska is not None
    assert result.image_data.data_url is not None
    assert result.image_data.time is not None


def test_png_image(assets_folder: Path, default_config: AnalyzerSettings) -> None:
    """Test the MediaAnalyzer functionality for a png image."""
    mock_caption_text = "A mock caption."
    with patch(
        "media_analyzer.machine_learning.caption.blip_captioner.BlipCaptioner.raw_caption"
    ) as mock_raw_caption:
        mock_raw_caption.return_value = mock_caption_text
        analyzer = MediaAnalyzer(default_config)
        result = analyzer.photo(assets_folder / "png_image.png")

    assert result.image_data.exif is not None
    assert result.image_data.data_url is not None
    assert result.image_data.time is not None
