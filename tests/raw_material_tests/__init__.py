from tests import Test
from EnGo.models.raw_material import RawMaterial


class RawMaterialTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.raw_material = RawMaterial(
            material_name="Test Material"
        )
        self.raw_material.add()
