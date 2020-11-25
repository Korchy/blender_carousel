# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from bpy.types import AddonPreferences
from bpy.props import IntProperty
from bpy.utils import register_class, unregister_class


class CAROUSEL_preferences(AddonPreferences):
    bl_idname = __package__

    points_amount_default: IntProperty(
        name='Points amount',
        default=36
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'points_amount_default')


def register():
    register_class(CAROUSEL_preferences)


def unregister():
    unregister_class(CAROUSEL_preferences)
