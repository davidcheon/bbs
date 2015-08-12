# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChatContent'
        db.create_table(u'app1_chatcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fromuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app1.BBS_User'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pubdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app1', ['ChatContent'])


    def backwards(self, orm):
        # Deleting model 'ChatContent'
        db.delete_table(u'app1_chatcontent')


    models = {
        u'app1.bbs': {
            'Meta': {'object_name': 'BBS'},
            'bbs_content': ('django.db.models.fields.TextField', [], {}),
            'bbs_create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'bbs_from_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"}),
            'bbs_in_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.Category']"}),
            'bbs_summary': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bbs_title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app1.bbs_comment': {
            'Meta': {'object_name': 'BBS_Comment'},
            'comment_content': ('django.db.models.fields.TextField', [], {}),
            'comment_create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'comment_from_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"}),
            'comment_to_bbs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app1.bbs_comment_to_comment': {
            'Meta': {'object_name': 'BBS_Comment_To_Comment'},
            'comment_to_comment_content': ('django.db.models.fields.TextField', [], {}),
            'comment_to_comment_create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment_to_comment_from_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"}),
            'comment_to_comment_to_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_Comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app1.bbs_user': {
            'Meta': {'object_name': 'BBS_User'},
            'bbs_user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'bbs_user_photo': ('django.db.models.fields.files.ImageField', [], {'default': "'/home/dane/workspace/bbs/upload_imgs/default.png'", 'max_length': '100'}),
            'bbs_user_signature': ('django.db.models.fields.CharField', [], {'default': "'nothing to leave'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app1.bbs_user_loginout_infor': {
            'Meta': {'object_name': 'BBS_User_Loginout_Infor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'login_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'logout_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"})
        },
        u'app1.category': {
            'Meta': {'object_name': 'Category'},
            'category_manager': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"}),
            'category_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app1.chatcontent': {
            'Meta': {'object_name': 'ChatContent'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fromuser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pubdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'app1.onlineuser': {
            'Meta': {'object_name': 'OnlineUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'login_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"})
        },
        u'app1.sendmessage': {
            'Meta': {'object_name': 'SendMessage'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fromuser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app1.BBS_User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'senddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'touser': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app1']