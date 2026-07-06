from copystatic import delete_public, copy_to_public
from generate_page import generate_page, generate_page_recursive
import sys


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]


    delete_public("./docs")
    copy_to_public(public_path="./docs")
    generate_page_recursive("./content", "./template.html", "./docs", basepath)
    

main()
