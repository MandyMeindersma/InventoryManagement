import numpy as np

class Packer:
    def __init__(self):
        self.packing_options = []
        self.INFINITY = 1000000000000000
        self.MINIMUM  = 100000000000

    def find_packing(self, material, container, containers, containers_used):
        """ given some max material we can carry and a list of containers we can hold all that material width,
            this function will return the containers we need to ship to give us the fullest package,
            with the least ammount of containers.
            material - int (initially our max weight)
            container - the container we currently are trying to add (initially set to 0)
            containers - list of containers we want to package with
            containers_used - the containers we have used throughout this recursion (initially set to [])"""
        if material <= 0:
            return (self.INFINITY, [1]*100)
        if material <= container:
            return (material, containers_used)
        else:
            for container in containers:
                new_container = []
                new_container.extend(containers_used)
                new_container.append(container)
                self.packing_options.append(self.find_packing(material-container, container, containers, new_container))

            min_containers = self.MINIMUM

            # getting the indices with the least empty room
            values = [i[0] for i in self.packing_options]
            np_values = np.array(values)
            searchval = min(values)
            indexs = np.where(np_values == searchval)[0]

            #creating the object to send to shipping while choosing the least ammount of things to ship as well.
            for index in indexs:
                if len(self.packing_options[index][1]) <= min_containers:
                    min_containers = len(self.packing_options[index][1])
                    materials_that_work = self.packing_options[index]

            try:
                return materials_that_work
            except:
                return (0, [])

    def find_most_efficient_packing(self, material, container):
        self.packing_options = []
        return self.find_packing(material, 0, container, [])


# Testing purposes:
# packer = Packer()
# packed_tuple = packer.find_most_efficient_packing(1800, [300, 700])
# packed_tuple2 = packer.find_most_efficient_packing(1800, [700, 300])
# print(packed_tuple)
# print(packed_tuple2)
