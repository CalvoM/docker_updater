import argparse
import subprocess as subp
import shlex
from typing import List, Optional
import sys

class DockerImageUpdater:
    def __init__(self, prog_name: str):
        self.prog_name = prog_name

    def get_sys_images(self) -> Optional[List[str]]:
        cmd = "docker image ls"
        args = shlex.split(cmd)
        try:
            p = subp.Popen(args, stdout=subp.PIPE, stderr=subp.PIPE)
            out, err = p.communicate()
            return_msg = ""
            if out:
                return_msg = out.decode("utf-8")
            lines = [l for l in return_msg.split("\n") if len(l)]
            if len(lines) == 1:
                print("No docker images installed")
                return None
            images_lines = lines[1:]
            images = []
            for l in images_lines:
                words = [w for w in l.split(" ") if len(w)]
                images.append(words[0])
            return images
        except FileNotFoundError as e:
            if e.filename == "docker":
                print("docker is not installed")
        except Exception as e:
            print(e.__str__())
            print(sys.exc_info())
        return None

    def update_docker(self, args: argparse.Namespace):
        images = args.images
        sys_images = self.get_sys_images()
        if sys_images:
            using_sys_images: bool = False
            if len(images) == 1 and images[0] == "*":
                print("Updating all the images in the system")
                images = sys_images
                using_sys_images = True
            for i in images:
                if not using_sys_images:
                    if i not in sys_images:
                        print(f"{i} image not found on your system")
                        continue
                print(f"Updating {i}")
                cmd = f"docker pull {i}"
                cargs = shlex.split(cmd)
                p = subp.Popen(cargs)
                out,err = p.communicate()
                print(out, err)
            if(args.prune):
                cmd = "docker image prune"
                cargs = shlex.split(cmd)
                p = subp.Popen(cargs)
                out,err = p.communicate()

    def run(self):
        parser = argparse.ArgumentParser(prog=self.prog_name)
        parser.add_argument("--images", nargs="+", default=["*"])
        parser.add_argument("--prune", help="prune the dangling docker images", action="store_true")
        args = parser.parse_args()
        self.update_docker(args)
