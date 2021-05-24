# Execution:
import sys
import json
from viewport.js_api import JsApi
from viewport.js_api.cef_bindings import cef_bound_properties

from settings import current
# Config
output_path = current['interface']['pages']['static-dir'] + "/scripts/python_wrapper_2.js"

def iterate_api(p_api_struct: dict, level: list = []):
    for key in p_api_struct:
        prefix = ".".join(level)

        if p_api_struct[key] is None:
            if prefix == "":
                p_api_struct[key] = f"pywebview.api.{key}"
            else:
                p_api_struct[key] = f"pywebview.api.{prefix}.{key}"

        else:
            next_level = level[:]
            next_level.append(key)

            iterate_api(p_api_struct[key], next_level)

def rebuild_api():
    global output_path
    api_struct = JsApi.api_struct

    cef_props_string = ""

    for i in cef_bound_properties:
        cef_props_string += f"window.{i[0]} = null;\n"

    iterate_api(api_struct)

    api_json_str = json.dumps(api_struct, indent=4, sort_keys=True)
    api_js = api_json_str.replace("\"", "").replace("\n", "\n    ")

    out_js = f"""
console.log("loading Python_Wrapper");

{cef_props_string}
let py = null;
// let py_exec = null;

window.addEventListener('pywebviewready', function() {{
    
    py = {api_js}
    
    console.log("pwv ready");
}});
"""


    outfile = open(output_path, "w")
    outfile.write(out_js)
    outfile.close()

    print("JS API Regenerated:")
    print("===================================")
    print(out_js)
    print("===================================")

if __name__ == '__main__':
    rebuild_api()
    sys.exit(0)
