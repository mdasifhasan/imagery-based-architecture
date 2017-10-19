import sys

DEBUG = False # True

class Input:
    def __init__(self, relation, obj1, obj2):
        self.relation = relation
        self.obj1 = obj1
        self.obj2 = obj2
        self.objects = [obj1, obj2]

    def __str__(self):
        return self.obj1 + ", " + self.relation + ", " + str(self.obj2)

class Object:
    def __init__(self, obj_label):
        self.relations = {}
        self.obj_label = obj_label
        pass

class Image:
    def __init__(self):
        self.objects = {}
        pass

class ShortTermMemory:
    def __init__(self):
        self.imagesByObj = {}
        print("Constructing ShortTermMemory")

    def addImage(self, image):
        for obj_label in image.objects:
            if obj_label in self.imagesByObj:
                self.imagesByObj[obj_label].append(image)
            else:
                self.imagesByObj[obj_label] = [image]
    def printImages(self):
        pass

# This is the root class that supports imagery based spatial relathionship reasoning
# To construct an instance of this class a set of spatial relationships must be provided
# It uses a short term memory to that memorizes the images and helps querying
class ImageryArch:

    def __init__(self, target_relations):
        print("Constructing imagery arch")
        self.stm = ShortTermMemory()
        self.target_relations = target_relations

    # queries whether a particular relation holds between two objects
    # a relation between two objects holds true if and only if there is a path between the two
    # objects with each link being the target relation
    def queryRelation(self, obj1, obj2, target_relation):
        if DEBUG:
            print("\n\nQuerying relation", target_relation,"between", obj1, obj2)

        relations = []
        front = []
        explored = []
        images = self.stm.imagesByObj[obj2]
        if DEBUG:
            print("#images of ", obj2, len(images))
        for image in images:
            if image in explored:
                continue
            explored.append(image)
            self.extendFrontier(obj2, image, front, target_relation)

        while len(front) > 0:
            object = front.pop()
            if object.obj_label == obj1:
                return True
            else:
                images = self.stm.imagesByObj[object.obj_label]
                if DEBUG:
                    print("#images of ", object.obj_label, len(images))
                for image in images:
                    if image in explored:
                        continue
                    explored.append(image)
                    self.extendFrontier(object.obj_label, image, front, target_relation)
        return False

    # find all the objects other than obj1 in the image that are realated with obj1
    # with the target relation and extend the frontier with those objects
    def extendFrontier(self, obj1_label, image, front, target_relation):
        if DEBUG:
            print("extend front with obj:", obj1_label, len(front)), "for target_relation:", target_relation
        obj1 = image.objects[obj1_label]
        if target_relation in obj1.relations:
            if obj1.relations[target_relation] is not None:
                if DEBUG:
                    print("extending frontier with rel:" , target_relation , "-", obj1.relations[target_relation].obj_label)
                front.append(obj1.relations[target_relation])
        if DEBUG:
            print("after extending the front: ", len(front))
            for object in front:
                print(obj1_label , target_relation , object.obj_label)

    # queries what relations hold between obj1 and obj2
    def query(self, obj1, obj2):

        print("\n\nQuerying relation between", obj1, obj2)

        relations = {}
        for r in self.target_relations:
            if self.queryRelation(obj1, obj2, r):
                relations[r] = True

        print("Relation between", obj1, "and", obj2)
        if len(relations) == 0:
            print("I don't know.")
        else:
            for r in relations:
                print(r, "= true")

