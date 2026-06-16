from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    split_nodes_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes_list.append(node)
        else:
            split_text = node.text.split(delimiter)
            # if there are correct amount of delimiters then the text will always be split into a list with length of increments of 3
            # the affected text will always be in every other index in the list 
            if len(split_text) < 3 or (len(split_text) > 3 and len(split_text) % 2 == 0):
                raise Exception("no delimiters or no closing delimiter in text")
            for i in range(len(split_text)):
                if i % 2 == 0: #means is not the affected text 
                    if split_text[i]: #if there is a text, not just empty index 
                        new_node = TextNode(split_text[i], TextType.TEXT)
                        split_nodes_list.append(new_node)
                else:
                    if split_text[i]:
                        new_node = TextNode(split_text[i], text_type)
                        split_nodes_list.append(new_node)
                    else:
                        raise Exception("no text between delimiters")
    return split_nodes_list


