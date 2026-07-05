import os
import shutil


def delete_public(public_path: str = "./public") -> None:
    if os.path.exists(public_path):
        shutil.rmtree(public_path)


def copy_to_public(
    static_path: str = "./static", public_path: str = "./public"
) -> None:
    if not os.path.exists(public_path):
        os.mkdir(public_path)

    file_list = os.listdir(static_path)
    for file in file_list:
        file_path = os.path.join(static_path, file)
        if os.path.isfile(file_path):
            print(f" * {file_path} -> {public_path}")
            shutil.copy(file_path, public_path)
        else:  # when file is a directory
            new_public_path = os.path.join(public_path, file)
            copy_to_public(file_path, new_public_path)


def copy_to_public_v2(src: str = "./static", trg: str = "./public") -> None:
    shutil.copytree(src, trg)
