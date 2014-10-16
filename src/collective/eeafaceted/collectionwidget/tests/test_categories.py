# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.eeafaceted.collectionwidget.testing import IntegrationTestCase
from plone import api


class TestCategories(IntegrationTestCase):
    """Test computation of collection categories"""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.folder = self.portal.folder

    def test_no_categories(self):
        from collective.eeafaceted.collectionwidget.categories import (
            CategoriesFromFolder
        )
        """There should be no categories
        when the folder does not hold any folders.
        """
        categories = CategoriesFromFolder(self.folder).values
        self.assertFalse(categories)

    def test_categories(self):
        from collective.eeafaceted.collectionwidget.categories import (
            CategoriesFromFolder
        )
        """There should be categories
        """
        api.content.create(
            id='category1',
            type='Folder',
            title='Category 1',
            container=self.folder
        )
        api.content.create(
            id='category2',
            type='Folder',
            title='Category 2',
            container=self.folder
        )
        categories = CategoriesFromFolder(self.folder).values
        self.assertEquals(len(categories), 2)
        self.assertTrue(('category1', 'Category 1') in categories)
        self.assertTrue(('category2', 'Category 2') in categories)

    def test_categories_only_from_folder(self):
        from collective.eeafaceted.collectionwidget.categories import (
            CategoriesFromFolder
        )
        """Only folders are categories
        """
        api.content.create(
            type='Folder',
            title='category1',
            container=self.folder
        )
        api.content.create(
            type='Folder',
            title='category2',
            container=self.folder
        )
        api.content.create(
            type='Document',
            title='not a category',
            container=self.folder
        )
        categories = CategoriesFromFolder(self.folder).values
        self.assertEquals(len(categories), 2)

    def test_categories_ordered(self):
        from collective.eeafaceted.collectionwidget.categories import (
            CategoriesFromFolder
        )
        """categories should be ordered as the folders in the dashboard
        """
        api.content.create(
            id='category1',
            type='Folder',
            title='Category 1',
            container=self.folder
        )
        api.content.create(
            id='category2',
            type='Folder',
            title='Category 2',
            container=self.folder
        )
        categories = CategoriesFromFolder(self.folder).values
        self.assertEquals(('category1', 'Category 1'), categories[0])
        self.assertEquals(('category2', 'Category 2'), categories[1])
        self.folder.moveObjectsUp(['category2'])
        categories = CategoriesFromFolder(self.folder).values
        self.assertEquals(('category2', 'Category 2'), categories[0])
        self.assertEquals(('category1', 'Category 1'), categories[1])

    def test_no_subCategorie(self):
        from collective.eeafaceted.collectionwidget.categories import (
            CategoriesFromFolder
        )
        """subfolders are not categories
        """
        category1 = api.content.create(
            type='Folder',
            title='category1',
            container=self.folder
        )
        api.content.create(
            type='Folder',
            title='category3',
            container=category1
        )
        api.content.create(
            type='Folder',
            title='category2',
            container=self.folder
        )
        categories = CategoriesFromFolder(self.folder).values
        self.assertEquals(len(categories), 2)