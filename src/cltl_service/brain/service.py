import logging
from typing import List

from cltl.brain.long_term_memory import LongTermMemory
from cltl.combot.event.emissor import AnnotationEvent
from cltl.combot.infra.config import ConfigurationManager
from cltl.combot.infra.event import Event, EventBus
from cltl.combot.infra.resource import ResourceManager
from cltl.combot.infra.time_util import timestamp_now
from cltl.combot.infra.topic_worker import TopicWorker
from cltl_service.backend.schema import TextSignalEvent

logger = logging.getLogger(__name__)

CONTENT_TYPE_SEPARATOR = ';'


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
        response = []
        for capsule in event.payload:
            logger.debug("Capsule: (%s)", capsule)
            try:
                brain_response = self._brain.update(capsule, reason_types=True, create_label=True)
                # brain_response = brain_response_to_json(brain_response)
                response.append(brain_response)
            except:
                logger.exception("Brain error")

        if response:
            # TODO: transform brain responses into proper EMISSOR annotations (what to do about thoughts?)
            # extractor_event = self._create_payload(response)
            self._event_bus.publish(self._output_topic, Event.for_payload(response))

    def _create_payload(self, response):
        # TODO: transform brain responses into proper EMISSOR annotations
        # extract mentions from capsules and put them in the annotation
        signal = AnnotationEvent.for_scenario(None, timestamp_now(), timestamp_now(), None, response)

        return TextSignalEvent.create(signal)
