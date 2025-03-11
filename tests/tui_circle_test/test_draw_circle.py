from tui.circle import FilledEllipse

def main():
	circle = FilledEllipse(20, 5, 9, 4, 128, 0, 255)
	circle.paint()
	with open(1, 'w') as out:
		circle.render(out)
		out.write("\n")

if __name__ == '__main__':
	main()