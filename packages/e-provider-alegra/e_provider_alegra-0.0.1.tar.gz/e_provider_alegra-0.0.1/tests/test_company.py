import unittest
from unittest.mock import Mock, patch

from alegra.client import ApiClient
from alegra.config import ApiConfig
from alegra.models.company import (
    Address,
    Certificate,
    Company,
    GovernmentStatus,
    NotificationByEmail,
    Webhook,
    Webhooks,
)


class TestCompanyResource(unittest.TestCase):
    def setUp(self):
        self.config = ApiConfig(
            api_key="ce5PgRbegtMgcwt9pPnPYNpCNuy0Nxmm5ohKZHSU", environment="sandbox"
        )
        self.client = ApiClient(self.config)

    def test_create_company(self):
        company_data = Company(
            name="Soluciones Alegra S.A.S",
            identification="111111111",
            dv="2",
            useAlegraCertificate=True,
            governmentStatus=GovernmentStatus(payrolls="AUTHORIZED"),
            organizationType=1,
            identificationType="31",
            regimeCode="R-99-PN",
            email="email@email.com",
            phone="1234567890",
            address=Address(
                address="Cra. 13 #12-12 Edificio A & A",
                city="11001",
                department="11",
                country="CO",
            ),
        )

        company = self.client.companies.create(company_data)

        self.assertEqual(company.name, "Soluciones Alegra S.A.S")
        self.assertEqual(company.identification, "111111111")
        self.assertEqual(company.dv, "2")
        self.assertTrue(company.useAlegraCertificate)
        self.assertEqual(company.organizationType, 1)
        self.assertEqual(company.identificationType, "31")
        self.assertEqual(company.regimeCode, "R-99-PN")
        self.assertEqual(company.email, "email@email.com")
        self.assertEqual(company.address.address, "Cra. 13 #12-12 Edificio A & A")
        self.assertEqual(company.address.city, "11001")
        self.assertEqual(company.address.department, "11")
        self.assertEqual(company.address.country, "CO")
