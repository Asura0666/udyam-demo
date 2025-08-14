import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from typing import Optional, Any
from sqlmodel import (
    Column,
    Field,
    SQLModel,
    Relationship,
)
from sqlalchemy import (
    Boolean,
    Text,
    ForeignKey,
    Integer,
)
from enum import Enum


class YesNo(str, Enum):
    YES = "1"
    NO = "2"

class GSTINStatus(str, Enum):
    YES = "1"
    NO = "2"
    EXEMPTED = "3"

class UdyamApplication(SQLModel, table=True):
    __tablename__ = "udyam_applications"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )

    entrepreneur_name: Optional[str] = Field(
        default=None,
        max_length=255,
        sa_column=Column(pg.VARCHAR(255), nullable=True, index=True),
    )

    aadhaar_last4: Optional[str] = Field(
        default=None,
        max_length=4,
        sa_column=Column(pg.VARCHAR(4), nullable=True),
    )
    aadhaar_hash: Optional[str] = Field(
        default=None,
        max_length=255,
        sa_column=Column(pg.VARCHAR(255), nullable=True, index=True),
    )
    aadhaar_consent: bool = Field(
        default=False,
        sa_column=Column(
            Boolean, default=False, nullable=False
        ),
    )
    aadhaar_verified: bool = Field(
        default=False, sa_column=Column(Boolean, default=False, nullable=False)
    )
    aadhaar_verified_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            pg.TIMESTAMP(timezone=False), nullable=True
        ),  
    )

    # PAN Verification Fields
    pan_masked: Optional[str] = Field(
        default=None,
        max_length=20,
        sa_column=Column(pg.VARCHAR(20), nullable=True, index=True),
    )
    pan_hash: Optional[str] = Field(
        default=None,
        max_length=255,
        sa_column=Column(pg.VARCHAR(255), nullable=True, index=True),
    )
    pan_holder_name: Optional[str] = Field(
        default=None,
        max_length=255,
        sa_column=Column(pg.VARCHAR(255), nullable=True),
    )
    dob_or_doi: Optional[date] = Field(
        default=None, sa_column=Column(pg.DATE, nullable=True) 
    )
    type_of_organisation: Optional[str] = Field(
        default=None, max_length=50, sa_column=Column(pg.VARCHAR(50), nullable=True)
    )
    previous_year_itr_filed: bool | None = Field(
        default=None, sa_column=Column(Boolean, nullable=True)
    )

    has_gstin_status: GSTINStatus | None = Field(
        default=None, sa_column=Column(pg.VARCHAR(10), nullable=True)
    ) 
    pan_verified: bool = Field(
        default=False, sa_column=Column(Boolean, default=False, nullable=False)
    )
    pan_verified_at: Optional[datetime] = Field(
        default=None, sa_column=Column(pg.TIMESTAMP(timezone=False), nullable=True)
    )

    status: str = Field(
        default="draft",
        max_length=20,
        sa_column=Column(pg.VARCHAR(20), default="draft", nullable=False, index=True),
    )

    form_payload: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(
            pg.JSONB, nullable=False
        ),
    )
    last_validation_errors: Optional[dict[str, Any]] = Field(
        default=None, sa_column=Column(pg.JSONB, nullable=True)
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            pg.TIMESTAMP(timezone=False), default=datetime.utcnow, nullable=False
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            pg.TIMESTAMP(timezone=False), default=datetime.utcnow, nullable=False
        ),
    )

    # Relationships (example, assuming you might link attempts back)
    verification_attempts: list["VerificationAttempt"] = Relationship(
        back_populates="udyam_application",
        sa_relationship_kwargs={"lazy": "selectin"},  # Or "selectin" for eager loading
    )
    
    @property
    def has_gstin_bool(self) -> bool | None:
        if self.has_gstin_status == GSTINStatus.YES:
            return True
        if self.has_gstin_status == GSTINStatus.NO:
            return False
        return None  # exempted or unset


class VerificationAttempt(SQLModel, table=True):
    __tablename__ = "verification_attempts"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )

    app_id: uuid.UUID = Field(
        # foreign_key="udyam_applications.id", # REMOVED: Redundant foreign_key argument
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey("udyam_applications.id"),
            nullable=False,
            index=True,
        )
    )

    kind: str = Field(
        max_length=20,  # E.g., "aadhaar_otp" | "pan"
        sa_column=Column(pg.VARCHAR(20), nullable=False, index=True),
    )

    success: bool = Field(
        default=False, sa_column=Column(Boolean, default=False, nullable=False)
    )

    payload: dict[str, Any] = Field(
        default_factory=dict,  # Use default_factory for mutable defaults
        sa_column=Column(pg.JSONB, nullable=False),  # Use JSONB
    )

    message: Optional[str] = Field(
        default=None, sa_column=Column(Text, nullable=True)  # Text for longer messages
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            pg.TIMESTAMP(timezone=False), default=datetime.utcnow, nullable=False
        ),
    )

    # Relationship back to UdyamApplication
    udyam_application: Optional[UdyamApplication] = Relationship(
        back_populates="verification_attempts"
    )
