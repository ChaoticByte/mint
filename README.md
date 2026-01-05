# mint - Minimal Text Markup

Mint is a minimal text markup language that can be compiled to html.

As of version 0.1, mint supports

    - comments
    - headings
    - subheadings
    - italic text
    - bold text
    - underline text
    - keep whitespaces (html `<pre>`)
    - manual line breaks (html `br`)


# Syntax

> [!NOTE]  
> See `example.mint` for a working usage example.

Like HTML, Mint uses tags to style documents.
A tag consists of a forward slash `/`, one letter (e.g. `b`) and another forward slash.
Tags toggle a style, so you can start bold text with `/b/` and end it with `/b/`.

## Comments

```
/#/This is a comment/#/
```
> [!WARNING]  
> Comments aren't compiled into html comments, but skipped!


## Headings and Sub-headings

```
/h/Heading/h/

/s/Subheading/s/
```

Headings are compiled into `<h1>`, subheadings into `<h2>`.


## Bold, italic and underlined text

```
Text can be /b/bold/b/, /i/italic/i/ and /u/underlined/u/, or /b//i//u/everything at once/b//i//u/.
```

## Keep whitespaces

Whitespaces (spaces, newlines, etc.) won't get rendered in HTML.  
To preserve whitespaces, use

```
/e/
This text
           will be indented.
/e/
```

## Newlines

You can insert newlines with

```
/l/
```

> [!NOTE]  
> This tag cannot be closed.


## Escape slashes

If you want to write a `/`, use a

```
//
```

