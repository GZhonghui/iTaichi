import taichi as ti

ti.init(arch=ti.gpu)

K = 5

true_k = ti.field(dtype=ti.f32, shape=K)
solve_k = ti.field(dtype=ti.f32, shape=K, needs_grad=True)

train_x = ti.field(dtype=ti.f32, shape=(100,K))
train_y = ti.field(dtype=ti.f32, shape=100)

L = ti.field(dtype=ti.f32, shape=(), needs_grad=True)

@ti.func
def Fun(i):
    sum = 0.0
    for j in range(ti.static(K)):
        sum += train_x[i,j] * true_k[j]
    return sum

@ti.func
def Fun_Solve(i):
    sum = 0.0
    for j in range(ti.static(K)):
        sum += train_x[i,j] * solve_k[j]
    return sum

@ti.kernel
def init():
    for i in true_k:
        true_k[i] = ti.random()
    for i in solve_k:
        solve_k[i] = 0

    for i,j in train_x:
        train_x[i,j] = ti.random()
    for i in train_y:
        train_y[i] = Fun(i)

@ti.kernel
def train(i: ti.i32):
    L[None] = train_y[i] - Fun_Solve(i)

def main():
    init()

    for i in range(100):
        with ti.Tape(loss=L):
            train(i)

if __name__=='__main__':
    main()