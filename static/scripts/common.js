// import time_func from '/static/scripts/components/time_func.js';
// import Sidebar from '/static/scripts/components/sidebar.js';


function copy_json(json_in) {
    return JSON.parse(JSON.stringify(json_in));
}

function play_dead_cells() {
    py.exec("import subprocess\n" +
        "from settings import paths\n" +
        "subprocess.Popen([paths.get_game_exec()])");

}

