"""Idempotent seed script. Run from the project root:

    uv run python -m scripts.seed
"""

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Brand, Property

BRAND_NAME = "Aurelia"

BRAND_GUIDELINES = """\
Language: British English. Formality: formal.
Tone: professional, warm, courteous, empathetic, sophisticated.
Style: use sentence case; correct grammar and punctuation; British spelling;
avoid contractions, colloquialisms and informal language; prefer "We";
avoid the first person singular ("I", "me").
Preferred vocabulary (use naturally, without repetition): Welcome, Delight,
Heart, Personalised, Apologise, Experiences, Superior, Luxurious, Spacious,
Exquisite, Delectable, Gourmet, Fine dining, Divine, Heavenly.
Preferred phrases: We look forward to welcoming you; We are delighted to
share; Thank you for your patience; We apologise for any inconvenience;
Please let us know; Regarding your request; It is our pleasure to assist you;
We regret to inform you; Should you have any questions; Please do not
hesitate to contact us.
Never use: persons (say Guest); Specializing (say Specialising); revert / revert
back (say confirm, respond or reply); apologize (say apologise); bespoke
(say Personalised).
Thank-you replies: "It is a pleasure, Sir/Madam."
"""

PROPERTY_NAME = "Aurelia Singapore"


def seed() -> None:
    with SessionLocal() as session:
        # Brand: find by name, create if missing, then sync the fields
        brand = session.scalar(select(Brand).where(Brand.name == BRAND_NAME))
        if brand is None:
            brand = Brand(name=BRAND_NAME)
            session.add(brand)
        brand.customer_term = "Guest"
        brand.communication_guidelines = BRAND_GUIDELINES
        brand.is_active = True
        session.flush()  # sends the INSERT now so brand.id is available

        # Property: unique per (brand, name)
        prop = session.scalar(
            select(Property).where(
                Property.brand_id == brand.id, Property.name == PROPERTY_NAME
            )
        )
        if prop is None:
            prop = Property(brand_id=brand.id, name=PROPERTY_NAME)
            session.add(prop)
        prop.property_term = "luxury hotel"
        prop.communication_guidelines = ""  # empty = inherit brand style
        prop.is_active = True

        session.commit()
        print(f"Seeded brand {brand.id} and property {prop.id}")


if __name__ == "__main__":
    seed()
