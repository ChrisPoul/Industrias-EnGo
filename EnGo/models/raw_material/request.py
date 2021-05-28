

class RawMaterialRequest:

    def __init__(self, raw_material):
        self.raw_material = raw_material

    def add(self):
        error = self.raw_material.validation.validate()
        if not error:
            self.raw_material.add()

        return error