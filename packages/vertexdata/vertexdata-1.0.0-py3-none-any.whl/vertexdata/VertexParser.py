from sys import exit
from re import split

class Obj():
    """Handles Obj"""
    def __init__(self, source: str | list[str], file: bool=False) -> None:
        """
        Initialises the Obj Object.
        Args:
            source (str | list[str]): 
                if source is a string, will splitlines
                if source is a list[str], will trust that it is split by lines
                if neither, will raise ValueError
            [optional] file (bool):
                Specifies if source is instead a file path instead of the obj_data
                If true, will read the data from the file specified by source
                If false, will simply set source as the obj_data 
        """
        self.obj_data: list[str] = self.read_file(source) if file else source

    @property
    def obj_data(self) -> list[str]:
        """
        Return:
            The class's obj_data
        """
        return self._obj_data
    
    @obj_data.setter
    def obj_data(self, source: str | list[str]) -> None:
        """
        Sets valid obj_data.
        Args:
            source (str | list[str]): 
                if source is a string, will splitlines
                if source is a list[str], will trust that it is split by lines
                if neither, will raise ValueError
        """
        # surprisingly cant do match type(source)?
        if type(source) == str:
            self._obj_data: list[str] = source.splitlines(True)
        elif type(source) == list:
            self._obj_data: list[str] = source
        else:
            raise ValueError("VertexParser accepts str or list[str] as source")

    @staticmethod
    def read_file(source: str) -> list[str] | None:
        """
        Reads the obj_data from source
        Args:
            source (str): the file path
        """
        try:
            with open(source, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print("Given obj file doesn't exist")
            exit()


class Target():
    """Handles target"""
    def __init__(self, source: str, target: str, data: str) -> None:
        """
        Initialises the Target Object.
        Args:
            source (str): The initial obj_data or file path in which obj_data is
            target (str): File path in which data will be written
            data (str): The data to write
        """
        self.target: str = target if target else f"{source.removesuffix('.obj')}.vd.obj" if source.endswith(".obj") else ''
        self.data: str = data

    def write_file(self) -> None:
        """
        Writes the Data to Target.target if target is specified
        """
        if self.target:
            try:
                with open(self.target, 'w') as file:
                    file.write(self.data)
            except:
                print("Unable to write in target file")
                exit()
        else:
            print("Specify target output")
            exit()


class Vertex():
    """
    Vertex class for each vertex position in obj_data 
    Denoted by a line started with a v
    """
    def __init__(self, vertex: str) -> None:
        """
        Initialises a Vertex object.
        Sets the vertex as a list[str] where list has x,y,z
        """
        self.vertex: list[str] = vertex

    @property
    def vertex(self) -> list[str]:
        """
        Returns:
            vertex (list[str])
        """
        return self._vertex
    
    @vertex.setter
    def vertex(self, v: str) -> None:
        """
        Sets self.vertex by splitting by spaces and popping the v letter
        For example,
        "v  1 2 3" becomes ["1", "2", "3"]
        
        Args:
            v (str): The vertex line
        """
        self._vertex = v.split()
        self._vertex.pop(0)


class Texture():
    """
    Texture class for each vertex texture in obj_data 
    Denoted by a line started with a vt
    """
    def __init__(self, texture: str) -> None:
        """
        Initialises a Texture Object.
        Sets the texture as a list[str] where list has x,y
        """
        self.texture: list[str] = texture

    @property
    def texture(self) -> list[str]:
        """
        Returns:
            texture (list[str]): ie. ["1", "2"]
        """
        return self._texture
    
    @texture.setter
    def texture(self, vt: str) -> None:
        """
        Sets self.texture by splitting by spaces and popping the vt letter
        For example,
        "vt  1 2" becomes ["1", "2"]
        
        Args:
            vt (str): The vertex texture line
        """
        self._texture = vt.split()
        self._texture.pop(0)


class Normal():
    """
    Normal class for each vertex normal in obj_data 
    Denoted by a line started with a vn
    """
    def __init__(self, normal: str) -> None:
        """
        Initialises a Normal Object.
        Sets the normal as a list[str] where list has x,y,z
        """
        self.normal: list[str] = normal

    @property
    def normal(self) -> list[str]:
        """
        Returns:
            normal (list[str]): ie. ["1", "2", "3"]
        """
        return self._normal
    
    @normal.setter
    def normal(self, vn: str) -> None:
        """
        Sets self.normal by splitting by spaces and popping the vn letter
        For example,
        "vn  1 2 3" becomes ["1", "2", "3"]
        
        Args:
            vn (str): The vertex normal line
        """
        self._normal = vn.split()
        self._normal.pop(0)


class Face():
    """
    Face class for each face in obj_data
    Denoted by a line starting with f
    """
    def __init__(self, face: str, vertices: list[Vertex], normals: list[Normal], 
                 textures: list[Texture], no_normal_data: bool, no_texture_data: bool
    ) -> None:
        """
        Initialises a Face Object
        Args:
            face (str): a line starting with f
            vertices (list[Vertex]): a list of all Vertex Objects
            normals (list[Normal]): a list of all Normal Objects
            texture (list[Texture]): a list of all Texture Objects
            no_normal_data (bool): determines if Normal Objects should be ignored
            no_texture_data (bool): determines if Texture Objects should be ignored
        """
        self.face: list[str] = face
        self.vertices: list[Vertex] = vertices
        self.normals: list[Normal] = normals
        self.textures: list[Texture] = textures
        self.no_normal_data: bool = no_normal_data
        self.no_texture_data: bool = no_texture_data

    @property
    def face(self) -> list[str]:
        """
        Returns:
            face (list[str]): ie. ["1//1", "2//1", "3//1"]
        """
        return self._face
    
    @face.setter
    def face(self, f: str) -> None:
        """
        Sets self.face by splitting by spaces and popping the f letter
        For example,
        "f  1//1 2//1 3//1" becomes ["1//1", "2//1", "3//1"]
        
        Args:
            f (str): The face line
        """
        self._face: list[str] = f.split()
        self._face.pop(0)

    def construct(self) -> str:
        """
        Constructs a triangle from face

        Returns:
            triangle (str)
        """
        triangle: str = ""
        for data in self.face:
            info = split(r"\/\/?", data)
            vertex = normal = texture = ''
            match len(info):
                case 3:
                    vertex, texture, normal = info
                case 2:
                    vertex, normal = info
                case 1:
                    vertex = info[0]
            try:
                if vertex:
                    vertex = ", ".join(self.vertices[int(vertex) - 1].vertex) + ', '
                if texture and not self.no_texture_data:
                    texture = ", ".join(self.textures[int(texture) - 1].texture) + ', '  
                else:
                    texture = ''            
                if normal and not self.no_normal_data:
                    normal = ", ".join(self.normals[int(normal) - 1].normal) + ','
                else:
                    normal = ''
            except ValueError:
                print("Obj file contains non-integers as indexing vertex info :sob:")
                exit()
            else:
                triangle += vertex + texture + normal + '\n'
        return triangle


class VertexParser():
    """Handles parsing of an obj"""
    def __init__(self, source: str, target: str, no_normal_data: bool=False, 
                 no_texture_data: bool=False, read_file: bool=False) -> None:
        """
        Initialises a VertexParser Object

        Args:
            source (str): 
                The data of the obj or a file path to obj
                This is specified by read_file
            target (str):
                The file path to target
                Can be provided empty if you won't use output_file()
            no_normal_data (str): The flag for which if true won't parse normals
            no_texture_data (str): The flag for which if true won't parse textures
            read_file (str): Specifies if source is a file path or data of an obj
        """
        self.obj: Obj = Obj(source, read_file)
        self.target: Target = Target(source, target, '')
        self.vertices: list[Vertex] = []
        self.normals: list[Normal] = []
        self.textures: list[Texture] = []
        self.no_normal_data: bool = no_normal_data
        self.no_texture_data: bool = no_texture_data

    def parse(self) -> None:
        """
        Iterates through the lines and determines the starting letter
        Adds to a list[Object] for corresponding letter then constructs Triangles.
        """
        for line in self.obj.obj_data:
            if line[0] == 'v':
                match line[1]:
                    case ' ':
                        self.vertices.append(Vertex(line))
                    case 'n':
                        self.normals.append(Normal(line))
                    case 't':
                        self.textures.append(Texture(line))
                    case _:
                        print("what kind of vertex info do you have??")
                        exit()
            elif line[0] == 'f':
                face = Face(line, self.vertices, self.normals, self.textures, 
                            self.no_normal_data, self.no_texture_data).construct()
                self.target.data += face

    def output(self) -> str:
        """
        Returns:
            data (str): data of vertices information
        """
        return self.target.data
    
    def output_file(self) -> None:
        """
        Wrapper for Target Object's write_file xd
        """
        self.target.write_file()