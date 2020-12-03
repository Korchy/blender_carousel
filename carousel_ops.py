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
        Carousel.turntable_init(
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


class CAROUSEL_OT_turntable_select_points(Operator):
    bl_idname = 'carousel.turntable_select_points'
    bl_label = 'Select Points'
    bl_description = 'Select Turntable points'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.turntable_select_points(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(Carousel.turntable_collection_name))


class CAROUSEL_OT_turntable_to_prev_point(Operator):
    bl_idname = 'carousel.turntable_to_prev_point'
    bl_label = 'To Prev'
    bl_description = 'Move camera to the previous point'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.turntable_to_prev_point(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(Carousel.turntable_collection_name))


class CAROUSEL_OT_turntable_to_next_point(Operator):
    bl_idname = 'carousel.turntable_to_next_point'
    bl_label = 'To Next'
    bl_description = 'Move camera to the next point'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.turntable_to_next_point(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(Carousel.turntable_collection_name))


class CAROUSEL_OT_turntable_to_active_point(Operator):
    bl_idname = 'carousel.turntable_to_active_point'
    bl_label = 'To Active'
    bl_description = 'Move camera to the active point'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.turntable_to_active_point(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(Carousel.turntable_collection_name)) \
               and context.active_object \
               and context.active_object.type == 'EMPTY' \
               and 'point_' in context.active_object.name


class CAROUSEL_OT_turntable_clear(Operator):
    bl_idname = 'carousel.turntable_clear'
    bl_label = 'Clear'
    bl_description = 'Clear Turntable preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        Carousel.turntable_clear(
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
    register_class(CAROUSEL_OT_turntable_select_points)
    register_class(CAROUSEL_OT_turntable_to_prev_point)
    register_class(CAROUSEL_OT_turntable_to_next_point)
    register_class(CAROUSEL_OT_turntable_to_active_point)
    register_class(CAROUSEL_OT_turntable_clear)


def unregister():
    unregister_class(CAROUSEL_OT_turntable_clear)
    unregister_class(CAROUSEL_OT_turntable_to_active_point)
    unregister_class(CAROUSEL_OT_turntable_to_next_point)
    unregister_class(CAROUSEL_OT_turntable_to_prev_point)
    unregister_class(CAROUSEL_OT_turntable_select_points)
    unregister_class(CAROUSEL_OT_turntable_init)
    unregister_class(CAROUSEL_OT_turntable)
