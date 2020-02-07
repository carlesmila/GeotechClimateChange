# Import arcpy module
import arcpy
import arcgisscripting
import os.path

# Set current workspace
arcpy.env.workspace = "N:\\gdmp\\Solar\\BOMNetCDFConversion\\python_test.gdb"
gp = arcgisscripting.create(9.3)
variable = "mean_exposure"
dimension = "month"
xdimension = "longitude"
ydimension = "latitude"
valueSelectionMethod = "BY_VALUE"
outLoc = "N:\\gdmp\\Solar\\BOMNetCDFConversion\\python_test.gdb"


# Create Python list of netCDF files in the folder using glob module
import glob
listNetCDF = glob.glob("E:\\SOLAR_DATA\\netcdf\\monthly_means_daily_ghe\\*.nc")

# Iterate through the Python list and print file name
for nc in listNetCDF:

        print "Processing: " + nc
        ncFP = gp.CreateObject("NetCDFFileProperties", nc)
        nc_Dims = nc_FP.getDimensions()

        # Iterate through each file to get the dimension size
        for ncDim in nc_Dims:
            
                ncDimSize = ncFP.GetDimensionSize(ncDim)

                for i in range(0, ncFP.GetDimensionSize(ncDim)):

                    if ncDim == "month":
                        
                        ncDimValue = ncFP.GetDimensionValue(ncDim, i)
                        nowFile = os.path.basename(nc)
                        
                        # Create names to be assigned to the output rasters based on the month, store in nowFileNew
                        if ncDimValue == 1:
                            
                            nowFileNew = nowFile[0:-8]+ "_jan"

                        elif ncDimValue == 2:

                            nowFileNew = nowFile[0:-8]+ "_feb"

                        elif ncDimValue == 3:

                            nowFileNew = nowFile[0:-8]+ "_mar"

                        elif ncDimValue == 4:

                            nowFileNew = nowFile[0:-8]+ "_apr"

                        elif ncDimValue == 5:

                            nowFileNew = nowFile[0:-8]+ "_may"

                        elif ncDimValue == 6:

                            nowFileNew = nowFile[0:-8]+ "_june"

                        elif ncDimValue == 7:

                            nowFileNew = nowFile[0:-8]+ "_july"

                        elif ncDimValue == 8:

                            nowFileNew = nowFile[0:-8]+ "_aug"

                        elif ncDimValue == 9:

                            nowFileNew = nowFile[0:-8]+ "_sept"

                        elif ncDimValue == 10:

                            nowFileNew = nowFile[0:-8]+ "_oct"

                        elif ncDimValue == 11:

                            nowFileNew = nowFile[0:-8]+ "_nov"

                        else:

                            nowFileNew = nowFile[0:-8]+ "_dec"

                            # Convert the netCDF files into individual raster layers
                            arcpy.MakeNetCDFRasterLayer_md(nc, variable, xdimension, ydimension, nowFileNew, "", ncDimValue, valueSelectionMethod)
                            
                            # Convert the raster layers into rasters
                            arcpy.CopyRaster_management(nowFileNew, outLoc + nowFileNew, "", "", "", "NONE", "NONE", "")

                            print ncDimValue, i
                            
            
        
        
        


