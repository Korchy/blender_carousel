# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class CAROUSEL_PT_panel(Panel):
    bl_idname = 'CAROUSEL_PT_panel'
    bl_label = 'Carousel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Carousel'

    def draw(self, context):
        self.layout.operator('carousel.turntable', icon='DISC')


def register():
    register_class(CAROUSEL_PT_panel)


def unregister():
    unregister_class(CAROUSEL_PT_panel)
