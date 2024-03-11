# Codigo inspirado en la implementacin de GeekforGeeks
# https://www.geeksforgeeks.org/convex-hull-using-graham-scan/

from functools import cmp_to_key

# A class used to store the x and y coordinates of points
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __str__(self):
		return f'({self.x}, {self.y})'
	def __repr__(self):
		return f'({self.x}, {self.y})'

# A global point needed for sorting points with reference
# to the first point
p0 = Point(0, 0)

# A utility function to find next to top in a stack
def nextToTop(S):
	return S[-2]

# A utility function to return square of distance
# between p1 and p2
def distSq(p1, p2):
	return ((p1.x - p2.x) * (p1.x - p2.x) +
			(p1.y - p2.y) * (p1.y - p2.y))

# To find orientation of ordered triplet (p, q, r).
# The function returns following values
# 0 --> p, q and r are collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p, q, r):
	val = ((q.y - p.y) * (r.x - q.x) -
		(q.x - p.x) * (r.y - q.y))
	if val == 0:
		return 0 # collinear
	elif val > 0:
		return 1 # clock wise
	else:
		return 2 # counterclock wise

# A function used by cmp_to_key function to sort an array of
# points with respect to the first point
def compare(p1, p2):

	# Find orientation
	o = orientation(p0, p1, p2)
	if o == 0:
		if distSq(p0, p2) >= distSq(p0, p1):
			return -1
		else:
			return 1
	else:
		if o == 2:
			return -1
		else:
			return 1

# Prints convex hull of a set of n points.
def convexHull(points, n, layers=0):
	# if there are no points to form a convex hull
	if n == 0:
		return layers
	
	# if it's the last point
	if n == 1:
		print(f"Capa {layers+1}: {points[0]}")
		return layers+1

	# Find the bottommost point
	ymin = points[0].y
	min = 0
	for i in range(1, n):
		y = points[i].y

		# Pick the bottom-most or choose the left
		# most point in case of tie
		if ((y < ymin) or
			(ymin == y and points[i].x < points[min].x)):
			ymin = points[i].y
			min = i

	# Place the bottom-most point at first position
	points[0], points[min] = points[min], points[0]

	# Sort n-1 points with respect to the first point.
	# A point p1 comes before p2 in sorted output if p2
	# has larger polar angle (in counterclockwise
	# direction) than p1
	p0 = points[0]
	points = sorted(points[1:], key=cmp_to_key(compare))

	# Create an empty stack and push first three points
	# to it.
	S = []
	S.append(p0)
	S.append(points[0])

	# Process remaining n-2 points
	for i in range(1, n-1):
	
		# Keep removing top while the angle formed by
		# points next-to-top, top, and points[i] makes
		# a non-left turn
		while ((len(S) > 1) and
		(orientation(nextToTop(S), S[-1], points[i]) != 2)):
			S.pop()
		S.append(points[i])

	# Now stack has the output points,
	# print contents of stack
	print(f'Capa {layers+1}:', end=' ')
	print(S[0], end=' ')
	while len(S) > 1:
		p = S[-1]
		print(p, end=' ')
		# remove from list of points
		points.remove(p)
		S.pop()
	print()

	# count the remaining layers
	return convexHull(points, len(points), layers+1)

# Driver Code
input_points = [
	(0,9), 													        (9,9),
		    (1,8), 											  (8,8),
		    	   (2,7), 							   (7,7),
		    	   		  (3,6), 	    	   (6,6),
		    	   		  	     (4,5), (5,5),
		    	   		  	     (4,4), (5,4),
		    	   		  (3,3), 			   (6,3),
		    	   (2,2), 							 (7,2),
		    (1,1), 											 (8,1),
	(0,0), 														    (9,0)
]
points = []
for point in input_points:
	points.append(Point(point[0], point[1]))

n = len(points)
l = convexHull(points, n)
print(f'Numero de capas: {l}')