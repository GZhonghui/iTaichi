import taichi as ti

ti.init(arch=ti.gpu)

n = 640
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(n, n))

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

def main():
    try:
        time_step = 0
        render_rate = 0.01
        while True:
            paint(time_step * render_rate)
            gui.set_image(pixels)
            gui.show()

            time_step += 1
            
    except RuntimeError:
        pass

if __name__=='__main__':
    main()