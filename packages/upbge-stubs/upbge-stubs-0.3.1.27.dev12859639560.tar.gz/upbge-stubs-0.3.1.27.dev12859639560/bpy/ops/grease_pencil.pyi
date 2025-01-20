"""


Grease Pencil Operators
***********************

:func:`active_frame_delete`

:func:`bake_grease_pencil_animation`

:func:`brush_stroke`

:func:`caps_set`

:func:`clean_loose`

:func:`copy`

:func:`cyclical_set`

:func:`delete`

:func:`delete_frame`

:func:`dissolve`

:func:`duplicate`

:func:`duplicate_move`

:func:`erase_box`

:func:`erase_lasso`

:func:`extrude`

:func:`extrude_move`

:func:`fill`

:func:`frame_clean_duplicate`

:func:`frame_duplicate`

:func:`insert_blank_frame`

:func:`interpolate`

:func:`interpolate_sequence`

:func:`join_selection`

:func:`layer_active`

:func:`layer_add`

:func:`layer_duplicate`

:func:`layer_duplicate_object`

:func:`layer_group_add`

:func:`layer_group_color_tag`

:func:`layer_group_remove`

:func:`layer_hide`

:func:`layer_isolate`

:func:`layer_lock_all`

:func:`layer_mask_add`

:func:`layer_mask_remove`

:func:`layer_mask_reorder`

:func:`layer_merge`

:func:`layer_move`

:func:`layer_remove`

:func:`layer_reveal`

:func:`material_copy_to_object`

:func:`material_hide`

:func:`material_isolate`

:func:`material_lock_all`

:func:`material_lock_unselected`

:func:`material_lock_unused`

:func:`material_reveal`

:func:`material_select`

:func:`material_unlock_all`

:func:`move_to_layer`

:func:`paintmode_toggle`

:func:`paste`

:func:`primitive_arc`

:func:`primitive_box`

:func:`primitive_circle`

:func:`primitive_curve`

:func:`primitive_line`

:func:`primitive_polyline`

:func:`reorder`

:func:`reproject`

:func:`reset_uvs`

:func:`sculpt_paint`

:func:`sculptmode_toggle`

:func:`select_all`

:func:`select_alternate`

:func:`select_ends`

:func:`select_less`

:func:`select_linked`

:func:`select_more`

:func:`select_random`

:func:`select_similar`

:func:`separate`

:func:`set_active_material`

:func:`set_curve_resolution`

:func:`set_curve_type`

:func:`set_handle_type`

:func:`set_material`

:func:`set_selection_mode`

:func:`set_start_point`

:func:`set_uniform_opacity`

:func:`set_uniform_thickness`

:func:`snap_cursor_to_selected`

:func:`snap_to_cursor`

:func:`snap_to_grid`

:func:`stroke_material_set`

:func:`stroke_merge_by_distance`

:func:`stroke_reset_vertex_color`

:func:`stroke_simplify`

:func:`stroke_smooth`

:func:`stroke_subdivide`

:func:`stroke_subdivide_smooth`

:func:`stroke_switch_direction`

:func:`stroke_trim`

:func:`texture_gradient`

:func:`trace_image`

:func:`vertex_brush_stroke`

:func:`vertex_color_brightness_contrast`

:func:`vertex_color_hsv`

:func:`vertex_color_invert`

:func:`vertex_color_levels`

:func:`vertex_color_set`

:func:`vertex_group_normalize`

:func:`vertex_group_normalize_all`

:func:`vertex_group_smooth`

:func:`vertexmode_toggle`

:func:`weight_brush_stroke`

:func:`weight_invert`

:func:`weight_sample`

:func:`weight_toggle_direction`

:func:`weightmode_toggle`

"""

import typing

def active_frame_delete(*args, all: bool = False) -> None:

  """

  Delete the active Grease Pencil frame(s)

  """

  ...

def bake_grease_pencil_animation(*args, frame_start: int = 1, frame_end: int = 250, step: int = 1, only_selected: bool = False, frame_target: int = 1, project_type: str = 'KEEP') -> None:

  """

  Bake Grease Pencil object transform to Grease Pencil keyframes

  """

  ...

