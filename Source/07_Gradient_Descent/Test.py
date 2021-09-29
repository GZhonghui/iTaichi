import taichi as ti

ti.init(arch=ti.gpu)

x = ti.field(dtype=ti.f32, shape=(), needs_grad=True)
y = ti.field(dtype=ti.f32, shape=(), needs_grad=True)

@ti.kernel
def F():
    y[None] = x[None] + 1

@ti.kernel
def init():
    x[None] = 0
    y[None] = 0

def main():
    init()

    with ti.Tape(loss=y):
        F()
        print(x.grad[None])

if __name__=='__main__':
    main()