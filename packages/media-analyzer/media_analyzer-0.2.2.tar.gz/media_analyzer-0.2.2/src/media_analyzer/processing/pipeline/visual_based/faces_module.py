from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.frame_data import FrameData
from media_analyzer.machine_learning.facial_recognition.insight_facial_recognition import (
    InsightFacialRecognition,
)
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule

facial_recognition = InsightFacialRecognition()


class FacesModule(PipelineModule[FrameData]):
    """Get faces from an image."""

    def process(self, data: FrameData, _: FullAnalyzerConfig) -> None:
        """Get faces from an image."""
        data.faces = facial_recognition.get_faces(data.image)