def brush_stroke(*args, stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL', pen_flip: bool = False) -> None:

  """

  Draw a new stroke in the active Grease Pencil object

  """

  ...

def caps_set(*args, type: str = 'ROUND') -> None:

  """

  Change curve caps mode (rounded or flat)

  """

  ...

def clean_loose(*args, limit: int = 1) -> None:

  """

  Remove loose points

  """

  ...

def copy() -> None:

  """

  Copy the selected Grease Pencil points or strokes to the internal clipboard

  """

  ...

def cyclical_set(*args, type: str = 'TOGGLE', subdivide_cyclic_segment: bool = True) -> None:

  """

  Close or open the selected stroke adding a segment from last to first point

  """

  ...

def delete() -> None:

  """

  Delete selected strokes or points

  """

  ...

def delete_frame(*args, type: str = 'ACTIVE_FRAME') -> None:

  """

  Delete Grease Pencil Frame(s)

  """

  ...

def dissolve(*args, type: str = 'POINTS') -> None:

  """

  Delete selected points without splitting strokes

  """

  ...

def duplicate() -> None:

  """

  Duplicate the selected points

  """

  ...

def duplicate_move(*args, GREASE_PENCIL_OT_duplicate: GREASE_PENCIL_OT_duplicate = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Make copies of the selected Grease Pencil strokes and move them

  """

  ...

def erase_box(*args, xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Erase points in the box region

  """

  ...

def erase_lasso(*args, path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, use_smooth_stroke: bool = False, smooth_stroke_factor: float = 0.75, smooth_stroke_radius: int = 35) -> None:

  """

  Erase points in the lasso region

  """

  ...

def extrude() -> None:

  """

  Extrude the selected points

  """

  ...

def extrude_move(*args, GREASE_PENCIL_OT_extrude: GREASE_PENCIL_OT_extrude = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude selected points and move them

  """

  ...

def fill(*args, invert: bool = False, precision: bool = False) -> None:

  """

  Fill with color the shape formed by strokes

  """

  ...

def frame_clean_duplicate(*args, selected: bool = False) -> None:

  """

  Remove any keyframe that is a duplicate of the previous one

  """

  ...

def frame_duplicate(*args, all: bool = False) -> None:

  """

  Make a copy of the active Grease Pencil frame(s)

  """

  ...

def insert_blank_frame(*args, all_layers: bool = False, duration: int = 0) -> None:

  """

  Insert a blank frame on the current scene frame

  """

  ...

def interpolate(*args, shift: float = 0.0, layers: str = 'ACTIVE', exclude_breakdowns: bool = False, use_selection: bool = False, flip: str = 'AUTO', smooth_steps: int = 1, smooth_factor: float = 0.0) -> None:

  """

  Interpolate Grease Pencil strokes between frames

  """

  ...

def interpolate_sequence(*args, step: int = 1, layers: str = 'ACTIVE', exclude_breakdowns: bool = False, flip: str = 'AUTO', smooth_steps: int = 1, smooth_factor: float = 0.0, type: str = 'LINEAR', easing: str = 'EASE_IN', back: float = 1.702, amplitude: float = 0.15, period: float = 0.15) -> None:

  """

  Generate 'in-betweens' to smoothly interpolate between Grease Pencil frames

  """

  ...

def join_selection(*args, type: str = 'JOIN') -> None:

  """

  New stroke from selected points/strokes

  """

  ...

def layer_active(*args, layer: int = 0) -> None:

  """

  Set the active Grease Pencil layer

  """

  ...

def layer_add(*args, new_layer_name: str = 'Layer') -> None:

  """

  Add a new Grease Pencil layer in the active object

  """

  ...

def layer_duplicate(*args, empty_keyframes: bool = False) -> None:

  """

  Make a copy of the active Grease Pencil layer

  """

  ...

def layer_duplicate_object(*args, only_active: bool = True, mode: str = 'ALL') -> None:

  """

  Make a copy of the active Grease Pencil layer to selected object

  """

  ...

def layer_group_add(*args, new_layer_group_name: str = '') -> None:

  """

  Add a new Grease Pencil layer group in the active object

  """

  ...

def layer_group_color_tag(*args, color_tag: str = 'COLOR1') -> None:

  """

  Change layer group icon

  """

  ...

def layer_group_remove(*args, keep_children: bool = False) -> None:

  """

  Remove Grease Pencil layer group in the active object

  """

  ...

def layer_hide(*args, unselected: bool = False) -> None:

  """

  Hide selected/unselected Grease Pencil layers

  """

  ...

def layer_isolate(*args, affect_visibility: bool = False) -> None:

  """

  Make only active layer visible/editable

  """

  ...

def layer_lock_all(*args, lock: bool = True) -> None:

  """

  Lock all Grease Pencil layers to prevent them from being accidentally modified

  """

  ...

def layer_mask_add(*args, name: str = '') -> None:

  """

  Add new layer as masking

  """

  ...

def layer_mask_remove() -> None:

  """

  Remove Layer Mask

  """

  ...

def layer_mask_reorder(*args, direction: str = 'UP') -> None:

  """

  Reorder the active Grease Pencil mask layer up/down in the list

  """

  ...

def layer_merge(*args, mode: str = 'ACTIVE') -> None:

  """

  Combine layers based on the mode into one layer

  """

  ...

def layer_move(*args, direction: str = 'UP') -> None:

  """

  Move the active Grease Pencil layer or Group

  """

  ...

def layer_remove() -> None:

  """

  Remove the active Grease Pencil layer

  """

  ...

def layer_reveal() -> None:

  """

  Show all Grease Pencil layers

  """

  ...

def material_copy_to_object(*args, only_active: bool = True) -> None:

  """

  Append Materials of the active Grease Pencil to other object

  """

  ...

def material_hide(*args, invert: bool = False) -> None:

  """

  Hide active/inactive Grease Pencil material(s)

  """

  ...

def material_isolate(*args, affect_visibility: bool = False) -> None:

  """

  Toggle whether the active material is the only one that is editable and/or visible

  """

  ...

def material_lock_all() -> None:

  """

  Lock all Grease Pencil materials to prevent them from being accidentally modified

  """

  ...

def material_lock_unselected() -> None:

  """

  Lock any material not used in any selected stroke

  """

  ...

def material_lock_unused() -> None:

  """

  Lock and hide any material not used

  """

  ...

def material_reveal() -> None:

  """

  Unhide all hidden Grease Pencil materials

  """

  ...

def material_select(*args, deselect: bool = False) -> None:

  """

  Select/Deselect all Grease Pencil strokes using current material

  """

  ...

def material_unlock_all() -> None:

  """

  Unlock all Grease Pencil materials so that they can be edited

  """

  ...

def move_to_layer(*args, target_layer_name: str = '', add_new_layer: bool = False) -> None:

  """

  Move selected strokes to another layer

  """

  ...

def paintmode_toggle(*args, back: bool = False) -> None:

  """

  Enter/Exit paint mode for Grease Pencil strokes

  """

  ...

def paste(*args, paste_back: bool = False, keep_world_transform: bool = False) -> None:

  """

  Paste Grease Pencil points or strokes from the internal clipboard to the active layer

  """

  ...

def primitive_arc(*args, subdivision: int = 62, type: str = 'ARC') -> None:

  """

  Create predefined Grease Pencil stroke arcs

  """

  ...

def primitive_box(*args, subdivision: int = 3, type: str = 'BOX') -> None:

  """

  Create predefined Grease Pencil stroke boxes

  """

  ...

def primitive_circle(*args, subdivision: int = 94, type: str = 'CIRCLE') -> None:

  """

  Create predefined Grease Pencil stroke circles

  """

  ...

def primitive_curve(*args, subdivision: int = 62, type: str = 'CURVE') -> None:

  """

  Create predefined Grease Pencil stroke curve shapes

  """

  ...

def primitive_line(*args, subdivision: int = 6, type: str = 'LINE') -> None:

  """

  Create predefined Grease Pencil stroke lines

  """

  ...

def primitive_polyline(*args, subdivision: int = 6, type: str = 'POLYLINE') -> None:

  """

  Create predefined Grease Pencil stroke polylines

  """

  ...

def reorder(*args, direction: str = 'TOP') -> None:

  """

  Change the display order of the selected strokes

  """

  ...

def reproject(*args, type: str = 'VIEW', keep_original: bool = False, offset: float = 0.0) -> None:

  """

  Reproject the selected strokes from the current viewpoint as if they had been newly drawn (e.g. to fix problems from accidental 3D cursor movement or accidental viewport changes, or for matching deforming geometry)

  """

  ...

def reset_uvs() -> None:

  """

  Reset UV transformation to default values

  """

  ...

def sculpt_paint(*args, stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL', pen_flip: bool = False) -> None:

  """

  Sculpt strokes in the active Grease Pencil object

  """

  ...

def sculptmode_toggle(*args, back: bool = False) -> None:

  """

  Enter/Exit sculpt mode for Grease Pencil strokes

  """

  ...

def select_all(*args, action: str = 'TOGGLE') -> None:

  """

  (De)select all visible strokes

  """

  ...

def select_alternate(*args, deselect_ends: bool = False) -> None:

  """

  Select alternated points in strokes with already selected points

  """

  ...

def select_ends(*args, amount_start: int = 0, amount_end: int = 1) -> None:

  """

  Select end points of strokes

  """

  ...

def select_less() -> None:

  """

  Shrink the selection by one point

  """

  ...

def select_linked() -> None:

  """

  Select all points in curves with any point selection

  """

  ...

def select_more() -> None:

  """

  Grow the selection by one point

  """

  ...

def select_random(*args, ratio: float = 0.5, seed: int = 0, action: str = 'SELECT') -> None:

  """

  Selects random points from the current strokes selection

  """

  ...

def select_similar(*args, mode: str = 'LAYER', threshold: float = 0.1) -> None:

  """

  Select all strokes with similar characteristics

  """

  ...

def separate(*args, mode: str = 'SELECTED') -> None:

  """

  Separate the selected geometry into a new Grease Pencil object

  """

  ...

def set_active_material() -> None:

  """

  Set the selected stroke material as the active material

  """

  ...

def set_curve_resolution(*args, resolution: int = 12) -> None:

  """

  Set resolution of selected curves

  """

  ...

def set_curve_type(*args, type: str = 'POLY', use_handles: bool = False) -> None:

  """

  Set type of selected curves

  """

  ...

def set_handle_type(*args, type: str = 'AUTO') -> None:

  """

  Set the handle type for bezier curves

  """

  ...

def set_material(*args, slot: str = 'DEFAULT') -> None:

  """

  Set active material

  """

  ...

def set_selection_mode(*args, mode: str = 'POINT') -> None:

  """

  Change the selection mode for Grease Pencil strokes

  """

  ...

def set_start_point() -> None:

  """

  Select which point is the beginning of the curve

  """

  ...

def set_uniform_opacity(*args, opacity: float = 1.0) -> None:

  """

  Set all stroke points to same opacity

  """

  ...

def set_uniform_thickness(*args, thickness: float = 0.1) -> None:

  """

  Set all stroke points to same thickness

  """

  ...

def snap_cursor_to_selected() -> None:

  """

  Snap cursor to center of selected points

  """

  ...

def snap_to_cursor(*args, use_offset: bool = True) -> None:

  """

  Snap selected points/strokes to the cursor

  """

  ...

def snap_to_grid() -> None:

  """

  Snap selected points to the nearest grid points

  """

  ...

def stroke_material_set(*args, material: str = '') -> None:

  """

  Assign the active material slot to the selected strokes

  """

  ...

def stroke_merge_by_distance(*args, threshold: float = 0.001, use_unselected: bool = False) -> None:

  """

  Merge points by distance

  """

  ...

def stroke_reset_vertex_color(*args, mode: str = 'BOTH') -> None:

  """

  Reset vertex color for all or selected strokes

  """

  ...

def stroke_simplify(*args, factor: float = 0.01, length: float = 0.05, distance: float = 0.01, steps: int = 1, mode: str = 'FIXED') -> None:

  """

  Simplify selected strokes

  """

  ...

def stroke_smooth(*args, iterations: int = 10, factor: float = 1.0, smooth_ends: bool = False, keep_shape: bool = False, smooth_position: bool = True, smooth_radius: bool = True, smooth_opacity: bool = False) -> None:

  """

  Smooth selected strokes

  """

  ...

def stroke_subdivide(*args, number_cuts: int = 1, only_selected: bool = True) -> None:

  """

  Subdivide between continuous selected points of the stroke adding a point half way between them

  """

  ...

def stroke_subdivide_smooth(*args, GREASE_PENCIL_OT_stroke_subdivide: GREASE_PENCIL_OT_stroke_subdivide = None, GREASE_PENCIL_OT_stroke_smooth: GREASE_PENCIL_OT_stroke_smooth = None) -> None:

  """

  Subdivide strokes and smooth them

  """

  ...

def stroke_switch_direction() -> None:

  """

  Change direction of the points of the selected strokes

  """

  ...

def stroke_trim(*args, path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, use_smooth_stroke: bool = False, smooth_stroke_factor: float = 0.75, smooth_stroke_radius: int = 35) -> None:

  """

  Delete stroke points in between intersecting strokes

  """

  ...

def texture_gradient(*args, xstart: int = 0, xend: int = 0, ystart: int = 0, yend: int = 0, flip: bool = False, cursor: int = 5) -> None:

  """

  Draw a line to set the fill material gradient for the selected strokes

  """

  ...

def trace_image(*args, target: str = 'NEW', radius: float = 0.01, threshold: float = 0.5, turnpolicy: str = 'MINORITY', mode: str = 'SINGLE', use_current_frame: bool = True, frame_number: int = 0) -> None:

  """

  Extract Grease Pencil strokes from image

  """

  ...

def vertex_brush_stroke(*args, stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL', pen_flip: bool = False) -> None:

  """

  Draw on vertex colors in the active Grease Pencil object

  """

  ...

def vertex_color_brightness_contrast(*args, mode: str = 'BOTH', brightness: float = 0.0, contrast: float = 0.0) -> None:

  """

  Adjust vertex color brightness/contrast

  """

  ...

def vertex_color_hsv(*args, mode: str = 'BOTH', h: float = 0.5, s: float = 1.0, v: float = 1.0) -> None:

  """

  Adjust vertex color HSV values

  """

  ...

def vertex_color_invert(*args, mode: str = 'BOTH') -> None:

  """

  Invert RGB values

  """

  ...

def vertex_color_levels(*args, mode: str = 'BOTH', offset: float = 0.0, gain: float = 1.0) -> None:

  """

  Adjust levels of vertex colors

  """

  ...

def vertex_color_set(*args, mode: str = 'BOTH', factor: float = 1.0) -> None:

  """

  Set active color to all selected vertex

  """

  ...

def vertex_group_normalize() -> None:

  """

  Normalize weights of the active vertex group

  """

  ...

def vertex_group_normalize_all(*args, lock_active: bool = True) -> None:

  """

  Normalize the weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

  """

  ...

def vertex_group_smooth(*args, factor: float = 0.5, repeat: int = 1) -> None:

  """

  Smooth the weights of the active vertex group

  """

  ...

def vertexmode_toggle(*args, back: bool = False) -> None:

  """

  Enter/Exit vertex paint mode for Grease Pencil strokes

  """

  ...

def weight_brush_stroke(*args, stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL', pen_flip: bool = False) -> None:

  """

  Draw weight on stroke points in the active Grease Pencil object

  """

  ...

def weight_invert() -> None:

  """

  Invert the weight of active vertex group

  """

  ...

def weight_sample() -> None:

  """

  Set the weight of the Draw tool to the weight of the vertex under the mouse cursor

  """

  ...

def weight_toggle_direction() -> None:

  """

  Toggle Add/Subtract for the weight paint draw tool

  """

  ...

def weightmode_toggle(*args, back: bool = False) -> None:

  """

  Enter/Exit weight paint mode for Grease Pencil strokes

  """

  ...
