from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from office365.sharepoint.lists.list import List, ListItem

import pandas as pd
import tempfile


class ListItemError(TypeError):
    err_dict = {'item_creation': ['Item Creation Error',
                                 'Error found in item: {} \nItem Details {}'],
                'hdr_row': ['File Header Row Error',
                            'Error found in file header row. \nExpected\n   {} \nbut found\n   {}'],
                'no_data': ['Data Error',
                            'No readable data has been found in {}{}'],
                'data_types': ['Data Type Error',
                               'Expected data types {}\nError found in row {}'],
                'type_check': ['Data Type Validation Error',
                               'Unable to validate data types for Fields {}\nand Types {}'],
                'fld_ren_ne': ['Blob Error',
                               'Field rename: "{}" does not exist in {}'],
                'fld_ren_ae': ['Blob Error',
                               'Field rename: "{}" already exists in {}'],
                'fld_drop': ['Blob Error',
                             'Field delete: "{}" does not exist in {}']}

    def __init__(self, err_vars):
        """
Raise this when there's a list item error
        :param err_vars:
        """
        self.err_code = err_vars[0]
        self.error = ''
        self.message = ''
        self.description = ''
        self.long_desc = ''
        self.add_vars = []
        self.set_error(err_vars)

    def __str__(self):
        return '\n'.join(['TypeError:', self.error, self.message])

    def set_error(self, err_vars):
        if len(err_vars) > 0:
            if isinstance(err_vars[1], pd.DataFrame):
                self.description = err_vars[1].to_string()
            else:
                self.description = err_vars[1]
        if len(err_vars) > 1:
            if isinstance(err_vars[2], pd.DataFrame):
                self.long_desc = err_vars[2].to_string()
            else:
                self.long_desc = err_vars[2]

        err_vals = self.err_dict.get(self.err_code)
        if err_vals:
            self.error = err_vals[0]
            err_str = err_vals[1]
        else:
            self.error = 'Unkown Error'
            err_str = 'Error found with code: ' + self.err_code + ' params -\n 1.  {}\n 2.  {}'
        arg_str = ''
        if len(err_vars) > 3:
            for x in err_vars[3]:
                arg_str += '\n' + x + ': ' + err_vars[3][x]

        self.message = err_str.format(self.description, self.long_desc) + arg_str


def get_sp_list_item(context, sp_list_name, list_item_id):
    sp_list: List = context.web.lists.get_by_title(sp_list_name)
    list_item: ListItem = sp_list.get_item_by_id(list_item_id)
    context.load(list_item).execute_query()
    # print('mso_sharepoint.get_sp_list_item', list_item)
    return list_item


def update_sp_list_item(ctx, item, new_values: dict):
    for prop in new_values:
        item.set_property(prop, new_values[prop])
    item.update()
    ctx.execute_query()


def df_from_list(rows):
    row_dict = {}
    for row in rows:
        d = row.properties
        row_dict[d['ID']] = d
    return pd.DataFrame.from_dict(row_dict, orient='index')


def get_sp_list(context, sp_list_name, list_fields=None, caml_query='', list_limit=100):
    def list_to_df(list_items):
        row_dict = {}
        for item in list_items:
            d = item.properties
            row_dict[d['ID']] = d
        return pd.DataFrame.from_dict(row_dict, orient='index')

    sp_list = context.web.lists.get_by_title(sp_list_name)
    rows = sp_list.get_items(caml_query=caml_query)
    # context.load(rows)
    context.execute_query()
    df = list_to_df(rows)
    if df.shape[0] > 0 and list_fields:
        df = df[list_fields]
    # print('mso_sharepoint.get_sp_list', df.columns)
    return df


def get_sp_list_by_display_name(context, sp_list_name, list_fields, list_filter=None, list_limit=100):
    sp_list = context.web.lists.get_by_title(sp_list_name)
    context.load(sp_list)
    context.execute_query()

    # Get fields (columns) of the list
    fields = sp_list.fields
    context.load(fields)
    context.execute_query()
    # Map display names to internal names
    display_to_internal_names = {field.properties["InternalName"]: field.properties["Title"] for field in fields}

    if list_filter:
        rows = sp_list.items.filter(list_filter).top(list_limit)
    else:
        rows = sp_list.items.top(list_limit)
    context.load(rows)
    context.execute_query()
    df = df_from_list(rows)
    df.rename(columns=display_to_internal_names, inplace=True)
    if list_fields and df.shape[0] > 0:
        df = df[list_fields]
    # print('mso_sharepoint.get_sp_list', rows)
    return df


def df_from_sp_list(ctx, sp_list_name, list_fields, caml_query):
    if list_fields:
        file_list = get_sp_list(ctx, sp_list_name, list_fields.keys(), caml_query)
        file_list.rename(columns=list_fields, inplace=True)
    else:
        file_list = get_sp_list(ctx, sp_list_name, caml_query)

    return file_list


def download_attachment(ini, list_item, file_type=None, file_name=None):
    ctx = ini.ctx
    ctx.load(list_item)
    ctx.execute_query()

    # Load attachments
    attachments = list_item.attachment_files
    ctx.load(attachments)
    ctx.execute_query()

    output = []

    # Iterate through attachments and download the one with the specified extension
    for attachment in attachments:
        # ini.app_log.create_entry(['mso_sharepoint', 'download_attachment - checking file_type', file_type,
        #                           attachment.properties["FileName"]])
        if file_name:
            if attachment.properties["FileName"] == file_name:
                temp_file = tempfile.TemporaryFile()
                attachment.download(temp_file).execute_query()
                ini.app_log.create_entry(['mso_sharepoint', 'download_attachment - single', file_name])
                return temp_file
        elif attachment.properties["FileName"].endswith(file_type):
            temp_file = tempfile.TemporaryFile()
            attachment.download(temp_file).execute_query()
            output.append(temp_file)
            ini.app_log.create_entry(['mso_sharepoint', 'download_attachment - multiple', file_type, file_name])
    return output


def create_job(context, job_details):
    """
    :type context: ClientContext
    :type job_details: pd.Series
    """
    jobs_list = context.web.lists.get_by_title('Jobs')
    try:
        job_properties = {
            'Title': job_details.Title,
            'EndUser': job_details.EndUser,
            'Product': job_details.Product,
            'MatchType': job_details.MatchType,
            'Matches': int(job_details.Matches),
            'Royalty': float(job_details.Royalty),
            'ResellerNameId': int(job_details.ResellerNameId),
            'JobDate': job_details.JobDate,
            'Invoiced': bool(job_details.Invoiced),
            'PoRaised': bool(job_details.PoRaised)
        }
    except TypeError as e:
        raise ListItemError(['job_creation', job_details, e])
    if isinstance(job_details.Gross, int):
        job_properties['Gross'] = job_details.Gross
    if isinstance(job_details.JobRef, str):
        job_properties['JobRef'] = job_details.JobRef
    # print('mso_sharepoint.create_job', job_properties)
    return jobs_list.add_item(job_properties).execute_query()


class SpList:
    def __init__(self, ini, list_name, filter_str=None):
        self.name = list_name
        self.ctx = ini.ctx
        self.list_fields = ini.SpListFields.get(list_name)
        self.filter = CamlQuery.parse(filter_str)
        self.df = df_from_sp_list(self.ctx, self.name, self.list_fields, self.filter)

    def refresh(self):
        self.df = df_from_sp_list(self.ctx, self.name, self.list_fields, self.filter)
        return self.df

