from flask import Blueprint, request, jsonify
from models.property import Property
from extensions import db
import uuid
from datetime import datetime
import requests
import pandas as pd
from flask import send_file
import io
import json

property_bp = Blueprint("property_bp", __name__)

import json
import re

def parse_area(area):
    if not area:
        return None

    match = re.search(r'\d+', str(area).replace(',', ''))

    if match:
        return int(match.group())

    return None

def format_date(date_value):
    if not date_value:
        return ""

    if isinstance(date_value, str):
        try:
            date_value = datetime.fromisoformat(
                date_value.replace("Z", "")
            )
        except:
            return date_value

    return date_value.strftime("%d %b %Y")

@property_bp.route("/crm/properties", methods=["GET"])
def get_properties():
    properties = Property.query.order_by(Property.id.desc()).all()

    result = []

    for p in properties:

        # ✅ SAFE PHOTOS PARSE
        photos = []
        if p.photos:
            try:
                photos = json.loads(p.photos)
            except:
                photos = p.photos.split(",")

        # ✅ SAFE FEATURES PARSE
        features = []
        if p.features:
            try:
                features = json.loads(p.features)
            except:
                features = p.features.split(",")

        result.append({
            "id": p.property_id,
            "title": p.title or "",
            "location": p.locality or "",
            "city": p.city or "",
            "type": p.property_type or "",
            "price": p.price or "",
            "bedrooms": int(p.bedrooms) if p.bedrooms else None,
            "bathrooms": int(p.bathrooms) if p.bathrooms else None,
            "area": parse_area(p.size),

            "description": p.description or "",
            "owner_name": p.name or "",
            "owner_mobile": p.mobile or "",
            "owner_email": p.email or "",

            "status": (p.status or "pending").lower(),

            "listedDate": format_date(p.created_at),

            "photos": photos,
            "features": features,
        })

    return jsonify(result)

@property_bp.route("/crm/add-property", methods=["POST"])
def add_property():
    data = request.json or {}

    new_property = Property(
        property_id="PROP" + str(uuid.uuid4().hex[:6]).upper(),
        title=data.get("title"),
        locality=data.get("location"),
        city=data.get("city"),
        property_type=data.get("type"),
        price=str(data.get("price")),
        bedrooms=str(data.get("bedrooms")),
        bathrooms=str(data.get("bathrooms")),
        size=str(data.get("area")),
        status="pending"
    )

    db.session.add(new_property)
    db.session.commit()

    return {"status": "success", "message": "Property added"}

@property_bp.route("/crm/update-property-status", methods=["POST"])
def update_property_status():

    data = request.json

    property = Property.query.filter_by(
        property_id=data["id"]
    ).first()

    if not property:
        return {
            "status": "error",
            "message": "Property not found"
        }, 404

    property.status = data.get("status")

    if "listing_type" in data:
        property.listing_type = data.get("listing_type")

    db.session.commit()

    # ==================================
    # SEND PUSH NOTIFICATION
    # ==================================

    if property.status.lower() == "approved":

        try:

            response = requests.post(
                "https://fundsarthi.onrender.com/api/send-notification",
                json={
                    "mobile": property.mobile,
                    "title": "Property Approved",
                    "body": f"Your property '{property.title}' has been approved and is now live."
                },
                timeout=10
            )

            print(
                "PROPERTY APPROVAL PUSH:",
                response.text
            )

        except Exception as e:

            print(
                "PROPERTY APPROVAL ERROR:",
                str(e)
            )

    elif property.status.lower() == "rejected":

        try:

            response = requests.post(
                "https://fundsarthi.onrender.com/api/send-notification",
                json={
                    "mobile": property.mobile,
                    "title": "Property Rejected",
                    "body": f"Your property '{property.title}' could not be approved."
                },
                timeout=10
            )

            print(
                "PROPERTY REJECT PUSH:",
                response.text
            )

        except Exception as e:

            print(
                "PROPERTY REJECT ERROR:",
                str(e)
            )

    return {
        "status": "success",
        "message": "Property updated successfully"
    }

@property_bp.route("/crm/import-properties", methods=["POST"])
def import_properties():

    if "file" not in request.files:
        return jsonify({
            "status":"error",
            "message":"No file uploaded"
        }),400

    file=request.files["file"]

    try:

        df=pd.read_csv(file)

        count=0

        for _,row in df.iterrows():

            property=Property(
                property_id="PROP"+uuid.uuid4().hex[:6].upper(),

                title=row.get("title"),
                locality=row.get("location"),
                city=row.get("city"),
                property_type=row.get("type"),

                price=str(row.get("price")),
                bedrooms=str(row.get("bedrooms")),
                bathrooms=str(row.get("bathrooms")),
                size=str(row.get("area")),

                description=row.get("description"),
                name=row.get("owner_name"),
                mobile=str(row.get("owner_mobile")),
                email=row.get("owner_email"),

                purpose=row.get("purpose"),

                status="approved",

                listing_type=row.get(
                    "listing_type",
                    "normal"
                )
            )

            db.session.add(property)

            count+=1

        db.session.commit()

        return jsonify({
            "status":"success",
            "message":f"{count} properties imported successfully."
        })

    except Exception as e:

        return jsonify({
            "status":"error",
            "message":str(e)
        }),500
    

@property_bp.route("/crm/export-properties", methods=["GET"])
def export_properties():

    properties = Property.query.all()

    rows = []

    for p in properties:

        photos = ""

        if p.photos:
            try:
                photos = "|".join(json.loads(p.photos))
            except:
                photos = p.photos

        rows.append({
            "title": p.title,
            "location": p.locality,
            "city": p.city,
            "type": p.property_type,
            "price": p.price,
            "bedrooms": p.bedrooms,
            "bathrooms": p.bathrooms,
            "area": p.size,
            "description": p.description,
            "owner_name": p.name,
            "owner_mobile": p.mobile,
            "owner_email": p.email,
            "purpose": p.purpose,
            "status": p.status,
            "listing_type": p.listing_type,
            "photos": photos,
            "created_at": p.created_at,
        })

    df = pd.DataFrame(rows)

    output = io.StringIO()

    df.to_csv(output, index=False)

    mem = io.BytesIO()

    mem.write(output.getvalue().encode("utf-8"))

    mem.seek(0)

    return send_file(
        mem,
        mimetype="text/csv",
        as_attachment=True,
        download_name="properties.csv",
    )    


@property_bp.route("/crm/delete-property/<property_id>", methods=["DELETE"])
def delete_property(property_id):

    property = Property.query.filter_by(
        property_id=property_id
    ).first()

    if not property:
        return jsonify({
            "status":"error",
            "message":"Property not found"
        }),404

    db.session.delete(property)
    db.session.commit()

    return jsonify({
        "status":"success",
        "message":"Property deleted"
    })


@property_bp.route("/crm/delete-properties", methods=["POST"])
def delete_properties():

    data = request.json

    ids = data.get("ids", [])

    if not ids:
        return jsonify({
            "status":"error",
            "message":"No properties selected"
        }),400

    Property.query.filter(
        Property.property_id.in_(ids)
    ).delete(synchronize_session=False)

    db.session.commit()

    return jsonify({
        "status":"success",
        "message":f"{len(ids)} properties deleted."
    })        