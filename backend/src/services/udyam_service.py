from datetime import datetime, date
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import UdyamApplication, GSTINStatus, YesNo
from enum import Enum

TYPE_OF_ORGANISATION_MAP = {
    "1": "Proprietary / एकल स्वामित्व",
    "2": "Hindu Undivided Family / हिंदू अविभाजित परिवार (एचयूएफ)",
    "3": "Partnership / पार्टनरशिप",
    "4": "Co-Operative / सहकारी",
    "5": "Private Limited Company / प्राइवेट लिमिटेड कंपनी",
    "6": "Public Limited Company / पब्लिक लिमिटेड कंपनी",
    "7": "Self Help Group / स्वयं सहायता समूह",
    "9": "Limited Liability Partnership / सीमित दायित्व भागीदारी",
    "10": "Society / सोसाईटी",
    "11": "Trust / ट्रस्ट",
    "8": "Others / अन्य",
}

def make_json_safe(data: dict):
    """Convert Enums and dates to JSON-serializable values."""
    def convert(value):
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        if isinstance(value, list):
            return [convert(v) for v in value]
        return value
    return convert(data)

class UdyamService:
    async def submit_registration(self, app_id, form_payload: dict, session: AsyncSession):
        stmt = select(UdyamApplication).where(UdyamApplication.id == app_id)
        app = (await session.exec(stmt)).first()

        if not app:
            raise ValueError("Application not found")

        # Entrepreneur name
        app.entrepreneur_name = form_payload.get("entrepreneurName")

        # Map type_of_organisation from numeric to text
        org_value = form_payload.get("typeOfOrganisation")
        if org_value in TYPE_OF_ORGANISATION_MAP:
            app.type_of_organisation = TYPE_OF_ORGANISATION_MAP[org_value]
        else:
            app.type_of_organisation = org_value

        # DOB / DOI
        app.dob_or_doi = form_payload.get("dobOrDoi")

        # Previous year ITR
        prev_itr = form_payload.get("previousYearITR")
        if prev_itr in (YesNo.YES.value, YesNo.NO.value):
            app.previous_year_itr_filed = (prev_itr == YesNo.YES.value)

        # GSTIN status
        gst = form_payload.get("hasGSTIN")
        if gst in (GSTINStatus.YES.value, GSTINStatus.NO.value, GSTINStatus.EXEMPTED.value):
            app.has_gstin_status = GSTINStatus(gst)

        # ✅ Store JSON-safe payload
        app.form_payload = make_json_safe(form_payload)

        app.status = "submitted"
        app.updated_at = datetime.utcnow()

        await session.commit()

        return {"registrationId": str(app.id), "status": app.status}
