from wizlib.parser import WizParser

from busy.command import QueueCommand
from busy.model.item import Item


class AddCommand(QueueCommand):

    name = 'add'
    selection_optional = True
    pop: bool = False

    @classmethod
    def add_args(cls, parser: WizParser):
        # Special case, no filter argument
        parser.add_argument('--queue', '-q', default='tasks', nargs='?')
        parser.add_argument('--pop', '-p', action='store_true', default=None)
        parser.add_argument('markup', default="", nargs='?')

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('markup'):
            self.markup = self.app.ui.get_text('Item: ')

    @QueueCommand.wrap
    def execute(self):
        if self.markup:
            item = Item(self.markup)
            if self.pop:
                self.collection.insert(0, item)
            else:
                self.collection.append(item)
        self.set_next_item_status()
