"""Pipe all necessary steps to extract, translate and store programs."""

from dreamcoder.dreamcoder import ECResult
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.stats import Statistics
from lapspython.translation import Translator
from lapspython.types import CompactResult
from lapspython.utils import json_dump, json_read, load_checkpoint


class Pipeline:
    """Pipelines the entire extraction/translation process of LapsPython."""

    @classmethod
    def extract_translate(
        cls,
        result: ECResult,
        json_path: str = '',
        mode: str = 'python'
    ) -> CompactResult:
        """Extract and translate programs from a checkpoint.

        :param result: Checkpoint loaded directly from the program.
        :type result: dreamcoder.dreamcoder.ECResult
        :param json_path: Path to dump or read from json
        :type json_path: string
        :returns: Extracted and translated programs
        :rtype: lapspython.types.CompactResult
        """
        mode = mode.lower()
        print(f'Language Mode: {mode.upper()}')
        if mode == 'r':
            print('WARNING: Code verification for R not implemented')
        print('\nParsing grammar...', flush=True)
        parser = GrammarParser(result.grammars[-1], mode)
        json = json_read(json_path)
        if json != {}:
            new_invented = json['grammar'].invented
            parser.fix_invented(new_invented)
        grammar = parser.parsed_grammar

        print('\nTranslating synthesized programs...', flush=True)
        translator = Translator(grammar, mode)
        extractor = ProgramExtractor(result, translator)
        result = extractor.compact_result

        if mode == 'python':
            print('\nCollecting descriptive statistics:')
            stats = Statistics(result)
            print(stats)
            stats.plot_histogram(result)

        print('\nSampling 1 valid translation:')
        sample = result.sample()
        if len(sample) > 0:
            print(sample['annotation'])
            print(sample['best_program'], end='\n\n')
            print(sample['best_valid_translation'])
        else:
            print('No validated translation found')

        print('\nSaving results...', end=' ')
        if json_path != '':
            json_dump(json_path, grammar, extractor.compact_result)
        print('Done')

        return result

    @classmethod
    def from_checkpoint(cls, filepath: str, mode='python') -> CompactResult:
        """Load checkpoint, then extract and translate.

        :param checkpoint: Checkpoint name in checkpoints directory.
        :type checkpoint: str
        :returns: Extracted and translated programs
        :rtype: lapspython.types.CompactResult
        """
        print('Loading checkpoint...', end=' ')
        result = load_checkpoint(filepath)
        print('Done')
        json_path = f'{filepath}_{mode.lower()}'
        return cls.extract_translate(result, json_path, mode)
