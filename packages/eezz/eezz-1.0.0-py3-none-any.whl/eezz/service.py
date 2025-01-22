# -*- coding: utf-8 -*-
"""
    This module implements the following classes:

    * **TService**: A singleton for TGlobalService
    * **TServiceCompiler**: A Lark compiler for HTML EEZZ extensions
    * **TTranslate**: Extract translation info from HTML to create a POT file
    * **TQuery**: Class representing the query of an HTML request

"""
from    dataclasses import dataclass
from    loguru      import logger

import  re
import  itertools
import  json
import  sys
from    bs4                 import Tag, BeautifulSoup
from    pathlib             import Path
from    importlib           import import_module, reload
from    lark                import Lark, Transformer, Tree, UnexpectedInput
from    lark.exceptions     import UnexpectedCharacters
from    typing              import Any, TypeVar
from    Crypto.PublicKey    import RSA

T = TypeVar('T')


class TService:
    """ Container for unique environment as

    * path descriptors
    * stores assignments of the parser
    * stores RSA application key
    """
    _mod = int("C5F23FA172317A1F6930C0F9AF79FF044D34BFD1336E5A174155953487A4FF0C744A093CA7044F39842AC685AB37C55F1F01F0055561BAD9C3EEA22B28D09F061875ED5BDB2F1F2B797B1BEF6534C0D4FCEFAFFA8F3A91396961165241564BD6E3CA08023F2A760A0B54A4A6A996CDF7DE3491468C199566EE5993FCFD03A2B285AD6FBBC014A20C801618EE19F88EB8E6359624A35FDD7976F316D6AB225CF85DA5E63AB30248D38297A835CF16B9799973C2F9F05F5F850B3152B3A05F06FEC0FBDA95C70911F59F6A11A1451822ABFE4FE5A021F7EA983BDE9F442302891DCF51B7322EAFB88950F2617B7120F9B87534719DCA27E87D82A183CB37BC7045", 16)
    _exp = int("10001", 16)
    _private_key:       RSA.RsaKey  = None          #: :meta private:
    _public_key:        RSA.RsaKey  = None          #: :meta private:
    _root_path:         Path        = None          #: :meta private: Root path for the HTTP server
    _resource_path:     Path        = None          #: :meta private:
    _global_objects:    dict        = None          #: :meta private:
    _host:              str         = 'localhost'   #: :meta private:
    _websocket_addr:    str         = '8100'        #: :meta private:
    _translate:         bool        = False         #: :meta private:

    @property
    def private_key(self) -> RSA.RsaKey:
        """ :meta private: """
        if not TService._private_key:
            TService._private_key = RSA.construct((TService._mod, TService._exp))
        return TService._private_key

    @property
    def public_key(self) -> RSA.RsaKey:
        """ :meta private: """
        if not TService._public_key:
            TService._public_key  = self.private_key.public_key()
        return TService._public_key

    @property
    def root_path(self) -> Path:
        """ :meta private: """
        if not TService._root_path:
            TService._root_path = Path.cwd()
        return TService._root_path

    @property
    def resource_path(self) -> Path:
        """ :meta private: """
        return self.root_path / 'resources'

    @property
    def public_path(self) -> Path:
        """ :meta private: """
        return self.root_path

    @property
    def application_path(self) -> Path:
        """ :meta private: """
        return self.root_path / 'applications'

    @property
    def document_path(self) -> Path:
        """ :meta private: """
        return self.root_path / 'database'

    @property
    def database_path(self) -> Path:
        """ :meta private: """
        return self.document_path / 'eezz.db'

    @property
    def locales_path(self) -> Path:
        """ :meta private: """
        return self.resource_path / 'locales'

    @property
    def logging_path(self) -> Path:
        """ :meta private: """
        return self.root_path / 'logs'

    @property
    def host(self) -> str:
        """ :meta private: """
        return TService._host

    @property
    def websocket_addr(self) -> str:
        """ :meta private: """
        return TService._websocket_addr

    @property
    def objects(self) -> dict:
        """ :meta private: """
        if not TService._global_objects:
            TService._global_objects = dict()
        return TService._global_objects

    @property
    def translate(self):
        """ :meta private: """
        return TService._translate

    @classmethod
    def set_environment(cls, root_path: str, host: str = 'localhost', address: str = '8000'):
        """ :meta private: """
        cls._root_path      = Path(root_path).absolute()
        cls._host           = host
        cls._websocket_addr = address

        #  application_path    = cls._root_path / 'applications'
        #  sys.path.append(application_path.as_posix())

    def get_method(self, obj_id: str, a_method_name: str) -> tuple:
        """ Get a method by name for a given object

        :param str obj_id:          Unique hash-ID for object as stored in :py:meth:`eezz.service.TService.assign_object`
        :param str a_method_name:   Name of the method
        :return:    tuple(object, method, parent-tag)
        :raise      AttributeError: Class has no method with the given name
        """
        try:
            x_object, x_tag, x_descr = self.objects[obj_id]
            x_method = getattr(x_object, a_method_name)
            return x_object, x_method, x_tag, x_descr
        except AttributeError as x_except:
            logger.exception(x_except)
            raise x_except

    def assign_object(self, obj_id: str, description: str, attrs: dict, a_tag: Tag = None, force_reload: bool = False) -> None:
        """ _`assign_object` Assigns an object to an HTML tag

        :param str      obj_id:         Unique object-id
        :param str      description:    Path to the class: <directory>.<module>.<class>
        :param dict     attrs:          Attributes for the constructor
        :param bs4.Tag  a_tag:          Parent tag which handles an instance of this object
        :param bool     force_reload:   Force reloading
        :raise AttributeError:  Class not found
        :raise IndexError:      description systax does not match
        """
        try:
            x_list  = description.split('.')
            x, y, z = x_list[0], x_list[1], x_list[2]
        except IndexError as x_except:
            logger.exception(f'Check assign specification: package.module.class versus {description}')
            raise x_except

        x_path = self.application_path
        if not str(x_path) in sys.path:
            sys.path.append(str(x_path))

        try:
            x_module    = import_module(f'{x}.{y}')
            if force_reload:
                x_module = reload(x_module)

            x_class     = getattr(x_module, z)
            x_object    = x_class(**attrs) if attrs else x_class()
            self.objects.update({obj_id: (x_object, a_tag, description)})
            logger.debug(f'assign {obj_id} {x}/{y}/{z}')
        except AttributeError as x_except:
            logger.exception(x_except)
        except ModuleNotFoundError as x_except:
            logger.critical(x_except)
            exit(0)

    def get_object(self, obj_id: str) -> Any:
        """ Get the object for a given ID

        :param str obj_id: Unique hash-ID for object as stored in :func:`eezz.service.TGlobalService.assign_object`
        :return: The assigned object
        """
        x_object, x_tag, x_descr = self.objects[obj_id]
        return x_object

    def get_tag_ref(self, obj_id: str) -> Any:
        """ Get Tag and descriptor for a given object ID

        :param str  obj_id:  Object ID
        :return:    Tag and descriptor
        :rtype:     dict
        """
        x_object, x_tag, x_descr = self.objects[obj_id]
        return x_tag, x_descr


