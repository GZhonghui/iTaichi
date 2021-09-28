import taichi as ti
import time

ti.init(arch=ti.gpu)

# move 1 width/height in 3 seconds
move_speed = 3.0

render_range = ti.Vector.field(2, dtype=ti.f32, shape=2)

n = 640
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(n, n))
pixels_u8 = ti.Vector.field(3, dtype=ti.u8, shape=(n, n))

@ti.kernel
def init():
    render_range[0] = (-2.25, 0.75)
    render_range[1] = (-1.5, 1.5)

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
        x_length = render_range[0][1] - render_range[0][0]
        y_length = render_range[1][1] - render_range[1][0]
        z = ti.Vector([0.0, 0.0], dt=ti.f32)
        c = ti.Vector([
            render_range[0][0] + i * x_length / n,
            render_range[1][0] + j * y_length / n], dt=ti.f32)
        iterations = 0
        while z.norm() < 20 and iterations < 100:
            z = complex_sqr(z) + c
            iterations += 1
        pixels[i, j] = color(1 - iterations / 100)

gui = ti.GUI("Mandelbrot Set", res=(n, n))

init()

def main():
    try:
        now_time = time.time()
        lst_time = time.time()

        while True:
            paint()
            gui.set_image(pixels)
            gui.show()

            now_time = time.time()
            del_time = now_time - lst_time
            lst_time = now_time

            x_length = render_range[0][1] - render_range[0][0]
            y_length = render_range[1][1] - render_range[1][0]

            x_mid = (render_range[0][1] + render_range[0][0]) * 0.5
            y_mid = (render_range[1][1] + render_range[1][0]) * 0.5

            for e in gui.get_events():
                if e.key == ti.GUI.WHEEL:
                    scale = e.delta[1] / 100
                    scale = scale if scale > 0 else -1 / scale
                    render_range[0][0] = x_mid - x_length * 0.5 * scale
                    render_range[0][1] = x_mid + x_length * 0.5 * scale
                    render_range[1][0] = y_mid - y_length * 0.5 * scale
                    render_range[1][1] = y_mid + y_length * 0.5 * scale
                    
            # ! get_events first!
            if gui.is_pressed('a'):
                render_range[0][0] -= x_length * del_time / move_speed
                render_range[0][1] -= x_length * del_time / move_speed
            if gui.is_pressed('d'):
                render_range[0][0] += x_length * del_time / move_speed
                render_range[0][1] += x_length * del_time / move_speed
            if gui.is_pressed('w'):
                render_range[1][0] += y_length * del_time / move_speed
                render_range[1][1] += y_length * del_time / move_speed
            if gui.is_pressed('s'):
                render_range[1][0] -= y_length * del_time / move_speed
                render_range[1][1] -= y_length * del_time / move_speed
            
    except RuntimeError:
        pass

if __name__=='__main__':
    main()