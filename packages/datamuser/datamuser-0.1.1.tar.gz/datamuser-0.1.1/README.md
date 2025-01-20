# datamuse-cli

A command line interface for the Datamuse API.

## Installation

This tool isn't uploaded to pypi yet because the name `datamuse-cli` is already taken there...

```bash
pip install [TO_BE_DETERMINED]
```

## Usage

See `datamuse --help` for usage information:
```
usage: datamuse [-h] [-n MAX_RESULTS] [-f {csv,line,json}] [-m [METADATA]]
                [-t TOPICS] [-l LEFT_CONTEXT] [-r RIGHT_CONTEXT]
                [-V {es,enwiki}] [-q QUERY_ECHO] [-d] [-v]
                mode word

Unofficial command line interface for the Datamuse API. Datamuse API
documentation: https://www.datamuse.com/api/

positional arguments:
  mode                  Type of word relationship to query:
                          ml - "Means like" (words with similar meanings)
                          sl - "Sounds like" (words with similar
                                pronunciation)
                          sp - "Spelled like" (words with similar
                                spelling)
                          rhy - Rhymes with
                          n2a - "Noun to adjective" (adjectives commonly
                                used to describe the given noun)
                          a2n - "Adjective to noun" (nouns commonly
                                modified by the given adjective)
                          syn - Synonyms
                          ant - Antonyms
                          trg - "Triggers" (words statistically
                                associated with the query word in the same
                                piece of text)
                          spc - More specific terms (hyponyms)
                          gen - More general terms (hypernyms)
                          com - "Comprises" (direct holonyms)
                          par - "Part of" (direct meronyms)
                          fol - Frequent followers
                          pre - Frequent predecessors
                          hom - Homophones (sound-alike words)
                          cns - Consonant match
                          sug - Suggestions (autocomplete)
  word                  Word or phrase to query

options:
  -h, --help            show this help message and exit
  -n, --max-results MAX_RESULTS
                        Maximum number of results to return (default: 10)
  -f, --format {csv,line,json}
                        Output format: comma-separated, line-by-line, or JSON
                        (default: csv)
  -m, --metadata [METADATA]
                        Which metadata to include in results. Options include:
                        - d (definitions)
                        - p (parts of speech)
                        - s (syllable count)
                        - r (pronunciation)
                        - f (word frequency)
                        If omitted, no metadata is included. If specified
                        without a value, all metadata is included: 'dpsrf'.
  -t, --topics TOPICS   Optional topic words. Results will be skewed toward
                        these topics. At most 5 words can be specified. Space
                        or comma delimited. Nouns work best.
  -l, --left-context LEFT_CONTEXT
                        Left context: an optional hint about the word that
                        appears immediately to the left. (Only a single word
                        may be specified.)
  -r, --right-context RIGHT_CONTEXT
                        Right context: an optional hint about the word that
                        appears immediately to the right. (Only a single word
                        may be specified.)
  -V, --vocabulary {es,enwiki}
                        Identifier for alternative vocabulary to use. By
                        default, a 550,000-term English vocabulary is used.
  -q, --query-echo QUERY_ECHO
                        Query echo: see Datamuse documentation for details.
  -d, --debug           Enable debug mode. This will print the API request to
                        the console.
  -v, --version         show program's version number and exit

(Note that compared to the Datamuse API, this tool reverses the meanings of the
"spc" and "gen" parameters.)
```

## Examples

Words that have similar meanings to "happy":
```
$ datamuse ml happy
pleased, blissful, content, glad, contented, joyful, euphoric, joyous, fortunate, riant
```

Words that sound like "spot":
```
$ datamuse sl spot
spot, spott, spout, spit, spite, spat, spate, sput, spight, spet
```

Adjectives that are often used to modify the noun "tree", skewed toward the topic of "Carribean":
```
$ datamuse --topics carribean a2n tree
tropical, mango, small, entire, stately, shady, giant, famous, lemon, palm
```

Hyponyms (more specific terms) of "stone":
```
$ datamuse spc stone
calculus, cornerstone, crystal, conglomerate, capstone, gravel, marble, sill, lava, magma
```

Three antonyms of "day", returned in JSON format, with pronunciation and frequency metadata:
```
$ datamuse -n 3 -f json -m rf ant day
[
  {
    "word": "night",
    "score": 3407,
    "tags": [
      "pron:N AY1 T ",
      "f:145.767264"
    ]
  },
  {
    "word": "dark",
    "score": 2295,
    "tags": [
      "pron:D AA1 R K ",
      "f:68.871627"
    ]
  },
  {
    "word": "nighttime",
    "score": 988,
    "tags": [
      "pron:N AY1 T T AY0 M ",
      "f:1.016966"
    ]
  }
]
```

## Future features

The Datamuse API supports queries involving a spelling filter alongside other
parameters, for instance "words that have a similar meaning to 'point' and have
'o' as the third letter":

[https://api.datamuse.com/words?ml=point&sp=??o*]()

Currently, the `datamuse-cli` tool does not support this feature.


## Datamuse API page

https://www.datamuse.com/api/
