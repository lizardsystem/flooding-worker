Changelog of flooding-worker
===================================================


1.5 (2012-10-15)
----------------

- Added task TASK_CALCULATE_STATISTICS.

- Fixed error on model's combination in openbreach.py.


1.4 (2012-09-21)
----------------

Added task that can calculate scenario statistics (namely, total
inundation area and inundated volume). Also made it into a management
command for ease of use.


1.3 (2012-09-14)
----------------

- Close db connection in png_genaration.py before saving images.

- Exclude an empty value of color_mapping_name field bij in png_generation.py.

- Added authentication check.


1.2 (2012-09-07)
----------------

- Close connection before spawning subprocess and on the end of the task.


1.1 (2012-09-03)
----------------

- Added functionality to update scenario status (perform_task.py, presentationlayer_generation.py)


1.0 (2012-08-29)
----------------

- Added functionality to replace FileHandler of the root logger with a
  specific FileHandler per worker.

- Added 'parent_code' field to WorkflowTemplateTask to define a task's tree.

- Deleted 'sequence' field.

- Added heartbeat option to broker connection.

- Added functionality to start workers as subprocess.

- Added success field to WorkflowTask model.

- Added function to define status of workflow.

- Added unit tests.

- Added heartbeat functionality.

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
