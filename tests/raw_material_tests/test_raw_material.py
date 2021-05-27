from EnGo.models import raw_material
from . import RawMaterialTest
from EnGo.models.raw_material import RawMaterial


class TestAdd(RawMaterialTest):

    def test_should_add_raw_material(self):
        raw_material = RawMaterial(
            material_name="Some Material"
        )
        raw_material.add()

        self.assertIn(raw_material, self.db.session)


class TestUpdate(RawMaterialTest):

    def test_should_update_raw_material(self):
        self.raw_material.material_name = "New Name"
        self.raw_material.update()
        self.db.session.rollback()

        self.assertEqual(self.raw_material.material_name, "New Name")


class TestDelete(RawMaterialTest):

    def test_should_delete_raw_material(self):
        self.raw_material.delete()

        self.assertNotIn(self.raw_material, self.db.session)


class TestGet(RawMaterialTest):

    def test_sould_return_raw_material_given_valid_id(self):
        raw_material = RawMaterial.get(self.raw_material.id)

        self.assertEqual(raw_material, self.raw_material)


class TestGetAll(RawMaterialTest):

    def test_should_return_all_raw_materials(self):
        raw_materials = RawMaterial.get_all()

        self.assertEqual(raw_materials, [self.raw_material])


class TestSearch(RawMaterialTest):

    def test_should_return_raw_material_given_valid_search_term(self):
        result = RawMaterial.search(self.raw_material.material_name)

        self.assertEqual(result, self.raw_material)


