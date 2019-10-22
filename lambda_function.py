# -*- coding: utf-8 -*-

# This is an Alexa Skill about irregular verbs in English.
# The skill is intended and built for an Italian audience.
# The following code contains Italian words.

from six import PY2
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import SsmlOutputSpeech
import irregular_verbs
from irregular_verbs import IRREGULAR_VERBS
import os
import json
import random

skill_name = "Paradigmi Inglesi"
help_text = (
    "Puoi chiedermi, ad esempio: ripetiamo i paradigmi. Oppure: qual è il paradigma di fly?")

verbo_slot_key = "VERBS"
verbo_slot = "verbo"

verboconiugato_slot_key = "CONJVERBS"
verboconiugato_slot = "verboconiugato"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech = "Ciao! Ripassiamo insieme i verbi irregolari inglesi."

    handler_input.response_builder.speak(
        speech + " " + help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Alla prossima!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response

# --------------------------------------------------------------------------------------------------------------------------- #

# !!!!! PARADIGMA INTENT !!!!!!
@sb.request_handler(can_handle_func=is_intent_name("ParadigmaIntent"))
def paradigma_handler(handler_input):
    """Check if a verb is provided in slot values. If provided, then
    looks for the paradigm in the irregular_verbs file.
    If not, then it asks user to provide the verb again.
    """

    # iterate over the dictionaries in irregular_verbs.py and looks for
    # the verb in the slot. If it finds it, it returns the dictionary
    def get_verb(irregular_verbs, filled_verbo_slot):
        for dictionary in IRREGULAR_VERBS["verbs"]:
            if dictionary["Base"] == verbo:
                return dictionary

    # type: (HandlerInput) -> Response
    attribute_manager = handler_input.attributes_manager
    session_attr = attribute_manager.session_attributes
    slots = handler_input.request_envelope.request.intent.slots

    if verbo_slot in slots:  # if slot is filled
        verbo = slots[verbo_slot].value
        handler_input.attributes_manager.session_attributes[
            verbo_slot_key] = verbo  # verbo is equal to what i said ex. know

        # execute the function based on the verb the user asks for. askedVerb
        # becomes equal to the dictionary returned by the function
        askedVerb = get_verb(irregular_verbs.IRREGULAR_VERBS, verbo)
        # check if a dictionary was returned and if the verb is read
        if verbo == "read" and askedVerb:
            askedVerb = get_verb(irregular_verbs.IRREGULAR_VERBS, verbo)
            pastSimple = askedVerb["PS"]
            pastPart = askedVerb["PP"]
            speech = ("Il paradigma di <lang xml:lang='en-GB'>{}</lang> è <voice name='Emma'><lang xml:lang='en-GB'>to {}, <phoneme alphabet='ipa' ph='rɛd'>{}</phoneme>, <phoneme alphabet='ipa' ph='rɛd'>{}</phoneme></lang></voice>".format(verbo, verbo, pastSimple, pastPart))
            reprompt = ("Cosa vuoi chiedermi?")
            handler_input.response_builder.set_should_end_session(True)
        # check if a dictionary was returned
        elif askedVerb:
            pastSimple = askedVerb["PS"]
            pastPart = askedVerb["PP"]
            speech = ("Il paradigma di <lang xml:lang='en-GB'>{}</lang> è <voice name='Emma'><lang xml:lang='en-GB'>to {}, {}, {}</lang></voice>".format(
                verbo, verbo, pastSimple, pastPart))
            reprompt = ("Cosa vuoi chiedermi?")
            handler_input.response_builder.set_should_end_session(True)
        # otherwise assume it's a regular verb
        else:
            speech = (
                "Non trovo il verbo <lang xml:lang='en-GB'>{}</lang>. Se è corretto, allora la sua coniugazione è regolare".format(verbo))
            reprompt = ("Cosa vuoi chiedermi?")
            handler_input.response_builder.set_should_end_session(True)

    # if slot isn't filled, repeat helptext
    else:
        speech = ("Non ho capito." + help_text)
        handler_input.response_builder.ask(help_text)

    handler_input.response_builder.speak(speech).ask(
        reprompt).set_should_end_session(True)
    return handler_input.response_builder.response

# -----------------------------------------------------------------------------#

# !!!!!!!!! REVERSE INTENT !!!!!!!!!!
@sb.request_handler(can_handle_func=is_intent_name("ReverseIntent"))
def reverse_handler(handler_input):
    """Check if a verb is provided in slot values. If provided, then
    looks for the paradigm in the irregular_verbs file.
    If not, then it asks user to provide the verb again.
    """

    # iterate over the dictionaries in irregular_verbs.py and looks for
    # the verb in the slot. If it finds it, it returns the dictionary
    def get_verb(irregular_verbs, filled_verboconiugato_slot):
        for dictionary in IRREGULAR_VERBS["verbs"]:
            if dictionary["PS"] == verboconiugato or dictionary["PP"] == verboconiugato:
                return dictionary

    # type: (HandlerInput) -> Response
    attribute_manager = handler_input.attributes_manager
    session_attr = attribute_manager.session_attributes
    slots = handler_input.request_envelope.request.intent.slots

    if verboconiugato_slot in slots:  # if slot is filled
        verboconiugato = slots[verboconiugato_slot].value
        handler_input.attributes_manager.session_attributes[
            verboconiugato_slot_key] = verboconiugato  # verbo is equal to what i said ex. know

        # execute the function based on the verb the user asks for. askedVerb
        # becomes equal to the dictionary returned by the function
        askedVerb = get_verb(irregular_verbs.IRREGULAR_VERBS, verboconiugato)

        if verboconiugato == "read" and askedVerb:
            baseVerb = askedVerb["Base"]
            pastSimple = askedVerb["PS"]
            pastPart = askedVerb["PP"]
            traduzione = askedVerb["Italiano"]
            speech = ("<lang xml:lang='en-GB'>{}</lang> è il verbo <voice name='Emma'><lang xml:lang='en-GB'>to {}</lang></voice>. Il suo paradigma è <voice name='Emma'><lang xml:lang='en-GB'>to {}, <phoneme alphabet='ipa' ph='rɛd'>{}</phoneme>, <phoneme alphabet='ipa' ph='rɛd'>{}</phoneme></lang></voice>. Significa <phoneme alphabet='ipa' ph='ˈlɛdʤere'>{}</phoneme>.".format(verboconiugato, baseVerb, baseVerb, pastSimple, pastPart, traduzione))
            reprompt = ("Cosa vuoi chiedermi?")
            handler_input.response_builder.set_should_end_session(True)
        elif askedVerb:
            baseVerb = askedVerb["Base"]
            pastSimple = askedVerb["PS"]
            pastPart = askedVerb["PP"]
            traduzione = askedVerb["Italiano"]
            speech = ("<lang xml:lang='en-GB'>{}</lang> è il verbo <voice name='Emma'><lang xml:lang='en-GB'>to {}</lang></voice>. Il suo paradigma è <voice name='Emma'><lang xml:lang='en-GB'>to {}, {}, {}</lang></voice>. Significa {}.".format(
                verboconiugato, baseVerb, baseVerb, pastSimple, pastPart, traduzione))
            reprompt = ("Cosa vuoi chiedermi?")
            handler_input.response_builder.set_should_end_session(True)
        else:
            speech = (
                "Non trovo il verbo <lang xml:lang='en-GB'>{}</lang>. Se è corretto, allora la sua coniugazione è regolare".format(verboconiugato))
            reprompt = ("Cosa vuoi chiedermi?")
            handler_input.response_builder.set_should_end_session(True)

    # if slot isn't filled, repeat helptext
    else:
        speech = ("Non ho capito." + help_text)
        handler_input.response_builder.ask(help_text)

    handler_input.response_builder.speak(speech).ask(
        reprompt).set_should_end_session(True)
    return handler_input.response_builder.response

# -----------------------------------------------------------------------------#

    # !!!!!!!!! INTERROGAMI INTENT !!!!!!!!!!


@sb.request_handler(can_handle_func=is_intent_name("InterrogamiIntent"))
def interrogami_handler(handler_input):

    # iterate over the dictionaries in irregular_verbs.py and looks for
    # the verb in the slot. If it finds it, it returns the dictionary
    def get_random_verb(irregular_verbs):
        randomVerb = random.choice(IRREGULAR_VERBS["verbs"])
        return randomVerb

    randomizedVerb = get_random_verb(irregular_verbs.IRREGULAR_VERBS)

    if randomizedVerb["Base"] == "read":
        chosenVerb = randomizedVerb["Base"]
        chosenVerbPS = randomizedVerb["PS"]
        chosenVerbPP = randomizedVerb["PP"]
        speech = ("Ok. Dimmi il paradigma di <voice name='Emma'><lang xml:lang='en-GB'>to {}</lang></voice>. <break time='5s'/>Ok, ora tocca a me. Il paradigma è <voice name='Emma'><lang xml:lang='en-GB'>to {}, <phoneme alphabet='ipa' ph='rɛd'>{}</phoneme>, <phoneme alphabet='ipa' ph='rɛd'>{}</phoneme></lang></voice>".format(chosenVerb, chosenVerb, chosenVerbPS, chosenVerbPP))
        reprompt = ("Cosa vuoi chiedermi?")
        handler_input.response_builder.set_should_end_session(True)
    else:
        chosenVerb = randomizedVerb["Base"]
        chosenVerbPS = randomizedVerb["PS"]
        chosenVerbPP = randomizedVerb["PP"]
        speech = ("Ok. Dimmi il paradigma di <voice name='Emma'><lang xml:lang='en-GB'>to {}</lang></voice>. <break time='5s'/>Ok, ora tocca a me. Il paradigma è <voice name='Emma'><lang xml:lang='en-GB'>to {}, {}, {}</lang></voice>".format(chosenVerb, chosenVerb, chosenVerbPS, chosenVerbPP))
        reprompt = ("Cosa vuoi chiedermi?")
        handler_input.response_builder.set_should_end_session(True)

    # handler_input.response_builder.set_should_end_session(True)
    handler_input.response_builder.speak(speech).ask(
        reprompt).set_should_end_session(True)
    return handler_input.response_builder.response

# -----------------------------------------------------------------------------#

# -----------------------------------------------------------------------------#

    # !!!!!!!!! DID NOT UNDERSTAND INTENT !!!!!!!!!! intent filled with nonsense phrases in order to have alexa default to this one (when alexa doesn't know how to respond to an utterance, it will invoke the intent with the bigger number of utterances. it's usually interrogamiIntent, now it's this one)


@sb.request_handler(can_handle_func=is_intent_name("DidNotUnderstandIntent"))
def did_not_understand_handler(handler_input):

    speech = ("{} non può aiutarti con la tua richiesta. Puoi chiedermi il paradigma di un verbo irregolare, oppure possiamo ripetere insieme i paradigmi!".format(skill_name))
    reprompt = ("Cosa vuoi chiedermi?")
    handler_input.response_builder.set_should_end_session(True)

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response

# -----------------------------------------------------------------------------#


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "{} non può aiutarti con la tua richiesta."
        "Puoi chiedermi il paradigma di un verbo irregolare,"
        "oppure possiamo ripetere insieme i paradigmi!").format(skill_name)
    reprompt = ("Puoi chiedermi il paradigma di un verbo irregolare,"
                "oppure possiamo ripassare insieme i paradigmi")
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


def convert_speech_to_text(ssml_speech):
    """convert ssml speech to text, by removing html tags."""
    # type: (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content."""
    # type: (HandlerInput, Response) -> None
    response.card = SimpleCard(
        title=skill_name,
        content=convert_speech_to_text(response.output_speech.ssml))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Log response from alexa service."""
    # type: (HandlerInput, Response) -> None
    print("Alexa Response: {}\n".format(response))


@sb.global_request_interceptor()
def log_request(handler_input):
    """Log request to alexa service."""
    # type: (HandlerInput) -> None
    print("Alexa Request: {}\n".format(handler_input.request_envelope.request))


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))

    speech = "Si è verificato un problema. Riprova!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


######## Convert SSML to Card text ############
# This is for automatic conversion of ssml to text content on simple card
# You can create your own simple cards for each response, if this is not
# what you want to use.

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if not PY2:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)

################################################


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()
