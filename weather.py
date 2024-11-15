import matplotlib.pyplot as plt

def basicPlot():
  # Sample data
  x = [1, 2, 3, 4, 5]
  y = [10, 20, 25, 30, 35]

  # Create the plot
  plt.plot(x, y, marker='o')

  # Add titles and labels
  plt.title('Simple Line Plot')
  plt.xlabel('X-axis Label')
  plt.ylabel('Y-axis Label')

  # Show the plot
  plt.show()

def barPlot():
  # Sample data
  categories = ['A', 'B', 'C', 'D', 'E']
  values = [5, 7, 3, 8, 6]

  # Create the bar chart
  plt.bar(categories, values)

  # Add titles and labels
  plt.title('Simple Bar Chart')
  plt.xlabel('Categories')
  plt.ylabel('Values')

  # Show the plot
  plt.show()

option = 0
while option != 3:
    option = int(input('Input a number:'))
    if option == 1:
      basicPlot()
    elif option == 2:
      barPlot()
    elif option == 3:
      break
    else:
      print('Invalid!')