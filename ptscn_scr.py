import PhotoScan as ps
import os 
import math

dir = r'D:\ptscn\afs_input'
proj_dir = r'D:\ptscn\project'
las_dir = r'D:\ptscn\point_cloud'

doc = ps.app.document
chunk = doc.addChunk()
chunk.addPhotos([os.path.join(dir, file) for file in os.listdir(dir)])

def convert_wgs_to_utm(chunk):
    camera = chunk.cameras[10]
    lat = float(camera.photo.meta['Exif/GPSLatitude'])
    lon = float(camera.photo.meta['Exif/GPSLongitude'])
    utm_band = str((math.floor((lon + 180) / 6) % 60) + 1)
    utm_band = '0' + utm_band if len(utm_band) == 1 else utm_band
    epsg_code = 'EPSG::326' + utm_band if lat >= 0 else 'EPSG::327' + utm_band
    return epsg_code

chunk.matchPhotos(accuracy=ps.HighAccuracy, generic_preselection=True,reference_preselection=True)
chunk.alignCameras()
doc.save(os.path.join(proj_dir, 'proj2.psx'))
chunk.buildDepthMaps(quality=PhotoScan.MediumQuality, filter=PhotoScan.AggressiveFiltering)
doc.save(os.path.join(proj_dir, 'proj2.psx'))
chunk.buildDenseCloud()
doc.save(os.path.join(proj_dir, 'proj2.psx'))

proj = ps.CoordinateSystem(convert_wgs_to_utm(chunk))

chunk.dense_cloud.classifyGroundPoints()
chunk.exportPoints(path=os.path.join(las_dir, 'exp.laz'), format=ps.PointsFormat.PointsFormatLAZ, projection=proj,blockw=10000)
doc.save(os.path.join(proj_dir, 'proj2.psx'))
chunk = doc.chunk

chunk.buildDem()
chunk.exportDem(path=os.path.join(las_dir, 'dem.tif'),projection=proj,dx = 0.02, dy=0.02,blockw=25000,blockh=25000)

chunk.buildOrthomosaic(projection=proj,dx = 0.02, dy=0.02 )
chunk.exportOrthomosaic(path=os.path.join(las_dir, 'orto.tif'),projection=proj,blockw=25000,blockh=25000,tiff_compression=ps.TiffCompression.TiffCompressionLZW)
