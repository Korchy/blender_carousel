# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from .object import Object
from mathutils import Vector
import math


class Carousel:
    turntable_collection_name = 'turntable'

    @classmethod
    def turntable(cls, context, scene_data, selection):
        # mate turntable sequence
        cls.turntable_init(
            context=context,
            scene_data=scene_data,
            selection=selection
        )

    @classmethod
    def turntable_init(cls, context, scene_data, selection):
        # init scene for turntable
        # turntable collection
        turntable_collection = cls._turntable_collection(
            context=context,
            scene_data=scene_data
        )
        # bounding sphere (target)
        b_sphere_co, b_sphere_radius = Object.bounding_sphere(
            objects=selection,
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
        camera_location = (b_sphere_co.x - camera_ring_radius, b_sphere_co.y, b_sphere_co.z)
        camera_data = scene_data.cameras.new(name='cam')
        camera_data.lens = lens
        camera_data.sensor_width = sensor_width
        camera = scene_data.objects.new(name='cam', object_data=camera_data)
        # camera.location = camera_location
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
        cls._turntable_to_point(
            context=context,
            scene_data=scene_data,
            point_number=0
        )

    @classmethod
    def turntable_select_points(cls, context, scene_data):
        # select all points
        cls._deselect_all(context=context)
        points = cls._turntable_points(
            scene_data=scene_data
        )
        for point in points:
            point.select_set(state=True)

    @classmethod
    def turntable_to_active_point(cls, context, scene_data):
        # camera to active point
        active_point = context.active_object if context.active_object \
                                                and context.active_object.type == 'EMPTY' \
                                                and 'point_' in context.active_object.name else None
        if active_point:
            camera = cls._turntable_camera(scene_data=scene_data)
            if camera:
                camera.parent = active_point

    @classmethod
    def turntable_to_next_point(cls, context, scene_data):
        # camera to next point
        camera = cls._turntable_camera(scene_data=scene_data)
        if camera and camera.parent:
            max_number = context.preferences.addons[__package__].preferences.points_amount_default - 1
            next_point_number = int(camera.parent.name[-3:]) + 1
            next_point_number = 0 if next_point_number > max_number else next_point_number
            next_point = next((point for point in cls._turntable_points(scene_data=scene_data)
                               if point.name == 'point_' + str(next_point_number).zfill(3)), None)
            if next_point:
                camera.parent = next_point

    @classmethod
    def turntable_to_prev_point(cls, context, scene_data):
        # camera to previous point
        camera = cls._turntable_camera(scene_data=scene_data)
        if camera and camera.parent:
            max_number = context.preferences.addons[__package__].preferences.points_amount_default - 1
            prev_point_number = int(camera.parent.name[-3:]) - 1
            prev_point_number = max_number if prev_point_number < 0 else prev_point_number
            prev_point = next((point for point in cls._turntable_points(scene_data=scene_data)
                               if point.name == 'point_' + str(prev_point_number).zfill(3)), None)
            if prev_point:
                camera.parent = prev_point

    @classmethod
    def _turntable_to_point(cls, context, scene_data, point_number=0):
        # camera to point
        point = next((point for point in cls._turntable_points(scene_data=scene_data)
                      if point.name == 'point_' + str(point_number).zfill(3)), None)
        if point:
            camera = cls._turntable_camera(scene_data=scene_data)
            if camera:
                camera.parent = point

    @classmethod
    def turntable_clear(cls, context, scene_data):
        # remove all objects
        turntable_collection = cls._turntable_collection(
            context=context,
            scene_data=scene_data
        )
        for obj in turntable_collection.objects:
            scene_data.objects.remove(obj, do_unlink=True)
        # remove collection
        scene_data.collections.remove(turntable_collection)

    @classmethod
    def _turntable_collection(cls, context, scene_data):
        # return turntable collection
        turntable_collection = scene_data.collections.get(cls.turntable_collection_name)
        if not turntable_collection:
            turntable_collection = scene_data.collections.new(
                name=cls.turntable_collection_name
            )
            context.scene.collection.children.link(child=turntable_collection)
        return turntable_collection

    @classmethod
    def _turntable_camera(cls, scene_data):
        # return turntable camera
        turntable_collection = scene_data.collections.get(cls.turntable_collection_name)
        turntable_camera = next((obj for obj in turntable_collection.objects if obj.type == 'CAMERA'), None)
        return turntable_camera

    @classmethod
    def _turntable_points(cls, scene_data):
        # return turntable points list
        turntable_collection = scene_data.collections.get(cls.turntable_collection_name)
        if turntable_collection:
            return (point for point in turntable_collection.objects if point.type == 'EMPTY' and 'point_' in point.name)
        else:
            return None

    @staticmethod
    def _deselect_all(context):
        # deselect all selected objects
        for obj in context.selected_objects:
            obj.select_set(state=False)
