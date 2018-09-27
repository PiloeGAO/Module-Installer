'''
Copyright (C) 2018 Leo DEPOIX
LEONUMERIQUE@GMAIL.com

Created by Leo DEPOIX

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy, subprocess, sys, os
from bpy import context
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty
import importlib

class UIAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    python_filepath = StringProperty(
            name="Python File Path (blender python exec)",
            subtype='FILE_PATH',
            default=sys.executable, #use bundled-python to get correct path
            ) #Python file path
            
            #Windows path: "yourPathToBlender/2.79/python/bin/python.exe
            #MacOS (steam): "/Users/yourusername/Library/Application Support/Steam/steamapps/common/Blender/blender.app/Contents/Resources/2.79/python/bin/python3.5m"
            #MacOS (nosteam): "yourPathToBlender/blender.app/Contents/Resources/2.79/python/bin/python3.5m"
            #Linux: ?

    pip_install_file = StringProperty(
            name="PIP install file",
            subtype='FILE_PATH',
            default=bpy.utils.user_resource('SCRIPTS', path="addons/Module-Installer/utils/get-pip.py"), #Locate get-pip.py to install PIP
            ) #PIP install file

    pip_filepath = StringProperty(
            name="PIP File Path (blender python PIP)",
            subtype='FILE_PATH',
            default=sys.executable, #ONLY WORKING ON WINDOWS CURRENTLY
            ) #Python file path

            #Windows path: "yourPathToBlender/2.79//python/Scripts/pip.exe"
            #MacOS (steam): "/Users/youruser/Library/Application Support/Steam/steamapps/common/Blender/blender.app/Contents/Resources/2.79/python/bin/pip"
            #MacOS (nosteam): "yourPathToBlender/blender.app/Contents/Resources/2.79/python/bin/pip"
            #Linux: ?

    pip_modules = StringProperty(
            name="PIP modules (just space between modules)",
            subtype='NONE',
            ) #PIP modules wanted by user

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is preferences to setup PIP and new modules")

        box = layout.box()
        box.prop(self, "python_filepath")
        box.prop(self, "pip_install_file")
        box.operator("system.install_pip")
        
        box.prop(self, "pip_filepath")
        box.prop(self, "pip_modules")
        box.operator("system.install_modules")
        box.operator("system.uninstall_modules")


class SYSTEM_OT_addon_module_installer(Operator):
    bl_idname = "system.addon_module_installer"
    bl_label = "Add-on Module Installer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        return {'FINISHED'}

class PIPInstaller(bpy.types.Operator): #PIP installer class
    bl_idname = "system.install_pip"
    bl_label = "Install PIP"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        print("Let's install PIP")

        command = subprocess.Popen("\"" + addon_prefs.python_filepath +  "\" \"" + addon_prefs.pip_install_file + "\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) #Command to install PIP

        if command.wait() != 0:
            output, error = command.communicate()
            self.report({'ERROR'}, str(error))
        else:
            self.report({'INFO'}, "PIP installed successfully")

        return {'FINISHED'}

class ModuleInstaller(bpy.types.Operator): #Modules installer class
    bl_idname = "system.install_modules"
    bl_label = "Install Modules"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        print("Let's install modules")

        command = subprocess.Popen("\"" + addon_prefs.python_filepath + "\" \"" + addon_prefs.pip_filepath + "\" install " + addon_prefs.pip_modules, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) #Command to install modules

        if command.wait() != 0:
            output, error = command.communicate()
            self.report({'ERROR'}, str(error))
        else:
            self.report({'INFO'}, "Modules installed successfully")

        return {'FINISHED'}

class ModuleUninstaller(bpy.types.Operator): #Modules uninstaller class
    bl_idname = "system.uninstall_modules"
    bl_label = "Uninstall Modules"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        print("Let's uninstall modules")

        command = subprocess.Popen("\"" + addon_prefs.python_filepath + "\" \"" + addon_prefs.pip_filepath + "\" uninstall " + addon_prefs.pip_modules, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) #Command to install modules

        if command.wait() != 0:
            output, error = command.communicate()
            self.report({'ERROR'}, str(error))
        else:
            self.report({'INFO'}, "Modules installed successfully")

        return {'FINISHED'}
