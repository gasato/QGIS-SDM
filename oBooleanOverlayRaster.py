# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************

Map Comparison Techniques. Normalization between 0-1 using ratio techniques
Based on Herzfeld, U.C. & Merriam, D.F.1990.

toDo:


"""

__author__ = 'Carlos Gabriel Asato'
__date__ = 'June 2019'

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsRasterBandStats,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterMultipleLayers, 
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination)
import processing
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry



class oBooleanOverlayRaster(QgsProcessingAlgorithm):
    """
   
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_LST = 'INPUT_LST'
    OUTPUT    = 'OUTPUT'
 
    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return oBooleanOverlayRaster()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'oBooleanOverlayRaster'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Raster Boolean Overlay')
        

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Overlay Analysis')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Overlay Analysis'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Raster Boolean Overlay. Input raster must be binarized (values [0,1])")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LST,
                self.tr('Input raster layers'),
                QgsProcessing.TypeRaster
            )
        )
        
   
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Boolean Overlay Map')
            )
        )


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        rasterInputLst = self.parameterAsLayerList(
            parameters,
            self.INPUT_LST,
            context
        )
        
        outputFile = self.parameterAsOutputLayer(
            parameters,
            self.OUTPUT,
            context
        )
        
        feedback.pushInfo('Output File: ' + outputFile)
        
        rasterInput = rasterInputLst[0]
        rExtent  = rasterInput.extent()    
        '''
        provider = rasterInput.dataProvider()
        stats    = provider.bandStatistics(1, QgsRasterBandStats.All, rExtent, 0)
        minVal   = stats.minimumValue
        maxVal   = stats.maximumValue
        '''
        rasterDict = {}
        cont = 1
        rEntriesLst = []
        
        for r in rasterInputLst:
            
            rName = 'raster' + str(cont) + '@1'
        
            rasterDict[rName]        = QgsRasterCalculatorEntry()
            rasterDict[rName].ref    = rName
            rasterDict[rName].raster = r
            
            rEntriesLst.append(rasterDict[rName])
        
            if cont != 1: fsum = fsum + ' + %s ' % rName
            else: fsum = rName

            cont += 1
                
        
        
        feedback.pushInfo('Formula: ' + str(fsum))
        calc = QgsRasterCalculator(fsum, outputFile, 'GTiff', rExtent, rasterInput.width(), rasterInput.height(), rEntriesLst)
        
        feedback.pushInfo("p calc1")
        calc.processCalculation()
        feedback.pushInfo("En of calxulation")

        

        return {self.OUTPUT: outputFile}
        
