"""Extends LAPS with translation from lambda calculus to Python."""

from dreamcoder.dreamcoder import ECResult
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.translation import Translator
from lapspython.types import CompactResult
from lapspython.utils import load_checkpoint


class Pipeline:
    """Pipelines the entire extraction/translation process of LapsPython."""

    @classmethod
    def extract_translate(cls, result: ECResult) -> CompactResult:
        """Extract and translate programs from a checkpoint.

        :param result: Checkpoint loaded directly from the program.
        :type result: dreamcoder.dreamcoder.ECResult
        :returns: Extracted and translated programs
        :rtype: lapspython.types.CompactResult
        """
        parser = GrammarParser(result.grammars[-1])
        grammar = parser.parsed_grammar
        translator = Translator(grammar)
        extractor = ProgramExtractor(result, translator)
        return extractor.compact_result

    @classmethod
    def from_checkpoint(cls, checkpoint: str) -> CompactResult:
        """Load checkpoint, then extract and translate.

        :param checkpoint: Checkpoint name in checkpoints directory.
        :type checkpoint: str
        :returns: Extracted and translated programs
        :rtype: lapspython.types.CompactResult
        """
        result = load_checkpoint(checkpoint)
        return cls.extract_translate(result)


# debug results = Pipeline.from_checkpoint('re2_best_dsl_language')
