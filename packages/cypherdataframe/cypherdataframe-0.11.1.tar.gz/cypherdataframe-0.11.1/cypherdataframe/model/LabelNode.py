from dataclasses import dataclass

from cypherdataframe.model.Property import Property


@dataclass(frozen=True)
class LabelNode:
    return_id: str
    label: str
    post_label_str: str | None
    properties: list[Property]
    collect: bool = False

    def properties_by_final_assigment(self):
        return {prop.final_assigment(self.return_id): prop for prop in self.properties}

    def property_fragments_by_cypher_assignments(self):
        if self.collect:
            start_cap = "collect("
            end_cap = ")"
        else:
            start_cap = ""
            end_cap = ""

        prop_by = {
            prop.final_assigment(self.return_id): (
                f" {start_cap}{prop.cypher_assigment(self.return_id)}{end_cap}" 
                f" as {prop.final_assigment(self.return_id)} "
            )
            for prop in self.properties
        }

        return prop_by
