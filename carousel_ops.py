# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .carousel import Carousel


class CAROUSEL_OT_turntable(Operator):
    bl_idname = 'carousel.turntable'
    bl_label = 'Turntable'
    bl_description = 'Make turntable image sequence'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        Carousel.turntable(context=context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


def register():
    register_class(CAROUSEL_OT_turntable)


def unregister():
    unregister_class(CAROUSEL_OT_turntable)
