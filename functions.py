#HelperFunctions.py
#Functions shared between many classes stored here
#Reduce code clutter

	objCollision(obj1, obj2)
		if math.sqrt(pow((obj1.collisionx) - obj2.collisionx, 2) + pow((obj1.collisiony) - obj2.collisiony, 2)) < obj1.range:
			return True
		else:
			return False