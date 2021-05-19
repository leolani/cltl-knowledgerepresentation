import logging
import numpy as np
import os
from typing import Dict

from cltl.combot.infra.util import Bounds
from tests.brain_external.obj import Object

logger = logging.getLogger(__name__)


class Face(Object):
    """
    Face Object

    Parameters
    ----------
    name: str
        Name of Person
    confidence: float
        Name Confidence
    representation: np.ndarray
        Face Feature Vector
    bounds: Bounds
        Face Bounding Box
    image: AbstractImage
        Image Face was Found in
    """

    UNKNOWN = "Stranger"

    def __init__(self, name, confidence, representation, bounds, image):
        # type: (str, float, np.ndarray, Bounds, AbstractImage) -> None
        super(Face, self).__init__(Face.UNKNOWN if name == FaceClassifier.NEW else name,
                                   confidence, bounds, image)

        self._representation = representation

    @property
    def representation(self):
        """
        Face Representation

        Returns
        -------
        representation: np.ndarray
            Face Feature Vector
        """
        return self._representation


class FaceClassifier(object):
    """
    Classify Faces of People

    Parameters
    ----------
    people: Dict[str, np.ndarray]
        Known People as <name, representations> dictionary
    n_neighbors: int
    """
    NEW = "NEW"
    EXTENSION = ".bin"

    def __init__(self, people, n_neighbors=20):
        # type: (Dict[str, np.ndarray], int) -> None

        self._people = people
        self._n_neighbors = n_neighbors

        self._names = sorted(self.people.keys())
        self._indices = list(range(len(self._names)))

        if self.people:
            self._labels = np.concatenate(
                [[index] * len(self.people[name]) for name, index in zip(self._names, self._indices)])
            self._features = np.concatenate([self.people[name] for name in self._names])
            self._classifier = KNeighborsClassifier(self._n_neighbors)
            self._classifier.fit(self._features, self._labels)

        self._log = logger.getChild(self.__class__.__name__)
        self._log.info("Initialized FaceClassifier")

    @property
    def people(self):
        # type: () -> Dict[str, np.ndarray]
        """
        People Dictionary

        Returns
        -------
        people: dict
        """
        return self._people

    def add(self, name, vector):
        # type: (str, np.ndarray) -> None
        """
        Add Person to Face Classifier

        Parameters
        ----------
        name: str
        vector: np.ndarray
            Concatenated Representations (float32 array of length 128n)
        """
        people = self._people
        people[name] = vector

        self._names = sorted(self.people.keys())
        self._indices = list(range(len(self._names)))

        if self.people:
            self._labels = np.concatenate(
                [[index] * len(self.people[name]) for name, index in zip(self._names, self._indices)])
            self._features = np.concatenate([self.people[name] for name in self._names])
            self._classifier = KNeighborsClassifier(self._n_neighbors)
            self._classifier.fit(self._features, self._labels)

    def classify(self, representation, bounds, image):
        """
        Classify Face Observation as Particular Person

        Parameters
        ----------
        representation: np.ndarray
            Observed Face Representation (from OpenFace.represent)
        bounds: Bounds
            Face Bounds (relative to Image)
        image: AbstractImage
            Image in which Face was Observed

        Returns
        -------
        person: Face
            Classified Person
        """

        if not self.people:
            return Face(self.NEW, 0.0, representation, bounds, image)

        # Get distances to nearest Neighbours
        distances, indices = self._classifier.kneighbors(representation.reshape(-1, FaceDetector.FEATURE_DIM))
        distances, indices = distances[0], indices[0]

        # Get numerical label associated with closest face
        labels = self._labels[indices]
        label = np.bincount(labels).argmax()

        # Retrieve name and calculate confidence
        name = self._names[label]
        confidence = float(np.mean(labels == label))

        return Face(name, confidence, representation, bounds, image)

    def accuracy(self):
        """
        Calculate Classifier Cross Validation Accuracy

        Returns
        -------
        accuracy: float
        """
        return float(np.mean(cross_val_score(self._classifier, self._features, self._labels, cv=5)))

    @classmethod
    def from_directory(cls, directory):
        """
        Construct FaceClassifier from directory of <name>.bin files

        Parameters
        ----------
        directory: str

        Returns
        -------
        face_classifier: FaceClassifier
        """
        return cls(FaceClassifier.load_directory(directory))

    @staticmethod
    def load_directory(directory):
        """
        Load People from directory of <name>.bin files

        Parameters
        ----------
        directory: str

        Returns
        -------
        people: dict
            Dictionary of <name>: <representations> pairs
        """
        people = {}
        for path in os.listdir(directory):
            if path.endswith(FaceClassifier.EXTENSION):
                name = os.path.splitext(path)[0]
                features = np.fromfile(os.path.join(directory, path), np.float32).reshape(-1, FaceDetector.FEATURE_DIM)
                people[name] = features
        return people


# pepper.framework.sensor.api
class FaceDetector(object):
    TOPIC = "pepper.framework.sensor.api.face_detector.topic"
    TOPIC_NEW = "pepper.framework.sensor.api.face_detector.topic.new"
    TOPIC_KNOWN = "pepper.framework.sensor.api.face_detector.topic.known"

    FEATURE_DIM = 128

    def represent(self, image):
        # type: (np.ndarray) -> Iterable[(np.ndarray, Bounds)]
        """
        Represent Face in Image as 128-dimensional vector

        Parameters
        ----------
        image: np.ndarray
            Image (possibly containing a human face)

        Returns
        -------
        result: list of (np.ndarray, Bounds)
            List of (representation, bounds)
        """
        raise NotImplementedError()
