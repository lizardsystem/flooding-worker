#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson

from action import Action

import logging

TASK_COMPUTE_SOBEK_MODEL_120 = "120"
TASK_PERFORM_SOBEK_SIMULATION_130 = "130"
TASK_COMPUTE_RISE_SPEED_132 = "132"
TASK_COMPUTE_MORTALITY_GRID_134 = "134"
TASK_SOBEK_PNG_GENERATION_150 = "150"
TASK_HISSSM_SIMULATION_160 = "160"
TASK_SOBEK_EMBANKMENT_DAMAGE_162 = "162"
TASK_HISSSM_PNG_GENERATION_180 = "180"
TASK_SOBEK_PRESENTATION_GENERATION_155 = "155"
TASK_HISSSM_PRESENTATION_GENERATION_185 = "185"


class ActionTask(Action):

    def __init__(self, connection, task_code):
        self.task_code = task_code
        self.connection = connection
        self.body = None
        self.log = logging.getLogger('lizard-flooding.action.task')

    def next_queues(self):
        """
        Recovers queues(s) of next task(s)
        by increasing the sequence.
        """
        next_sequence = int(self.body["next_sequence"]) + 1
        instruction = self.body["instruction"]
        queues = []
        for (queue_code, sequence) in instruction.iteritems():
            if int(sequence) == next_sequence:
                queues.append(queue_code)
        return queues

    def increase_sequence(self):
        self.body["next_sequence"] = int(self.body["next_sequence"]) + 1

    def set_current_task(self, queue):
        self.body["curr_task_code"] = queue

    def callback(self, ch, method, properties, body):
        """sends logging to logging queue"""
        self.body = simplejson.loads(body)
        self.log.info("Start task")

        try:
            self.run_task(self.task_code)
        except Exception as ex:
            self.log.error("{0}".format(ex))
            return

        self.log.info("End task")
        queues = self.next_queues()
        self.increase_sequence()
        for queue in queues:
            self.set_current_task(queue)
            self.send_trigger_message(self.body,
                                 "Message emitted to queue %s" % queue,
                                 queue)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run_task(self, code):
        if code == TASK_COMPUTE_SOBEK_MODEL_120:
            self.log.debug("execute TASK_COMPUTE_SOBEK_MODEL_120")
            from lizard_flooding_worker.client.worker.tasks import openbreach
            openbreach.set_broker_logging_handler(self.broker_logging_handler)
            remarks = 'openbreach-' + openbreach.__revision__
            success_code = openbreach.compute_sobek_model(
                self.body["workflow_id"],
                'c:/temp/%02d/' % self.body["next_sequence"])
        elif code == TASK_PERFORM_SOBEK_SIMULATION_130:
            self.log.debug("execute TASK_PERFORM_SOBEK_SIMULATION_130")
            # import spawn
            # remarks = 'spawn-' + spawn.__revision__
            # result = spawn.perform_sobek_simulation(
            #     self.connection,
            #     self.scenario,
            #     self.last_id,
            #     3600,
            #     'lzfl_%03d'%self.sequential)
            # log.debug("spawing returned %s" % (result,))
            # success_code = (result[0] == 0)
        elif code == TASK_SOBEK_PNG_GENERATION_150:
            self.log.debug("execute TASK_SOBEK_PNG_GENERATION_150")
            # import png_generation
            # remarks = 'png_generation-' + png_generation.__revision__
            # success_code = png_generation.sobek(
            #     self.connection,
            #     self.scenario,
            #     'c:/temp/%02d/'%self.sequential)
        elif code == TASK_COMPUTE_RISE_SPEED_132:
            self.log.debug("execute TASK_COMPUTE_RISE_SPEED_132")
            # import calculaterisespeed_132
            # remarks = 'calculaterisespeed_132-' + calculaterisespeed_132.__revision__
            # success_code = calculaterisespeed_132.perform_calculation(
            #     self.connection,
            #     'c:/temp/%02d/'%self.sequential,
            #     self.scenario,
            #    self.hisssm_year)
        elif code == TASK_COMPUTE_MORTALITY_GRID_134:
            self.log.debug("execute TASK_COMPUTE_MORTALITY_GRID_134")
            # import calculatemortalitygrid_134
            # remarks = 'calculatemortalitygrid_134-' + calculatemortalitygrid_134.__revision__
            # success_code = calculatemortalitygrid_134.perform_calculation(
            #     self.connection,
            #     'c:/temp/%02d/'%self.sequential,
            #     self.scenario,
            #     self.hisssm_year)
        elif code == TASK_SOBEK_PRESENTATION_GENERATION_155:
            self.log.debug("execute TASK_SOBEK_PRESENTATION_GENERATION_155")
            # import presentationlayer_generation
            # remarks = 'presentationlayer_generation-' + presentationlayer_generation.__revision__
            # success_code = presentationlayer_generation.perform_presentation_generation(
            #     lizard.settings,
            #     self.scenario)
        elif code == TASK_HISSSM_SIMULATION_160:
            self.log.debug("execute TASK_HISSSM_SIMULATION_160")
            # import hisssm_160
            # remarks = 'hisssm_160-' + hisssm_160.__revision__
            # success_code = hisssm_160.perform_HISSSM_calculation(
            #     self.connection,
            #     self.hisssm_location,
            #     self.scenario,
            #     self.hisssm_year)
        elif code == TASK_SOBEK_EMBANKMENT_DAMAGE_162:
            log.debug("execute TASK_SOBEK_EMBANKMENT_DAMAGE_162")
            # import kadeschade_module
            # remarks = 'kadeschade_module-' + kadeschade_module.__revision__
            # success_code, extra_remarks = kadeschade_module.calc_damage(self.scenario)
            # remarks = extra_remarks + remarks
        elif code == TASK_HISSSM_PNG_GENERATION_180:
            self.log.debug("execute TASK_HISSSM_PNG_GENERATION_180")
            # import png_generation
            # remarks = 'png_generation-' + png_generation.__revision__
            # success_code = png_generation.his_ssm(
            #     self.connection,
            #     self.scenario,
            #     'c:/temp/%02d/'%self.sequential)
        elif code == TASK_HISSSM_PRESENTATION_GENERATION_185:
            log.debug("execute TASK_HISSSM_PRESENTATION_GENERATION_185")
            # import presentationlayer_generation
            # remarks = 'presentationlayer_generation-' + presentationlayer_generation.__revision__
            # success_code = presentationlayer_generation.perform_presentation_generation(
            #     lizard.settings,
            #     self.scenario)
        else:
            self.log.warning("selected a '%s' task but don't know what it is" % code)
            #remarks = remarks + '\nunknown task'
