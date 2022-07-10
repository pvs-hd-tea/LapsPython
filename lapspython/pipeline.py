"""Pipe all necessary steps to extract, translate and store programs."""

import logging

from dreamcoder.dreamcoder import ECResult
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.stats import Statistics
from lapspython.translation import Translator
from lapspython.types import CompactResult
from lapspython.utils import json_dump, json_read, load_checkpoint


class Pipeline:
    """Pipelines the entire extraction/translation process of LapsPython."""

    def __init__(self):
        """Construct Pipeline object and setup logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @classmethod
    def extract_translate(
        cls,
        result: ECResult,
        json_path: str = ''
    ) -> CompactResult:
        """Extract and translate programs from a checkpoint.

        :param result: Checkpoint loaded directly from the program.
        :type result: dreamcoder.dreamcoder.ECResult
        :param json_path: Path to dump or read from json
        :type json_path: string
        :returns: Extracted and translated programs
        :rtype: lapspython.types.CompactResult
        """
        parser = GrammarParser(result.grammars[-1])
        json = json_read(json_path)
        if json != {}:
            new_invented = json['grammar'].invented
            parser.fix_invented(new_invented)
        grammar = parser.parsed_grammar
        translator = Translator(grammar)
        extractor = ProgramExtractor(result, translator)
        result = extractor.compact_result
        stats = Statistics(result)
        stats.log()
        stats.plot_histogram(result)
        if json_path != '':
            json_dump(json_path, grammar, extractor.compact_result)
        return result

    @classmethod
    def from_checkpoint(cls, filepath: str) -> CompactResult:
        """Load checkpoint, then extract and translate.

        :param checkpoint: Checkpoint name in checkpoints directory.
        :type checkpoint: str
        :returns: Extracted and translated programs
        :rtype: lapspython.types.CompactResult
        """
        logging.info('Loading checkpoint...')
        result = load_checkpoint(filepath)
        logging.info('Checkpoint loaded.')
        return cls.extract_translate(result, filepath)
