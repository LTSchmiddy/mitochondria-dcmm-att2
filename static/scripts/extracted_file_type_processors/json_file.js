// class JSONEditorOptions {
//     constructor(p_editor_data) {
//         this.editor_data_obj = p_editor_data;
//     }
//
//     onChangeJSON (current_json) {
//         console.log("JSON Changed");
//         console.log(this.editor_data_obj);
//     }
// }


class JsonFileEditorData {
    constructor(name, path, container_selector = ".editor-content", editor_options = {}) {
        this.name = name;
        this.path = path;
        this.container_selector = container_selector;
        this.editor = null;
        this.original_json = "";

        this._async_construction(editor_options);
    }

    get_editor_options() {
        let self = this;

        return {
            modes: ['tree', 'view', 'form', 'preview'],

            onChangeJSON: (current_json)=>{
                this.onChangeJSON(current_json);
            }

        }
    }

    async _async_construction(editor_options) {
        let file_json = await py.files.read_json_file(this.path);

        this.editor = new JSONEditor(this.get_editor_container(), this.get_editor_options());
        this.editor.set(file_json);

        this.set_original_json();
    }

    set_original_json() {
        this.original_json = copy_json(this.get_json());
    }

    get_editor_view() {
        return extracted_file_get_editor(this.path);
    }

    get_editor_container() {
        return this.get_editor_view().children(this.container_selector).get()[0];
    }

    get_json() {
        // console.log(this.editor.get());
        return this.editor.get();
    }

    set_json(json_obj) {
        this.editor.set(json_obj);
    }

    switch_to() {
        extracted_file_show_editor(this.path);
    }

    async save_file() {
        // await py.files.write_json_file(this.path, JSON.stringify(this.get_json()));
        await py.files.write_json_file(this.path, this.get_json());
        this.set_original_json();

    }

    async revert_file() {
        this.set_json(await py.files.read_json_file(this.path));
        this.set_original_json();
    }

    is_json_original() {
        return JSON.stringify(this.get_json()) !== JSON.stringify(this.original_json);
    }

    onChangeJSON (current_json) {
        // console.log(this.is_json_original());

        if (this.is_json_original()) {


        }
    }
}



async function _extracted_file_load_json_editor(name, path) {
    if (!mod_editor_opened_tabs.hasOwnProperty(path)) {
        console.log(`'${path}' not opened...`);
        return null;
    }

    $.post("/panes/mod_editor/editors/json_editor", {name: name, path: path}, async (data, status) => {
        await extracted_file_show_editor("");
        extracted_file_editor_area.get()[0].innerHTML += data;

        let editor_data = mod_editor_opened_tabs[path];
        editor_data.data_obj = new JsonFileEditorData(name, path);

        extracted_file_show_editor(path);

    });


}