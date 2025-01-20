# MIT License

# Copyright (c) 2022 CS Goh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from dataclasses import dataclass, field
from .painter import Painter
from .timeline import Timeline


@dataclass(kw_only=True)
class Marker:
    """A marker used to show the "Now" vertical line on the timeline"""

    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)
    line_colour: str = field(init=True, default=None)
    line_width: int = field(init=True, default=None)
    line_style: str = field(init=True, default=None)

    text: str = field(init=False, default="▼")
    label_x: int = field(init=False, default=0)
    label_y: int = field(init=False, default=0)
    label_width: int = field(init=False, default=0)
    label_height: int = field(init=False, default=0)
    line_from_x: int = field(init=False, default=0)
    line_from_y: int = field(init=False, default=0)
    line_to_x: int = field(init=False, default=0)
    line_to_y: int = field(init=False, default=0)
    not_in_timeline_range: bool = field(init=False, default=False)

    def set_label_draw_position(self, painter: Painter, timeline: Timeline) -> None:
        """Set marker label draw position

        Args:
            painter (Painter): Pillow wrapper class instance
            timeline (Timeline): Timeline instance
        """
        current_date = datetime.now()
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        label_pos_percentage = 0
        correct_timeline = False
        for timeline_item in timeline.timeline_items:
            if timeline_item.start <= current_date <= timeline_item.end:
                # calc label position
                (
                    correct_timeline,
                    label_pos_percentage,
                ) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode, current_date
                )
                if correct_timeline is True:
                    break

        self.not_in_timeline_range = not correct_timeline
        self.line_from_x = timeline_item.box_x + (
            timeline_item.box_width * label_pos_percentage
        )
        self.label_y = painter.next_y_pos + 8
        self.label_width, self.label_height = painter.get_text_dimension(
            self.text, self.font, self.font_size
        )
        self.label_x = self.line_from_x - (self.label_width / 2) + 1
        self.line_from_y = self.label_y + self.label_height + 4
        painter.next_y_pos = self.label_y + self.label_height

    def set_line_draw_position(self, painter: Painter) -> None:
        """Set marker line draw position

        Args:
            painter (Painter): Pillow wrapper class instance
        """
        self.line_to_x = self.line_from_x
        self.line_to_y = painter.next_y_pos + 10

    def draw(self, painter: Painter) -> None:
        """Draw marker

        Args:
            painter (Painter): Pillow wrapper class instance
        """
        if self.not_in_timeline_range is False:
            painter.draw_text(
                self.label_x,
                self.label_y + 5,
                self.text,
                self.font,
                self.font_size,
                self.font_colour,
            )

            painter.draw_line(
                self.line_from_x,
                self.line_from_y,
                self.line_to_x,
                self.line_to_y,
                self.line_colour,
                line_transparency=0.9,
                line_width=self.line_width,
                line_style=self.line_style,
            )
