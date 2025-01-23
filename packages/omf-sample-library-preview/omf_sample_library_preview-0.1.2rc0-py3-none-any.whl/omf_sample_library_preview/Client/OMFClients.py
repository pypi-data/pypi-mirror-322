from __future__ import annotations

from ..Models.OMFMessageAction import OMFMessageAction
from ..Models.OMFMessageType import OMFMessageType
from ..Models.OMFData import OMFData

from ..Models.OMFMessageAction import OMFMessageAction
from ..Models.OMFMessageType import OMFMessageType
from ..Models.OMFContainer import OMFContainer
from ..Models.OMFData import OMFData
from ..Models.OMFLinkData import OMFLinkData
from ..Models.OMFMessageAction import OMFMessageAction
from ..Models.OMFMessageType import OMFMessageType
from ..Models.OMFType import OMFType

import gzip
import json
import logging

from .OMFClient import OMFClient

import requests


class OMFClients(object):
    """Handles communication with OMF Endpoints."""

    def __init__(
        self):
        self.__OMFClient: list[OMFClient] = []
        

    @property
    def Clients(self) -> list[OMFClient]:
        """
        Gets the base url
        :return:
        """
        return self.__OMFClient

    def addClient(
        self,
        client: OMFClient,
    ) -> requests.Response:
        """
        """
        self.__OMFClient.append(client)  
    
    def omfRequests(
        self,
        message_type: OMFMessageType,
        action: OMFMessageAction,
        omf_data: list[OMFType | OMFContainer | OMFData | OMFLinkData],
    ) -> requests.Response:
        """
        Base OMF request function
        :param message_type: OMF message type
        :param action: OMF action
        :param omf_data: OMF data
        :return: Http response
        """         
        compressed_body = OMFClient.compressOMFMessage(omf_data)

        for client in self.__OMFClient:
            client.omfRequest(message_type,action,compressed_body)
    
