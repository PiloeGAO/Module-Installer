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

import bpy
import platform, subprocess, sys, os
from bpy import context
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty
import importlib

import modules_installer_popups

class SYSTEM_UL_UIAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__
    
    python_path = ""
    pip_path = ""
    pip_present = True #Set by default pip installed
    
    modules_reader_path = bpy.utils.user_resource('SCRIPTS', path="addons/Module-Installer/modules.txt") #Get path of modules.txt
            
    try: #Check if it is installed
        import pip 
    except ImportError: #If not set pip to False
        pip_present = False
        
    if pip_present:
        if platform.system() == "Windows": #Paths for Windows 
            python_path = os.path.join(os.path.dirname(sys.executable), bpy.app.version_string[:4]+"/python/bin", "python.exe")
            pip_path = os.path.join(os.path.dirname(sys.executable), bpy.app.version_string[:4]+"/python/Scripts", "pip.exe")
        elif platform.system() == "Darwin": #Paths for MacOS
            python_path = os.path.join(os.path.normpath(os.path.join(os.path.dirname(sys.executable), *([".."] * 1)) ), "Resources/"+bpy.app.version_string[:4]+"/python/bin", "python3.5m")
            pip_path = os.path.join(os.path.normpath(os.path.join(os.path.dirname(sys.executable), *([".."] * 1)) ), "Resources/"+bpy.app.version_string[:4]+"/python/bin", "pip")
        elif platform.system() == "Linux": #Paths for Linux
            python_path = os.path.join(os.path.dirname(sys.executable), bpy.app.version_string[:4]+"/python/bin", "python3.5m")
            pip_path = os.path.join(os.path.dirname(sys.executable), bpy.app.version_string[:4]+"/python/bin", "pip")
        else: #Paths for other
            print("System unkwon!")
            python_path = os.path.join(os.path.dirname(sys.executable))
            pip_path = os.path.join(os.path.dirname(sys.executable))
    
    python_filepath = StringProperty(
            name="Python File Path (blender python exec)",
            subtype='FILE_PATH',
            default=python_path, #use bundled-python to get correct path
            ) #Python file path

    pip_install_file = StringProperty(
            name="PIP install file",
            subtype='FILE_PATH',
            default=bpy.utils.user_resource('SCRIPTS', path="addons/Module-Installer/utils/get-pip.py"), #Locate get-pip.py to install PIP
            ) #PIP install file

    pip_filepath = StringProperty(
            name="PIP File Path (blender python PIP)",
            subtype='FILE_PATH',
            default=pip_path, #Use pip_filepath 
            )

    pip_modules = StringProperty(
            name="PIP modules (just space between modules)",
            subtype='NONE',
            ) #PIP modules wanted by user

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is preferences to setup PIP and new modules")
        
        box = layout.box()
        box.prop(self, "python_filepath")
        if not SYSTEM_UL_UIAddonPreferences.pip_present == True:
            if(pip_path != null):
                bpy.context.window_manager.popup_menu(modules_installer_popups.PIPInstallPopup.draw, title="PIP Install", icon='INFO')
            box.prop(self, "pip_install_file")
            box.operator("system.install_pip")
        
        else: #Use pip_present to show/hide install panel
            box.prop(self, "pip_filepath")
            modules_reader_present = SYSTEM_OT_ModulesReader.execute(SYSTEM_UL_UIAddonPreferences.python_path, SYSTEM_UL_UIAddonPreferences.pip_path, SYSTEM_UL_UIAddonPreferences.modules_reader_path)
            if(modules_reader_present):
                box.prop(self, "pip_modules")
                box.operator("system.install_modules")
                box.operator("system.uninstall_modules")
            else:
                box.operator(SYSTEM_OT_ModulesReader.uninstall(SYSTEM_UL_UIAddonPreferences.python_path, SYSTEM_UL_UIAddonPreferences.pip_path, SYSTEM_UL_UIAddonPreferences.modules_reader_path), title="Uninstall modules")


class SYSTEM_OT_addon_module_installer(Operator):
    bl_idname = "system.addon_module_installer"
    bl_label = "Add-on Module Installer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        user_preferences = context.user_preferences #Get preferences
        addon_prefs = user_preferences.addons[__package__].preferences #Show addon preferences

        return {'FINISHED'}

class SYSTEM_OT_PIPInstaller(bpy.types.Operator): #PIP installer class
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
            self.report({'INFO'}, "PIP installed successfully - Please restart Blender!")

        return {'FINISHED'}

class SYSTEM_OT_ModulesReader(): #Class with all modules.txt fonctions      
    def execute(python_filepath, pip_filepath, modules_reader_path):
        print("Let's get modules from a file")
        
        print("filesize:" + str(os.path.getsize(modules_reader_path)))
        if(os.path.getsize(modules_reader_path) > 139):
            SYSTEM_OT_ModulesReader.installer(python_filepath, pip_filepath, modules_reader_path)
            return False
        else:
            return True
    
    def installer(python_filepath, pip_filepath, modules_reader_path):
        command = subprocess.Popen("\"" + python_filepath + "\" \"" + pip_filepath + "\" install " + modules_reader_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) #Command to install modules

        if command.wait() != 0:
            output, error = command.communicate()
            bpy.types.Operator.report({'ERROR'}, str(error)) #Error on Operator with no attribute called 'report'
        else:
            bpy.types.Operator.report({'INFO'}, "Modules installed successfully - Please restart Blender!") #Error on Operator with no attribute called 'report'
            
    def uninstaller(python_filepath, pip_filepath, modules_reader_path):
        command = subprocess.Popen("\"" + python_filepath + "\" \"" + pip_filepath + "\" uninstall " + modules_reader_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) #Command to install modules

        if command.wait() != 0:
            output, error = command.communicate()
            bpy.types.Operator.report({'ERROR'}, str(error)) #Error on Operator with no attribute called 'report'
        else:
            bpy.types.Operator.report({'INFO'}, "Modules uninstalled successfully - Please restart Blender!") #Error on Operator with no attribute called 'report'

class SYSTEM_OT_ModuleInstaller(bpy.types.Operator): #Modules installer class
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
            self.report({'INFO'}, "Modules installed successfully - Please restart Blender!")

        return {'FINISHED'}

class SYSTEM_OT_ModuleUninstaller(bpy.types.Operator): #Modules uninstaller class
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
            self.report({'INFO'}, "Modules installed successfully - Please restart Blender!")

        return {'FINISHED'}
