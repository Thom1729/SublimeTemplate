# SublimeTemplate
A simple, powerful file template system for Sublime Text.

## Usage

Press <kbd>ctrl</kbd><kbd>shift</kbd><kbd>M</kbd> (on Mac, <kbd>⌘</kbd><kbd>shift</kbd><kbd>M</kbd>) to open the template selector.

## Creating a template

A template is a file with the `.sublime-template` extension that resembles the following:

```
description: For demonstration purposes.
scope: source.markdown
---
# Hello, World!

This is an example of a sublime-template!
```

Templates have two sections, separated by a line containing only `---`. The first section contains information about the template (in YAML). The second section is the body of the template, containing any text you would like. You can use snippet placeholders in the body.

### Template metadata

#### Name

The name of the template as it will appear in the template selector. If omitted, defaults to the name of the template file (minus the `.sublime-template` extension).

#### Description

The description that will appear in the template selector below the name. If omitted, defaults to the path of the template.

#### Scope

If specified, the new file will use the usual syntax definition for that scope. Cannot be combined with the `syntax` option.

#### Syntax

The resource path of a syntax definition to use for the new file. Cannot be combined with the `scope` option.

#### Settings

A mapping of settings to set on the new view.
