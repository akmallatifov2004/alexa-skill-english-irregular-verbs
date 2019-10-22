<a href="https://www.amazon.it/sfal-Paradigmi-Inglesi/dp/B07Z4MCDSP/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=paradigmi+inglesi&qid=1571733872&s=digital-skills&sr=1-1"><img src="https://i.imgur.com/Cinx9S2.png" title="ParadigmiInglesi" alt="ParadigmiInglesi"></a>

# Alexa Skill: Paradigmi Inglesi (English Idioms)

> Alexa Skill written in Python that helps you learn and repeat paradigms of irregular verbs in English (the skill is in Italian).

> All the paradigms are read by the English voice of Alexa.

## Example

```
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
```

---

## Enable Skill (Italy only)


- <a href="https://www.amazon.it/sfal-Paradigmi-Inglesi/dp/B07Z4MCDSP/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=paradigmi+inglesi&qid=1571733872&s=digital-skills&sr=1-1" target="_blank">Paradigmi Inglesi on Amazon.it</a>


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- [MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2019 © <a href="https://github.com/sfal" target="_blank">sfal</a>.
