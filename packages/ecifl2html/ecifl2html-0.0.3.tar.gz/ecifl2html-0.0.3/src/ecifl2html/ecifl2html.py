"""This module defines helper HTML functions."""

import re


class FormattedTextToHTML:
    """Class to convert formatted text to HTML."""

    def __init__(self, text: str):
        """
        Initialize the FormattedTextToHTML class with the provided text.

        :param str text: The formatted text to be converted.
        """
        self.text = text

    def __str__(self):
        return self.convert()

    def __call__(self):
        return self.convert()

    @staticmethod
    def _close_open_lists(html_lines, in_ordered_list, in_unordered_list):
        """
        Close any open ordered or unordered lists.

        :param html_lines: List of HTML lines to append closing tags to.
        :param in_ordered_list: Boolean flag indicating if an ordered list is open.
        :param in_unordered_list: Boolean flag indicating if an unordered list is open.
        :return: Updated html_lines, in_ordered_list, in_unordered_list
        """
        if in_ordered_list:
            html_lines.append("</ol>")
            in_ordered_list = False
        if in_unordered_list:
            html_lines.append("</ul>")
            in_unordered_list = False
        return html_lines, in_ordered_list, in_unordered_list

    def convert(self) -> str:
        """
        Convert the formatted text to HTML.

        :return: The converted HTML string.
        :rtype: str
        """
        lines = self.text.split("\n")  # Split the input text into lines
        html_lines: list[str] = []  # List to store the converted HTML lines
        in_ordered_list = False  # Flag to track if we are inside an ordered list
        in_unordered_list = False  # Flag to track if we are inside an unordered list
        in_code_block = False  # Flag to track if we are inside a code block

        for line in lines:
            if line.startswith("```"):
                # Toggle the code block flag
                (
                    html_lines,
                    in_ordered_list,
                    in_unordered_list,
                ) = self._close_open_lists(
                    html_lines, in_ordered_list, in_unordered_list
                )
                if in_code_block:
                    html_lines.append("</code></pre>")
                    in_code_block = False
                else:
                    html_lines.append("<pre><code>")
                    in_code_block = True
            elif in_code_block:
                # If inside a code block, add the line as is
                html_lines.append(line)
            else:
                # Match headers with the pattern 'h. ', 'hh. ', etc.
                header_match = re.match(r"^(h+)\. (.+)", line)
                if header_match:
                    header_level = len(
                        header_match.group(1)
                    )  # Determine the header level
                    content = header_match.group(2)  # Extract the content of the header
                    html_lines.append(f"<h{header_level}>{content}</h{header_level}>")
                elif line.startswith("p. "):
                    # Convert paragraphs with the pattern 'p. '
                    html_lines.append(f"<p>{line[3:]}</p>")
                elif line.startswith("i. "):
                    # Convert images with the pattern 'i. <path> => <caption>'
                    parts = line[3:].split(" => ", 1)
                    if len(parts) == 2:
                        path, caption = parts
                        html_lines.append(
                            f'<img src="{path}" alt="{caption}"><figcaption>{caption}</figcaption>'
                        )
                    else:
                        html_lines.append(
                            f'<img src="{parts[0]}" alt=""><figcaption></figcaption>'
                        )
                elif line.startswith("#. "):
                    # Convert ordered list items with the pattern '#. '
                    if not in_ordered_list:
                        html_lines.append("<ol>")
                        in_ordered_list = True
                    html_lines.append(f"<li>{line[3:]}</li>")
                elif line.startswith("-. "):
                    # Convert unordered list items with the pattern '-. '
                    if not in_unordered_list:
                        html_lines.append("<ul>")
                        in_unordered_list = True
                    html_lines.append(f"<li>{line[3:]}</li>")
                else:
                    # Close any open lists if the line does not match any pattern
                    (
                        html_lines,
                        in_ordered_list,
                        in_unordered_list,
                    ) = self._close_open_lists(
                        html_lines, in_ordered_list, in_unordered_list
                    )
                    html_lines.append(line)

        # Ensure any open lists are closed at the end
        if in_ordered_list:
            html_lines.append("</ol>")
        if in_unordered_list:
            html_lines.append("</ul>")
        if in_code_block:
            html_lines.append("</code></pre>")

        return "\n".join(html_lines)  # Join the HTML lines into a single string
