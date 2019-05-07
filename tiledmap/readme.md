
```shell
tilecut /Users/huangziwei/Desktop/vt.jpeg -wm -ul "113.37889344222961,22.935684880426955" -lv 17 -min 15
```

```shell
tilecut /Users/huangziwei/Desktop/lol_crop2.jpg -lv 6 -ul 4575,3840
```

```shell
tilecut /Users/huangziwei/china.png -lv 4 -max 6 -ul "67.5000000,55.77657301866757" -t 512 -wm
```

经纬度直投
```shell
tilecut /Users/huangziwei/Desktop/wmts.jpeg -lv 18 -ll -ul "113.38027954101562,22.93121337890625"
tilecut /Users/huangziwei/china_lnglat.png -lv 5 -ll -ul "67.5,56.25" -max 6
```

下载
```shell
downloadmap.py 4 5,11 7,14
downloadmap.py 5 3,22 7,28 -t
```