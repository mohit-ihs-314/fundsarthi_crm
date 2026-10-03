from flask import Blueprint, jsonify, request
from models.property_enquiry import PropertyEnquiry
from extensions import db


property_enquiry_bp = Blueprint(
    "property_enquiry",
    __name__,
    url_prefix="/api/crm/property-enquiries"
)


# GET ALL PROPERTY ENQUIRIES
@property_enquiry_bp.route("/", methods=["GET"])
def get_property_enquiries():

    enquiries = (
        PropertyEnquiry.query
        .order_by(PropertyEnquiry.created_at.desc())
        .all()
    )

    return jsonify({
        "success": True,
        "count": len(enquiries),
        "data": [enquiry.to_dict() for enquiry in enquiries]
    })


# UPDATE ENQUIRY STATUS
@property_enquiry_bp.route("/<int:enquiry_id>/status", methods=["PUT"])
def update_property_enquiry_status(enquiry_id):

    enquiry = PropertyEnquiry.query.get(enquiry_id)

    if not enquiry:
        return jsonify({
            "success": False,
            "message": "Property enquiry not found"
        }), 404

    data = request.get_json() or {}

    status = data.get("status")

    if not status:
        return jsonify({
            "success": False,
            "message": "Status is required"
        }), 400

    enquiry.status = status.lower()

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Property enquiry status updated",
        "data": enquiry.to_dict()
    })


# DELETE ENQUIRY
@property_enquiry_bp.route("/<int:enquiry_id>", methods=["DELETE"])
def delete_property_enquiry(enquiry_id):

    enquiry = PropertyEnquiry.query.get(enquiry_id)

    if not enquiry:
        return jsonify({
            "success": False,
            "message": "Property enquiry not found"
        }), 404

    db.session.delete(enquiry)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Property enquiry deleted"
    })
