'use strict';

function copy_json(json_in) {
    return JSON.parse(JSON.stringify(json_in));
}

function play_dead_cells() {
    py.dc_game.start_game();

}


