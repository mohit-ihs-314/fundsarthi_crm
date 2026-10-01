from flask import Blueprint, jsonify, request
from models.banner import Banner
from extensions import db


banner_bp = Blueprint(
    "banner",
    __name__,
    url_prefix="/api/crm/banners"
)


# =========================================================
# GET ALL BANNERS
# =========================================================

@banner_bp.route("/", methods=["GET"])
def get_banners():

    banners = (
        Banner.query
        .order_by(
            Banner.display_order.asc(),
            Banner.id.desc()
        )
        .all()
    )

    return jsonify({
        "success": True,
        "data": [banner.to_dict() for banner in banners]
    })


# =========================================================
# CREATE BANNER
# =========================================================

@banner_bp.route("/", methods=["POST"])
def create_banner():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title")
    image_url = data.get("image_url")

    if not title:
        return jsonify({
            "success": False,
            "message": "Title is required"
        }), 400

    if not image_url:
        return jsonify({
            "success": False,
            "message": "Image URL is required"
        }), 400

    banner = Banner(
        title=title,
        image_url=image_url,
        redirect_url=data.get("redirect_url"),
        is_active=data.get("is_active", True),
        display_order=data.get("display_order", 0),
        start_date=data.get("start_date"),
        end_date=data.get("end_date")
    )

    db.session.add(banner)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Banner created successfully",
        "data": banner.to_dict()
    }), 201


# =========================================================
# UPDATE BANNER
# =========================================================

@banner_bp.route("/<int:banner_id>", methods=["PUT"])
def update_banner(banner_id):

    banner = Banner.query.get(banner_id)

    if not banner:
        return jsonify({
            "success": False,
            "message": "Banner not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "title" in data:
        banner.title = data["title"]

    if "image_url" in data:
        banner.image_url = data["image_url"]

    if "redirect_url" in data:
        banner.redirect_url = data["redirect_url"]

    if "is_active" in data:
        banner.is_active = data["is_active"]

    if "display_order" in data:
        banner.display_order = data["display_order"]

    if "start_date" in data:
        banner.start_date = data["start_date"]

    if "end_date" in data:
        banner.end_date = data["end_date"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Banner updated successfully",
        "data": banner.to_dict()
    })


# =========================================================
# DELETE BANNER
# =========================================================

@banner_bp.route("/<int:banner_id>", methods=["DELETE"])
def delete_banner(banner_id):

    banner = Banner.query.get(banner_id)

    if not banner:
        return jsonify({
            "success": False,
            "message": "Banner not found"
        }), 404

    db.session.delete(banner)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Banner deleted successfully"
    })
