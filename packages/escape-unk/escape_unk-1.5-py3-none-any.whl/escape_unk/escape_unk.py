from argparse import ArgumentParser
from sentencepiece.sentencepiece_model_pb2 import ModelProto
import sentencepiece as sp
import logging
import re
import sys

try:
    from .utils import setup_logging
except ImportError:
    from utils import setup_logging

RE_ESCAPE = re.compile(r"([¹²³\u2070-\u209F])")

def main():
    parser = ArgumentParser()
    parser.add_argument('-m','--spm_model', required=True)
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    args = parser.parse_args()
    setup_logging(args)

    spm = sp.SentencePieceProcessor(args.spm_model)

    # Check if model has byte_fallback
    mp = ModelProto()
    mp.ParseFromString(spm.serialized_model_proto())
    if mp.trainer_spec.HasField('byte_fallback') and mp.trainer_spec.byte_fallback:
        args.byte_fallback = True
    else:
        args.byte_fallback = False
    del mp

    def encode(text, output_type=str):
        ''' SentencePiece encoding without control tokens '''
        return spm.encode(text, add_bos=False, add_eos=False,
                          out_type=output_type)

    def escape(text):
        ''' Convert unicode string to hex values '''
        #TODO choose escape delimiters based on spm vocab to avoid OOV
        logging.debug(f"Escaping '{text}'")
        return '[[' + text.encode('utf-8').hex() +']]'

    def escape_regex(text):
        ''' Apply escaping to characters matching by the regex '''
        toks = []
        for s in RE_ESCAPE.split(text):
            if RE_ESCAPE.match(s):
                toks.append(escape(s))
            else:
                toks.append(s)

        return ''.join(toks)

    def process(segment):
        # Apply escaping to superscripts and other characters before they are normalized by SP
        segment = escape_regex(segment)

        escaped = []
        # Encode to ids and pieces and escape pieces that are unknown
        ids = encode(segment, int)
        pieces = encode(segment)
        for id_, piece in zip(ids, pieces):
            if spm.is_unknown(id_):
                # Escape
                escaped.append(escape(piece))
            else:
                escaped.append(piece)

        # Detokenize manually to void spm introducing spaces in escaped text
        # lstrip to remove initial space that is removed by spm.decode
        return ''.join(escaped).replace('▁', ' ').lstrip()

    last_num_parts = 0
    for i, line in enumerate(sys.stdin):
        if args.byte_fallback: # If byte-fallback, just cat
            print(line, end='')
            continue

        parts = line.strip().split('\t')

        # If input is a tsv, escape each field individually
        for j, segment in enumerate(parts):
            print(process(segment), end='')
            if j < len(parts) - 1:
                print('\t', end='')
        print()

        if last_num_parts != len(parts) and last_num_parts != 0:
            raise ValueError(f"Line {i+1}: different number of tabs. prev: {last_num_parts} curr: {len(parts)}")
        last_num_parts = len(parts)



if __name__ == "__main__":
    main()
