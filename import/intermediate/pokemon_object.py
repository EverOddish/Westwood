from lxml import etree

class PokemonObject():
    def __init__(self):
        self.xml_file = None
        self.tab = '\t'

    def make_tag_with_text(self, tag, text):
        element = etree.Element(tag)
        element.text = text
        return element

    def pretty_print(self, root):
        lines = etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True, standalone=False).decode("utf-8").split("\n")
        for i in range(len(lines)):
            line = lines[i]
            out_line = ""
            for j in range(0, len(line), 2):
                if line[j:j + 2] == '  ':
                    out_line += self.tab
                else:
                    out_line += line[j:]
                    break
            lines[i] = out_line
        return "\n".join(lines)

    def dump_to_file(self, root_element, xml_file):
        close = False
        if None == xml_file:
            xml_file = open(xml_file, 'w')
            close = True

        contents = self.pretty_print(root_element)

        xml_file.write(contents)

        if close:
            xml_file.close()
