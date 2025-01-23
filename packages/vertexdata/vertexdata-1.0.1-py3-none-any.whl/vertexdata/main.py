from vertexdata import *

def main():
    args: cli.Args = cli.Args()
    v: VertexParser.VertexParser = VertexParser.VertexParser(
        args.args.obj_file, args.args.target_file, 
        args.args.no_normal_data, args.args.no_texture_data, True
    )
    v.parse()
    v.output_file()

if __name__ == "__main__":
    main()