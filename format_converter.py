from argparse import ArgumentParser, Namespace
from os import listdir, path
from typing import Any, Callable, TextIO, Union
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree


def convert_to_abbreviated(filename: str, input_directory: str, output_directory: str, **kwargs):
    input_path: str = f"{input_directory}/{filename}"
    output_path: str = f"{output_directory}/{filename}"

    input_tree: ElementTree = ET.parse(input_path)
    output_root: Element = Element("doc")
    current_paragraph: Union[Element, None] = None
    for node in input_tree.iter():
        if node.tag == "para":
            new_paragraph_attrib: dict[str, str] = {"id": node.attrib["id"]}
            new_paragraph: Element = Element("para", attrib=new_paragraph_attrib)
            current_paragraph = new_paragraph
            output_root.append(new_paragraph)
        elif node.tag == "sent":
            if current_paragraph is None:
                raise ValueError("Sentence reached before paragraph.")
            else:
                new_sentence_attrib: dict[str, str] = {"id": node.attrib["id"], "type": node.attrib.get("type", " ")}
                new_sentence: Element = Element("sent", attrib=new_sentence_attrib)
                new_sentence.text = node.attrib["cont"]
                current_paragraph.append(new_sentence)
        else:
            pass

    output_tree: ElementTree = ElementTree(output_root)
    ET.indent(output_tree, space="\t", level=0)
    output_tree.write(output_path, encoding="utf-8", xml_declaration=True)

def convert_to_brat(filename: str, input_directory: str, output_directory: str, **kwargs):
    name, _ = filename.rsplit(".")
    input_path: str = f"{input_directory}/{filename}"
    output_path: str = f"{output_directory}/{name}.txt"
    log: TextIO = kwargs["log"]

    # Note that the numbers here have been set up to start at 1 rather than 0.

    input_tree: ElementTree = ET.parse(input_path)
    output_string: str = ""
    current_paragraph_number: Union[int, None] = None
    for node in input_tree.iter():
        if node.tag == "para":
            current_paragraph_number = int(node.attrib['id']) + 1
            output_string += f"<Paragraph {current_paragraph_number}>\n"
        elif node.tag == "sent":
            node_type: str = node.attrib.get("type", " ")
            if node_type == "InSentenceBIE":
                if log is not None:
                    sentence_id: int = int(node.attrib['id']) + 1
                    log.write(f"File {name}: Paragraph {current_paragraph_number}, Sentence {sentence_id}\n")
                output_string += ">>> "
            output_string += f"{node.attrib['cont']}\n"
        else:
            pass

    with open(output_path, encoding="utf-8", mode="w+") as output_file:
        output_file.write(output_string)


FORMATTING_FUNCTION_TABLE: dict[str, Callable[[str, str, str], None]] = {
    "abbreviated": convert_to_abbreviated,
    "brat": convert_to_brat
}

def get_formatting_function(formatting_function_name: str) -> Callable[[str, str, str], None]:
    try:
        chosen_formatting_function: Callable = FORMATTING_FUNCTION_TABLE[formatting_function_name]
    except KeyError:
        raise ValueError(f"The format <{formatting_function_name}> is not currently supported.")
    return chosen_formatting_function


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("input_directory")
    parser.add_argument("output_directory")
    parser.add_argument("--format", type=get_formatting_function, required=True)
    parser.add_argument("--log-file", type=str, default=None)
    args: Namespace = parser.parse_args()

    if path.isdir(args.input_directory) is False:
        raise ValueError(f"The input directory <{args.input_directory}> is not a valid directory.")
    elif path.isdir(args.output_directory) is False:
        raise ValueError(f"The output directory <{args.output_directory}> is not a valid directory.")

    if args.log_file is not None:
        log_path: str = f"{args.output_directory}/{args.log_file}.txt"
        log_file: Union[TextIO, None] = open(log_path, encoding="utf-8", mode="w+")
        log_file.write("# Paibi Sentence Locations\n")
        log_file.write("# File <Number>: Paragraph <Number>, Sentence <Number>\n")
    else:
        log_file = None
    formatting_kwargs: dict[str, Any] = {"log": log_file}

    files: list[str] = listdir(args.input_directory)
    for file in files:
        args.format(file, args.input_directory, args.output_directory, **formatting_kwargs)
