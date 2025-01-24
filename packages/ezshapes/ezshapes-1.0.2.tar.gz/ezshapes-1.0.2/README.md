# Ezshapes

Ezshapes is a Pygame wrapper made to facilitate ease in making shapes and scenes.

---

## Getting Started

---

All of the functions ezshapes has is held under its **renderer** library. Simply import the tools from **ezshapes.renderer**

```python
from ezshapes.renderer import *
```

Making a scene is as simple as choosing the size (measured in pixels). Set up your scene and decide on the name with the `setup()` function.

After setup everything through ezshapes is rendered on screen **per frame**. Each frame is made through placing shapes in one iteration of a loop then drawing to it by using `update_screen()`.

```python
setup(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)

while True:

  """
  Your code here!
  """
  set_background('skyblue')

  update_screen()
```

Any shapes can be placed within the main loop and before the `update_screen()` call, which will be rendered on screen in the order they are processed. This means that two shapes in the same place can **draw over** one another if they overlap.

As ezshapes wraps around pygame, pygame events and such can still be checked inside of the main loop. The only thing currently inaccessible is the display surface.

All shapes accept a color, which can either be a hex digit string in the form of `"#rrggbb"` or an accepted color string from [pygame's color dictionary](https://github.com/pygame/pygame/blob/main/src_py/colordict.py).

---

## Functions

> `setup(width, height, name="Ezshapes Scene")`

Creates the display surface for the scene with the specified width and height, can optionally include a name for the window.

| Argument | Type           | Description                            |
| -------- | -------------- | -------------------------------------- |
| width    | int            | Width of the display screen in pixels  |
| height   | int            | Height of the display screen in pixels |
| name     | str (Optional) | Display name of the window             |

---

> `update_screen()`

Calls `pygame.display.update()` draws to the screen.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| None     | --   | --          |

---

> `set_background(color='grey70')`

Fills the screen with the given color. If given an not given an invalid color or no color, defaults to gray. Highly recommended to call this function before any shapes.

| Argument | Type | Description                    |
| -------- | ---- | ------------------------------ |
| color    | str  | Color to fill the screen with. |

---

> `get_screen_width()`

Return the width of the current display, equal to the width given to the `setup()` function.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| None     | --   | --          |

| Returns | Type | Description                   |
| ------- | ---- | ----------------------------- |
| width   | int  | Width of the screen in pixels |

---

> `get_screen_height()`

Return the height of the current display, equal to the width given to the `setup()` function.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| None     | --   | --          |

| Returns | Type | Description                    |
| ------- | ---- | ------------------------------ |
| height  | int  | Height of the screen in pixels |

> `key_pressed(key)`

Returns True or False on whether the given `key` is being held. Is not case sensitive, eg. "A" and "a" are treated as the same.

| Argument | Type | Description      |
| -------- | ---- | ---------------- |
| key      | str  | The key to check |

| Returns | Type | Description                           |
| ------- | ---- | ------------------------------------- |
| pressed | bool | Whether given key is detected as held |

## Shapes

> `rect(left, top, width, height, color)`

Creates a rectangle on screen, starting from the top-left corner to the right and downwards by the width and height respectively. The rectangle is filled with one solid color, if the color is invalid it will default to gray.

| Argument | Type           | Description                                                          |
| -------- | -------------- | -------------------------------------------------------------------- |
| left     | int            | x-coordinate for the top-left corner of the rectangle                |
| top      | int            | y-coordinate for the top-left corner of the rectangle                |
| width    | int            | Width of the rectangle extending right from the top-left corner      |
| height   | int            | Height of the rectangle extending downwards from the top-left corner |
| color    | str (Optional) | Solid color to fill the rectangle                                    |

---

> `ellipse(centerx, centery, width, height, color)`

Creates an ellipse on screen, stretching to either side of the center with the given width and height. The ellipse is filled with one solid color, if the color is considered invalid it will default to gray.

| Argument | Type           | Description                                              |
| -------- | -------------- | -------------------------------------------------------- |
| centerx  | int            | x-coordinate for the center of the ellipse               |
| centery  | int            | y-coordinate for the center of the ellipse               |
| width    | int            | Width of the ellipse extending outwards from the center  |
| height   | int            | Height of the ellipse extending outwards from the center |
| color    | str (Optional) | Solid color to fill the ellipse                          |

---

> `circle(centerx, centery, radius, color)`

Creates a circle on screen, equivalent to making an ellipse with equal height and width.

| Argument | Type           | Description                               |
| -------- | -------------- | ----------------------------------------- |
| centerx  | int            | x-coordinate for the center of the circle |
| centery  | int            | y-coordinate for the center of the circle |
| radius   | int            | Radius of the circle                      |
| color    | str (Optional) | Solid color to fill the circle            |

---

> `triangle(p1x, p1y, p2x, p2y, p3x, p3y, color)`

Creates a triangle on screen, drawn between 3 given points.

| Argument | Type           | Description                        |
| -------- | -------------- | ---------------------------------- |
| p1x      | int            | x-coordinate for the first vertex  |
| p1y      | int            | y-coordinate for the first vertex  |
| p2x      | int            | x-coordinate for the second vertex |
| p2y      | int            | y-coordinate for the second vertex |
| p3x      | int            | x-coordinate for the third vertex  |
| p3y      | int            | y-coordinate for the third vertex  |
| color    | str (Optional) | Solid color to fill the ellipse    |

---

> `line(p1x, p1y, p2x, p2y, width=1)`

Draws a line on screen between two given points. A width less than 1 will result in nothing being drawn.

| Argument | Type | Description                       |
| -------- | ---- | --------------------------------- |
| p1x      | int  | x-coordinate for the first point  |
| p1y      | int  | y-coordinate for the first point  |
| p2x      | int  | x-coordinate for the second point |
| p2y      | int  | y-coordinate for the second point |
| width    | int  | width of the line                 |
