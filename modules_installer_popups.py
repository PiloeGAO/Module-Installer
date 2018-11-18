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

class PIPInstallPopup(bpy.types.Menu):
    bl_idname = "SYSTEM_OP_pip_install_query"
    bl_label = "Select"
    

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="PIP is needed, we will install it!")
        layout.operator("system.install_pip")
