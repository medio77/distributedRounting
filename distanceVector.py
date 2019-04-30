import copy


class Router:

    def __init__(self, id, name, neighbors):
        self.id = id
        self.neighbors = neighbors
        self.name = name
        self.input_buffer = []
        self.vector = [{"id": id, "name": name, "distance": 0,
                        "interface": 0}]  # format is: (id,name,distance,interface)
        # interface 0 is self interface

    def put_in_buffer(self, item):
        self.input_buffer.append(item)

    def read_from_buffer(self):
        return self.input_buffer

    def remove_from_buffer(self):
        self.input_buffer = []


def show_result(router):
    print(router.name, router.vector)


def announce(announce_router, announce_routers):  # in this func routers announce their vector to their neighbors
    for neighbor_id in announce_router.neighbors:
        for neighbor_candidate in announce_routers:
            if neighbor_candidate.id == neighbor_id:
                neighbor_candidate.put_in_buffer(announce_router.vector)


def update_vector(routers_update):  # in this func routers update their distance vectors considering their input buffers
    for router in routers_update:
        for buffer_item in router.input_buffer:  # buffer is list of vectors...so..
            for buffer_vector in buffer_item:
                matching_item_list = []

                for vector_item in router.vector:
                    if buffer_vector['name'] == vector_item['name']:
                        matching_item_list.append(vector_item)

                if not matching_item_list:  # if there is a new vector item in input buffer
                    update_item = copy.deepcopy(buffer_vector)  # warning: buffer vector is corrupted after this
                    update_item['distance'] += 1
                    router.vector.append(update_item)

                else:  # if buffer item is not new in vector... so we must check if the buffer item is better or not:
                    for matching_item in matching_item_list:
                        if buffer_vector['distance'] + 1 < matching_item['distance']:
                            update_item = copy.deepcopy(buffer_vector)
                            update_item['distance'] += 1
                            router.vector.remove(matching_item)
                            router.vector.append(update_item)

    for router in routers:  # to clear all router's buffers after processing new vectors
        router.input_buffer = []


if __name__ == '__main__':

    routers = [Router(1, "A", [2, 3, 5, 6]),  # setting up routers... making topology here
               Router(2, "B", [1, 3]),
               Router(3, "C", [1, 2, 4]),
               Router(4, "D", [3, 7]),
               Router(5, "E", [1]),
               Router(6, "F", [1, 7]),
               Router(7, "G", [4, 6])]

    for i in range(10):  # repeating announcement and update for a while  so vectors become stabilized

        for router in routers:
            announce(router, routers)

        update_vector(routers)

    for router in routers:  # to show final vectors as result
        for vector_item in router.vector:
            print(router.name, "  ", vector_item['distance'], vector_item['name']),

