from collections.abc import Mapping
from typing import Literal, Optional
from planning_center_python.api._pco_service import PcoService
from planning_center_python.models._pagination_params import PaginationParams
from planning_center_python.models.person import Person


class PersonService(PcoService):
    class UrlParams(Mapping[str, str]):
        include: list[
            Literal[
                "addresses",
                "emails",
                "field_data",
                "households",
                "inactive_reason",
                "marital_status",
                "name_prefix",
                "name_suffix",
                "organization",
                "person_apps",
                "phone_numbers",
                "platform_notifications",
                "primary_campus",
                "school",
                "social_profiles",
            ]
        ]
        order: Literal[
            "accounting_administrator",
            "anniversary",
            "birthdate",
            "child",
            "given_name",
            "grade",
            "graduation_year",
            "last_name",
            "middle_name",
            "nickname",
            "people_permissions",
            "site_administrator",
            "gender",
            "inactivated_at",
            "created_at",
            "updated_at",
            "first_name",
            "remote_id",
            "membership",
            "status",
        ]
        pagination: PaginationParams
        # query_params:

    def get(self, id: str, params: Optional[UrlParams] = None) -> Person:
        response = self._request("GET", f"{Person.OBJECT_URL}/{id}", params)
        return Person(response.data)
