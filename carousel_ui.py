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
        layout = self.layout
        layout.label(text='Automatic')
        layout.operator('carousel.turntable', icon='DISC')
        layout.label(text='By steps')
        layout.operator('carousel.turntable_init', icon='PRESET_NEW')
        row = layout.row()
        col = row.column()
        box = col.box()
        row1 = box.row()
        row1.operator('carousel.turntable_to_prev_point', icon='TRIA_LEFT', text='')
        row1.operator('carousel.turntable_to_active_point', icon='VIS_SEL_11')
        row1.operator('carousel.turntable_to_next_point', icon='TRIA_RIGHT', text='')
        col = row.column()
        box = col.box()
        box.operator('carousel.turntable_select_points', icon='POINTCLOUD_DATA', text='')
        row = layout.row()
        row.operator('carousel.turntable_render_all', icon='RENDER_RESULT')
        row.operator('carousel.turntable_render_current', icon='IMAGE_DATA')
        layout.operator('carousel.turntable_clear', icon='CANCEL')


def register():
    register_class(CAROUSEL_PT_panel)


def unregister():
    unregister_class(CAROUSEL_PT_panel)