class TServiceCompiler(Transformer):
    """ Transforms the parser tree into a list of dictionaries
    The transformer output is in json format

    :param bs4.Tag  a_tag:      The parent tag
    :param str      a_id:       A unique object id
    :param dict     a_query:    The URL query part
    """
    def __init__(self, a_tag: Tag, a_id: str = '', a_query: dict = None):
        super().__init__()
        self.m_id       = a_id
        self.m_tag      = a_tag
        self.m_query    = a_query
        self.m_service  = TService()

    @staticmethod
    def simple_str(item):
        """ :meta private: Parse a string token """
        return ''.join([str(x) for x in item])

    @staticmethod
    def escaped_str(item):
        """ :meta private: Parse an escaped string """
        return ''.join([x.strip('"') for x in item])

    @staticmethod
    def qualified_string(item):
        """ :meta private: Parse a qualified string: ``part1.part2.part3`` """
        return '.'.join([str(x) for x in item])

    @staticmethod
    def selector_string(item):
        """ :meta private: """
        return f"[{'.'.join(item)}]"

    @staticmethod
    def array_element(item):
        """ :meta private: """
        return item

    def set_style(self, item):
        """ :meta private: """
        x_style_dict = dict()

        if x_style := self.m_tag.attrs.get('style'):
            x_style_dict = {y[0]: y[1] for y in [x.split(':') for x in x_style.strip(';').split(';')]}
        x_style_dict.update({item[0]: item[1]})
        self.m_tag.attrs['style'] = ';'.join([f'{x}:{y}' for x, y in x_style_dict.items()])
        return {}

    @staticmethod
    def setenv(item):
        """ :meta private: """
        return {item[0]: item[1]}

    @staticmethod
    def list_updates(item):
        """ :meta private: Accumulate 'update' statements """
        return list(itertools.accumulate(item, lambda a, b: a | b))[-1]

    @staticmethod
    def list_arguments(item):
        """ :meta private: Accumulate arguments for function call """
        return list(itertools.accumulate(item, lambda a, b: a | b))[-1]

    def onload_section(self, item):
        """ :meta private: """
        self.m_tag['data-eezz-onload'] = 'eezzy_onload(this)'
        return {'onload': item[0]}

    @staticmethod
    def update_section(item):
        """ :meta private: Parse 'update' section """
        return {'update': item[0]}

    @staticmethod
    def update_item(item):
        """ :meta private: Parse 'update' expression"""
        return {item[0]: item[1]} if len(item) == 2 else {item[0]: item[0]}

    @staticmethod
    def update_task(item):
        """ :meta private: """
        x_function, x_args = item[0].children
        return {'call': {'function': x_function, 'args': x_args}}

    def update_function(self, item):
        """ :meta private: """
        x_function, x_args = item[1].children
        return {item[0]: {'function': x_function, 'args': x_args, 'id': self.m_id}}

    @staticmethod
    def assignment(item):
        """ :meta private: Parse 'assignment' expression: ``variable = value`` """
        return {item[0]: item[1]}

    @staticmethod
    def format_string(item):
        """ :meta private: Create a format string: ``{value}`` """
        return f'{{{".".join(item)}}}'

    @staticmethod
    def format_value(item):
        """ :meta private: Create a format string: ``{key.value}`` """
        return  f'{{{".".join([str(x[0]) for x in item[0].children])}}}'

    def template_section(self, item):
        """ :meta private: Create tag attributes """
        template = {'data-eezz-template': item[0]}
        self.m_tag['data-eezz-template'] = item[0]
        if len(item) > 1:
            template['data-eezz-reference']   = item[1]
            self.m_tag['data-eezz-reference'] = item[1]
        return template

    def parameter_section(self, item):
        """ :meta private: Create tag attributes """
        if item[0] in ('name', 'match', 'file', 'progress', 'type'):
            self.m_tag[f'data-eezz-{item[0]}'] = item[1]
            return {item[0]: item[1]}
        if item[0] in 'format' and item[1] in ('br', 'p'):
            self.m_tag[f'data-eezz-{item[0]}'] = '<br>' if item[1] == 'br' else '</p><p>'
            return {item[0]: item[1]}
        if item[0] in 'process' and item[1] in 'sync':
            return {item[0]: item[1]}
        raise UnexpectedInput(f'parameter section: {item[0]} = {item[1]}')
        # return {item[0]: item[1]}

    def funct_assignment(self, item):
        """ :meta private: Parse 'function' section """
        x_function, x_args = item[0].children
        self.m_tag['onclick'] = 'eezzy_click(event, this)'
        return {'call': {'function': x_function, 'args': x_args, 'id': self.m_id}}

    def post_init(self, item):
        """ :meta private: Parse 'post-init' section for function assignment """
        x_method_name, x_method_args = item[0].children
        x_obj, x_method, x_tag, x_descr = TService().get_method(self.m_id, x_method_name)
        x_method(**x_method_args) if x_method_args else x_method()
        return {'oninit': 'done'}

    def table_assignment(self, item):
        """ :meta private: Parse 'assign' section, assigning a Python object to an HTML-Tag
        The table assignment uses TQuery to format arguments
        In case the arguments are not all present, the format is broken and process continues with default """
        x_function, x_args = item[0].children

        try:
            x_query = TQuery(self.m_query)
            x_args  = {x_key: x_val.format(query=x_query) for x_key, x_val in x_args.items()} if x_args else {}
        except AttributeError as x_except:
            logger.error(f'table_assignment {x_except}: {x_function}, {x_args}')
        TService().assign_object(self.m_id, x_function, x_args, self.m_tag)
        return {'assign': {'function': x_function, 'args': x_args, 'id': self.m_id}}


