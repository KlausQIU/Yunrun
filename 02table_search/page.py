#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2012-12-13

from bson import ObjectId, DBRef
from core.web import HandlerBase
from framework.mvc.web import url
from framework.data.mongo import db,Document
from framework.web import paging, JSONEncoder
from core.logic.page import create_page, remove_page, save_page
from core.platform.user.permissions import getChildren , savePermissionsList
import json
from tornado.template import Template


@url("/([a-z0-9]{24})/page/list.html")

class List(HandlerBase):
    def get(self, systemid):
        name = self.get_argument('nameID','')
        alias = self.get_argument('aliasID', '')
        url = self.get_argument('urlID', '')
        category = self.get_argument('categoryID','')

        self.context.systemid = systemid
        self.context.paging = paging.parse(self)
        condition = { "system.$id" : ObjectId(systemid) }

        if name:
            condition['name'] = {'$regex': name}
        if alias:
            condition['alias'] = {'$regex': alias}
        if url:
            condition['url'] = {'$regex': url}
        if category:
            condition['category'] = DBRef("pagecategory",ObjectId(category))

        self.context.paging.count = db.page.find(condition).count()
        self.context.objs = db.page.find(condition).sort([ ("name", -1 ) ]).skip(paging.skip(self.context.paging)).limit(self.context.paging.size)
        self.context.categorys = list(db.pagecategory.find())

        #table.html
        #title
        self.context.attr=[
        {'name': '名称', 'type': 'str','alias':'name'},
        {'name': '别名', 'type': 'str','alias':'alias'},
        {'name': '地址', 'type': 'str','alias':'url'},
        {'name': '类型', 'type':'list','alias':''},
        {'name': '描述', 'type':'unsearch','alias':''},
        {'name': '设计', 'type':'unsearch'},
        {'name': '操作', 'type':'unsearch'}]
        

        self.context.pros = ('name','alias','url','category','description')

        self.context.design = {
        '浏览':['browse','_blank',''],
        '设计':['design','_blank',''],
        '代码':['code','_blank',''],
        '关系':['relation','_blank',''],
        }

        self.context.control = {
        '编辑':['none','','show_edit'],
        '权限':['none','','show_user_children'],
        '删除':['remove','','']
        }

        self.context.iClass = {
        '浏览':'glyphicon glyphicon-globe',
        '设计':'glyphicon glyphicon-list-alt',
        '代码':'glyphicon glyphicon-list',
        '关系':'glyphicon glyphicon-list-alt',
        '编辑':'glyphicon glyphicon-edit',
        '权限':'glyphicon glyphicon-cog',
        '删除':'glyphicon glyphicon-remove'
        }

        return self.template()

@url("/([a-z0-9]{24})/page/edit.html")
class Edit(HandlerBase):
    def get(self, systemid):
        id = self.get_argument("pageid")
        page = db.page.find_one({ "_id" : ObjectId(id) })
        return self.json(page, cls=JSONEncoder)

    def post(self, systemid):
        id = self.get_argument("_id", "")
        page = Document()
        page.name = self.get_argument("name", "").lower().replace(" ","")
        page.alias = self.get_argument("alias", "")
        page.url = self.get_argument("url", "").lower().replace(" ","")
        page.description = self.get_argument("description", "")
        page.category = DBRef("pagecategory", ObjectId(self.get_argument("category")))
        page.system = DBRef("system", ObjectId(systemid))
        
        if not id:
            page.controls = []
            page.settings = {}
            db.page.save(page)
            create_page(systemid, page)
        else:
            db.page.update({"_id" : ObjectId(id)}, { "$set" : page })

        return self.redirect("list.html")


@url("/([a-z0-9]{24})/page/remove.html")
class Remove(HandlerBase):
    def get(self, systemid):
        return self.post(systemid)

    def post(self, systemid):
        id = self.get_argument("pageid")
        page = db.page.find_one({ "_id" : ObjectId(id) })

        remove_page(systemid, page)
        db.page.remove({ "_id" : page._id })

        self.redirect("list.html")


@url("/([a-z0-9]{24})/page/selectlayout.html")
class SelectLayout(HandlerBase):
    def get(self, systemid):
        self.context.pageid = self.get_argument("pageid")
        self.context.layouts = db.layout.find({ "system.$id" : ObjectId(systemid)})

        return self.template()

@url("/([a-z0-9]{24})/page/setlayout.html")
class SetLayout(HandlerBase):
    def get(self, systemid):
        return self.post(systemid)
        
    def post(self, systemid):
        pageid = self.get_argument("pageid", "")
        layoutid = self.get_argument("layoutid", "")
        script_paths = self.request.files.get('script_paths', [])

        page = db.page.find_one({ "_id" : ObjectId(pageid) })
        if layoutid:
            page.layout = DBRef("layout", ObjectId(layoutid))

        del page["_id"]
        db.page.update({"_id" : ObjectId(pageid)}, { "$set" : page })
        page._id = ObjectId(pageid)
        if "styles" not in page:
            page["styles"] = dict()
       
        save_page(systemid, page)

        return self.redirect("../ide/myframe.html?target=page&id=" + pageid)
        

@url("/page/settings.html")
class GetInput(HandlerBase):
    def post(self):
        id = self.get_argument("pageid")
        page = db.page.find_one({ "_id" : ObjectId(id) }, { "settings" : 1 })
        if "settings" in page:
            return self.json(page["settings"], cls=JSONEncoder)

        return self.json({ "rule_settings" : {}, "control_settings" : {} }, cls=JSONEncoder)


@url("/([a-z0-9]{24})/page/userchildren.html")
class GetUserChildren(HandlerBase):
    def post(self,systemid):
        objid = self.get_argument("objid", "")
        objtype = self.get_argument("objtype", "")
        uid = self.get_argument("uid", "")
        show = self.get_argument("show", True)
  
        return self.json(getChildren(systemid,objid,objtype,uid,show),cls=JSONEncoder)
    
@url("/([a-z0-9]{24})/page/savepermissions.html")
class SavePermissions(HandlerBase):
    def post(self,systemid):        
        permissions = json.loads(self.get_argument("permissions", "{}"))
        objectid = self.get_argument("objectid", "")
        if permissions:
            uid = str(self.session["current_user"]._id)
            savePermissionsList(systemid,uid,objectid,permissions)

        return self.json({ "status" : "ok" })    
        
        
        
