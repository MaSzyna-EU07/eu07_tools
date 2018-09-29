class SCNLight:
    def __init__(self, location, ambient, diffuse, specular):
        self._location = Vector3(location)
        self._ambient = ColorRGB(ambient)
        self._diffuse = ColorRGB(diffuse)
        self._specular = ColorRGB(specular)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = Vector3(location)

    @property
    def ambient(self):
        return self._ambient

    @ambient.setter
    def ambient(self, ambient):
        self._ambient = ColorRGB(ambient)

    @property
    def diffuse(self):
        return self._diffuse

    @diffuse.setter
    def diffuse(self, diffuse):
        self._diffuse = ColorRGB(diffuse)

    @property
    def specular(self):
        return self._specular

    @specular.setter
    def specular(self, specular):
        self._specular = ColorRGB(specular)