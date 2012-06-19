# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WorkflowTemplate'
        db.create_table('flooding_worker_workflowtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=30)),
        ))
        db.send_create_signal('flooding_worker', ['WorkflowTemplate'])

        # Adding model 'Workflow'
        db.create_table('flooding_worker_workflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.WorkflowTemplate'], null=True, blank=True)),
            ('scenario', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tstart', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tfinished', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('logging_level', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('flooding_worker', ['Workflow'])

        # Adding model 'TaskType'
        db.create_table('flooding_worker_tasktype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('flooding_worker', ['TaskType'])

        # Adding model 'WorkflowTemplateTask'
        db.create_table('flooding_worker_workflowtemplatetask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.TaskType'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('max_failures', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_duration_minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('workflow_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.WorkflowTemplate'])),
        ))
        db.send_create_signal('flooding_worker', ['WorkflowTemplateTask'])

        # Adding model 'WorkflowTask'
        db.create_table('flooding_worker_workflowtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.Workflow'])),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.TaskType'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('max_failures', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_duration_minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tstart', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tfinished', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('successful', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('flooding_worker', ['WorkflowTask'])

        # Adding model 'Logging'
        db.create_table('flooding_worker_logging', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.Workflow'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flooding_worker.WorkflowTask'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('flooding_worker', ['Logging'])


    def backwards(self, orm):
        
        # Deleting model 'WorkflowTemplate'
        db.delete_table('flooding_worker_workflowtemplate')

        # Deleting model 'Workflow'
        db.delete_table('flooding_worker_workflow')

        # Deleting model 'TaskType'
        db.delete_table('flooding_worker_tasktype')

        # Deleting model 'WorkflowTemplateTask'
        db.delete_table('flooding_worker_workflowtemplatetask')

        # Deleting model 'WorkflowTask'
        db.delete_table('flooding_worker_workflowtask')

        # Deleting model 'Logging'
        db.delete_table('flooding_worker_logging')


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
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'workflow_template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flooding_worker.WorkflowTemplate']"})
        }
    }

    complete_apps = ['flooding_worker']
