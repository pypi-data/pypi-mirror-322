'''
This module defines the XML Reader.

Extraction is based on BeautifulSoup.
'''

import bs4
import logging
from os.path import isfile
from requests import Response
from typing import Dict, Iterable, Tuple, List

from .. import extract
from .core import Reader, Source, Document, Field
from ..xml_tag import CurrentTag, resolve_tag_specification, TagSpecification


logger = logging.getLogger()

class XMLReader(Reader):
    '''
    A base class for Readers that extract data from XML files.

    The built-in functionality of the XML reader is quite versatile, and can be further
    expanded by adding custom Tag classes or extraction functions that interact directly with
    BeautifulSoup nodes.

    The Reader is suitable for datasets where each file should be extracted as a single
    document, or ones where each file contains multiple documents.

    In addition to generic extractor classes, this reader supports the `XML` extractor.

    Attributes:
        tag_toplevel: the top-level tag to search from in source documents.
        tag_entry: the tag that corresponds to a single document entry in source
            documents.
        external_file_tag_toplevel: the top-level tag to search from in external
            documents (if that functionality is used)

    '''

    tag_toplevel: TagSpecification = CurrentTag()
    '''
    The top-level tag in the source documents.

    Can be:

    - An XMLTag
    - A callable that takes the metadata of the document as input and returns an
        XMLTag.
    '''

    tag_entry: TagSpecification = CurrentTag()
    '''
    The tag that corresponds to a single document entry.

    Can be:

    - An XMLTag
    - A callable that takes the metadata of the document as input and returns an
        XMLTag
    '''

    external_file_tag_toplevel: TagSpecification = CurrentTag()
    '''
    The toplevel tag in external files (if you are using that functionality).

    Can be:

    - An XMLTag
    - A callable that takes the metadata of the document as input and returns an
        XMLTag. The metadata dictionary includes the values of "regular" fields for
        the document.
    '''

    def source2dicts(self, source: Source) -> Iterable[Document]:
        '''
        Given an XML source file, returns an iterable of extracted documents.

        Parameters:
            source: the source file to extract. This can be a string with the path to
                the file, or a tuple with a path and a dictionary containing metadata.
        
        Returns:
            an iterable of document dictionaries. Each of these is a dictionary,
                where the keys are names of this Reader's `fields`, and the values
                are based on the extractor of each field.
        '''
        # Make sure that extractors are sensible
        self._reject_extractors(extract.CSV)

        filename, soup, metadata = self._filename_soup_and_metadata_from_source(source)

        # split fields that read an external file from regular fields
        external_fields = [field for field in self.fields if
            isinstance(field.extractor, extract.XML) and field.extractor.external_file
        ]
        regular_fields = [field for field in self.fields if
            field not in external_fields
        ]

        # extract information from external xml files first, if applicable
        if len(external_fields):
            if  metadata and 'external_file' in metadata:
                external_soup = self._soup_from_xml(metadata['external_file'])
            else:
                logger.warn(
                    'Some fields have external_file property, but no external file is '
                    'provided in the source metadata'
                )
                external_soup = None        

        required_fields = [
            field.name for field in self.fields if field.required]

        # iterate through entries
        top_tag = resolve_tag_specification(self.__class__.tag_toplevel, metadata)
        bowl = top_tag.find_next_in_soup(soup)

        if bowl:
            entry_tag = resolve_tag_specification(self.__class__.tag_entry, metadata)
            spoonfuls = entry_tag.find_in_soup(bowl)
            for i, spoon in enumerate(spoonfuls):
                # Extract fields from the soup
                field_dict = {
                    field.name: field.extractor.apply(
                        soup_top=bowl,
                        soup_entry=spoon,
                        metadata=metadata,
                        index=i,
                    ) for field in regular_fields if not field.skip
                }

                if external_fields and external_soup:
                    metadata.update(field_dict)
                    external_dict = self._external_source2dict(
                        external_soup, external_fields, metadata)
                else:
                    external_dict = {
                        field.name: None
                        for field in external_fields
                    }

                # yield the union of external fields and document fields
                field_dict.update(external_dict)
                if all(field_name in field_dict for field_name in required_fields):
                    yield field_dict
        else:
            logger.warning(
                'Top-level tag not found in `{}`'.format(filename))

    def _external_source2dict(self, soup, external_fields: List[Field], metadata: Dict):
        '''
        given an external xml file with metadata,
        return a dictionary with tags which were found in that metadata
        wrt to the current source.
        '''
        tag = resolve_tag_specification(self.__class__.external_file_tag_toplevel, metadata)
        bowl = tag.find_next_in_soup(soup)

        if not bowl:
            logger.warning(
                'Top-level tag not found in `{}`'.format(metadata['external_file']))
            return {field.name: None for field in external_fields}

        return {
            field.name: field.extractor.apply(
                soup_top=bowl, soup_entry=bowl, metadata=metadata
            )
            for field in external_fields
        }

    def _filename_soup_and_metadata_from_source(self, source: Source) -> Tuple[str, bs4.BeautifulSoup, Dict]:
        if isinstance(source, str):
            filename = source
            soup = self._soup_from_xml(filename)
            metadata = {}
        elif isinstance(source, bytes):
            soup = self._soup_from_data(source)
            filename = None
            metadata = {}
        elif isinstance(source, Response):
            soup = self._soup_from_data(source.text)
            filename = None
            metadata = {}
        else:
            if isinstance(source[0], str):
                filename = source[0]
                soup = self._soup_from_xml(filename)
            else:
                filename = None
                if isinstance(source[0], bytes):
                    soup = self._soup_from_data(source[0])
                elif isinstance(source[0], Response):
                    soup = self._soup_from_data(source[0].text)
            metadata = source[1] or None
        return filename, soup, metadata

    def _soup_from_xml(self, filename):
        '''
        Returns beatifulsoup soup object for a given xml file
        '''
        # Loading XML
        logger.info('Reading XML file {} ...'.format(filename))
        with open(filename, 'rb') as f:
            data = f.read()
        logger.info('Loaded {} into memory...'.format(filename))
        return self._soup_from_data(data)

    def _soup_from_data(self, data):
        '''
        Parses content of a xml file
        '''
        return bs4.BeautifulSoup(data, 'lxml-xml')
