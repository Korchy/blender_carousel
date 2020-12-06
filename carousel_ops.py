# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .carousel import TurnTable
from .carousel_render import CarouselRender


class CAROUSEL_OT_turntable(Operator):
    bl_idname = 'carousel.turntable'
    bl_label = 'Turntable'
    bl_description = 'Make turntable image sequence'
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None  # timer for modal calling

    def execute(self, context):
        # do all automatic
        # to object mode
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        # init
        TurnTable.init(
            context=context,
            scene_data=bpy.data,
            selection=context.selected_objects
        )
        # batch render
        CarouselRender.batch_render(
            context=context,
            scene_data=bpy.data
        )
        # to monitor normal finishing
        self._timer = context.window_manager.event_timer_add(
            time_step=0.5,
            window=context.window
        )
        # to monitor cancelling
        context.window_manager.modal_handler_add(operator=self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'ESC'}:
            context.window_manager.event_timer_remove(self._timer)
            CarouselRender.clear()
            TurnTable.clear(
                context=context,
                scene_data=bpy.data
            )
            return {'CANCELLED'}
        if event.type == 'TIMER':
            if CarouselRender.mode() is None:
                context.window_manager.event_timer_remove(self._timer)
                TurnTable.clear(
                    context=context,
                    scene_data=bpy.data
                )
                return {'FINISHED'}
        return {'PASS_THROUGH'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects) \
               and not bpy.data.collections.get(TurnTable.collection_name)


class CAROUSEL_OT_turntable_init(Operator):
    bl_idname = 'carousel.turntable_init'
    bl_label = 'Init'
    bl_description = 'Init Turntable preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        TurnTable.init(
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
               and not bpy.data.collections.get(TurnTable.collection_name)


class CAROUSEL_OT_turntable_select_points(Operator):
    bl_idname = 'carousel.turntable_select_points'
    bl_label = 'Select Points'
    bl_description = 'Select Turntable points'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        TurnTable.select_points(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(TurnTable.collection_name))


class CAROUSEL_OT_turntable_to_prev_point(Operator):
    bl_idname = 'carousel.turntable_to_prev_point'
    bl_label = 'To Prev'
    bl_description = 'Move camera to the previous point'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        TurnTable.to_prev_point(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(TurnTable.collection_name))


class CAROUSEL_OT_turntable_to_next_point(Operator):
    bl_idname = 'carousel.turntable_to_next_point'
    bl_label = 'To Next'
    bl_description = 'Move camera to the next point'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        TurnTable.to_next_point(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(TurnTable.collection_name))


class CAROUSEL_OT_turntable_to_active_point(Operator):
    bl_idname = 'carousel.turntable_to_active_point'
    bl_label = 'To Active'
    bl_description = 'Move camera to the active point'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        TurnTable.to_active_point(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return TurnTable.active_point_number(
            context=context,
            scene_data=bpy.data
        ) is not None


class CAROUSEL_OT_turntable_render_active(Operator):
    bl_idname = 'carousel.turntable_render_active'
    bl_label = 'Render Active Point'
    bl_description = 'Render form the active point position'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        CarouselRender.point_render(
            context=context,
            scene_data=bpy.data,
            point_number=TurnTable.active_point_number(
                context=context,
                scene_data=bpy.data
            )
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return TurnTable.active_point_number(
            context=context,
            scene_data=bpy.data
        ) is not None


class CAROUSEL_OT_turntable_render_all(Operator):
    bl_idname = 'carousel.turntable_render_all'
    bl_label = 'Render All'
    bl_description = 'Render all the sequence'
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None  # timer for modal calling

    def execute(self, context):
        CarouselRender.batch_render(
            context=context,
            scene_data=bpy.data
        )
        # to monitor normal finishing
        self._timer = context.window_manager.event_timer_add(
            time_step=0.5,
            window=context.window
        )
        # to monitor cancelling
        context.window_manager.modal_handler_add(operator=self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'ESC'}:
            CarouselRender.clear()
            context.window_manager.event_timer_remove(self._timer)
            return {'CANCELLED'}
        if event.type == 'TIMER':
            if CarouselRender.mode() is None:
                context.window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}
        return {'PASS_THROUGH'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(TurnTable.collection_name))


class CAROUSEL_OT_turntable_clear(Operator):
    bl_idname = 'carousel.turntable_clear'
    bl_label = 'Clear'
    bl_description = 'Clear Turntable preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_mode = context.object.mode if context.object else 'OBJECT'
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        TurnTable.clear(
            context=context,
            scene_data=bpy.data
        )
        if context.object:
            bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get(TurnTable.collection_name))


def register():
    register_class(CAROUSEL_OT_turntable)
    register_class(CAROUSEL_OT_turntable_init)
    register_class(CAROUSEL_OT_turntable_select_points)
    register_class(CAROUSEL_OT_turntable_to_prev_point)
    register_class(CAROUSEL_OT_turntable_to_next_point)
    register_class(CAROUSEL_OT_turntable_to_active_point)
    register_class(CAROUSEL_OT_turntable_render_active)
    register_class(CAROUSEL_OT_turntable_render_all)
    register_class(CAROUSEL_OT_turntable_clear)


def unregister():
    unregister_class(CAROUSEL_OT_turntable_clear)
    unregister_class(CAROUSEL_OT_turntable_render_all)
    unregister_class(CAROUSEL_OT_turntable_render_active)
    unregister_class(CAROUSEL_OT_turntable_to_active_point)
    unregister_class(CAROUSEL_OT_turntable_to_next_point)
    unregister_class(CAROUSEL_OT_turntable_to_prev_point)
    unregister_class(CAROUSEL_OT_turntable_select_points)
    unregister_class(CAROUSEL_OT_turntable_init)
    unregister_class(CAROUSEL_OT_turntable)
