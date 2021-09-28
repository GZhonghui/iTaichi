import taichi as ti
import numpy as np
from math import pi

ti.init(arch=ti.gpu)

vertices = ti.Vector.field(3, dtype=ti.f32, shape=(8,))
indices = ti.Vector.field(3, dtype=ti.i32, shape=(12,))
rgb = ti.Vector.field(3, dtype=ti.f32, shape=(8,))

@ti.kernel
def fill_rgb():
    for i in vertices:
        rgb[i] = (vertices[i]) * 0.5

@ti.kernel
def move_cube(x: ti.f32, y: ti.f32, z: ti.f32):
    for i in vertices:
        vertices[i][0] += x
        vertices[i][1] += y
        vertices[i][2] += z

@ti.kernel
def rotate_y(angle: ti.f32):
    for i in vertices:
        new_location = ti.Vector([
            vertices[i][0] * ti.cos(angle) - vertices[i][2] * ti.sin(angle),
            vertices[i][1],
            vertices[i][2] * ti.cos(angle) + vertices[i][0] * ti.sin(angle)])
        vertices[i] = new_location

def create_cube():
    vertices[0]=(-1, -1, -1)
    vertices[1]=(-1, -1,  1)
    vertices[2]=( 1, -1, -1)
    vertices[3]=( 1, -1,  1)
    vertices[4]=(-1,  1, -1)
    vertices[5]=(-1,  1,  1)
    vertices[6]=( 1,  1, -1)
    vertices[7]=( 1,  1,  1)

    indices[ 0]=(0, 1, 2)
    indices[ 1]=(1, 2, 3)
    indices[ 2]=(4, 5, 6)
    indices[ 3]=(5, 6, 7)
    indices[ 4]=(0, 2, 4)
    indices[ 5]=(2, 4, 6)
    indices[ 6]=(1, 3, 5)
    indices[ 7]=(3, 5, 7)
    indices[ 8]=(0, 1, 4)
    indices[ 9]=(1, 4, 5)
    indices[10]=(2, 3, 6)
    indices[11]=(3, 6, 7)

    fill_rgb()

create_cube()

def main():
    for t in range(360):
        if t < 180:
            move_cube(0,  0.01, 0)
        else:
            move_cube(0, -0.01, 0)
        rotate_y(2 * pi / 360)

        if not t%4:
            mesh_writer = ti.PLYWriter(num_vertices=8, num_faces=12, face_type="tri")        
            
            np_vertices = vertices.to_numpy()
            np_indices = indices.to_numpy()
            np_rgb = rgb.to_numpy()

            mesh_writer.add_vertex_pos(np_vertices[:,0], np_vertices[:,1], np_vertices[:,2])
            mesh_writer.add_vertex_color(np_rgb[:,0], np_rgb[:,1], np_rgb[:,2])
            mesh_writer.add_faces(np_indices)

            mesh_writer.export_frame_ascii(t, "Cube.ply")

if __name__=='__main__':
    main()