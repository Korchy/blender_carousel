# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_carousel

from . import carousel_ops
from . import carousel_ui
from . import carousel_preferences
from .addon import Addon


bl_info = {
    'name': 'Carousel',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 90, 0),
    'location': '3D Viewport window - N-panel - Carousel',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-carousel/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-carousel/',
    'description': 'Easily making 360 turntable image sequence'
}


def register():
    if not Addon.dev_mode():
        carousel_preferences.register()
        carousel_ops.register()
        carousel_ui.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version')


def unregister():
    if not Addon.dev_mode():
        carousel_ui.unregister()
        carousel_ops.unregister()
        carousel_preferences.unregister()


if __name__ == '__main__':
    register()
