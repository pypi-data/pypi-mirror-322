from textual_englyph import EnGlyph
from textual.app import App, ComposeResult
from textual.widgets import Button, Label
from textual.containers import Vertical

class Test(App):
    fsize = 11
    def compose(self) -> ComposeResult:
        with Vertical():
            self.enhello = EnGlyph("Hello Textual!", basis=(2,3), id="enhello")
            yield Label( "A Button", id="enlabel" )
            yield EnGlyph("+")
            yield self.enhello
            yield EnGlyph("=")
            yield Button( str(self.enhello), variant="primary" )

    def on_button_pressed(self):
        self.fsize += 1
        self.query_one("#enhello").update( font_size=self.fsize )
        self.query_one("#enlabel").update( str(self.fsize)+"gx" )

if __name__ == "__main__":
    Test().run()
