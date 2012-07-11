# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'WorkflowTemplateTask.parent_code'
        db.add_column('flooding_worker_workflowtemplatetask', 'parent_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_task_code', null=True, to=orm['flooding_worker.TaskType']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'WorkflowTemplateTask.parent_code'
        db.delete_column('flooding_worker_workflowtemplatetask', 'parent_code_id')


    models = {
        'flooding_worker.logging': {
            'Meta': {'object_name': 'Logging'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.WorkflowTask']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.Workflow']"})
        },
        'flooding_worker.tasktype': {
            'Meta': {'object_name': 'TaskType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flooding_worker.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logging_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scenario': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.WorkflowTemplate']", 'null': 'True', 'blank': 'True'}),
            'tfinished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tstart': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'flooding_worker.workflowtask': {
            'Meta': {'object_name': 'WorkflowTask'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.TaskType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_duration_minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_failures': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'tfinished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tstart': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.Workflow']"})
        },
        'flooding_worker.workflowtemplate': {
            'Meta': {'object_name': 'WorkflowTemplate'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'flooding_worker.workflowtemplatetask': {
            'Meta': {'object_name': 'WorkflowTemplateTask'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.TaskType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_duration_minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_failures': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_task_code'", 'null': 'True', 'to': "orm['flooding_worker.TaskType']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'workflow_template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.WorkflowTemplate']"})
        }
    }

    complete_apps = ['flooding_worker']
