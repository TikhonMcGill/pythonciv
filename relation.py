class Relation:

    def __init__(self,giver,receiver):
        self.name = ""
        self.description = ""
        self.giver = giver
        self.receiver = receiver
        giver.diplomatic_relations.append(self)
        receiver.diplomatic_relations.append(self)

    def describe_relation(self):
        print(self.description.replace("*",giver.official_name).replace("^",receiver.official_name))

    def get_other_side(self,wisher):
        if wisher==self.giver:
            return self.receiver
        else:
            return self.giver
