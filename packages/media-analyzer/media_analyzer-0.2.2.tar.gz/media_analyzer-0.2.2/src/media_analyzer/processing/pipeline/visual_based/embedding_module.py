from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.interfaces.frame_data import FrameData
from media_analyzer.machine_learning.embedding.clip_embedder import CLIPEmbedder
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule

embedder = CLIPEmbedder()


class EmbeddingModule(PipelineModule[FrameData]):
    """Embed an image using CLIP."""

    def process(self, data: FrameData, _: FullAnalyzerConfig) -> None:
        """Embed an image using CLIP."""
        embedding = embedder.embed_image(data.image).tolist()
        assert isinstance(embedding, list)
        data.embedding = embedding  # type: ignore[assignment]
