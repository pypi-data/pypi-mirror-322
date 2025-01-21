from typing import ClassVar

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.enums.analyzer_module import AnalyzerModule, FileModule
from media_analyzer.data.interfaces.image_data import ImageData, TagData
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule


class TagsModule(PipelineModule[ImageData]):
    """Extract weather data from the time and place an image was taken."""

    depends: ClassVar[set[AnalyzerModule]] = {FileModule.EXIF}

    def process(self, data: ImageData, _: FullAnalyzerConfig) -> None:
        """Get tags such as is_panorama, is_night_sight, is_motion_photo, etc."""
        assert data.exif is not None
        wide_ratio = 2
        is_panorama = data.exif.width / data.exif.height > wide_ratio

        # TODO the rest

        data.tags = TagData(
            is_hdr=False,
            is_360=False,
            is_burst=False,
            is_panorama=is_panorama,
            is_timelapse=False,
            is_slowmotion=False,
            is_night_sight=False,
            is_motion_photo=False,
        )
