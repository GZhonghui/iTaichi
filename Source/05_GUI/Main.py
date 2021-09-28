import taichi as ti

ti.init(arch=ti.gpu)

def main():
    window = ti.ui.Window('Window Title', (640, 360))

if __name__=='__main__':
    main()