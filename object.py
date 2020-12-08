# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from mathutils import Vector


class Object:

    @staticmethod
    def bounding_sphere(objects, context, mode='BBOX'):
        # return the bounding sphere center and radius for objects (in global coordinates)
        if not isinstance(objects, list):
            objects = [objects]
        points_co_global = []
        if mode == 'GEOMETRY':
            # GEOMETRY - by all vertices/points - more precis, more slow
            for obj in objects:
                # to take into modifiers and transforms
                depsgraph = context.evaluated_depsgraph_get()
                obj = obj.evaluated_get(depsgraph)
                if obj.type == 'MESH':
                    points_co_global.extend([obj.matrix_world @ vertex.co for vertex in obj.data.vertices])
                elif obj.type == 'CURVE':
                    for spline in obj.data.splines:
                        points_co_global.extend([obj.matrix_world @ point.co for point in spline.bezier_points])
                else:
                    # cant get all points - use bbox
                    points_co_global.extend([obj.matrix_world @ Vector(bbox) for bbox in obj.bound_box])
        elif mode == 'BBOX':
            # BBOX - by object bounding boxes - less precis, quick
            for obj in objects:
                points_co_global.extend([obj.matrix_world @ Vector(bbox) for bbox in obj.bound_box])

        def get_center(l):
            return (max(l) + min(l)) / 2 if l else 0.0

        x, y, z = [[point_co[i] for point_co in points_co_global] for i in range(3)]
        b_sphere_center = Vector([get_center(axis) for axis in [x, y, z]]) if (x and y and z) else None
        b_sphere_radius = max(((point - b_sphere_center) for point in points_co_global)) if b_sphere_center else None
        return b_sphere_center, b_sphere_radius.length
