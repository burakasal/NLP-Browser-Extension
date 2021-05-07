import spacy
import nltk

def nerEng(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    OrganizationList = []
    GPEList = []
    PersonList = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text not in PersonList:
                PersonList.append(ent.text)
        if ent.label_ == "ORG":
            if ent.text not in OrganizationList:
                OrganizationList.append(ent.text)
        if ent.label_ == "GPE":
            if ent.text not in GPEList:
                GPEList.append(ent.text)

    TaggedOrganizations = ', '.join(OrganizationList)
    TaggedPersons = ', '.join(PersonList)
    TaggedGeographicalEntities = ', '.join(GPEList)
    return(TaggedOrganizations, TaggedPersons, TaggedGeographicalEntities)
