from typing import Optional
from pydantic import BaseModel

from rich.console import Group
from rich.columns import Columns
from rich.panel import Panel

import numpy as np

class Cell (BaseModel):
    cell_value:str
    cell_color:Optional[str]=None
    rgb_array_color:tuple[int,int,int]

    debug_value:Optional[str]=None
    debug_color:Optional[str]=None

    def _render_rgb_array(self):
        return np.array(self.rgb_array_color, dtype=np.uint8),
    
    def _render_human(self, debug:bool):
        render_value = (
            self.debug_value if self.debug_value is not None else self.cell_value
        ) if debug else self.cell_value
        render_color = (
            self.debug_color if self.debug_color is not None else self.cell_color
        ) if debug else self.cell_color

        if render_color is None: return self._render_ansi(debug=debug)
        return f"[{render_color}]{render_value}[/{render_color}]"

    def _render_ansi(self, debug:bool):
        render_value = (
            self.debug_value if self.debug_value is not None else self.cell_value
        ) if debug else self.cell_value
        return render_value

    def render(self, mode="human", debug:bool=False):
        match mode:
            case "rgb_array": return self._render_rgb_array()
            case "human": return self._render_human(debug=debug)
            case "ansi": return self._render_ansi(debug=debug)
            case _: raise NotImplementedError(f"'{mode}' is not a valid mode.")

class Grid (BaseModel):
    size:tuple[int,int]=(5,5)
    panel_style:str="white"
    panel_style_debug:str="red"
    
    @property
    def height(self): return self.size[0]

    @property
    def width(self): return self.size[1]

    @property
    def console_size(self):
        return self.height+2, (self.width*2)+3

    def _render_rgb_array(self, cells:list[list[Cell]]):
        return np.array([
            [cell.render(mode="rgb_array") for cell in row]
            for row in cells
        ], dtype=np.uint8)

    def _render_human(self, cells:list[list[Cell]], debug:bool):
        grid = [[
            cell.render(mode="human", debug=debug) for cell in row
        ] for row in cells]
        panel = Panel.fit(
            Group(*[
                Columns(row, equal=True) for row in grid #type:ignore
            ])
        )
        panel.style=self.panel_style_debug if debug else self.panel_style
        panel.height = self.height + 2
        panel.width = (self.width * 2) + 3
        return panel

    def _render_ansi(self, cells:list[list[Cell]], debug:bool):
        return "\n".join([ #type:ignore
            "".join([cell.render(mode="ansi", debug=debug) for cell in row]) #type:ignore
            for row in cells
        ])

    def _validate_input(self, cells:list[list[Cell]]):
        if len(cells) != self.height: return False
        for row in cells:
            if len(row) != self.width or not all(isinstance(cell, Cell) for cell in row):
                return False
        return True

    def render(self, cells:list[list[Cell]], mode:str="human", debug:bool=False):
        assert self._validate_input(cells), "grid.render:: invalid input."
        match mode:
            case "rgb_array": return self._render_rgb_array(cells)
            case "human": return self._render_human(cells, debug)
            case "ansi": return self._render_ansi(cells, debug)
            case _: raise NotImplementedError(f"'{mode}' is not a valid mode.")
