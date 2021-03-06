# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from bpy.types import AddonPreferences
from bpy.props import IntProperty, EnumProperty
from bpy.utils import register_class, unregister_class


class CAROUSEL_preferences(AddonPreferences):
    bl_idname = __package__

    points_amount_default: IntProperty(
        name='Points amount',
        subtype='UNSIGNED',
        min=1,
        max=999,
        default=36
    )

    center_count_mode: EnumProperty(
        name='Count mode',
        items=[
            ('GEOMETRY', 'GEOMETRY', '', '', 0),
            ('BBOX', 'BBOX', '', '', 1)
        ],
        default='BBOX'
    )

    camera_lens_default: IntProperty(
        name='Camera Focal Length',
        subtype='DISTANCE',
        min=1,
        max=5000,
        default=60
    )

    camera_sensor_width_default: IntProperty(
        name='Camera Sensor Width',
        subtype='DISTANCE',
        min=1,
        max=100,
        default=36
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'points_amount_default')
        layout.label(text='Default Camera Data')
        layout.prop(self, 'camera_lens_default')
        layout.prop(self, 'camera_sensor_width_default')
        layout.label(text='Performance')
        layout.prop(self, 'center_count_mode')


def register():
    register_class(CAROUSEL_preferences)


def unregister():
    unregister_class(CAROUSEL_preferences)
