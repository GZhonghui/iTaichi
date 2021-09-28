import taichi as ti
import cv2 as cv
from taichi.lang.ops import mod

ti.init(arch=ti.gpu)

n = 640
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(n, n))
pixels_u8 = ti.Vector.field(3, dtype=ti.u8, shape=(n, n))

@ti.kernel
def convert_pixel():
    for i,j in pixels:
        for k in ti.static(range(3)):
            pixels_u8[i,j][2-k]=ti.cast(pixels[i,j][k] * 255.999, ti.u8)

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])

@ti.func
def color(x):
    return ti.Vector([x, 1 - abs(x - 0.5), 1 - x])

@ti.kernel
def paint(t: ti.f32):
    for i, j in pixels:
        # Euler's formula: e^{i*x} = cos(x) + sin(x)*i
        # c = 0.7885 * e^{i*a}
        c = ti.Vector([ti.cos(t), ti.sin(t)]) * 0.7885
        z = ti.Vector([i / n - 0.5, j / n - 0.5]) * 3
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = color(1 - iterations * 0.02)

gui = ti.GUI("Julia Set", res=(n, n))

video_fps = 30
video_file_name = 'Encode.mp4'
video_encoder = cv.VideoWriter(video_file_name, \
    cv.VideoWriter_fourcc(*'mp4v'), \
    video_fps, (n, n))

def main():
    try:
        time_step = 0        
        save_rate = 3
        render_rate = 0.01
        while True:
            paint(time_step * render_rate)
            gui.set_image(pixels)
            gui.show()

            time_step += 1

            # Save Range
            if time_step * render_rate < 2 * 3.1415926:
                if not mod(time_step, save_rate):
                    convert_pixel()
                    video_encoder.write(pixels_u8.to_numpy())
            
    except RuntimeError:
        pass
    video_encoder.release()

if __name__=='__main__':
    main()