class TTranslate:
    """ The class TTranslate executes the EEZZ grammar and translates the input to a JSON object """
    @staticmethod
    def generate_pot(a_soup, a_title):
        """ :meta private: Generate a POT file from HTML file

        :param a_soup: The HTML page for translation
        :param a_title: The file name for the POT file
        """
        " todo: argument a_tile must be a a simple string  "
        x_regex = re.compile('[a-zA-Z0-9]+')
        x_group = x_regex.findall(a_title)
        if not x_group:
            logger.error(f'Cannot create file {a_title}')

        try:
            x_pot_file = TService().locales_path / f'{x_group[0]}.pot'
            x_elements = a_soup.find_all(lambda x_tag: x_tag.has_attr('data-eezz-i18n'))
            x_path_hdr = TService().locales_path / 'template.pot'
            with x_pot_file.open('w', encoding='utf-8') as f:
                with x_path_hdr.open('r', encoding='utf-8') as f_hdr:
                    f.write(f_hdr.read())
                for x_elem in x_elements:
                    f.write(f"msgid  \"{x_elem['data-eezz-i18n']}\"\n"
                            f"msgstr \"{[str(x) for x in x_elem.descendants]}\"\n\n")
        except FileNotFoundError as x_except:
            logger.exception(x_except)
            raise x_except