# This is implementation specific functionality
# It convevrts the inputs to images of objects and set their
# corresponding spatial relationships.
def create_input_image(input):
    obj1 = Object(input.obj1)
    obj2 = Object(input.obj2)
    image = Image()
    image.objects[input.obj1] = obj1
    image.objects[input.obj2] = obj2

    if input.relation == "left":
        obj1.relations["right"] = obj2
        obj2.relations["left"] = obj1
    elif input.relation == "right":
        obj1.relations["left"] = obj2
        obj2.relations["right"]= obj1
    elif input.relation == "above":
        obj1.relations["bottom"] = obj2
        obj2.relations["above"] = obj1
    elif input.relation == "bottom":
        obj1.relations["above"] = obj2
        obj2.relations["bottom"] = obj1


    print("\ncreated obj:", input.obj1)
    for r in obj1.relations:
        # if obj1.relations[r] is not None:
        print("rel:" + r + "-", obj1.relations[r].obj_label)

    print("\ncreated obj:", input.obj2)
    for r in obj2.relations:
        # if obj1.relations[r] is not None:
        print("rel:" + r + "-", obj2.relations[r].obj_label)

    return image

# The fork is to the left of the plate. The plate is to the left of the knife.
def test1():
    imageArch = ImageryArch(["left", "right", "above", "bottom"])

    imageArch.stm.addImage(create_input_image(Input("left", "fork", "plate")))
    imageArch.stm.addImage(create_input_image(Input("left", "plate", "knife")))

    imageArch.query("fork", "knife")

    print("\nTest 1 finished")


# The fork is to the left of the plate. The plate is above the napkin
def test2():
    imageArch = ImageryArch(["left", "right", "above", "bottom"])

    imageArch.stm.addImage(create_input_image(Input("left", "fork", "plate")))
    imageArch.stm.addImage(create_input_image(Input("above", "plate", "napkin")))

    imageArch.query("fork", "napkin")
    print("\nTest 2 finished")


# The fork is to the left of the plate. The spoon is to the left of the plate.
def test3():
    imageArch = ImageryArch(["left", "right", "above", "bottom"])

    imageArch.stm.addImage(create_input_image(Input("left", "fork", "plate")))
    imageArch.stm.addImage(create_input_image(Input("left", "spoon", "plate")))

    imageArch.query("fork", "spoon")
    print("\nTest 3 finished")



# The fork is to the left of the plate. The spoon is to the left of the fork. The knife is to the left
# of the spoon. The pizza is to the left of the knife. The cat is to the left of the pizza.
def test4():
    imageArch = ImageryArch(["left", "right", "above", "bottom"])

    imageArch.stm.addImage(create_input_image(Input("left", "fork", "plate")))
    imageArch.stm.addImage(create_input_image(Input("left", "spoon", "fork")))
    imageArch.stm.addImage(create_input_image(Input("left", "knife", "spoon")))
    imageArch.stm.addImage(create_input_image(Input("left", "pizza", "knife")))
    imageArch.stm.addImage(create_input_image(Input("left", "cat", "pizza")))

    imageArch.query("plate", "cat")
    print("\nTest 4 finished")



# The plate is to the right of the fork. The knife is to the right of the plate.
def test5():
    imageArch = ImageryArch(["left", "right", "above", "bottom"])

    imageArch.stm.addImage(create_input_image(Input("right", "plate", "fork")))
    imageArch.stm.addImage(create_input_image(Input("right", "knife", "plate")))

    imageArch.query("fork", "knife")
    print("\nTest 5 finished")


# The plate is to the right of the fork. The knife is to the right of the plate. The pizza is to the left of the fork
def test6():
    imageArch = ImageryArch(["left", "right", "above", "bottom"])

    imageArch.stm.addImage(create_input_image(Input("right", "plate", "fork")))
    imageArch.stm.addImage(create_input_image(Input("right", "knife", "plate")))
    imageArch.stm.addImage(create_input_image(Input("left", "pizza", "fork")))

    imageArch.query("pizza", "knife")
    print("\nTest 6 finished")



if __name__ == "__main__":
    if len(sys.argv)> 1:
        if sys.argv[1] == "1":
            test1()
        elif sys.argv[1] == "2":
            test2()
        elif sys.argv[1] == "3":
            test3()
        elif sys.argv[1] == "4":
            test4()
        elif sys.argv[1] == "5":
            test5()
        elif sys.argv[1] == "6":
            test6()
        else:
            test6()
    else:
        test6()