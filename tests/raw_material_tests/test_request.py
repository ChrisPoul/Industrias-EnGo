from . import RawMaterialTest
from EnGo.models.raw_material import RawMaterial


class TestAdd(RawMaterialTest):

    def test_should_add_raw_material_given_valid_raw_material(self):
        raw_material = RawMaterial(
            material_name="Valid Material"
        )
        raw_material.request.add()

        self.assertIn(raw_material, self.db.session)