import taichi as ti

ti.init(arch=ti.gpu)

n = 640
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(n, n))
pixels_u8 = ti.Vector.field(3, dtype=ti.u8, shape=(n, n))

@ti.kernel
def convert_pixel():
    for i,j in pixels:
        for k in ti.static(range(3)):
            # OpenCV and Taichi are different
            pixels_u8[i,j][2-k]=ti.cast(pixels[j,i][k] * 255.999, ti.u8)

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])

@ti.func
def color(x):
    return ti.Vector([x, 1 - abs(x - 0.5), 1 - x])

@ti.kernel
def paint():
    for i, j in pixels:
        z = ti.Vector([0.0, 0.0], dt=ti.f32)
        c = ti.Vector([i / n - 0.75, j / n - 0.5], dt=ti.f32) * 3
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = color(1 - iterations * 0.02)

gui = ti.GUI("Mandelbrot Set", res=(n, n))

def main():
    try:
        while True:
            paint()
            gui.set_image(pixels)
            gui.show()
            
    except RuntimeError:
        pass

    try:
        import cv2 as cv
    except:
        pass
    else:
        convert_pixel()
        cv.imwrite('Mandelbrot Set.png', pixels_u8.to_numpy())

if __name__=='__main__':
    main()