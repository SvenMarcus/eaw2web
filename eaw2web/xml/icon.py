from xml.etree.ElementTree import Element


def icon_name(child: Element):
    icon_name_tag = child.find("Icon_Name")

    if icon_name_tag is not None and icon_name_tag.text is not None:
        return (
            icon_name_tag.text.replace(".TGA", "").replace(".tga", "").upper().strip()
        )

    return ""
