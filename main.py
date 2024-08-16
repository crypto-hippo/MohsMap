from flask import Flask, render_template
from config import config
from jinja_vars import jinja_vars
from google.cloud import firestore
from utility import load_blueprints, setup_google_cloud_logging
import jinja2
import os

client = firestore.Client()
setup_google_cloud_logging()


def create_flask_app():
    # csrf = CSRFProtect()
    flask_app = Flask(__name__)
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
    flask_app.secret_key = config["secret_key"]
    flask_app.debug = True
    blueprints = load_blueprints()
    for bp in blueprints:
        flask_app.register_blueprint(bp)
    return flask_app


app = create_flask_app()
app.jinja_env.globals.update(**jinja_vars)


# routes 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#
# @app.route("/search", methods=["POST"])
# def search():
#     logger = Logger()
#     dao = DAO()
#
#     try:
#         search_value = str(request.form["search_value"]).strip()
#         all_results = []
#
#         if len(search_value.strip()) == 5 and search_value.isdigit():
#             # logger.log("Searching %s" % search_value)
#             by_zip = dao.by_zip(search_value)
#             # logger.log(str(by_zip))
#             all_results.extend(by_zip)
#
#         else:
#             by_name = dao.by_name(search_value)
#             all_results.extend(by_name)
#
#         return jsonify(all_results)
#
#     except Exception as e:
#         return logger.filename + " " + str(e)
#         # return jsonify({"error": True})
#
# @app.route("/current_surgeons", methods=["POST"])
# def get_current_surgeons():
#     logger = Logger()
#
#     try:
#         dao = DAO()
#         # lat, lng = request.form["lat"], request.form["lng"]
#         surgeons = dao.get_surgeons()
#         return jsonify(surgeons)
#
#     except Exception as e:
#         logger.log(str(e))
#         return "Your request cannot be processed at this time"
#
# @app.route("/logout")
# def logout():
#     logger = Logger()
#
#     try:
#         session["admin_authenticated"] = None
#         return redirect(url_for("index"))
#
#     except Exception as e:
#         logger.log(str(e))
#
# @app.route("/admin", methods=["GET"])
# def admin():
#     logger = Logger()
#
#     try:
#         access = session.get("admin_authenticated", None)
#         if access:
#             return render_template("admin_panel.html")
#
#         else:
#             return render_template("admin_login.html")
#
#     except Exception as e:
#         logger.log(str(e))
#         # return "Your request cannot be processed at this time"
#
# @app.route("/admin_login", methods=["POST"])
# def admin_login():
#     try:
#         access = session.get("admin_authenticated", None)
#         if access:
#             return redirect(url_for("admin"))
#
#         else:
#             password = str(request.form["password"]).strip()
#             if password == "96cfbea314b3489b96ab9a4c4ce09066":
#                 session["admin_authenticated"] = True
#                 return redirect(url_for("admin"))
#             else:
#                 return redirect(url_for("admin"))
#
#     except Exception as e:
#         raise e
#         # return "Your request cannot be processed at this time"
#
# def title_exists(results, title):
#     for r in results:
#         if r["title"] == title:
#             return True
#     return False
#
# def is_last_name(search_value, title):
#     if "," in title:
#         name = title.split(",")[0]
#         name_args = name.split(" ")
#         if name_args[-1].strip().lower() == search_value.lower():
#             return True
#     else:
#         print("\nNo comma found\n")
#
#     return False
#
# def format_surgeons(results):
#     unique_surgeons = []
#
#     try:
#         unique_results = []
#
#         for result in results:
#             title = result["title"]
#             if title not in unique_results:
#                 unique_results.append(title)
#                 unique_surgeons.append(result)
#
#         return unique_surgeons
#
#     except Exception as e:
#         print (str(e))
#         return unique_surgeons
#
#
# @app.route("/get_surgeons_by_title", methods=["POST"])
# @site_login_required
# def get_surgeons_by_title():
#     try:
#         dao = DAO()
#         title = request.form.get("title", None)
#
#         if title:
#             surgeons_editable = dao.by_title(title)
#             surgeons_editable_deleted = dao.by_title(title, deleted=True)
#
#             return_data = {
#                 "surgeons_editable": surgeons_editable,
#                 "surgeons_editable_deleted": surgeons_editable_deleted
#             }
#
#             return jsonify(return_data)
#
#         else:
#             return "No title found"
#
#     except Exception as e:
#         print(str(e))
#         return jsonify({})
#
# @app.route("/update_value", methods=["POST"])
# @site_login_required
# def update_value():
#     try:
#         column = request.form.get("column", None)
#         value = request.form.get(column, None)
#
#         surgeon_id = request.form.get("surgeon_id", None)
#
#         if value and surgeon_id:
#             dao = DAO()
#             success = dao.update(column, surgeon_id, value)
#             return jsonify(success)
#             # if column == "training":
#             #     value = json.loads(value)
#             #     dao = DAO()
#             #     success = dao.update_training(value, surgeon_id)
#             #     return jsonify(success)
#
#             # else:
#             #     dao = DAO()
#             #     success = dao.update(column, surgeon_id, value)
#             #     return jsonify(success)
#
#         else:
#             pass
#
#     except Exception as e:
#         raise e
#         return jsonify({"Error": "Something went wrong"})
#
# @app.route("/update_checkbox", methods=["POST"])
# @site_login_required
# def update_checkbox():
#     try:
#         checked = request.form.get("checked", None)
#         _id = request.form.get("surgeon_id", None)
#         if _id:
#             dao = DAO()
#             doit = dao.update("uneditable", _id, int(checked))
#             return jsonify(doit)
#
#     except Exception as e:
#         print(str(e))
#
# @app.route("/admin/search", methods=["POST"])
# @site_login_required
# def admin_search():
#     try:
#         search_value = str(request.form.get("search_value", None))
#         if search_value and search_value.strip():
#             search_value = search_value.strip()
#             dao = DAO()
#             results = dao.by_name(search_value)
#
#             final_results = []
#
#             for result in results:
#                 title = result["title"]
#                 if is_last_name(search_value, title):
#                     # if not title_exists(final_results, title):
#                     final_results.append(result)
#
#
#             final_results = format_surgeons(final_results)
#
#             return jsonify(list(final_results))
#
#     except Exception as e:
#         print(str(e))
#         return jsonify({"Error": "Something went wrong"})
#
# @app.route("/admin/unique/latlng", methods=["POST"])
# @site_login_required
# def unique_latlng(*args, **kwargs):
#     try:
#         title = request.form.get("title", None)
#         if title:
#             dao = DAO()
#             unique_set = []
#
#             latlngs = dao.get_latlngs(title)
#
#             for latlng_obj in latlngs:
#                 current_latlngs = latlng_obj["latlng"].split("|")
#                 for latlng in current_latlngs:
#                     if latlng not in unique_set:
#                         unique_set.append(latlng)
#
#             return jsonify(unique_set)
#
#     except Exception as e:
#         return jsonify({"Error": "Something went wrong"})
#
#
#
#
# # def admin():
# #     logger = Logger()
# #     try:
# #         access = session.get("access", None)
# #         if access:
# #             dao = DAO()
# #             search_value = request.form["search_value"].strip()
# #             if search_value:
# #                 results = dao.by_name(search_value)
# #                 for result in results:
# #                     print(result)
#
# #         else:
# #             return "Access Required"
#
# #     except Exception as e:
# #         logger.log(str(e))
#
#
#
# # @app.route("/admin_panel", methods=["GET"])
# # def admin_panel():
# #     logger = Logger()
#
# #     try:
# #         access = session.get("access", None)
# #         if access:
# #             return render_template("admin_panel.html")
#
# #         else:
# #             return redirect(url_for("admin"))
#
# #     except Exception as e:
# #         logger.log(str(e))
# #         return "Your request cannot be processed at this time"
#
#
# @app.route("/contact_us")
# def contact_us():
#
#     try:
#         dao = DAO()
#
#         contact_us_content = dao.get_page_content("contact_us")
#         return render_template("contact_us.html", content = contact_us_content)
#
#     except Exception as e:
#         return "Your request cannot be processed"
#
# @app.route("/about_us")
# def about_us():
#
#     try:
#         dao = DAO()
#
#         about_us_content = dao.get_page_content("about_us")
#         return render_template("about_us.html", content = about_us_content)
#
#     except Exception as e:
#         return "Your request cannot be processed"
#
# @app.route("/why_acms")
# def why_acms():
#
#     try:
#         dao = DAO()
#
#         why_acms_content = dao.get_page_content("why_acms")
#         return render_template("why_acms.html", content = why_acms_content)
#
#     except Exception as e:
#         return "Your request cannot be processed"
#
# @app.route("/tos")
# def tos():
#
#     try:
#         dao = DAO()
#         tos_content = dao.get_page_content("tos")
#         return render_template("tos.html", content = tos_content)
#
#     except Exception as e:
#         return "Your request cannot be processed"
#
# # # admin panel edit page content routes
# # @app.route("/admin_panel/why_acms")
# # def why_acms_edit():
# #     try:
# #         dao = DAO()
# #         access = session.get("access", None)
# #         if access:
# #             why_acms = dao.get_page_content('why_acms')
# #             return render_template("admin_panel/why_acms.html", content_editable = why_acms)
#
# #         else:
# #             return redirect(url_for("index"))
#
# #     except Exception as e:
# #         return "Your request cannot be processed"
#
# # @app.route("/admin_panel/contact_us")
# # def contact_us_edit():
# #     try:
# #         dao = DAO()
# #         access = session.get("access", None)
# #         if access:
# #             contact_us = dao.get_page_content("contact_us")
# #             return render_template("admin_panel/contact_us.html", content_editable = contact_us)
#
# #         else:
# #             return redirect(url_for("index"))
#
# #     except Exception as e:
# #         return "Your request cannot be processed"
#
#
# # @app.route("/admin_panel/about_us")
# # def about_us_edit():
# #     try:
# #         dao = DAO()
# #         access = session.get("access", None)
#
# #         if access:
# #             about_us = dao.get_page_content("about_us")
# #             return render_template("admin_panel/about_us.html", content_editable = about_us)
#
# #         else:
# #             return redirect(url_for("index"))
#
# #     except Exception as e:
# #         return "Your request cannot be processed"
#
#
# # @app.route("/admin_panel/tos")
# # def tos_edit():
# #     try:
# #         dao = DAO()
# #         access = session.get("access", None)
#
# #         if access:
# #             tos = dao.get_page_content("tos")
# #             return render_template("admin_panel/tos.html", content_editable = tos)
#
# #         else:
# #             return redirect(url_for("index"))
#
# #     except Exception as e:
# #         return "Your request cannot be processed"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
