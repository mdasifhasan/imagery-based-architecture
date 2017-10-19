import sys

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
        # self.relations["left"] = None
        # self.relations["right"] = None
        # self.relations["above"] = None
        # self.relations["bottom"] = None
        self.obj_label = obj_label
        pass

class Image:
    def __init__(self):
        self.objects = {}
        pass

    def merge_image(self, image):
        for object in image.objects:
            if object in self.objects:
                s = image.objects[object]
                t = self.objects[object]
                if s.left == None and t.right == None:
                    t.right = s.right
                    s.left = t
                elif s.right == None and t.left == None:
                    t.left = s.left
                    s.left.right = t
                elif s.above == None and t.bottom == None:
                    t.bottom = s
                    s.above = t
                elif s.bottom == None and t.above == None:
                    t.above = s
                    s.bottom = t
        pass

class ShortTermMemory:
    def __init__(self):
        self.imagesByObj = {}
        print("Constructing ShortTermMemory")

    def addImage(self, image):
        # for obj in image.objects:
        #     if obj in self.imagesByObj:
        #         images_of_object = self.imagesByObj[obj]
        #         for image in images_of_object:
        #             image.merge_image(image)
        #         images_of_object.append(image)
        #     else:
        #         self.imagesByObj[obj] = [image]
        for obj_label in image.objects:
            if obj_label in self.imagesByObj:
                self.imagesByObj[obj_label].append(image)
            else:
                self.imagesByObj[obj_label] = [image]
    def printImages(self):
        pass

class ImageryArch:

    def __init__(self):
        print("Constructing imagery arch")
        self.stm = ShortTermMemory()

    def queryRelation(self, obj1, obj2, target_relation):

        print("\n\nQuerying relation", target_relation,"between", obj1, obj2)

        relations = []
        front = []
        explored = []
        images = self.stm.imagesByObj[obj2]
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
                print("#images of ", object.obj_label, len(images))
                for image in images:
                    if image in explored:
                        continue
                    explored.append(image)
                    self.extendFrontier(object.obj_label, image, front, target_relation)
        return False

    # find all the objects other than obj1 in the image that has a relation with obj1
    # and extend the front with these objects and their relations with obj1
    def extendFrontier(self, obj1_label, image, front, target_relation):
        print("extend front with obj:", obj1_label, len(front)), "for target_relation:", target_relation
        obj1 = image.objects[obj1_label]
        if target_relation in obj1.relations:
            if obj1.relations[target_relation] is not None:
                print("extending frontier with rel:" , target_relation , "-", obj1.relations[target_relation].obj_label)
                front.append(obj1.relations[target_relation])

        print("after extending the front: ", len(front))
        for object in front:
            print(obj1_label , target_relation , object.obj_label)

    def query(self, obj1, obj2):

        print("\n\nQuerying relation between", obj1, obj2)

        relations = {}
        if self.queryRelation(obj1, obj2, "above"):
            relations["above"] = True
        if self.queryRelation(obj1, obj2, "left"):
            relations["left"] = True
        if self.queryRelation(obj1, obj2, "right"):
            relations["right"] = True
        if self.queryRelation(obj1, obj2, "bottom"):
            relations["bottom"] = True

        print("Relation between", obj1, "and", obj2)
        if len(relations) == 0:
            print("I don't know.")
        else:
            for r in relations:
                print(r, "= true")

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
    imageArch = ImageryArch()

    imageArch.stm.addImage(create_input_image(Input("left", "fork", "plate")))
    imageArch.stm.addImage(create_input_image(Input("left", "plate", "knife")))

    imageArch.query("fork", "knife")

    print("\nTest 1 finished")


# The fork is to the left of the plate. The plate is above the napkin
def test2():
    imageArch = ImageryArch()

    imageArch.stm.addImage(create_input_image(Input("left", "fork", "plate")))
    imageArch.stm.addImage(create_input_image(Input("above", "plate", "napkin")))

    imageArch.query("fork", "napkin")
    print("\nTest 2 finished")

if __name__ == "__main__":
    test1()