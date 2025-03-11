#!/usr/bin/env python3

# To test this code, run
#     ln -s ../../scripts/tui
# first

from tui.circle import OutlineEllipse
from tui.screen import Screen

def main():
	screen  = Screen()
	circle1 = OutlineEllipse(20, 5, 9, 4, 128, 0, 255)
	circle2 = OutlineEllipse(8, 8, 9, 4, 0, 255, 200)
	circle3 = OutlineEllipse(150, 10, 9, 4, 128, 0, 255)

	screen.add_item(circle1)
	screen.add_item(circle2)
	screen.add_item(circle3)

	screen.paint()
	with open(1, 'w') as out:
		screen.render(out)
		out.write("\n")

if __name__ == '__main__':
	main()
