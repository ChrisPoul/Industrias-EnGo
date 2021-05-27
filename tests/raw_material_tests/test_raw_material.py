from . import RawMaterialTest
from EnGo.models.raw_material import RawMaterial


class TestAdd(RawMaterialTest):

    def test_should_add_raw_material(self):
        raw_material = RawMaterial(
            material="Material Name",
            price="10",
        )
        raw_material.add()

        self.assertIn(raw_material, self.db.session)


class TestUpdate(RawMaterialTest):

    def test_should_update_raw_material(self):
        self.raw_material.material = "New Material"
        self.raw_material.update()
        self.db.session.rollback()

        self.assertEqual(self.raw_material.material, "New Material")
