# MINT - Minimal Text Markup

MINT is a minimal text markup language that can be compiled to html.

For a syntax- and feature-overview, have a look at [Quick Reference](#quick-reference).


# Markup

Version 1

> [!NOTE]  
> See `example.mint` for a working usage example.

Like HTML, MINT uses tags to style documents.
A tag consists of a forward slash `/`, one letter (e.g. `b`) and another forward slash.
Tags toggle a style, so you can start bold text with `/b/` and end it with `/b/`.


## Quick Reference

| Markup      | HTML             | Meaning                |
| :---------: | :--------------: | ---------------------- |
| `/#/.../#/` |                  | Comment (**not compiled into HTML!**) |
| `/p/.../p/` | `<p>...</p>`     | Paragraph              |
| `/q/.../q/` | `<blockquote>...</blockquote>` | Blockquote |
| `/h/.../h/` | `<h1>...</h1>`   | Heading                |
| `/s/.../s/` | `<h2>...</h2>`   | Subheading             |
| `/i/.../i/` | `<i>...</i>`     | _Italic text_          |
| `/b/.../b/` | `<b>...</b>`     | **Bold text**          |
| `/u/.../u/` | `<u>...</u>`     | <u>Underlined text</u> |
| `/d/.../d/` | `<s>...</s>`     | ~~Deleted text~~       |
| `/e/.../e/` | `<pre>...</pre>` | Keep whitespaces (spaces, new lines, ...) |
| `/l/`       | `<br>`           | Line-break (new line)  |
| `//`        | `/`              | Escape a forward slash |


# Converter

To convert MINT to HTML, use the `mint2html.py` command-line tool.


## Supported platforms

I develop and test on **Linux** with **Python 3.13**, so the code should generally run on Unix-based systems.

There is no code implemented that only works on Unix systems, so it _should_ work on Microslop Windows, although I'm too lazy to test this.


## Example

```bash
./mint2html.py -i input_file.mint -o output_file.html
```

You can also omit the input/output files to read from stdin/output to stdout.

Use `mint2html.py --help` to view the full help text.

Tip: If you are in a bash shell, and have pandoc installed, you can pipe the output of mint2html.py directly into pandoc, e.g.:

```bash
./mint2html.py --input-file example.mint --minify | pandoc --from html -o example.epub
```
