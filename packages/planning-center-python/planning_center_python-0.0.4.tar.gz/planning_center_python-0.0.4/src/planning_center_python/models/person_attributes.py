from datetime import date, datetime
from pydantic import BaseModel


class PersonAttributes(BaseModel):
    avatar: str
    demographic_avatar_url: str
    first_name: str
    name: str
    status: str
    remote_id: int
    accounting_administrator: bool
    anniversary: date
    birthdate: date
    child: bool
    given_name: str
    grade: int
    graduation_year: int
    last_name: str
    middle_name: str
    nickname: str
    people_permissions: str
    site_administrator: bool
    gender: str
    inactivated_at: datetime
    medical_notes: str
    membership: str
    created_at: datetime
    updated_at: datetime
    can_create_forms: bool
    can_email_lists: bool
    directory_status: str
    passed_background_check: bool
    school_type: str
    mfa_configured: bool
