# rich_grid 

## Installation
To install **rich_grid**, run the following command:
```bash
pip install rich_grid
```

## Quick Start
```python
from rich import print

grid = Grid(size=(21,21))

PLAYER = Cell(cell_value="@", cell_color="cornflower_blue", rgb_array_color=(100, 149, 237))
EMPTY = Cell(cell_value=" ", debug_value="#", debug_color="black", rgb_array_color=(0, 0, 0))

cells = [[
    EMPTY for _ in range(grid.width)
] for _ in range(grid.height)] 

cells[grid.height//2][grid.width//2]=PLAYER
scene = grid.render(cells, debug=True, mode="human")

print(scene)
```

