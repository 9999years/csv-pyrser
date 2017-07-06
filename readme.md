> Loss of innocence has nothing to do with sex. It has to do with writing CSV
> parsers
>
> [— 0d-cody @valarucia1][1]

> How bad could it possibly be?
>
> — Me, right now

# CSV Pyrser

Get it? Like “parser” but with “py” because it’s written in “python”? Haha.

Anyways, it defines a `CSVParser` class, which contains a public function
`CSVParser.parse(txt)`, which takes CSV data as a string and returns a list
of lists (one list per row).

Commas are actually pretty inconvenient as a delimiter, given that they show
up all the time in text, such as twice in this sentence alone. Therefore,
`CSVParser.delimiter` is customizable and could be re-defined to something
sensible, like a tab, or something less sensible, like `U+200C Zero-Width
Non-Joiner`. *That’ll* take your QA people for a spin.

For further information on the CSV specification, refer to [RFC 4180][2] and
then maybe the source code just to make sure.

[1]: https://twitter.com/valarauca1/status/882842156582395905
[2]: https://tools.ietf.org/html/rfc4180
