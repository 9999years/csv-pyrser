class CSVParser:
    def __init__(self):
        self.field_start = True
        self.in_quotes = False
        self.quote_seen = False

    def parse(self, txt, delimiter=',', quote='"', crlf='\x0d\x0a'):
        tok = ''
        row = []
        ret = []
        for c in txt:
            if c is delimiter and self.in_quotes is False:
                row.append(tok)
                tok = ''
                self.field_start = True
                self.in_quotes = False
                if self.quote_seen:
                    self.quote_seen = False
            elif c is quote:
                if self.field_start:
                    # quoted field
                    self.in_quotes = True
                elif self.quote_seen:
                    # literal quote
                    tok += c
                    self.quote_seen = False
                elif self.in_quotes:
                    # field end or literal quote char
                    # deal with it next pass
                    self.quote_seen = True
                else:
                    # oh no
                    # not in quotes
                    raise ValueError(f'Quote character {quote} present in '
                        'un-quoted field. Wrap the field in quotes and '
                        'double the quote character to parse.')
            else:
                self.field_start = False
                tok += c
