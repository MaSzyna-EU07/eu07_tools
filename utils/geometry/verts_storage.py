class VertexStorageSectored:
    def __init__(self):
        self._vertices_sectors = {}
        self.vertices = []
        self.num_verts = 0

    def push(self, vertex):
        sector = self.get_sector(vertex.location)

        self.vertices.append(vertex)

        vertex_index = self.num_verts
        sector[vertex_index] = vertex
        self.num_verts += 1

        return vertex_index

    def find(self, vertex):
        sector = self.get_sector(vertex.location)
        for vertex_index, vertex_candidate in sector.items():
            if vertex_candidate.location.compare_equality(vertex.location):
                return vertex_index

        raise KeyError(f"{vertex} not exists in given sector {sector}")

    def __getitem__(self, index):
        return self.vertices[index]

    def __iter__(self):
        return iter(self.vertices)

    def get_sector(self, vector):
        sector_key = tuple(round(v, ndigits=2) for v in vector)
        sector = self._vertices_sectors.get(sector_key)

        if not sector:
            sector = self._vertices_sectors[sector_key] = {}

        return sector