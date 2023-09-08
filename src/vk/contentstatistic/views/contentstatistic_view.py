# -*- coding: utf-8 -*-

# from vk.contentstatistic import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone import api



# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IContentstatisticView(Interface):
    """Marker Interface for IContentstatisticView"""


@implementer(IContentstatisticView)
class ContentstatisticView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('contentstatistic_view.pt')

    def __call__(self):
        self.table_test()
        return self.index()

    def content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        types = portal_types.listContentTypes()
        return types

    def workflow_ids(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow_ids = portal_workflow.getWorkflowIds()
        return workflow_ids

    def workflow_states_orig(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow_ids = portal_workflow.getWorkflowIds()
        all_states = {}

        for workflow_id in workflow_ids:
            workflow = portal_workflow.getWorkflowById(workflow_id)
            if workflow is not None:
                states = workflow.states.objectIds()
                all_states[workflow_id] = states
        return all_states

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
        result_dict = {}
        for type in self.content_types():
            type_dict = {}
            for state in self.workflow_states():
                query = {
                    'portal_type': type,
                    'review_state': state,
                }
                state_results = portal_catalog(query)
                type_dict[state] = len(state_results)
            result_dict[type] = type_dict
        return result_dict

    def number_per_contenttype_and_workflow(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        portal_catalog = api.portal.get_tool('portal_catalog')
        result_dict = {}
        for type in self.content_types():
            type_dict = {}
            # alle objekte dieses contenttypes
            query = {
                'portal_type': type,
            }
            results = portal_catalog(query)
            for workflow in self.workflows():
                type_dict[workflow] = 0
            for result in results:

                obj = result.getObject()
                chain = portal_workflow.getChainFor(obj)
                if len(chain) == 0:
                    workflow = None
                else:
                    workflow = portal_workflow.getChainFor(obj)[0]
                if workflow in type_dict.keys():
                    type_dict[workflow] = type_dict[workflow] + 1
                else:
                    type_dict[workflow] = 1
            #print(type_dict)
            result_dict[type] = type_dict
        #print(result_dict)
        return result_dict


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
            print(column_key)
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

        for type in self.content_types():
            # alle objekte dieses contenttypes
            query = {
                'portal_type': type,
            }
            results = portal_catalog(query)

            for result in results:
                obj = result.getObject()
                chain = portal_workflow.getChainFor(obj)
                # hat das Objekt überhaupt einen Workflow
                if len(chain) != 0:
                    workflow = portal_workflow.getChainFor(obj)[0]
                    dict[type][workflow] = dict[type][workflow] + 1
                else:
                    dict[type]["(no workflow)"] = dict[type]["(no workflow)"]+1
        self.fill_sums(dict)
        return rows, columns, dict


    def number_per_contenttype(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        result_dict = {}
        for type in self.content_types():
            query = {
                'portal_type': type,
            }
            results = portal_catalog(query)
            result_dict[type] = len(results)
        return result_dict

    def number_per_workflow(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        result_dict = {}
        for state in self.workflow_states():
            query = {
                'review_state': state,
            }
            results = portal_catalog(query)
            result_dict[state] = len(results)
        return result_dict

    def number_of_contents(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        query = {}
        results = portal_catalog(query)
        return len(results)


    def wftest(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_workflow = api.portal.get_tool('portal_workflow')
        query = {
            'portal_type': 'Document',
        }
        results = portal_catalog(query)
        for result in results:
            print(portal_workflow.getChainFor(result.getObject()))
        types = self.content_types()
        for type in types:
            print(type,":",portal_workflow.getChainFor(type))
        print(portal_workflow.getDefaultChain())

    def workflows(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow_ids = portal_workflow.getWorkflowIds()
        return workflow_ids


    def table(self):
        columns = ['B','A','C','D']
        rows = ['1','2','3']
        dict = {}
        for row in rows:
            row_dict = {}
            for column in columns:
                row_dict[column] = 0
            dict[row]= row_dict
        print(dict)
        return rows, columns, dict

    def table_test(self):
        print(self.table)

