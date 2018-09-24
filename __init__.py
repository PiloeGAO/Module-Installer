bl_info = {
    "name": "Module Installer",
    "author": "PiloeGAO",
    "version": (0, 1),
    "blender": (2, 79, 0),
    "location": "SpaceBar Search -> Add-on Preferences",
    "description": "Installing new modules to blender",
    "warning": "In Dev",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System",
    }

import bpy, os
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

class UIAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    python_filepath = StringProperty(
            name="Python File Path (blender python exec)",
            subtype='FILE_PATH',
            ) #Python file path

    pip_install_file = StringProperty(
            name="PIP install file (get from official python website)",
            subtype='FILE_PATH',
            ) #PIP install file

    pip_modules = StringProperty(
            name="PIP modules (just space between modules)",
            subtype='NONE',
            ) #PIP modules neededs

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")

        box = layout.box()
        box.prop(self, "python_filepath")
        box.prop(self, "pip_install_file")
        box.operator("system.install_pip")

        box.prop(self, "pip_modules")
        box.operator("system.install_modules")
        box.operator("system.uninstall_modules")


class SYSTEM_OT_addon_module_installer(Operator):
    """Display example preferences"""
    bl_idname = "system.addon_module_installer"
    bl_label = "Add-on Module Installer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        return {'FINISHED'}

class PIPInstaller(bpy.types.Operator): #PIP installer class
    bl_idname = "system.install_pip"
    bl_label = "Install PIP"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        print("Let's install PIP")

        os.system(addon_prefs.python_filepath + " " + addon_prefs.pip_install_file) #Command to install PIP

        print("PIP installed successfully")
        return {'FINISHED'}

class ModuleInstaller(bpy.types.Operator): #Module installer class
    bl_idname = "system.install_modules"
    bl_label = "Install Modules"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        print("Let's install modules")

        python_dir = os.path.dirname(os.path.dirname(addon_prefs.python_filepath))
        pip_location = python_dir + "\Scripts\pip.exe" #Only for windows (mac and linux later)

        os.system(addon_prefs.python_filepath + " " + pip_location + " install " + addon_prefs.pip_modules) #Command to install modules

        return {'FINISHED'}

class ModuleUninstaller(bpy.types.Operator): #Modle uninstaller class
    bl_idname = "system.uninstall_modules"
    bl_label = "Uninstall Modules"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        print("Let's uninstall modules")

        python_dir = os.path.dirname(os.path.dirname(addon_prefs.python_filepath))
        pip_location = python_dir + "\Scripts\pip.exe" #Only for windows (mac and linux later)

        os.system(addon_prefs.python_filepath + " " + pip_location + " uninstall " + addon_prefs.pip_modules) #Command to uninstall modules

        return {'FINISHED'}

# Registration
def register():
    bpy.utils.register_class(SYSTEM_OT_addon_module_installer)
    bpy.utils.register_class(UIAddonPreferences)
    bpy.utils.register_class(PIPInstaller)
    bpy.utils.register_class(ModuleInstaller)
    bpy.utils.register_class(ModuleUninstaller)


def unregister():
    bpy.utils.unregister_class(SYSTEM_OT_addon_module_installer)
    bpy.utils.unregister_class(UIAddonPreferences)
    bpy.utils.unregister_class(PIPInstaller)
    bpy.utils.unregister_class(ModuleInstaller)
    bpy.utils.unregister_class(ModuleUninstaller)

if __name__ == "__main__":
    register()
