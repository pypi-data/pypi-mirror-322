from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.frame_data import FrameData
from media_analyzer.machine_learning.object_detection.resnet_object_detection import (
    ResnetObjectDetection,
)
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule

detector = ResnetObjectDetection()


class ObjectsModule(PipelineModule[FrameData]):
    """Detect objects in an image."""

    def process(self, data: FrameData, _: FullAnalyzerConfig) -> None:
        """Detect objects in an image."""
        data.objects = detector.detect_objects(data.image)
