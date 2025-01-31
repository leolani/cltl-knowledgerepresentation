import logging
from typing import List

from cltl.combot.infra.config import ConfigurationManager
from cltl.combot.infra.event import Event, EventBus
from cltl.combot.infra.resource import ResourceManager
from cltl.combot.infra.topic_worker import TopicWorker
from cltl.commons.discrete import UtteranceType

from cltl.brain.long_term_memory import LongTermMemory

logger = logging.getLogger(__name__)


class BrainService:
    @classmethod
    def from_config(cls, brain: LongTermMemory, event_bus: EventBus, resource_manager: ResourceManager,
                    config_manager: ConfigurationManager):
        config = config_manager.get_config("cltl.brain")

        return cls(config.get("topic_input"), config.get("topic_output"), brain, event_bus, resource_manager)

    def __init__(self, input_topic: str, output_topic: str, brain: LongTermMemory,
                 event_bus: EventBus, resource_manager: ResourceManager):
        self._brain = brain

        self._event_bus = event_bus
        self._resource_manager = resource_manager

        self._input_topic = input_topic
        self._output_topic = output_topic

        self._topic_worker = None

    @property
    def app(self):
        return None

    def start(self, timeout=30):
        self._topic_worker = TopicWorker([self._input_topic], self._event_bus, provides=[self._output_topic],
                                         resource_manager=self._resource_manager, processor=self._process,
                                         name=self.__class__.__name__)
        self._topic_worker.start().wait()

    def stop(self):
        if not self._topic_worker:
            pass

        self._topic_worker.stop()
        self._topic_worker.await_stop()
        self._topic_worker = None

    def _process(self, event: Event[List[dict]]):
        logger.debug("Processing event %s with %s capsules", event.id, len(event.payload))

        response = []
        for capsule in event.payload:
            logger.debug("Capsule: (%s)", capsule)

            try:
                brain_response = None
                if 'type' in capsule:
                    if capsule['type'] == 'context':
                        brain_response = self._brain.capsule_context(capsule)
                    else:
                        logger.error("Skipped capsule type: %s", capsule['type'])
                elif 'utterance_type' in capsule:
                    if capsule['utterance_type'] == UtteranceType.STATEMENT:
                        brain_response = self._brain.capsule_statement(capsule, reason_types=True, create_label=True)
                    elif capsule['utterance_type'] == UtteranceType.EXPERIENCE:
                        brain_response = self._brain.capsule_experience(capsule, create_label=True)
                    elif capsule['utterance_type'] == UtteranceType.EXPERIENCE_TRIPLE:
                        brain_response = self._brain.capsule_experience_triple(capsule, create_label=True)
                    elif capsule['utterance_type'] in (UtteranceType.IMAGE_MENTION, UtteranceType.TEXT_MENTION,
                                                       UtteranceType.TEXT_ATTRIBUTION, UtteranceType.IMAGE_ATTRIBUTION):
                        brain_response = self._brain.capsule_mention(capsule, create_label=True)
                    elif capsule['utterance_type'] == UtteranceType.QUESTION:
                        brain_response = self._brain.query_brain(capsule)
                    else:
                        logger.error("Skipped capsule utterance type: %s", capsule['utterance_type'])
                else:
                    logger.debug("Skipped capsule type: %s", capsule)

                try:
                    status = len(brain_response['response']) if 'response' in brain_response else 0
                except ValueError:
                    status = 0
                if status > 399:
                    logger.error("Brain response indicates failure (status %s)", status)

                if brain_response:
                    response.append(brain_response)
                logger.debug("Processed %s (%s)",
                             capsule['type'] if 'type' in capsule else capsule['utterance_type'],
                             brain_response)
            except:
                logger.exception("Brain error (%s)", capsule)

        if response:
            # TODO: transform brain responses into proper EMISSOR annotations (what to do about thoughts?)
            self._event_bus.publish(self._output_topic, Event.for_payload(response))
