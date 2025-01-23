import re
import yaml

section_re = re.compile(r'^---\s*$', re.MULTILINE)
role_re = re.compile(r'^\s*{{role "(.+)"}}\s*$', re.MULTILINE)
model_regex = re.compile('([^/]+)/(.+)')

class DoPrompt:
    def __init__(self, fpath):
        with open(fpath, 'r') as f:
            content = f.read()

        sections = section_re.split(content)

        if len(sections) != 3:
            raise ValueError('Missing section separator')

        metadata_section = sections[1]
        prompt_section = sections[2]

        self.metadata = yaml.safe_load(metadata_section)

        if 'model' not in self.metadata:
            raise ValueError('Missing model in metadata')

        model = model_regex.match(self.metadata['model'])
        self.model_vendor = model.group(1)
        self.model_name = model.group(2)
        self.model_config = self.metadata.get('config', {})

        self.prompt_template = prompt_section.strip()

    def validate_schema(self, values):
        schema = self.metadata.get('input', {}).get('schema')

        if schema is None:
            return

        recursively_validate_schema(schema, values)
        

    def get_metadata(self):
        return self.metadata

    def get_config(self, key):
        return self.model_config.get(key)

    def get_messages(self, values=None):
        current_message = None
        messages = []

        for line in self.prompt_template.splitlines():
            maybe_match = role_re.match(line)
            if maybe_match:
                if current_message:
                    messages.append({**current_message})

                current_message = {'role': maybe_match.group(1), 'content': ''}
            elif current_message:
                if len(current_message['content']) > 0:
                    current_message['content'] += '\n'
                current_message['content'] += line

        if current_message:
            messages.append(current_message)

        return [{'role': item['role'], 'content': render_handlebars(item['content'],
                                                                    self.get_rendered_values(values))}
                 for item in messages]
        

    def get_rendered_values(self, vals):
        values =  recursively_merge_dicts(self.metadata.get('input', {}).get('default', {}), vals)
        self.validate_schema(values)
        return values

    def complete(self, vals):
        if self.model_vendor == 'openai':
            from openai import OpenAI

            config = self.metadata.get('config')
            client = OpenAI(api_key=config.get('api_key'))

            completion = client.chat.completions.create(
                messages=self.get_messages(vals),
                model=self.model_name,
                temperature=config.get('temperature'),
            )

            return completion.choices[0].message.content
        raise ValueError('Only openai currently supports this shortcut')


def render_handlebars(content, values):
    from pybars import Compiler
    compiler = Compiler()

    template = compiler.compile(content)

    return template(values)


def recursively_merge_dicts(target_v, overlaying_v):
    if type(target_v) is dict:
        for k, v in overlaying_v.items():
            if type(v) is dict:
                target_v[k] = recursively_merge_dicts(target_v.get(k), overlaying_v[k])
            else:
                target_v[k] = v
        return target_v
    return overlaying_v


schema_key_regex = re.compile(r'([A-Za-z_\-]+)(\?)?(\(.+\))?')
def recursively_validate_schema(schema, values, prefix=''):
    for schema_k, schema_v in schema.items():
        result = schema_key_regex.match(schema_k)

        identifier = result.group(1)
        current_value = values.get(identifier)

        is_optional = result.group(2) is not None
        options_raw = result.group(3)
        nested_type = None
        description = None

        is_array = False
        is_enum = False
        is_object = False

        if options_raw:
            splitted_options = options_raw[1:-1].split(",", 1)
            nested_type = splitted_options[0].strip()

            if nested_type == 'enum':
                is_enum = True
            elif nested_type == 'object':
                is_object = True
            elif nested_type == 'array':
                is_array = True

            if(len(splitted_options) > 1):
                description = splitted_options[1]

            if(len(splitted_options) > 2):
                raise ValueError(f'Unexpected amount of options: {options_raw}')

        if not is_optional and current_value is None:
            raise ValueError(f'value of {prefix+identifier} is not marked as optional but is None')

        if is_optional and current_value is None:
            continue

        if is_object:
            if type(current_value) is dict:
                recursively_validate_schema(schema_v, current_value, prefix=prefix+identifier+'/')
            else:
                raise ValueError(f'value is expected to be an object but instead is {current_value}')

        elif is_array:
            if type(current_value) is list:
                for item in current_value:
                    if validate_scalar(schema_v, item):
                        continue

                    if not type(item) is dict:
                        raise ValueError(f'Expected "{schema_k}" item to be object, got {type(item)} instead')

                    recursively_validate_schema(schema_v, item, prefix=prefix+identifier+'/')
            else:
                raise ValueError(f'value of {prefix+identifier} expected to be an array but instead is {current_value}')

        elif is_enum:
            enum_values = set(schema_v)
            if current_value not in enum_values:
                raise ValueError(f'value of "{prefix+identifier}" expected to be {schema_v} but instead is {type(current_value)}')
        else:
            if not validate_scalar(schema_v, current_value):
                raise ValueError(f'value of "{prefix+identifier}" expected to be {schema_v} but instead is {type(current_value)}')
                
                


def validate_scalar(schema_type, value):
    if schema_type == 'string' and type(value) is str:
        return True
    if schema_type == 'integer' and type(value) is int:
        return True
    if schema_type == 'boolean' and type(value) is bool:
        return True
    if schema_type == 'number' and type(value) is float:
        return True
    if schema_type == 'any':
        return True

    return False
