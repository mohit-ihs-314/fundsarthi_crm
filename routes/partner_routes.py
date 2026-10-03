from flask import Blueprint, jsonify, request
from models.partner import Partner
from extensions import db


partner_bp = Blueprint(
    "partner",
    __name__,
    url_prefix="/api/crm/partners"
)


# GET ALL PARTNERS
@partner_bp.route("/", methods=["GET"])
def get_partners():

    partners = (
        Partner.query
        .order_by(Partner.created_at.desc())
        .all()
    )

    return jsonify({
        "success": True,
        "count": len(partners),
        "data": [partner.to_dict() for partner in partners]
    })


# UPDATE PARTNER STATUS
@partner_bp.route("/<int:partner_id>/status", methods=["PUT"])
def update_partner_status(partner_id):

    partner = Partner.query.get(partner_id)

    if not partner:
        return jsonify({
            "success": False,
            "message": "Partner not found"
        }), 404

    data = request.get_json() or {}
    status = data.get("status")

    if status not in ["pending", "approved", "rejected"]:
        return jsonify({
            "success": False,
            "message": "Invalid status"
        }), 400

    partner.status = status

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Partner status updated",
        "data": partner.to_dict()
    })


# DELETE PARTNER
@partner_bp.route("/<int:partner_id>", methods=["DELETE"])
def delete_partner(partner_id):

    partner = Partner.query.get(partner_id)

    if not partner:
        return jsonify({
            "success": False,
            "message": "Partner not found"
        }), 404

    db.session.delete(partner)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Partner deleted successfully"
    })
