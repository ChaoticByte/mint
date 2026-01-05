#!/usr/bin/env python3

# Copyright (c) 2026, Julian Müller (ChaoticByte)
# Licensed under the BSD 3-Clause License

# pylint: disable=line-too-long,missing-module-docstring,missing-class-docstring,missing-function-docstring

from html import escape
from pathlib import Path
from sys import stderr
from sys import stdin


class Logger:

    def __init__(self, disable: bool = True):
        self.disable = disable

    def __call__(self, *a):
        if not self.disable:
            print(*a, file=stderr, flush=True)


TAG_BOUNDARY = "/"


class MintTagToHtml:

    def __init__(self, tag: str, html_tag: str, state_attr_name: str):
        self.tag = tag
        self.html_tag = html_tag
        self.state_attr_name = state_attr_name


class ConverterState:

    output = ""

    pos = 0
    pos_offset = 0

    # wether this cycle actually converted something:
    cycle_had_op = False

    # (in)active styles/formats/blocks
    comment = False
    paragraph = False
    blockquote = False
    heading = False
    subheading = False
    italic = False
    bold = False
    underline = False
    strike_through = False
    whitespace_pre = False

    def complete_cycle(self):
        self.pos += self.pos_offset
        self.pos_offset = 1
        self.cycle_had_op = False

    def add_output(self, more: str):
        self.output += more
        self.cycle_had_op = True


class MintToHtmlConverter:

    '''A simple converter from Mint to HTML
    Currently supports:
    
        - comments                  /#/

        - paragraphs                /p/
        - block quotes              /q/

        - headings                  /h/
        - subheadings               /s/

        - italic                    /i/
        - bold                      /b/
        - underline                 /u/
        - deleted (strike-through)  /d/

        - keep whitespaces          /e/
        - line breaks               /l/
    '''

    def __init__(
        self,
        escape_html: bool = True,
        css: str = ""
    ):
        self.escape_html = escape_html
        self.css = css
        self.tags = [
            MintTagToHtml("#", None, "comment"),
            MintTagToHtml("p", "p", "paragraph"),
            MintTagToHtml("q", "blockquote", "blockquote"),
            MintTagToHtml("h", "h1", "heading"),
            MintTagToHtml("s", "h2", "subheading"),
            MintTagToHtml("i", "i", "italic"),
            MintTagToHtml("b", "b", "bold"),
            MintTagToHtml("u", "u", "underline"),
            MintTagToHtml("d", "s", "strike_through"),
            MintTagToHtml("e", "pre", "whitespace_pre"),
            MintTagToHtml("l", "br", None)
        ]

    def __call__(self, text_in: str, ) -> str:
        '''Convert mint to html'''
        # replace unwanted characters
        text_in = text_in.replace("\r", "")
        # html escape
        if self.escape_html:
            text_in = escape(text_in)
        # parsing & conversion
        state = ConverterState()

        def process_inline_tag(c1: str, state: ConverterState, t: MintTagToHtml):
            '''Process inline tags'''
            if c1 == t.tag:
                state.pos_offset += 2
                if not t.html_tag is None:
                    if t.state_attr_name is None:
                        state.add_output(f"<{t.html_tag}>")
                    else:
                        if getattr(state, t.state_attr_name):
                            state.add_output(f"</{t.html_tag}>")
                        else:
                            state.add_output(f"<{t.html_tag}>")
                # None html tags means that the containing text is skipped
                # This counts still as an operation, so cycle_had_op must be true
                if t.html_tag is None:
                    state.cycle_had_op = True
                if not t.state_attr_name is None:
                    setattr(state, t.state_attr_name, not getattr(state, t.state_attr_name))

        # add css
        if self.css != "":
            state.output += f"<style>{self.css}</style>"
        # process input
        len_text_in = len(text_in)
        while state.pos + 1 < len_text_in:
            c = text_in[state.pos]
            if state.pos + 1 >= len_text_in:
                # end of text
                state.output += c
                break
            c1 = text_in[state.pos + 1]
            if c == TAG_BOUNDARY:
                if c1 == TAG_BOUNDARY:
                    # e.g. // -> /
                    state.pos_offset += 1
                    state.add_output(TAG_BOUNDARY)
                    state.complete_cycle()
                    continue
                if state.pos + 2 < len_text_in:
                    c2 = text_in[state.pos + 2]
                    if c2 == TAG_BOUNDARY:
                        # process tags
                        for t in self.tags:
                            process_inline_tag(c1, state, t)
            if not state.cycle_had_op and not state.comment:
                state.output += c
            # complete this cycle's state
            state.complete_cycle()
        # cleanup
        state.output = state.output.strip()
        # return result
        return state.output


if __name__ == "__main__":
    from argparse import ArgumentParser

    argp = ArgumentParser()
    argp.add_argument("-i", "--input-file", help="Input file (will read from stdin until eof when omitted)", type=Path, required=False)
    argp.add_argument("-o", "--output-file", help="Output file (will print to stdout when omitted)", type=Path, required=False)
    argp.add_argument("--css", help="Add css to the html output", type=str, default="")
    argp.add_argument("--no-escape-html", help="Don't escape html in the input", action="store_true")
    argp.add_argument("--minify-html", help="Minify html output (requires minify-html from pypi)", action="store_true")
    argp.add_argument("--no-log", help="Don't show log messages", action="store_true")

    args = argp.parse_args()

    log = Logger(args.no_log)

    if args.input_file is None:
        log("Reading text from stdin until EOF ...")
        input_lines = []
        for l in stdin:
            input_lines.append(l)
        input_text = "\n".join(input_lines) # pylint: disable=invalid-name
        del input_lines
    else:
        log(f"Reading text from {str(args.input_file)} ...")
        input_text = args.input_file.read_text()

    log("Converting text ...")
    output_document = MintToHtmlConverter(
        escape_html=not args.no_escape_html,
        css=args.css
    )(input_text)

    if args.minify_html:
        log("Minifying html output ...")
        import minify_html
        output_document = minify_html.minify(output_document)

    if args.output_file is None:
        log("Writing output to stdout ...")
        print(output_document, flush=True)
    else:
        log(f"Writing output to {str(args.output_file)} ...")
        args.output_file.write_text(output_document)

    log("Goodbye.")
