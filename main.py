#   asteroids_main.py
#
#   A rewriting of my 2020-2021 python recreation of the arcade game Asteroids,
#   using better code practices and the experience I have gained over the past
#   2 and a half years since I made the original.
#
# 	I've never actually played the original game,
# 	so I have based this on YouTube videos and talking to people who have played it
#
# 	Game keys used are either Q for thrust, A for shoot and OP for rotation;
# 	or Up for Thrust, Space for shoot and Left and Right for Rotate.
# 	H for hyperspace jump.
#
# 	The program requires PyGame and Python 3
#
# 	Sound files all created by Torin Stephens
#
# 	Tested and developed under PyGame 2.1.2 and Python 3.8.5
#
#  	This program is free software: you can redistribute it and/or modify
#  	it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see  <https://www.gnu.org/licenses/>.

import pygame
import math
from collision import calculate_segment_intersect
import classes
import constants
