# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
class DocumentFolder(models.Model):
    _description = 'Document folder'
    _inherit = 'documents.folder' 
    admin_group_ids = fields.Many2many('res.groups',  'documents_folder_admin_groups',string="Groupe d'écriture")
    project_name=fields.Char('Nom du projet')
    country_name=fields.Char('Nom du pays')
    @api.onchange('parent_folder_id')
    def inherit_groups_write(self):
        if self.parent_folder_id:
            id_temp=self.parent_folder_id.id
            parent_folder=self.env['documents.folder'].search([('id','=',id_temp)],limit=1)
            if parent_folder.group_ids:
                for id in [group.id for group in  parent_folder.group_ids ]:
                    self.write({'group_ids':[(4,id)]})
    @api.onchange('parent_folder_id')
    def inherit_groups_read(self):
        if self.parent_folder_id:
            id_temp=self.parent_folder_id.id
            parent_folder=self.env['documents.folder'].search([('id','=',id_temp)],limit=1)
            if parent_folder.read_group_ids:
                for id in [group.id for group in  parent_folder.read_group_ids ]:
                    self.write({'read_group_ids':[(4,id)]})
    group_ids=fields.Many2many('res.groups', onchange=inherit_groups_write)
    read_group_ids=fields.Many2many('res.groups', onchange=inherit_groups_read)
    active=fields.Boolean('Active', default=True)
    def custom_groups(self):
        folders=self.env['documents.folder'].search([])
        for folder in folders:
            if folder.parent_folder_id:
                parent_folder_id=folder.parent_folder_id.id
                #raise UserError(_(folder.group_ids))
                parent_folder=self.env['documents.folder'].search([('id','=',parent_folder_id)])
     
                if folder.read_group_ids:
                    for id in [group.id for group in  folder.read_group_ids ]:
                        parent_folder.write({'read_group_ids':[(4,id)]})
                if folder.group_ids:
                    for id in [group.id for group in  folder.group_ids ]:
                        parent_folder.write({'read_group_ids':[(4,id)]})
        return()
    def view_inherit_workspace(self):
        form_view = self.env.ref('custom_documents.inherit_workspace_form_view')
        self.ensure_one()
        return {'name': _('Merci de saisir le nom du projet :'),
                'type': 'ir.actions.act_window',
                'res_model': 'documents.folder',
                'view_mode': 'form',
                'view_id': form_view.id,
                'res_id': self.id,
                'target': 'new'}
    def inherit_workspace(self):
        main_workspace_id=self.env['documents.folder'].search([('id','=',self.id)])
        document_folder=self.env['documents.folder']
        all_subfolders_00=self.env['documents.folder'].search([('parent_folder_id','=',main_workspace_id.id)])
        document_parent_0=document_folder.create({'name':self.project_name,'sequence':main_workspace_id.sequence+1,'parent_folder_id':main_workspace_id.id})
        document_parent_00=all_subfolders_00[0]
        all_subfolders0=self.env['documents.folder'].search([('parent_folder_id','=',document_parent_00.id)])
        if len(all_subfolders0)!=0:
            for i in all_subfolders0:
                document_folder=self.env['documents.folder']
                document_parent_1=document_folder.create({'name':i.name,'sequence':i.sequence,'parent_folder_id':document_parent_0.id})
                all_subfolders1=self.env['documents.folder'].search([('parent_folder_id','=',i.id)])
                if len(all_subfolders1)!=0:
                    for j in all_subfolders1:
                        document_folder=self.env['documents.folder']
                        document_parent_2=document_folder.create({'name':j.name,'sequence':j.sequence,'parent_folder_id':document_parent_1.id})
                        all_subfolders2=self.env['documents.folder'].search([('parent_folder_id','=',j.id)])
                        if len(all_subfolders2)!=0:
                            for k in all_subfolders2:
                                document_folder=self.env['documents.folder']
                                document_parent_3=document_folder.create({'name':k.name,'sequence':k.sequence,'parent_folder_id':document_parent_2.id})
                                all_subfolders3=self.env['documents.folder'].search([('parent_folder_id','=',k.id)])
                                if len(all_subfolders3)!=0:
                                    for m in all_subfolders3:
                                        document_folder=self.env['documents.folder']
                                        document_parent_4=document_folder.create({'name':m.name,'parent_folder_id':document_parent_3.id})
                                        all_subfolders4=self.env['documents.folder'].search([('parent_folder_id','=',m.id)])
                                        if len(all_subfolders4)!=0:
                                            for w in all_subfolders4:
                                                document_folder=self.env['documents.folder']
                                                document_parent_5=document_folder.create({'name':w.name,'parent_folder_id':document_parent_4.id})         
        return {'type': 'ir.actions.act_window_close'}
    def view_inherit_workspace_country(self):
        form_view = self.env.ref('custom_documents.inherit_workspace_country_form_view')
        self.ensure_one()
        return {'name': _('Merci de saisir ces informations :'),
                'type': 'ir.actions.act_window',
                'res_model': 'documents.folder',
                'view_mode': 'form',
                'view_id': form_view.id,
                'res_id': self.id,
                'target': 'new'}
    def inherit_workspace_country(self):
        main_workspace_id=self.env['documents.folder'].search([('id','=',self.id)])
        document_folder=self.env['documents.folder']
        document_parent_0=document_folder.create({'name':self.country_name,'sequence':main_workspace_id.sequence+1})
        all_subfolders0=self.env['documents.folder'].search([('parent_folder_id','=',main_workspace_id.id)])
        if len(all_subfolders0)!=0:
            for t,i in enumerate(all_subfolders0):
                document_folder=self.env['documents.folder']
                document_parent_1=document_folder.create({'name':i.name,'sequence':i.sequence,'parent_folder_id':document_parent_0.id})
                all_subfolders1=self.env['documents.folder'].search([('parent_folder_id','=',i.id)])
                if t==1:
                    all_subfolders1=all_subfolders1[:1]
                if len(all_subfolders1)!=0:
                    for j in all_subfolders1:
                        document_folder=self.env['documents.folder']
                        if t==1:
                            document_parent_2=document_folder.create({'name':self.project_name,'parent_folder_id':document_parent_1.id})
                        else:
                            document_parent_2=document_folder.create({'name':j.name,'parent_folder_id':document_parent_1.id})
                        all_subfolders2=self.env['documents.folder'].search([('parent_folder_id','=',j.id)])
                        if len(all_subfolders2)!=0:
                            for k in all_subfolders2:
                                document_folder=self.env['documents.folder']
                                document_parent_3=document_folder.create({'name':k.name,'parent_folder_id':document_parent_2.id})
                                all_subfolders3=self.env['documents.folder'].search([('parent_folder_id','=',k.id)])
                                if len(all_subfolders3)!=0:
                                    for m in all_subfolders3:
                                        document_folder=self.env['documents.folder']
                                        document_parent_4=document_folder.create({'name':m.name,'parent_folder_id':document_parent_3.id})
                                        all_subfolders4=self.env['documents.folder'].search([('parent_folder_id','=',m.id)])
                                        if len(all_subfolders4)!=0:
                                            for w in all_subfolders4:
                                                document_folder=self.env['documents.folder']
                                                document_parent_5=document_folder.create({'name':w.name,'parent_folder_id':document_parent_4.id})
                                                all_subfolders5=self.env['documents.folder'].search([('parent_folder_id','=',w.id)])
                                                if len(all_subfolders5)!=0:
                                                    for x in all_subfolders5:
                                                        document_folder=self.env['documents.folder']
                                                        document_parent_6=document_folder.create({'name':x.name,'parent_folder_id':document_parent_5.id})
                                                        all_subfolders6=self.env['documents.folder'].search([('parent_folder_id','=',x.id)])
                                                        if len(all_subfolders6)!=0:
                                                            for r in all_subfolders6:
                                                                document_folder=self.env['documents.folder']
                                                                document_parent_7=document_folder.create({'name':r.name,'parent_folder_id':document_parent_6.id})
        return {'type': 'ir.actions.act_window_close'}                        
    def delete_folders(self):
        self.env.cr.execute("""delete from documents_folder where create_date > (select NOW() - interval '1' hour)""")
    def delete_sign_archive(self):
        self.env.cr.execute("""delete from sign_template where active=False""")
"""class SignSendRequest(models.Model):
    _description = 'Sign Send Request'
    _inherit = 'sign.send.request' """









