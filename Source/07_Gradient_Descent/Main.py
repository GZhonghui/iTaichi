import taichi as ti
import matplotlib.pyplot as plt
import random

ti.init(arch=ti.gpu)

train_size = 100
epoch = 2

w = ti.field(dtype=ti.f32, shape=3)
x = ti.field(dtype=ti.f32, shape=train_size)
y = ti.field(dtype=ti.f32, shape=train_size)

solve_w = ti.field(dtype=ti.f32, shape=3, needs_grad=True)
loss = ti.field(dtype=ti.f32, shape=(), needs_grad=True)

@ti.func
def uniform(x, y):
    return x + ti.random() * (y - x)

@ti.func
def sqr(x):
    return x * x

@ti.func
def f(w, x):
    return w[0] * x * x + w[1] * x + w[2]

def pyf(w, x):
    return w[0] * x * x + w[1] * x + w[2]

@ti.kernel
def init():    
    w[0] = uniform(-1, 1)
    w[1] = uniform(-1, 1)
    w[2] = uniform(-3, 3)

    for i in range(ti.static(train_size)):
        x[i] = uniform(-1, 1)
        y[i] = f(w, x[i]) + uniform(-0.2, 0.2)

    for i in range(3):
        solve_w[i] = 0

@ti.kernel
def train(i: ti.i32):
    loss[None] = sqr(f(w, x[i]) - f(solve_w, x[i]))

@ti.kernel
def move(r: ti.f32):
    for i in solve_w:
        solve_w[i] -= solve_w.grad[i] * r

def main():
    init()

    plt.scatter(x.to_numpy(), y.to_numpy(), s=1)
    plt_x = [-1 + 0.1 * x for x in range(21)]
    plt_y = [pyf(solve_w, x) for x in plt_x]
    plt_data, = plt.plot(plt_x, plt_y)
    loss_text = plt.text(0, 0, 'loss')

    plt.ion()
    plt.show()

    frame_index = 0

    # Record Screen ~~
    # input()

    idx = [i for i in range(train_size)]
    for e in range(epoch):
        random.shuffle(idx)

        for i in idx:
            with ti.Tape(loss):
                train(i)
            
            move(0.1)

            plt_y = [pyf(solve_w, x) for x in plt_x]
            plt_data.set_ydata(plt_y)
            loss_text.set_text('loss = '+str(loss[None]))

            plt.draw()
            plt.pause(0.01)

            frame_index += 1
            # Save Image
            # if not frame_index%10:
                # plt.savefig('plt_'+str(frame_index)+'.png')

    plt.ioff()
    plt.show()

if __name__=='__main__':
    main()