# @dataclass(kw_only=True)
class TQuery:
    """ :meta private: Transfer the HTTP query to class attributes

    :param query: The query string in dictionary format
    """
    m_query: dict = None

    def __init__(self, query: dict):
        if not TQuery.m_query:
            TQuery.m_query = query

        if query:
            for x_key, x_val in query.items():
                setattr(self, x_key, ','.join(x_val))

    @property
    def query(self) -> dict:
        return TQuery.m_query


# --- Section for module tests
def test_parser(source: str) -> json:
    """ :meta private: """

    html = '<td style="font-size: .8em; font-family: monospace; background-color: rgb(244, 244, 244);"></td>'
    html = """ <area shape="rect" coords="  0, 0,  40, 20" data-eezz="event:  navigate(where_togo = 3), update: this.tbody"/>"""
    # Create soup from html
    soup           = BeautifulSoup(html, 'html.parser')
    x_parent_tag   = soup.area
    x_parser       = Lark.open(str(TService().resource_path / 'eezz.lark'))

    try:
        x_syntax_tree  = x_parser.parse(source)
        x_transformer  = TServiceCompiler(x_parent_tag, 'Directory')
        x_list_json    = x_transformer.transform(x_syntax_tree)

        logger.debug(x_parent_tag.prettify())
        if type(x_list_json) is Tree:
            x_result = list(itertools.accumulate(x_list_json.children, lambda a, b: a | b))[-1]
            logger.debug(x_result)
            return x_result
        else:
            x_res = dict()
            for x_key, x_val in x_list_json.items():
                x_result = x_val
                # if type(x_val) is Tree:
                #  x_result = list(itertools.accumulate(x_val.children, lambda a, b: a | b))[-1]
                # x_res[x_key] = x_result
            logger.debug(x_list_json)
            return x_list_json
    except UnexpectedCharacters as x_ex:
        logger.error(f'invalid expression: parent-tag={x_parent_tag.name}, position={x_ex.pos_in_stream}', stack_info=True, stacklevel=3)
        raise x_ex


@dataclass
class TestRow:
    """:meta private:"""
    path:   str = 'test/path/file'
    row_id: int = 100


def test_parser_area():
    """:meta private:"""
    source = """ format: p,  event:  navigate(where_togo = 3), update: this.tbody  """
    test_parser(source=source)


if __name__ == '__main__':
    """ :meta private: """
    # test parser
    TService.set_environment(root_path='/Users/alzer/Projects/github/eezz_full/webroot')

    logger.debug(f'{TService().resource_path=}')
    logger.debug("Test Lark Parser")

    test_parser_area()

    logger.debug("assign statement")
    x_source = """assign: examples.directory.TDirView(title="", path="/Users/alzer/Projects/github/eezz_full/webroot")"""
    test_parser(source=x_source)

    logger.debug("update statement 1")
    x_source = """ event: on_select(row={row.row_id}), update: elem1.innerHTML = {object.path} """
    test_parser(source=x_source)

    logger.debug("update statement 2")
    x_source = """ event: on_select(row={row.row_id}), update: elem1.innerHTML = {object.path}, elem2.innerHTML = {object.row_id}  """
    x_result = test_parser(source=x_source)
    logger.debug(x_result)

    x_source = 'name: directory, assign: examples.directory.TDirView(path=".", title="dir"), process:sync'
    x_result = test_parser(source=x_source)
    logger.debug(x_result)

    x_source = "event: FormInput.append(table_row = [field_index.value]), reference: cell.title"
    x_result = test_parser(source=x_source)
    logger.debug(x_result)

    x_source = """ 
                        template: cell (main), 
                        onload:   this.src = read_file(document_title={cell.attrs},file_name={cell.value}) """

    x_result = test_parser(source=x_source)
    logger.debug(f'{x_source} ==> {x_result}')

    logger.success('test finished')
    """
    # test parser exception and logging
    logger.debug(msg="Test the parser: wrong download statement:")
    logger.debug(msg="download: files(name=test1, author=albert), documents( main=main, prev=prev )")

    try:
        test_parser(source=""download: files(name=test1, author=albert), documents( main=main, prev=prev )"")
    except UnexpectedCharacters as xx_except:
        logger.error(msg='Test parser exception successful', stack_info=True)
"""