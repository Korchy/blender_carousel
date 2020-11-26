# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from mathutils import Vector


class Carousel:

    # _tmp_obj = []

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
        # camera target
        target_co = cls._geometry_center(
            objects=selection,
            count_mode=context.preferences.addons[__package__].preferences.center_count_mode
        )
        camera_target = scene_data.objects.new(name='camera_target', object_data=None)
        camera_target.location = target_co
        camera_target.empty_display_type = 'SPHERE'
        turntable_collection.objects.link(object=camera_target)

    @staticmethod
    def _geometry_center(objects: list, count_mode='BBOX'):
        # geometry center of objects
        objects_center_global = None
        if count_mode == 'GEOMETRY':
            # GEOMETRY - by vertices
            vertices_co_global = []
            for obj in objects:
                if obj.type == 'MESH':
                    vertices_co_global.extend([obj.matrix_world @ vertex.co for vertex in obj.data.vertices])
                if obj.type == 'CURVE':
                    for spline in obj.data.splines:
                        vertices_co_global.extend([obj.matrix_world @ point.co for point in spline.bezier_points])
                else:
                    vertices_co_global.append(obj.location)
            get_center = lambda l: (max(l) + min(l)) / 2
            x, y, z = [[vertex[i] for vertex in vertices_co_global] for i in range(3)]
            objects_center_global = [get_center(axis) for axis in [x, y, z]]
        elif count_mode == 'BBOX':
            # BBOX - by object bounding boxes
            obj_global_bbox_centers = []
            for obj in objects:
                obj_local_bbox_center = sum((Vector(bbox) for bbox in obj.bound_box), Vector()) / 8
                obj_global_bbox_centers.append(obj.matrix_world @ obj_local_bbox_center)
            objects_center_global = sum((center for center in obj_global_bbox_centers), Vector()) / len(obj_global_bbox_centers)
        return objects_center_global

    @classmethod
    def _turntable_collection(cls, context, scene_data):
        # return turntable collection
        turntable_collection = scene_data.collections.get('turntable')
        if not turntable_collection:
            turntable_collection = scene_data.collections.new(name='turntable')
            context.scene.collection.children.link(child=turntable_collection)
        return turntable_collection
