from copystatic import delete_public, copy_to_public
from generate_page import generate_page, generate_page_recursive


def main():
    delete_public()
    copy_to_public()
    #generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_page_recursive("./content", "./template.html", "./public")
    

main()
