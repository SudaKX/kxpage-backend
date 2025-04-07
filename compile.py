
import os, sys

DIST = "./app/pbf/"

if __name__ == '__main__':
    proto_folder = "./proto" if len(sys.argv) < 2 else sys.argv[1]
    proto_folder = os.path.normpath(proto_folder)
    files = [os.path.join(proto_folder, name) for name in os.listdir(proto_folder)]
    runtime_dist = os.path.normpath(DIST)
    path_front, path_key = os.path.split(runtime_dist)
    for file in files:
        file = os.path.normpath(file)
        os.system(f"protoc {file} --python_out={path_front} --proto_path {path_key}={proto_folder}")

