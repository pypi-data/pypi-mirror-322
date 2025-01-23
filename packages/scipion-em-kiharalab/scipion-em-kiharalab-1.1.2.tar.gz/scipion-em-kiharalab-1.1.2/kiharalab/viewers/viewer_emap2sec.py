# **************************************************************************
# *
# * Authors: Martín Salinas Antón (ssalinasmartin@gmail.com)
# *
# * Unidad de Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

# General imports
import os
from shutil import which

# Base Scipion viewer imports
import pyworkflow.viewer as pwviewer
from pwem.viewers.viewer_chimera import Chimera, ChimeraView

# Plugin imports
from ..protocols.protocol_emap2sec import ProtEmap2sec
from kiharalab.constants import EMAP2SEC_TYPE_EMAP2SECPLUS, EMAP2SECPLUS_MODE_DETECT_EVALUATE_STRUCTS

class Emap2secViewer(pwviewer.Viewer):
    """
    Wrapper to visualize different outputs of MAINMASTseg software.
    """
    _environments = [pwviewer.DESKTOP_TKINTER]
    _targets = [ProtEmap2sec]

    def _visualize(self, obj, **kwargs):
        views = []
        cls = type(obj)

        if issubclass(cls, ProtEmap2sec):
            filePath = self.chimeraViewFile()

            views.append(ChimeraView(filePath))

        return views

    def _validate(self):
        """
        This function validates the installation of Chimera so the files can be visualized.
        """
        errors = []
        if (which(Chimera.getProgram()) is None):
            errors.append("Chimera is not available. Please install it to visualize.")
        return errors
    
    def chimeraViewFile(self, axis=False):
        """
        This function creates the Chimera file needed to visualize the results.
        """
        # Creating cxc file for Chimera commands
        filePath = os.path.abspath(self.protocol._getExtraPath('chimera.cxc'))
        inputVolume = self.protocol.getVolumeAbsolutePath()

        # Open command
        openCommandPrefix = 'open'

        f = open(filePath, "w")
        # Adding axis to file if requested
        if axis:
            builFileName = os.path.abspath(self.protocol._getExtraPath("axis.bild"))
            Chimera.createCoordinateAxisFile(self.protocol.inputVolume.get().getDim()[0],
                bildFileName=os.path.abspath(self.protocol._getExtraPath("axis.bild")),
                sampling=self.protocol.inputVolume.get().getSamplingRate())
            f.write(f'{openCommandPrefix} {builFileName}\n')
            
            # Setting center of coordinates for the axis
            f.write('cofr 0,0,0\n')

        # Adding input Volume
        f.write(f'{openCommandPrefix} {inputVolume}\n')
        # Adding output Atom Struct
        f.write(f'{openCommandPrefix} {self.protocol.getOutputFile(inputVolume)}\n')
        # If evaluation mode on Emap2sec+, add reference pdb
        if self.protocol.executionType.get() == EMAP2SEC_TYPE_EMAP2SECPLUS and self.protocol.mode.get() == EMAP2SECPLUS_MODE_DETECT_EVALUATE_STRUCTS:
            f.write(f'{openCommandPrefix} {self.protocol.getStructAbsolutePath()}\n')
        f.close()

        # Returning written file 
        return filePath