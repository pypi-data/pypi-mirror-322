"""


gpu_extras submodule (gpu_extras.presets)
*****************************************

:func:`draw_circle_2d`

:func:`draw_texture_2d`

"""

import typing

import mathutils

import gpu

def draw_circle_2d(position: typing.Any, color: typing.Any, radius: float, *args, segments: int = None) -> None:

  """

  Draw a circle.

  """

  ...

def draw_texture_2d(texture: gpu.types.GPUTexture, position: mathutils.Vector, width: float, height: float) -> None:

  """

  Draw a 2d texture.

  """

  ...
