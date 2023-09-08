# -*- coding: utf-8 -*-

# from vk.contentstatistic import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone import api
from Missing import Missing

class IContentstatisticView(Interface):
    """Marker Interface for IContentstatisticView"""


@implementer(IContentstatisticView)
class ContentstatisticView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('contentstatistic_view.pt')

    def __call__(self):
        return self.index()

    def content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        content_types = portal_types.listContentTypes()
        return content_types

    def workflow_ids(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow_ids = portal_workflow.getWorkflowIds()
        return workflow_ids

    def workflow_states(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow_ids = portal_workflow.getWorkflowIds()
        all_states = []

        for workflow_id in workflow_ids:
            workflow = portal_workflow.getWorkflowById(workflow_id)
            if workflow is not None:
                states = workflow.states.objectIds()
                all_states = list(set(all_states)| set(states))
        return all_states

    def number_per_contenttype_and_state(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        columns = self.workflow_states()+ ["(no state)","sum",] # list
        rows = self.content_types() + ["sum"] # list
        dict = self.create_zero_dict(columns, rows)

        for content_type in self.content_types():
            for state in self.workflow_states():
                query = {
                    'portal_type': content_type,
                    'review_state': state,
                }
                state_results = portal_catalog(query)
                dict[content_type][state] = len(state_results)
                #print(dict)

            # count elements without review state
            query = {
                'portal_type': content_type,
            }
            results = portal_catalog(query)
            for result in results:
                if isinstance(result.review_state,Missing):
                    dict[content_type]["(no state)"] += 1

        self.fill_sums(dict)
        return rows, columns, dict, "Content Type \ Workflow State"


    def fill_sums(self,dict):
        # Zeilensummen
        for row_key in dict.keys():
            dict[row_key]["sum"] = 0
            for column_key in dict[row_key].keys():
                if column_key != "sum":
                    dict[row_key]["sum"] = dict[row_key]["sum"] + dict[row_key][column_key]
        # Spaltensummen
        column_keys = dict["sum"].keys() # zeile sum gibt es immer
        for column_key in column_keys:
            for row_key in dict.keys():
                if row_key != "sum":
                    dict["sum"][column_key] = dict["sum"][column_key] + dict[row_key][column_key]

    def create_zero_dict(self, columns, rows):
        dict = {}
        for row in rows:
            row_dict = {}
            for column in columns:
                row_dict[column] = 0
            dict[row]= row_dict
        return dict


    def number_per_contenttype_and_workflow(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        portal_catalog = api.portal.get_tool('portal_catalog')
        columns = self.workflow_ids()+ ("(no workflow)","sum",) # tuple
        rows = self.content_types() + ["sum"] # list
        dict = self.create_zero_dict(columns, rows)

        for content_type in self.content_types():
            # alle objekte dieses contenttypes
            query = {
                'portal_type': content_type,
            }
            results = portal_catalog(query)

            for result in results:
                obj = result.getObject()
                chain = portal_workflow.getChainFor(obj)
                # hat das Objekt überhaupt einen Workflow
                if len(chain) != 0:
                    workflow = portal_workflow.getChainFor(obj)[0]
                    dict[content_type][workflow] = dict[content_type][workflow] + 1
                else:
                    dict[content_type]["(no workflow)"] = dict[content_type]["(no workflow)"]+1
        self.fill_sums(dict)
        return rows, columns, dict, "Content Type \ Workflow"

