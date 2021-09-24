import taichi as ti

ti.init(arch=ti.gpu)

n = 320
pixels = ti.field(dtype=ti.f32, shape=(n * 2, n))

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])

@ti.kernel
def paint(t: ti.f32):
    for i, j in pixels:
        c = ti.Vector([1, 0.7885 * ti.exp(t)])
        z = ti.Vector([i / n - 1, j / n - 0.5]) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02

gui = ti.GUI("Julia Set", res=(n * 2, n))

def main():
    try:
        for i in range(1000000):
            paint(i * 0.03)
            gui.set_image(pixels)
            gui.show()
    except RuntimeError:
        pass

if __name__=='__main__':
    main()