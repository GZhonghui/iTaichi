# i[Taichi](https://taichi.graphics/)

## 01 Julia Set
> [Taichi] version 0.7.20, llvm 10.0.0, commit 284f75ed, win, python 3.7.9  
> Julia Set Animation, Colored. Ref: [Wikipedia](https://en.wikipedia.org/wiki/Julia_set)  
> C=0.7885\*Exp(i\*Time)
```
>> cd Source/01_Julia_Set
>> python Main.py
```
![Julia_Set](readMe/01_Julia_Set_01.gif)

## 02 Mandelbrot Set
> [Taichi] version 0.7.20, llvm 10.0.0, commit 284f75ed, win, python 3.7.9  
> Mandelbrot Set
```
>> cd Source/02_Mandelbrot_Set
>> python Main.py
```
![Mandelbrot_Set](readMe/02_Mandelbrot_Set_01.png)

## 03 Export Mesh
> [Taichi] version 0.7.20, llvm 10.0.0, commit 284f75ed, win, python 3.7.9  
> Export Mesh Sequence, then Import to 3rd Party Tools  
> The GIF is Rendered by **Blender** in this Sample
```
>> cd Source/03_Export_Mesh
>> python Main.py
It will generate ply files in the current folder
```
![Mesh_Sequence](readMe/03_Export_Mesh_01.gif)

## 04 Export Video
> [Taichi] version 0.7.20, llvm 10.0.0, commit 284f75ed, win, python 3.7.9  
> Encode Frames to Video, Relay on **opencv-python**
```
>> cd Source/04_Export_Video
>> python Main.py
Then you will get a mp4 file, you can convert it to GIF in Photoshop
```

## 05 GUI

## 06 Input
> [Taichi] version 0.7.20, llvm 10.0.0, commit 284f75ed, win, python 3.7.9  
> Handle Input Event via Taichi
```
>> cd Source/06_Input
>> python Main.py
```
![Input](readMe/06_Input_01.gif)

## 07 Gradient Descent
