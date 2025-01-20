"""


Property Flag Items
^^^^^^^^^^^^^^^^^^^

:HIDDEN:          
  Hidden.

  For operators: hide from places in the user interface where Blender would add the property automatically, like Adjust Last Operation. Also this property is not written to presets..

:SKIP_SAVE:       
  Skip Save.

  For operators: the value of this property will not be remembered between invocations of the operator; instead, each invocation will start by using the default value. Also this property is not written to presets..

:SKIP_PRESET:     
  Skip Preset.

  Do not write in presets.

:ANIMATABLE:      
  Animatable.

:LIBRARY_EDITABLE:
  Library Editable.

  This property can be edited, even when it is used on linked data (which normally is read-only). Note that edits to the property will not be saved to the blend file..

:PROPORTIONAL:    
  Adjust values proportionally to each other.

:TEXTEDIT_UPDATE: 
  Update on every keystroke in textedit 'mode'.

:OUTPUT_PATH:     
  Output Path.

.. _rna-enum-property-flag-items:

"""

import typing
