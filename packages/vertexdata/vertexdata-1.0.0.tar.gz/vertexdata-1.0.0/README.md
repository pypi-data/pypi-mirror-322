# .obj to vertex data
[![pypi version](https://img.shields.io/pypi/v/vertexdata.svg)](https://pypi.org/project/vertexdata/)
[![python versions](https://img.shields.io/pypi/pyversions/vertexdata.svg)](https://pypi.org/project/vertexdata/)
[![python package passing](https://github.com/alternyxx/vertexdata/actions/workflows/python-package.yml/badge.svg)](https://github.com/alternyxx/vertexdata/actions)
<br>
<br>
![A spinning blahaj](https://static.alternyxx.com/gif/blahaj.gif)
The above spinning blahaj was rendered in a browser with typescript, see at
[alternyxx.com/blahaj](https://alternyxx.com/blahaj)! The model can be found
[here](https://sketchfab.com/3d-models/blahaj-ce981de49111488c81ea646067abe1ec).
## Intended Usage
The program aims to make .obj files with **triangle** data, for example,
```
v 1 0 0
v 0 1 0
v 0 0 1

vn 0.577 0.577 0.577

f 1//1 2//2 3//3
```
to
```
1, 0, 0, 0.5777, 0.5777, 0.5777,
0, 1, 0, 0.5777, 0.5777, 0.5777,
0, 0, 1, 0.5777, 0.5777, 0.5777,
```
This is for parsing obj files to be suitable to feed to a vertex buffer.
For most cases, it'd be better to just use an index buffer though.
If your .obj file has faces with quads, which is usually the case, eg.
```
f 1/1/1 2/1/1 3/1/1 4/1/1
```
Then, you could change your vertex buffer accordingly to have 4 vertex coordinates in the 
case the graphics api you're using **supports quads**. Else, there is 
[github.com/StefanJohnsen/TriangulateOBJ-App](https://github.com/StefanJohnsen/TriangulateOBJ-App) 
to triangulate quads in a .obj file which is what I did for the blahaj!
## Installation 
### pip 
Make sure Python and pip is installed. Python version needs to be >= 3.10. Then run
```
pip install vertexdata
```
### Build
In case pip is blocked (happens to me), you can simply clone the repository and build
from scratch. This should be especially trivial as the project has 0 dependancies.
```
git clone https://github.com/alternyxx/VertexData
cd VertexData
pip install .
```
## Command Line Usage
Once installed, you can run
```
vertexdata obj_file {target_file}
```
to get vertex data in the target_file. By default, the program will generate all given 
vertex data, positions, textures and normals *if given*. To override this, you can pass
in
```
vertexdata obj_file {target_file} -nvn -nvt
```
to only generate the positions of the vertices.
For more information, run 
```
vertexdata --help
```
## Library
If you want to parse the vertices in this way in a python project, you can
```python
import vertexdata as vtd

def main():
    vertex_parser = vtd.VertexParser(
        source, target_file, no_normal_data=true, no_texture_data=true
    )
    vertex_parser.parse()
    your_vertices_data = vertexparser.output()
```
source can be a file which then you can do 
```python
vertexparser = vtd.VertexParser(
    source, target_file, read_file=true
)
```
If you don't need to output target as a file then you can pass an empty string. And,
finally, there's the flags, no_normal_data and no_texture_data.