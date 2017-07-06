class CSVParser:
    def __init__(self):
        self.delimiter       = ','
        self.quote           = '"'
        self.crlf            = '\x0d\x0a'
        self.crlflen         = len(self.crlf)
        self.tok             = ''
        self.row_raw         = ''
        self.field_start     = True
        self.in_quotes       = False
        self.quote_seen      = False
        self.fields          = 0
        self.passedcrlfchars = 0
        self.row_number      = 0

    def reset_field(self):
        self.tok             = ''
        self.field_start     = True
        self.in_quotes       = False
        self.quote_seen      = False

    def reset_row(self):
        self.reset_field()
        self.row_raw         = ''
        self.passedcrlfchars = 0

    def reset(self):
        self.reset_row()
        self.fields          = 0
        self.passedcrlfchars = 0
        self.row_number      = 0

    def parse_quote(self, c):
        if self.field_start:
            # quoted field
            self.in_quotes = True
            self.field_start = False
        elif self.quote_seen:
            # literal quote
            self.tok += c
            self.quote_seen = False
        elif self.in_quotes:
            # field end or literal quote char
            # deal with it next pass
            self.quote_seen = True
        else:
            # oh no
            # not in quotes --- invalid
            raise ValueError(f'Quote character {quote} present in '
                'un-quoted field. Wrap the field in quotes and '
                'double the quote character to parse.')

    def parse_row(self, txt):
        self.reset_field()
        row = []
        for c in txt:
            if c is self.delimiter and self.in_quotes is False:
                # field end
                row.append(self.tok)
                self.reset_field()
            elif c is self.quote:
                self.parse_quote(c)
            else:
                self.field_start = False
                self.tok += c
        row.append(self.tok)
        if len(row) is not self.fields:
            raise ValueError(f'Number of fields in row {self.row_number} '
                'isn\'t the same as number of fields in first row')
        return row

    def parse(self, txt):
        self.crlflen   = len(self.crlf)
        ret            = []
        self.row_number = 0

        for c in txt:
            if c is self.quote:
                self.parse_quote(c)
            elif c is self.delimiter and self.in_quotes is False:
                if self.row_number is 0:
                    self.fields += 1
                self.field_start = True
                self.row_raw += c
            else:
                if (self.in_quotes is False
                        and c is self.crlf[self.passedcrlfchars]):
                    if self.row_number is 0:
                        self.fields += 1
                    self.passedcrlfchars += 1
                    if self.passedcrlfchars is self.crlflen:
                        # row end!
                        ret.append(self.parse_row(self.row_raw))
                        self.row_number += 1
                        self.reset_row()
                else:
                    self.field_start = False
                    self.row_raw += c
        return ret

# cli, decoration

import argparse

csvparser = CSVParser()
csvparser.crlf = '\n'

prog = 'csvparse'
argparser = argparse.ArgumentParser(
    description='Simple CSV Parser',
    prog=prog)

argparser.add_argument('src_file', nargs='*',
    help='The filename of a CSV file or files to parse.')

argparser.add_argument('-', action='store_true', dest='use_stdin',
    help='Read from STDIN instead of a file.')

args = argparser.parse_args()

if args.use_stdin or args.src_file is None:
    # catenate stdinput, parse / render
    src = ''
    for line in sys.stdin:
        src += line + '\n'
    print(csvparser.parse(src))
    exit()

for fname in args.src_file:
    with open(fname, 'r', encoding='utf-8') as f:
        csvparser.reset()
        print(csvparser.parse(f.read()))
