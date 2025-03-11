from tui.circle import OutlineEllipse

def main():
	circle1 = OutlineEllipse(20, 5, 8, 4, 128, 0, 255)
	circle2 = OutlineEllipse(5, 8, 8, 4, 0, 255, 200)
	circle3 = OutlineEllipse(170, 10, 8, 4, 128, 0, 255)

	circle1.paint()
	circle2.paint()
	circle3.paint()
	with open(1, 'w') as out:
		circle1.render(out)
		circle2.render(out)
		circle3.render(out)
		out.write("\n")

if __name__ == '__main__':
	main()