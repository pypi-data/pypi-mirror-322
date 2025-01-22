import json
import logging
from collections import OrderedDict
from tricc_oo.models import TriccOperation, TriccOperator
from tricc_oo.strategies.output.base_output_strategy import BaseOutPutStrategy

logger = logging.getLogger("default")

class spiceCondition():
    eq: str = None
    targetId: str = None
    visibility: str = 'visible' # other option gone
    
    def __init__(self, eq=None, targetId=None, visibility='visible'):
        self.eq = eq
        self.targetId = targetId
        self.visibility = visibility

    
    def __repr__(self):
        self.__str__()
    def __str__(self):
        # Create a dictionary with only the required attributes
        return {
            "eq": self.eq,
            "targetId": self.targetId,
            "visibility": self.visibility
        }


class spiceOption():
    id: str = None
    name: str = None
    def __init__(self, id=None, name=None):
        self.id = id
        self.targetId = targetId

    
    def __repr__(self):
        self.__str__()
    def __str__(self):
        # Create a dictionary with only the required attributes
        return {
            "id": self.id,
            "name": self.name,
        }
        
class SpiceQuestion():
    condition: list = []
    errorMessage: str = None
    family: str = None
    titleSummary: str = None
    fieldName: str = None
    id: str = None
    isEnabled: bool = None
    isEnabled: bool = True
    isMandatory: bool = True
    isNeededDefault: bool = False
    isBooleanAnswer: bool = False
    isSummary: str = None
    optionsList: list = []
    optionType: str = 'boolean'
    orderId: str = None
    readOnly: bool = True
    title: str = None
    isInfo: str = 'gone'
    visibility: str = 'visible'

class SpiceStrategy(BaseOutPutStrategy):
    def __init__(self, project, output_path):
        super().__init__(project, output_path)
        self.form_layout = []
        self.conditions = []
        self.options_list = []

    def generate_base(self, node, **kwargs):
        return self.generate_json_condition(node, **kwargs)

    def generate_relevance(self, node, **kwargs):
        return self.generate_json_relevance(node, **kwargs)

    def generate_calculate(self, node, **kwargs):
        return self.generate_json_calculate(node, **kwargs)

    def do_clean(self):
        self.form_layout = []
        self.conditions = []
        self.options_list = []

    def get_kwargs(self):
        return {
            "form_layout": self.form_layout,
            "conditions": self.conditions,
            "options_list": self.options_list,
        }

    def generate_export(self, node, **kwargs):
        # Export logic to JSON format
        spice_

        self.form_layout.append(form_element)

    def export(self, start_pages, version):
        # Save the JSON output to a file
        file_name = f"{start_pages['main'].root.form_id}.json"
        output_path = os.path.join(self.output_path, file_name)
        
        with open(output_path, 'w') as json_file:
            json.dump({"formLayout": self.form_layout}, json_file, indent=4)
        
        logger.info(f"JSON form exported to {output_path}")

    def generate_json_condition(self, node, **kwargs):
        pass
            

    def generate_json_relevance(self, node, **kwargs):
        # Add relevance logic here if applicable
        pass

    def generate_json_calculate(self, node, **kwargs):
        # Add calculation logic here if applicable
        pass

    def process_export(self, start_pages, **kwargs):
        # Process nodes and export as JSON
        self.activity_export(start_pages["main"], **kwargs)

    def activity_export(self, activity, processed_nodes=set(), **kwargs):
        stashed_nodes = OrderedDict()
        for node in activity.nodes:
            if not is_ready_to_process(node, processed_nodes):
                stashed_nodes[node.id] = node
                continue
            processed_nodes.add(node)
            self.generate_export(node)
        
        # Handle stashed nodes (if needed)
    def tricc_operation_equal(self, ref_expressions):
        return {
          "eq": str(ref_expressions[1]),
          "targetId": str(ref_expressions[0]),
          "visibility": "visible"
        }

    def tricc_operation_in(self, ref_expressions):
        return {
          "eq": str(ref_expressions[0]),
          "targetId": str(ref_expressions[1]),
          "visibility": "visible"
        }
    
    def tricc_operation_in(self, ref_expressions):
        return ref_expressions[0].replace('visible', 'gone')