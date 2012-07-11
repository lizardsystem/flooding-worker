Changelog of flooding-worker
===================================================


0.6.3 (unreleased)
------------------

- Added functionality to replace FileHandler of the root logger with a
  specific FileHandler per worker.

- Added 'parent_code' field to WorkflowTemplateTask to define a task's tree.

- Deleted 'sequence' field.

0.6.2 (2012-06-28)
------------------

- Replaced broker settings, to config broker see README.rst.


0.6.1 (2012-06-19)
------------------

- Replaced dependency floding_worker.Workflow to flooding_lib.Scenario.

- Created a new initial migrationschema.

- Renamed lizard_flooding_worker to flooding_worker in Meta class of
  the model.

0.5.1 (2012-06-15)
------------------

- Add simplejson to dependencies.


0.5 (2012-06-15)
----------------

- Add initial south migration.


0.4 (2012-06-12)
----------------

- Nothing changed yet.


0.3.3 (2012-06-11)
------------------

- Nothing changed yet.


0.3.2 (2012-06-11)
------------------

- Nothing changed yet.


0.3.1 (2012-06-11)
------------------

- Added dependency to lizard_ui, test settings uses its settingshelper.


0.3 (2012-06-11)
----------------

- Renamed lizard-flooding-worker to flooding-worker. Renamed other
  libraries in the project and references to them.

- Left scripts that import from 'lizard', 'lizard.base',
  'lizard.flooding' and so on alone -- presumably these are obsolete
  anyway and can be removed?

0.2.1 (2012-06-08)
------------------

- Nothing changed yet.


0.2 (2012-06-08)
----------------

- INCOMPATIBLE CHANGE: Now relies on renamed flooding-lib


0.1 (2012-02-29)
----------------

- Added worker.
- Added tasks.
- Initial library skeleton created by nensskel.  [Alexandr Seleznev]
