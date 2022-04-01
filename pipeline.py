from utils import *

class LanguageDetection(BaseComponent):
  """
  | Custom pipeline for building language detection decision process
  """
  outgoing_edges = 3
  def run(self, documents: List[Document]) -> Tuple[Dict[Text, List[Document]], Text]:
    language = documents[0].meta['language']
    if language == "eng":
      return {"documents": documents}, "output_1"
    elif language == "deu" or language == "nld":
      return {"documents": documents}, "output_2"
    elif language == "fra":
      return {"documents": documents}, "output_3"


class MovieSentimentReviewsPipeline(Pipeline):
  """
  | Wrapper class which wrapping Pipeline class for integrating all the pipeline in one class
  """
  @staticmethod
  def dutch_translator():
    """
    | This static method that call the `TransformersTranslator` to translate to dutch
    """
    return TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-de-en")
  
  @staticmethod
  def french_translator():
    """
    | This static method that call the `TransformersTranslator` to translate to french
    """
    return TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-fr-en")
  
  @staticmethod
  def sentiment_analysis():
    """
    | This static method that call the `TransformersDocumentClassifier` for having zero-shot-classification in batch-mode.
    """
    return TransformersDocumentClassifier(model_name_or_path="valhalla/distilbart-mnli-12-3",
                                          task ="zero-shot-classification",
                                          labels=['good', 'neutral', 'bad']) 
  def __init__(self) -> None:
    super(MovieSentimentReviewsPipeline, self).__init__()

    self.add_node(component=LanguageDetection(),
                  name='LanguageDetection',
                  inputs=['Query'])
    self.add_node(component=MovieSentimentReviewsPipeline.dutch_translator(),
                  name='DutchTransformerTranslator',
                  inputs=['LanguageDetection.output_2'])
    self.add_node(component=MovieSentimentReviewsPipeline.french_translator(),
                  name='FrenchTransformerTranslator',
                  inputs=['LanguageDetection.output_3'])
    self.add_node(component=MovieSentimentReviewsPipeline.sentiment_analysis(),
                  name="SentimentAnalysis",
                  inputs=['LanguageDetection.output_1',
                          'DutchTransformerTranslator',
                          'FrenchTransformerTranslator'])