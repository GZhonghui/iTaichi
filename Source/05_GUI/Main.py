import taichi as ti

ti.init(arch=ti.gpu)

window = ti.ui.Window('GGUI', (360, 360))

def main():
    text_count = 1

    slider_value = 0
    color_value = (1, 1, 1)

    show_text = False
    show_win = False

    while window.running:
        window.GUI.begin('iTaichi', 0, 0, 1, 1)

        window.GUI.text('Hello Taichi GGUI ~~')
        window.GUI.text('')

        if window.GUI.button('Add'):
            text_count = min(text_count + 1, 5)
        if window.GUI.button('Delete'):
            text_count = max(text_count - 1, 1)
        if window.GUI.button('Reset'):
            text_count = 1

        for i in range(text_count):
            window.GUI.text('This is Text %d'%(i))

        window.GUI.text('')
        
        slider_value = window.GUI.slider_float('##Slider', slider_value, 0, 10)

        color_value = window.GUI.color_edit_3('##Color', color_value)
        
        window.GUI.text('')
        show_text = window.GUI.checkbox('Show Text', show_text)
        if show_text:
            window.GUI.text('Some Hidden Text')

        show_win = window.GUI.checkbox('Show Another Window', show_win)
        if show_win:
            window.GUI.begin('Sub Window', 0, 0.8, 1, 0.2)
            if window.GUI.button('Bye'):
                show_win = False
            window.GUI.end()

        window.GUI.end()
        window.show()

if __name__=='__main__':
    main()