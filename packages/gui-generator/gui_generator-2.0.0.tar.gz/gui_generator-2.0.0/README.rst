==========================
GUIgenerator
==========================
The gui-generator module facilitates the creation of simple GUI applications and can be installed using the pip package manager (pip install gui-generator). I created it. To generate a GUI window, we only need to provide a function for the program to execute and, if it takes any parameters, specify their descriptions that will display next to the input fields. They have to be entered in the same order as the function's parameters. We can also provide an additional description that will display at the top of the window by adding the desc parameter. After the user enters the values and clicks "Confirm," the given function will execute. The value it returns is displayed in a new window.

The addInput() method creates a separate window at runtime for collecting additional input. It can take an argument with a description that will display next to the input field.

Usage
==========================

   .. code-block:: bash
   
	from gui_generator import *

	def Average(n):
		s = 0
		for x in range(n):
			s += int(g.addInput("Enter a value:"))
		return s / n

	g = GUIgenerator()
	g.create(Average, args=["How many numbers:"], desc="Calculate the average value.")