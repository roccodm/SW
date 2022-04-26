N_fattori=5
i=1


while test $i -le $N_fattori
do
   gmt surface f$i.xyz -Gf$i.grd -I0.01 -R12/20/38/44
   gdalwarp -s_srs "EPSG:4326" -cutline path.shp -crop_to_cutline -of Gtiff -dstnodata 255 f$i.grd f$i.cut.grd -co COMPRESS=LZW -co TILED=YES --config GDAL_CACHEMAX 2048 -multi
   i=`expr $i + 1`
done

