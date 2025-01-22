# MkDocs Pills Plugin

This plugin allows you to add pills to your MkDocs pages. It is compatible with MkDocs Material and MkDocs Books.

## Installation

Install the plugin using pip:

```bash
pip install mkdocs-pills
```

Activate the plugin in your `mkdocs.yml`:

```yaml
plugins:
  - pills:
      unicode: true # default: true
      regex: true # default: true
```

## Usage

In you pages, you can add regex pills or unicode pills using the following syntax:

```markdown
Do you know the unicode char U+1F600? Unicode can be matched using the regex: `#!re /U\+([0-9A-F]{4})/`.
```