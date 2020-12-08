# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from .object import Object
from mathutils import Vector
import math


class TurnTable:

    collection_name = 'turntable'
    _backup = {
        'camera': None
    }

    @classmethod
    def init(cls, context, scene_data, selection):
        # init scene for turntable
        cls._make_backup(
            context=context
        )
        # turntable collection
        turntable_collection = cls._collection(
            context=context,
            scene_data=scene_data
        )
        # bounding sphere (target)
        b_sphere_co, b_sphere_radius = Object.bounding_sphere(
            objects=selection,
            context=context,
            mode=context.preferences.addons[__package__].preferences.center_count_mode
        )
        if not b_sphere_co:
            return
        camera_target = scene_data.objects.new(name='camera_target', object_data=None)
        camera_target.empty_display_type = 'SPHERE'
        camera_target.location = b_sphere_co
        camera_target.empty_display_size = b_sphere_radius
        turntable_collection.objects.link(object=camera_target)
        # camera
        sensor_width = context.preferences.addons[__package__].preferences.camera_sensor_width_default  # mm
        lens = context.preferences.addons[__package__].preferences.camera_lens_default  # mm
        # h or v - depends on render aspect ratio
        render_width = context.scene.render.resolution_x
        render_height = context.scene.render.resolution_y
        aspect = render_width / render_height
        if aspect > 1:
            h_fov_rad = 2 * math.atan(sensor_width / (2 * lens))
            v_fov_rad = 2 * math.atan((0.5 * render_height) / (0.5 * render_width / math.tan(h_fov_rad / 2)))
        else:
            v_fov_rad = 2 * math.atan(sensor_width / (2 * lens))
            h_fov_rad = 2 * math.atan((0.5 * render_width) / (0.5 * render_height / math.tan(v_fov_rad / 2)))
        min_angle = min(v_fov_rad, h_fov_rad)
        camera_ring_radius = b_sphere_radius / math.tan(min_angle / 2)
        camera_data = scene_data.cameras.new(name='cam')
        camera_data.lens = lens
        camera_data.sensor_width = sensor_width
        camera = scene_data.objects.new(name='cam', object_data=camera_data)
        context.scene.camera = camera   # make turntable camera active in scene
        turntable_collection.objects.link(object=camera)
        # camera targeting
        track_to = camera.constraints.new(type='TRACK_TO')
        track_to.target = camera_target
        # points cloud
        points_amount = context.preferences.addons[__package__].preferences.points_amount_default
        for i in range(points_amount):
            point = scene_data.objects.new(name='point_' + str(i).zfill(3), object_data=None)
            point.empty_display_type = 'PLAIN_AXES'
            angle = (360 * i / points_amount) * math.pi / 180
            null_location = Vector((camera_ring_radius * math.cos(angle), camera_ring_radius * math.sin(angle), 0))
            point.location = null_location + camera_target.location
            turntable_collection.objects.link(object=point)
        # camera to 0 point
        cls.to_point_number(
            context=context,
            scene_data=scene_data,
            point_number=0
        )

    @classmethod
    def select_points(cls, context, scene_data):
        # select all points
        cls._deselect_all(context=context)
        points = cls._points(
            scene_data=scene_data
        )
        for point in points:
            point.select_set(state=True)

    @classmethod
    def to_active_point(cls, context, scene_data):
        # camera to active point
        active_point_number = cls.active_point_number(
            context=context,
            scene_data=scene_data
        )
        if active_point_number is not None:
            cls.to_point_number(
                context=context,
                scene_data=scene_data,
                point_number=active_point_number,
                camera_view=True
            )

    @classmethod
    def to_next_point(cls, context, scene_data):
        # camera to next point
        camera = cls._camera(scene_data=scene_data)
        if camera and camera.parent:
            max_number = context.preferences.addons[__package__].preferences.points_amount_default - 1
            next_point_number = int(camera.parent.name[-3:]) + 1
            next_point_number = 0 if next_point_number > max_number else next_point_number
            next_point = cls._point_by_number(
                scene_data=scene_data,
                point_number=next_point_number
            )
            if next_point:
                context.view_layer.objects.active = next_point
                cls.to_point(
                    context=context,
                    scene_data=scene_data,
                    point=next_point
                )

    @classmethod
    def to_prev_point(cls, context, scene_data):
        # camera to previous point
        camera = cls._camera(scene_data=scene_data)
        if camera and camera.parent:
            max_number = context.preferences.addons[__package__].preferences.points_amount_default - 1
            prev_point_number = int(camera.parent.name[-3:]) - 1
            prev_point_number = max_number if prev_point_number < 0 else prev_point_number
            prev_point = cls._point_by_number(
                scene_data=scene_data,
                point_number=prev_point_number
            )
            if prev_point:
                context.view_layer.objects.active = prev_point
                cls.to_point(
                    context=context,
                    scene_data=scene_data,
                    point=prev_point
                )

    @classmethod
    def to_point(cls, context, scene_data, point, camera_view=False):
        # camera to point
        if point:
            camera = cls._camera(scene_data=scene_data)
            if camera:
                camera.parent = point
                if camera_view:
                    context.space_data.region_3d.view_perspective = 'CAMERA'    # switch to view from camera

    @classmethod
    def to_point_number(cls, context, scene_data, point_number=0, camera_view=False):
        # camera to point number xx
        cls.to_point(
            context=context,
            scene_data=scene_data,
            point=cls._point_by_number(
                scene_data=scene_data,
                point_number=point_number
            ),
            camera_view=camera_view
        )

    @classmethod
    def clear(cls, context, scene_data):
        # remove all objects
        turntable_collection = cls._collection(
            context=context,
            scene_data=scene_data
        )
        for obj in turntable_collection.objects:
            scene_data.objects.remove(obj, do_unlink=True)
        # remove collection
        scene_data.collections.remove(turntable_collection)
        # restore from backup
        cls._restore_backup(
            context=context
        )

    @classmethod
    def _collection(cls, context, scene_data):
        # return turntable collection
        turntable_collection = scene_data.collections.get(cls.collection_name)
        if not turntable_collection:
            turntable_collection = scene_data.collections.new(
                name=cls.collection_name
            )
            context.scene.collection.children.link(child=turntable_collection)
        return turntable_collection

    @classmethod
    def _camera(cls, scene_data):
        # return turntable camera
        turntable_collection = scene_data.collections.get(cls.collection_name)
        turntable_camera = next((obj for obj in turntable_collection.objects if obj.type == 'CAMERA'), None)
        return turntable_camera

    @classmethod
    def _points(cls, scene_data):
        # return turntable points list
        turntable_collection = scene_data.collections.get(cls.collection_name)
        if turntable_collection:
            return (point for point in turntable_collection.objects if point.type == 'EMPTY' and 'point_' in point.name)
        else:
            return None

    @classmethod
    def active_point_number(cls, context, scene_data):
        # return active point number
        turntable_collection = scene_data.collections.get(cls.collection_name)
        return int(context.active_object.name[-3:]) \
            if context.active_object \
            and context.active_object.type == 'EMPTY' \
            and (context.active_object in turntable_collection.objects[:]) \
            and 'point_' in context.active_object.name \
            else None

    @classmethod
    def _point_by_number(cls, scene_data, point_number):
        # return point by number
        turntable_points = cls._points(scene_data=scene_data)
        if turntable_points:
            return next((point for point in turntable_points if str(point_number).zfill(3) in point.name), None)
        else:
            return None

    @staticmethod
    def _deselect_all(context):
        # deselect all selected objects
        for obj in context.selected_objects:
            obj.select_set(state=False)

    @classmethod
    def _make_backup(cls, context):
        # make backup from current scene
        cls._backup['camera'] = context.scene.camera

    @classmethod
    def _restore_backup(cls, context):
        # restore data from backup to current scene
        context.scene.camera = cls._backup['camera']
