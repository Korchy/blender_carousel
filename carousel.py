# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from .object import Object


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
        # bounding sphere
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
        

    @classmethod
    def _turntable_collection(cls, context, scene_data):
        # return turntable collection
        turntable_collection = scene_data.collections.get('turntable')
        if not turntable_collection:
            turntable_collection = scene_data.collections.new(name='turntable')
            context.scene.collection.children.link(child=turntable_collection)
        return turntable_collection
