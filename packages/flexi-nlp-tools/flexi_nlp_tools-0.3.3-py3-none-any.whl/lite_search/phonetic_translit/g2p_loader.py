import certifi
import ssl
import logging

ssl._create_default_https_context = ssl._create_unverified_context
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

from g2p_en import G2p


logger = logging.getLogger(__name__)


_G2P_MODEL: G2p = None


def get_g2p_model() -> G2p:
    global _G2P_MODEL
    if _G2P_MODEL is None:
        # try:
        #     from nltk.corpus import cmudict
        #     import nltk
        #     cmudict.dict()
        #     nltk.data.find("averaged_perceptron_tagger_eng")
        # except LookupError:
        #     import certifi
        #     import ssl
        #     import nltk
        #
        #     ssl._create_default_https_context = ssl._create_unverified_context
        #     ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
        #
        #     logger.info("Downloading required NLTK resource: cmudict...")
        #     nltk.download('cmudict')
        #
        #     logger.info("Downloading required NLTK resource: averaged_perceptron_tagger_eng...")
        #     nltk.download('averaged_perceptron_tagger_eng')

        _G2P_MODEL = G2p()

    return _G2P_MODEL
