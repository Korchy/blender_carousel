# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .carousel import Carousel


class CAROUSEL_OT_turntable(Operator):
    bl_idname = 'carousel.turntable'
    bl_label = 'Turntable'
    bl_description = 'Make turntable image sequence'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.turntable(
            context=context,
            scene_data=bpy.data,
            selection=context.selected_objects
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects) \
               and not bpy.data.collections.get(Carousel.turntable_collection_name)


class CAROUSEL_OT_turntable_init(Operator):
    bl_idname = 'carousel.turntable_init'
    bl_label = 'Init'
    bl_description = 'Init Turntable preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.init_turntable(
            context=context,
            scene_data=bpy.data,
            selection=context.selected_objects
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects) \
               and not bpy.data.collections.get(Carousel.turntable_collection_name)


class CAROUSEL_OT_turntable_clear(Operator):
    bl_idname = 'carousel.turntable_clear'
    bl_label = 'Clear'
    bl_description = 'Clear Turntable preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.clear_turntable(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(Carousel.turntable_collection_name))


def register():
    register_class(CAROUSEL_OT_turntable)
    register_class(CAROUSEL_OT_turntable_init)
    register_class(CAROUSEL_OT_turntable_clear)


def unregister():
    unregister_class(CAROUSEL_OT_turntable_clear)
    unregister_class(CAROUSEL_OT_turntable_init)
    unregister_class(CAROUSEL_OT_turntable)
