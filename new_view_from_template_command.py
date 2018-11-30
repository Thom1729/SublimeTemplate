import sublime
import sublime_plugin

from sublime_lib.view_utils import new_view, close_view
from sublime_lib import show_selection_panel, ResourcePath, NamedSettingsDict

from collections import namedtuple

import yaml


TemplateDefinition = namedtuple(
    'TemplateDefinition',
    ['path', 'metadata', 'body']
)


def plugin_loaded():
    global SETTINGS
    SETTINGS = NamedSettingsDict("SublimeTemplate")


import re
EXPR = re.compile(r'^---$', re.MULTILINE)
def parse_yaml_body(text):
    i = EXPR.search(text).start()
    yaml_part = text[:i]
    body_part = text[i+4:]

    if len(body_part) and body_part[-1] == '\n':
        body_part = body_part[:-1]

    return (yaml.load(yaml_part) or {}, body_part)


def get_templates():
    return [
        TemplateDefinition(path, *parse_yaml_body(path.read_text()))
        for path in ResourcePath.glob_resources('*.sublime-template')
    ]


class NewViewFromTemplateCommand(sublime_plugin.WindowCommand):
    preview = None

    def run(self, context={}):
        self.context = context
        show_selection_panel(
            self.window,
            get_templates(),

            labels=lambda template: (
                template.metadata.get('name', template.path.stem),
                template.metadata.get('description', template.path),
            ),

            on_select=self.on_select,
            on_cancel=self.on_cancel,
            on_highlight=self.on_highlight if SETTINGS['preview_on_highlight'] else None,
        )

    def on_highlight(self, template):
        if self.preview:
            close_view(self.preview, force=True)

        self.preview = self.create_view_from_template(template)

    def on_cancel(self):
        if self.preview:
            close_view(self.preview, force=True)

        self.preview = None

    def on_select(self, template):
        if not self.preview:
            self.create_view_from_template(template)

        self.preview = None

    def create_view_from_template(self, template):
        kwargs = { k: v for k, v in template.metadata.items() if k in {'settings', 'syntax', 'scope'} }

        view = new_view(self.window, **kwargs)

        args = {'contents': template.body}
        args.update(self.context)
        view.run_command('insert_snippet', args)

        return view
