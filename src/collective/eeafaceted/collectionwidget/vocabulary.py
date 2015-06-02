# encoding: utf-8

from Products.CMFPlone.utils import safe_unicode
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedNavigable
from collective.eeafaceted.collectionwidget.interfaces import ICollectionCategories
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from plone import api
from zope.component import getAdapter
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class CollectionVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context, query=None):
        self.context = context

        items = []
        for brain in self.brains:
            redirect_to = ''
            current_url = context.absolute_url()
            brain_folder_url = '/'.join(brain.getURL().split('/')[:-1])
            # if not in same folder and collection container is a faceted
            # we will redirect to this faceted to use criteria defined there
            if not brain_folder_url == current_url:
                collection = brain.getObject()
                collection_container = collection.aq_inner.aq_parent
                if IFacetedNavigable.providedBy(collection_container):
                    # find the collection-link widget
                    criteria = ICriteria(collection_container).criteria
                    for criterion in criteria:
                        if criterion.widget == CollectionWidget.widget_type:
                            redirect_to = "{0}#{1}={2}"
                            # add a 'no_default=1' for links of collections of the root
                            if not IFacetedNavigable.providedBy(collection_container.aq_inner.aq_parent):
                                redirect_to = "{0}?no_default=1#{1}={2}"
                            redirect_to = redirect_to.format(brain_folder_url,
                                                             criterion.__name__,
                                                             collection.UID())
                            break

            items.append(SimpleTerm(brain.UID,
                                    brain.UID,
                                    (safe_unicode(brain.Title), redirect_to)))
        return SimpleVocabulary(items)

    @property
    def brains(self):
        # find root
        root = self.context
        while IFacetedNavigable.providedBy(root.aq_inner.aq_parent):
            root = root.aq_inner.aq_parent
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            path=dict(query='/'.join(root.getPhysicalPath())),
            object_provides='plone.app.collection.interfaces.ICollection',
            sort_on='getObjPositionInParent'
        )
        return brains


CollectionVocabularyFactory = CollectionVocabulary()


class CollectionCategoryVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context, query=None):
        # find root
        root = context
        while IFacetedNavigable.providedBy(root.aq_inner.aq_parent):
            root = root.aq_inner.aq_parent
        adapter = getAdapter(root, ICollectionCategories)
        items = [SimpleTerm(key, key, value) for key, value in adapter.values]
        return SimpleVocabulary(items)


CollectionCategoryVocabularyFactory = CollectionCategoryVocabulary()
