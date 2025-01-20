#!/usr/bin/env python3

import argparse
import json
import sys
import requests
from typing import List, Dict, Any
from importlib.metadata import version

VERSION = version("datamuser")
API_BASE = "https://api.datamuse.com/words"
API_SUGGEST_BASE = "https://api.datamuse.com/sug"
DEFAULT_MAX_RESULTS = 10

# This class is borrowed from
# https://stackoverflow.com/a/76962505/1516307
# and modified to apply special wrapping to the "mode" argument help text
class SmartHelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        WRAP_INDENT = 6  # Additional spaces for wrapped lines
        r = []
        for line in text.splitlines():
            n = self.lws(line)
            
            # Only apply special wrapping for the mode argument help text
            if text.startswith("Type of word relationship to query:"):
                # Get the split lines with adjusted width for indentation
                split_lines = list(super()._split_lines(line, width - n - WRAP_INDENT))
                if len(split_lines) > 1:
                    # First line gets normal indentation
                    r.append(' ' * n + split_lines[0])
                    # Subsequent lines get additional WRAP_INDENT spaces
                    r.extend(' ' * (n + WRAP_INDENT) + s for s in split_lines[1:])
                else:
                    # If no wrapping occurred, handle normally
                    r.extend(' ' * n + s for s in split_lines)
            else:
                # Default behavior for all other arguments
                r.extend(' ' * n + s for s in super()._split_lines(line, width - n))
        return r

    def _fill_text(self, text, width, indent):
        r = []
        for line in text.splitlines():
            n = self.lws(line)
            r.append(super()._fill_text(line, width, indent + ' ' * n))
        return '\n'.join(r)

    @staticmethod
    def lws(line):
        prefix = line[:len(line) - len(line.lstrip())]
        return len(prefix) + 3 * prefix.count('\t')


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unofficial command line interface for the Datamuse API. Datamuse API documentation: https://www.datamuse.com/api/",
        epilog="""(Note that compared to the Datamuse API, this tool reverses the meanings of the "spc" and "gen" parameters.)""",
        formatter_class=SmartHelpFormatter,
        )
    
    parser.add_argument('mode', metavar='mode', choices=[
        'ml',
        'sl',
        'sp',
        'rhy',
        'n2a',
        'a2n',
        'syn',
        'ant',
        'trg',
        'spc',
        'gen',
        'com',
        'par',
        'fol',
        'pre',
        'hom',
        'cns',
        'sug'
    ], help="""Type of word relationship to query:
  ml   - "Means like" (words with similar meanings)
  sl   - "Sounds like" (words with similar pronunciation)
  sp   - "Spelled like" (words with similar spelling)
  rhy  - Rhymes with
  n2a  - "Noun to adjective" (adjectives commonly used to describe the given noun)
  a2n  - "Adjective to noun" (nouns commonly modified by the given adjective)
  syn  - Synonyms
  ant  - Antonyms
  trg  - "Triggers" (words statistically associated with the query word in the same piece of text)
  spc  - More specific terms (hyponyms)
  gen  - More general terms (hypernyms)
  com  - "Comprises" (direct holonyms)
  par  - "Part of" (direct meronyms)
  fol  - Frequent followers
  pre  - Frequent predecessors
  hom  - Homophones (sound-alike words)
  cns  - Consonant match
  sug  - Suggestions (autocomplete)""")
    
    parser.add_argument('word', help="Word or phrase to query")
    
    parser.add_argument(
        '-n', '--max-results',
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Maximum number of results to return (default: {DEFAULT_MAX_RESULTS})"
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['csv', 'line', 'json'],
        default='csv',
        help="Output format: comma-separated, line-by-line, or JSON (default: csv)"
    )
    
    parser.add_argument(
        '-m', '--metadata',
        nargs='?',
        const='dpsrf',
        default='',
        help="Which metadata to include in results. Options include:\n" +
             "- d (definitions)\n- p (parts of speech)\n- s (syllable count)\n- r (pronunciation)\n- f (word frequency)\n" +
             "If omitted, no metadata is included. If specified without a value, all metadata is included: 'dpsrf'."
    )
    
    parser.add_argument(
        '-t', '--topics',
        type=str,
        nargs=1,
        help="Optional topic words. Results will be skewed toward these topics. At most 5 words can be specified, comma delimited. Nouns work best."
    )
    
    parser.add_argument(
        '-l', '--left-context',
        help="Left context: an optional hint about the word that appears immediately to the left. (Only a single word may be specified.)"
    )
    
    parser.add_argument(
        '-r', '--right-context',
        help="Right context: an optional hint about the word that appears immediately to the right. (Only a single word may be specified.)"
    )
    
    parser.add_argument(
        '-V', '--vocabulary',
        choices=['es', 'enwiki'],
        help="Identifier for alternative vocabulary to use. By default, a 550,000-term English vocabulary is used."
    )
    
    parser.add_argument(
        '-q', '--query-echo',
        help="Query echo: see Datamuse documentation for details."
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help="Enable debug mode. This will print the API request to the console."
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )
    
    return parser

