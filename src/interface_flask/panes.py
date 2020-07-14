import os

from flask import *

from data import pak_tools
from settings import current, exec_dir, paths

panes = Blueprint(
    'panes',
    __name__,
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['view-panes']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['view-panes']['static-dir'])
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['view-panes']['template-dir'],
    # static_folder=settings['interface']['view-panes']['static-dir']
)



@panes.route('/mod_editor/extract_dir_listing')
def extract_dir_listing():
    if len(os.listdir(paths.get_extract_dir())) == 0:
        return f"Extraction directory '{current['dirs']['extraction_profile']}' ('{paths.get_extract_dir()}') is empty"

    return render_template("view_pane_templates/mod_editor/extract_dir_listing.html", dir_list = pak_tools.tool_man.get_extract_tree(), dir_name="CastleDB")


@panes.route('/mod_editor/editor_tab', methods=['GET', 'POST'])
def editor_tab():
    # print("loading tab")
    # if request.method == "POST":
    # print(request.form.get('name'))
    # print(request.form.get('path'))

    name = request.form.get('name')
    path = request.form.get('path')

    return render_template("view_pane_templates/mod_editor/editor_tab.html", name=name, path=path)


# Editor Types:
@panes.route('/mod_editor/editors/json_editor', methods=['GET', 'POST'])
def json_editor():
    name = request.form.get('name')
    path = request.form.get('path')

    return render_template("view_pane_templates/mod_editor/editors/json_editor.html", name=name, path=path)

@panes.route('/mod_editor/editors/unknown_file_type_editor', methods=['GET', 'POST'])
def unknown_file_type_editor():
    name = request.form.get('name')
    path = request.form.get('path')

    return render_template("view_pane_templates/mod_editor/editors/unknown_file_type_editor.html", name=name, path=path)