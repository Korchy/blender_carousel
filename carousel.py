# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from .object import Object
from mathutils import Vector
import math


class Carousel:

    @classmethod
    def turntable(cls, context, scene_data, selection):
        # carousel
        cls._init_turntable(
            context=context,
            scene_data=scene_data,
            selection=selection
        )

    @classmethod
    def _init_turntable(cls, context, scene_data, selection):
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
        camera.location = camera_location
        turntable_collection.objects.link(object=camera)
        # camera targeting
        track_to = camera.constraints.new(type='TRACK_TO')
        track_to.target = camera_target
        # points cloud
        points_amount = context.preferences.addons[__package__].preferences.points_amount_default
        for i in range(points_amount):
            point = scene_data.objects.new(name='point', object_data=None)
            point.empty_display_type = 'PLAIN_AXES'
            angle = (360 * i / points_amount) * math.pi / 180
            null_location = Vector((camera_ring_radius * math.cos(angle), camera_ring_radius * math.sin(angle), 0))
            point.location = null_location + camera_target.location
            turntable_collection.objects.link(object=point)

    @classmethod
    def clear_turntable(cls, context, scene_data):
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
        turntable_collection = scene_data.collections.get('turntable')
        if not turntable_collection:
            turntable_collection = scene_data.collections.new(name='turntable')
            context.scene.collection.children.link(child=turntable_collection)
        return turntable_collection
