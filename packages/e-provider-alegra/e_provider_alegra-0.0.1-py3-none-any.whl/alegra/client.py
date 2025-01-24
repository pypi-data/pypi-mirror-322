import requests
import httpx

from alegra.config import ApiConfig
from alegra.models.company import Company
from alegra.models.dian import DianResource
from alegra.models.invoice import Invoice, InvoiceResponse, FileResponse
from alegra.models.payroll import Payroll
from alegra.models.test_set import TestSet
from alegra.resources.factory import ResourceFactory


class ApiClient:
    def __init__(self, config: ApiConfig, async_mode=False):
        self.config = config
        self.base_url = self.config.get_base_url()
        self.async_mode = async_mode
        self._initialize_resources()

    async def _async_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.config.api_key}"}, timeout=30.0
        ) as client:
            response = await client.request(method, url, **kwargs)
            return response.json()

    def _sync_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        with requests.Session() as session:
            session.headers.update({"Authorization": f"Bearer {self.config.api_key}"})
            response = session.request(method, url, **kwargs)
            return response.json()

    def _request(self, method, endpoint, **kwargs):
        if self.async_mode:
            return self._async_request(method, endpoint, **kwargs)
        else:
            return self._sync_request(method, endpoint, **kwargs)

    def _initialize_resources(self):
        self.company = ResourceFactory(
            self,
            "company",
            self._request,
            {
                "get": {
                    "model": Company,
                    "response_model": Company,
                    "response_key": "company",
                },
                "update": {
                    "model": Company,
                    "response_model": Company,
                    "response_key": "company",
                },
            },
        )
        self.companies = ResourceFactory(
            self,
            "companies",
            self._request,
            {
                "create": {
                    "model": Company,
                    "response_model": Company,
                    "response_key": "company",
                },
                "get": {
                    "model": Company,
                    "response_model": Company,
                    "response_key": "company",
                },
                "update": {
                    "model": Company,
                    "response_model": Company,
                    "response_key": "company",
                },
                "list": {
                    "model": Company,
                    "response_model": Company,
                    "response_key": "companies",
                },
            },
        )
        self.payrolls = ResourceFactory(
            self,
            "payrolls",
            self._request,
            {
                "create": {"model": Payroll, "response_key": "payroll"},
                "get": {"model": Payroll, "response_key": "payroll"},
                "update": {"model": Payroll, "response_key": "payroll"},
                "list": {"model": Payroll, "response_key": "payrolls"},
                "perform__replace": {"model": Payroll, "response_key": "payroll"},
                "perform__cancel": {"model": Payroll, "response_key": "payroll"},
            },
        )
        self.dian = ResourceFactory(
            self,
            "dian",
            self._request,
            {"list": {"model": DianResource, "response_key": "dian"}},
        )
        self.test_sets = ResourceFactory(
            self,
            "test-sets",
            self._request,
            {
                "create": {"model": TestSet, "response_key": "test_set"},
                "get": {"model": TestSet, "response_key": "test_set"},
            },
        )
        self.invoices = ResourceFactory(
            self,
            "invoices",
            self._request,
            {
                "create": {
                    "model": Invoice,
                    "response_model": InvoiceResponse,
                    "response_key": "invoice",
                },
                "get": {
                    "model": Invoice,
                    "response_model": InvoiceResponse,
                    "response_key": "invoice",
                },
                "perform__file_xml": {
                    "model": FileResponse,
                    "endpoint_suffix": "files/XML",
                    "response_model": FileResponse,
                    "response_key": "file",
                },
                "list": {
                    "model": InvoiceResponse,
                    "response_model": InvoiceResponse,
                    "response_key": "invoices",
                },
            },
        )