def query_datamuse(command: str, word: str, max_results: int, include_metadata: bool, topics: List[str], left_context: str, right_context: str, vocabulary: str, query_echo: str, debug: bool) -> List[Dict[str, Any]]:
    # Map command aliases to API parameters
    param_map = {
        'ml': 'ml',            # means like
        'sl': 'sl',            # sounds like
        'sp': 'sp',            # spelled like
        'rhy': 'rel_rhy',      # rhymes with
        'n2a': 'rel_jja',      # noun to adjective
        'a2n': 'rel_jjb',      # adjective to noun
        'syn': 'rel_syn',      # synonyms
        'trg': 'rel_trg',      # triggers
        'ant': 'rel_ant',      # antonyms
        'spc': 'rel_gen',      # > These two are reversed
        'gen': 'rel_spc',      # > because the names are confusing
        'com': 'rel_com',      # comprises
        'par': 'rel_par',      # part of
        'fol': 'rel_bga',      # frequent followers
        'pre': 'rel_bgb',      # frequent predecessors
        'hom': 'rel_hom',      # homophones
        'cns': 'rel_cns',      # consonant match
    }

    # We get better results if we ask for more results than we need.
    # We'll filter out the ones we don't need after the request.
    temp_max_results = max(max_results * 2, 30)

    # Handle suggestion endpoint separately
    if command == 'sug':
        endpoint = API_SUGGEST_BASE
        params = {
            's': word,
            'max': temp_max_results
        }
        if vocabulary:
            params['v'] = vocabulary
    else:
        endpoint = API_BASE
        params = {
            param_map[command]: word,
            'max': temp_max_results
        }
        
        if include_metadata:
            valid_metadata = ''.join(filter(lambda x: x in 'dpsrf', include_metadata))
            params['md'] = valid_metadata
        
        if topics:
            params['topics'] = ','.join(topics)
        if left_context:
            params['lc'] = left_context
        if right_context:
            params['rc'] = right_context
        if vocabulary:
            params['v'] = vocabulary
        if query_echo:
            params['qe'] = query_echo
    
    if debug:
        print(requests.get(endpoint, params=params).url)

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    # Only keep the top max_results results, sorted by score.
    # Not all results may have a score. We first return results with a score
    # (sorted by score), and then return any remaining results without a score,
    # in the order they were returned by the API.
    results_with_score = [result for result in response.json() if 'score' in result]
    results_without_score = [result for result in response.json() if 'score' not in result]
    sorted_results_with_score = sorted(results_with_score, key=lambda x: x['score'], reverse=True)[:max_results]
    results = sorted_results_with_score + results_without_score[:max_results - len(sorted_results_with_score)]

    return results

def format_output(results: List[Dict[str, Any]], format_type: str, include_metadata: bool) -> str:
    if format_type == 'json':
        return json.dumps(results, indent=2)
    
    # Extract just the words for non-JSON formats
    words = [result['word'] for result in results]

    if format_type == 'line':
        return '\n'.join(words)
    
    # Default to CSV format
    return ', '.join(words)

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        results = query_datamuse(
            args.mode,
            args.word,
            args.max_results,
            args.metadata,
            args.topics,
            args.left_context,
            args.right_context,
            args.vocabulary,
            args.query_echo,
            args.debug
        )
        
        output = format_output(results, args.format, args.metadata)
        print(output)
        
    except requests.RequestException as e:
        print(f"Error querying Datamuse API: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
