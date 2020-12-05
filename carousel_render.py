# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

import functools
import os
import bpy
from bpy.app.handlers import render_complete, render_cancel
from .carousel_file_system import CarouselFileSystem
from .carousel import TurnTable


class CarouselRender:

    _mode = None
    _context = None
    _scene_data = None
    _current_point = None
    _render_in_progress = False

    @classmethod
    def batch_render(cls, context, scene_data):
        # start batch render (all points)
        cls._mode = 'BATCH'
        cls._context = context
        cls._scene_data = scene_data
        cls._current_point = -1
        cls._render_next(
            context=context,
            scene_data=scene_data
        )

    @classmethod
    def point_render(cls, context, scene_data, point_number):
        # start render from single point
        if point_number:
            cls._mode = 'POINT'
            cls._context = context
            cls._scene_data = scene_data
            cls._current_point = point_number
            cls._render_next(
                context=context,
                scene_data=scene_data
            )

    @classmethod
    def _render_next(cls, context, scene_data):
        # render next
        cls._current_point += 1
        max_point_number = cls._context.preferences.addons[__package__].preferences.points_amount_default - 1
        if cls._current_point <= max_point_number:
            TurnTable.turntable_to_point(
                context=context,
                scene_data=scene_data,
                point_number=cls._current_point
            )
            if cls._on_render_finish not in render_complete:
                render_complete.append(cls._on_render_finish)
            if cls._on_render_cancel not in render_cancel:
                render_cancel.append(cls._on_render_cancel)
            # render with next point
            bpy.app.timers.register(functools.partial(cls._render), first_interval=1.0)
        else:
            cls._clear()

    @classmethod
    def _render(cls):
        # execute render
        rez = {'CANCELLED'}
        # for current_area in cls._context.window_manager.windows[0].screen.areas:
        #     if current_area.type == 'VIEW_3D':
        #         override_area = cls._context.copy()
        #         override_area['area'] = current_area
        #         override_area['window'] = bpy.context.window_manager.windows[0]
        #         print('INVOKE DEFAULT')
        #         rez = bpy.ops.render.render(override_area, 'INVOKE_DEFAULT')
        #         break
        if not cls._render_in_progress:
            cls._render_in_progress = True
            # rez = bpy.ops.render.render('EXEC_DEFAULT')
            rez = bpy.ops.render.render('INVOKE_DEFAULT', use_viewport=True)
        if rez == {'CANCELLED'}:
            # retry with timer
            cls._render_in_progress = False
            return 1.0
        else:
            return None

    @classmethod
    def _on_render_finish(cls, scene, unknown):
        # on finish render
        cls._save_image(scene=scene)
        cls._render_in_progress = False
        # render wit next point
        if cls._mode == 'BATCH':
            cls._render_next(
                context=cls._context,
                scene_data=cls._scene_data
            )
        else:
            cls._clear()

    @classmethod
    def _on_render_cancel(cls):
        # on render cancel
        cls._clear()

    @classmethod
    def _save_image(cls, scene):
        # save image from current render
        dest_dir = CarouselFileSystem.abs_path(
            path=cls._context.scene.render.filepath
        )
        if dest_dir:
            dest_dir = os.path.join(dest_dir, 'turntable')
            if not os.path.isdir(dest_dir):
                os.makedirs(name=dest_dir)
            file_name = 'point_' + str(cls._current_point).zfill(3) + scene.render.file_extension
            file_path = os.path.join(dest_dir, file_name)
            bpy.data.images['Render Result'].save_render(filepath=file_path)

    @classmethod
    def _clear(cls):
        cls._mode = None
        cls._context = None
        cls._scene_data = None
        cls._current_point = None
        cls._render_in_progress = False
        if cls._on_render_finish in render_complete:
            render_complete.remove(cls._on_render_finish)
        if cls._on_render_cancel in render_cancel:
            render_cancel.remove(cls._on_render_cancel)
