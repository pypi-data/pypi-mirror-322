/**
 *  Copyright (C) 2025  Albert Zedlitz
 *  
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
var g_eezz_socket_addr =   "ws://localhost:8100"  ;
var g_eezz_arguments   = "";
var g_eezz_web_socket;

window.onload = eezz_connect();

// User Callback Interface
class TEezz {
    constructor() {
        this.on_update  = (a_element) => {};
        this.on_animate = (a_element) => {};
    }
}

// Global user interface instance
eezz = new TEezz();

function eezz_status(msg) {
    var x_element = document.getElementById('eezz-status');
    if (x_element) {
        x_element.innerHTML = msg;
    }
}

// Open and controlling the WEB socket
// ------------------------------------------------------------------------------------------
function eezz_connect() {
    console.log('connect websocket ...');
	g_eezz_web_socket        = new WebSocket(g_eezz_socket_addr);
    g_eezz_web_socket.onopen = function() {
        console.log('on open websocket...');
        var x_title   = "document";
        var x_title_tags = document.getElementsByTagName('title');
        if (x_title_tags.length > 0) {
            x_title   = x_title_tags[0].innerHTML;
        }
        var x_body    = document.body;
        var x_json    = {"initialize": x_body.innerHTML, "args": g_eezz_arguments, 'title': x_title};
        g_eezz_web_socket.send(JSON.stringify(x_json));
        eezz_status('connected');
    }
    
    /* Error handling: Reopen connection */
    g_eezz_web_socket.onerror = function(a_error) {
        console.log('error on websocket ...');
        window.console.error(a_error);
        //eezz_status(a_error);
    }

    /* Error handling: Reopen connection */
    g_eezz_web_socket.onclose = function() {
        console.log('error on websocket ...');
        eezz_status('disconnected');
    }

    /* Wait for the application and update the document          */
    g_eezz_web_socket.onmessage = function(a_event) {
        var x_json = JSON.parse(a_event.data)

        // The main response is an update request
        if (x_json.update) {
            console.log('update  ');
            var x_array_descr = x_json.update;
            var x_element_map = new Map();

            for (var i = 0; i < x_array_descr.length; i++) {
                console.log("update " + x_array_descr[i]);
                var x_update_json = x_array_descr[i];

                try {
                    if ('javascript' == x_update_json['type']) {
                        var x_func = x_update_json["target"];
                        if (typeof window[x_func] === 'function') {
                            window[x_func](x_update_json);
                        }
                        continue;
                    }

                    var x_dest = x_update_json.target.split('.');
                    if (!x_element_map.has(x_dest[0])) {
                        x_element_map.set(x_dest[0], x_dest[0]);
                    }
                    dynamic_update(x_update_json);
                } catch(err) {
                    console.log("error " + err);
                    eezz_status("error " + err);
                }
            }

            // call update once per affected root element
            x_element_map.forEach((_value, key) => {
                eezz.on_update(key);
            })
        }

        // The backend might send events. The main event is the init-event, which is the response to the
        // initialization request. The idea is to put all long lasting methods into this loop, so that the
        // HTML page is not blocked at the first call.
        //if (x_json.event) {
        //    if (x_json.event == 'init') {
        //        for (x_element in x_list) {
        //        g_eezz_web_socket.send(x_element.getAttribute('data-eezz-init'));
        //    }
        //}
    }
}

// Dynamic update: The inner-HTML of the element is calculated by the server
// The result is send via WEB socket as json = {tag-name: html, ...}
// ------------------------------------------------------------------------------------------
function dynamic_update(a_update_json) {
    var x_dest      = a_update_json.target.split('.'); 
    var x_attr      = x_dest.pop();
    var x_elem_root = document.getElementById(x_dest[0]);
    var x_elem      = x_elem_root;

    if (x_attr == 'subtree') {
        if (a_update_json.value == '') {
            tree_collapse(x_elem);
            return;
        }
        if (a_update_json.value.option.startsWith('this')) {
            tree_expand(x_elem, a_update_json.value);
            return;
        }
        x_dest = a_update_json.value.option.split('.');
        x_elem = document.getElementById(x_dest[0]);
        x_elem.innerHTML = a_update_json.value.tbody;
        return;
    }

    if (x_elem.tagName == 'IMG') {
        x_elem.setAttribute(x_attr, 'data:image/png;base64,' + a_update_json.value);
        return;
    }

    if (a_update_json.type == 'base64') {
        a_update_json.value = window.atob(a_update_json.value);
    }

    for (var i = 1; i < x_dest.length; i++) {
        if (x_dest[i] == 'style') {
            x_elem.style[x_attr] = a_update_json.value;
            return;
        }
        x_elem = x_elem.querySelector(x_dest[i]);
    }

    if (x_elem == null) {
        if (x_dest.length > 1) {
            x_elem = document.querySelector('[data-eezz-subtree-id=' + x_dest[0] + ']');
            if (x_element)
                x_elem = x_elem.querySelector(x_dest[1]);
        }

        if (x_elem == null) {
            console.log("warning: target not found " + a_update_json.target);
            return;
        }
    }

    if (x_attr == 'innerHTML') {
        x_elem.innerHTML = a_update_json.value;

        x_new_elements   = x_elem.querySelectorAll('[data-eezz-onload]');
        if (x_new_elements) {
            var x_function_call;
            var x_function;

            for (var i = 0; i < x_new_elements.length; i++) {
                x_function_call = x_new_elements[i].getAttribute('data-eezz-onload');
                x_function      = x_function_call.split('(')[0];
                if (typeof window[x_function] === 'function') {
                    window[x_function](x_new_elements[i]);
                }
            }
        }
        return;
    }

    if (x_attr == 'outerHTML') {
        x_elem.outerHTML = a_update_json.value;
        return;
    }

    x_elem.setAttribute(x_attr, a_update_json.value);
}

// Collapse a tree element
// ------------------------------------------------------------------------------------------
function tree_collapse(a_node) {
    if (a_node.nextSibling) {
        if (a_node.nextSibling.getAttribute('data-eezz-subtree-id') == a_node.id) {
            a_node.nextSibling.remove();
        }
        // a_node.lastChild.remove();
    }
}

// Inserts a sub-tree into a tree <TR> element, which is defined a given element id
// The constrains are: subtree.tagName is table, and it contains a thead and a tbody
// ------------------------------------------------------------------------------------------
function tree_expand(a_node, subtree_value) {
    // Create a new node
    if (!subtree_value.template) {
        tree_collapse(a_node);
        return;
    }

    if (subtree_value.tbody == '') {
        return;
    }

    var x_nr_cols       = a_node.getElementsByTagName('td').length.toString()
    var x_row           = document.createElement('tr');
    var x_td            = document.createElement('td');

    x_td.setAttribute('colspan', x_nr_cols+1);
    x_row.setAttribute('data-eezz-subtree-id', a_node['id']);
    x_row.appendChild(x_td);

    x_td.innerHTML      = subtree_value.template;
    var x_table         = x_td.getElementsByTagName('table')[0];
    var x_caption       = x_td.getElementsByTagName('caption')[0];
    var x_thead         = x_td.getElementsByTagName('thead')[0];
    var x_tbody         = x_td.getElementsByTagName('tbody')[0];
    var x_tfoot         = x_td.getElementsByTagName('tfoot')[0];

    x_table.setAttribute('data-eezz-subtree-id',  a_node['id']);
    x_caption.remove();

    if (subtree_value.option.includes('tfoot')) {
        x_tfoot.innerHTML = subtree_value.tfoot;
    }
    else {
        x_tfoot.remove();
    }

    if (subtree_value.option.includes('thead')) {
        x_thead.innerHTML = subtree_value.thead;
    }
    else {
        x_thead.remove();
    }

    x_table.classList.add('clzz_node');
    x_tbody.classList.add('clzz_node');
    x_tbody.innerHTML = subtree_value.tbody;

    a_node.parentNode.insertBefore(x_row, a_node.nextSibling);
    a_node.setAttribute('data-eezz-subtree_state', 'expanded');

    // x_td = document.createElement('td');
    // x_td.classList.add('clzz_node_space')
    // x_td.style.width = '50px';
    // a_node.insertBefore(x_td, null);
}

// Read one file as set of chunks
// ------------------------------------------------------------------------------------------
function readOneFile(a_file, a_reference, a_response, src_files, src_volume, all_files, all_volume) {
    var x_chunk_size   = 1000000;
    var x_stream_descr = {
            'opcode':       'continue',
            'all_files':    all_files,
            'all_volume':   all_volume,
            'src_files':    src_files,
            'src_volume':   src_volume,
            'source':       a_reference,
            'name':         a_file.name,
            'chunk_size':   x_chunk_size};

    var x_finish_descr = {
            'opcode':       'finished',
            'all_volume':   all_volume,
            'all_files':    all_files,
            'src_files':    src_files,
            'src_volume':   src_volume,
            'source':       a_reference};

    var x_sequence = 0;
    var x_finish_response = JSON.parse(JSON.stringify(a_response));

    // Generate dummy function call for TTable:

    for (var i = 0; i < a_file.size; i += x_chunk_size) {
        (function(x_one_file, x_start_offset) {
            var x_current_chunk = Math.min(x_chunk_size, x_one_file.size - x_start_offset);

            var aReader = new FileReader();
            var aBlob   = a_file.slice(x_start_offset, x_start_offset + x_current_chunk);

            x_stream_descr['name']       = a_file.name;
            x_stream_descr['size']       = a_file.size;
            x_stream_descr['sequence']   = x_sequence;
            x_stream_descr['source']     = a_reference;

            for (var x_key in a_response.update) {
                if (a_response.update[x_key]['args']) {
                    a_response.update[x_key]['args']['file']        = x_stream_descr;
                    x_finish_response.update[x_key]['args']['file'] = x_finish_descr;
                }
            }

            aReader.onloadend    = (function(x_store_response) {
                    var x_response_str = JSON.stringify(x_store_response);
                    return function(e) {
                        g_eezz_web_socket.send(x_response_str);
                    }; })(x_finish_response);
            aReader.onprogress   = (function(x_store_response) { return function(e) {}; })(a_response);
            aReader.onload       = (function(x_store_response) {
                    var x_response_str = JSON.stringify(x_store_response);
                    return function(e) {
                        g_eezz_web_socket.send(e.target.result);
                        g_eezz_web_socket.send(x_response_str);
                    }; })(a_response);

            aReader.readAsArrayBuffer(aBlob);
        } )(a_file, i);
        x_sequence += 1;
    }
}

// Read files:
// ------------------------------------------------------------------------------------------
function read_files(a_descr) {
    asyncFileCnt   = 0;
    var x_source_list = a_descr['value'].files;
    var x_response    = a_descr;

    var x_all_files  = 0;
    var x_all_volume = 0;

    // Evaluate the full amount of files and data to transfer
    for (var i = 0; i < x_source_list.length; i++) {
        var x_reference      = x_source_list[i];
        var x_elements       = document.querySelector('[data-eezz-reference = ' + x_source_list[i] + ']');
        var x_file_element   = x_elements;
	    for (var j = 0; j < x_file_element.files.length; j++) {
	        x_all_files  += 1;
	        x_all_volume += x_file_element.files[j].size;
        }
    }

    for (var i = 0; i < x_source_list.length; i++) {
        var x_reference      = x_source_list[i];
        var x_elements       = document.querySelectorAll('[data-eezz-reference = ' + x_source_list[i] + ']');
        var x_file_element   = x_elements[0];
        var x_update_str     = x_file_element.getAttribute('data-eezz-json');
        var x_update         = JSON.parse(x_update_str);
        x_response['update'] = x_update.update;

        if (x_update.process) {
            x_response['process'] = x_update.process;
        }

        // Evaluate the amount of files and data to transfer for a specific source
        var x_src_volume = 0;
        for (var j = 0; j < x_file_element.files.length; j++) {
	        var x_file       = x_file_element.files[j];
	        x_src_volume    += x_file.size;
        }

	    for (var j = 0; j < x_file_element.files.length; j++) {
	        var x_file       = x_file_element.files[j];
	        var x_src_files  = x_file_element.files.length;
            readOneFile(x_file, x_reference, x_response, x_src_files, x_src_volume, x_all_files, x_all_volume);
	    }
    }
}

// ------------------------------------------------------------------------------------------
function eezzy_onload(aElement) {
    var x_json = JSON.parse(aElement.getAttribute('data-eezz-json'));
    var x_json_onload = x_json['onload'];
    var x_key_source  = Object.keys(x_json_onload)[0];
    var x_new_key     = x_key_source.replace('this', aElement.id);
    var x_json_update = {'update': {}};

    x_json_update['update'][x_new_key] = x_json_onload[x_key_source];
    console.log(JSON.stringify(x_json_update));
    setTimeout(function(a_json_args) {
        x_response = JSON.stringify(a_json_args);
        g_eezz_web_socket.send(x_response);
    }, 0, x_json_update);
}

// Function collects all eezz events from page using WEB-socket to
// send a request to the server
// ------------------------------------------------------------------------------------------
function eezzy_get_local_values(aElement, argument_dict) {
    var x_elem;
    var x_key;
    var x_source_descr;

    for (x_key in argument_dict) {
        x_source_descr = argument_dict[x_key].split('.');
        if (x_source_descr.length != 2) {
            continue;
        }
        if (x_key == 'this.subtree') {
            continue;
        }

        if (x_source_descr[0]) {
            x_elem = aElement
        }
        else {
            x_elem = document.getElementById(x_source_descr[0]);
        }

        if (x_elem) {
            var x_value = x_elem[x_source_descr[1]] || x_elem.getAttribute(x_source_descr[1]);
            if (x_value)
                argument_dict[x_key] = x_value;
        }
    }
}

// Function collects all eezz events from page using WEB-socket to
// send a request to the server
// ------------------------------------------------------------------------------------------
function eezzy_click(aEvent, aElement) {
    var x_post     = true;
    var x_response = "";
    var x_json     = JSON.parse(aElement.getAttribute('data-eezz-json'));

    if (!x_post) {
        return;
    }

    // Generated elements:
    //if (aElement.hasAttribute('data-eezz-template')) {
    //    if (x_json.call) {
    //        eezzy_get_local_values(aElement, x_json.call.args);
    //    }

    //    if (x_json.update) {
    //        eezzy_get_local_values(aElement, x_json.update);
    //    }
    //    x_response = JSON.stringify(x_json);
    //    g_eezz_web_socket.send(x_response);
    //    return;
    //}

    // User form elements: Collect the input data of this page.
    // The syntax for collection is as follows
    // function: {<name>, args: { name1: "id-of-element"."attribute-of-element", name2:... }, id: element}
    var x_function = x_json.call;
    if (x_function) {
        var x_args    = x_function.args;
        var x_element = document.getElementById(x_function.id);
        var x_attr;

        // We have to put the cells into the correct order again, before sending the result
        for (x_key in x_args) {
            var x_source = x_args[x_key];

            if (x_source.startsWith('[template.')) {
                var x_elem_list;
                var x_elem;
                var x_row_len = 0;
                var x_index;

                x_source      = x_source.replace('template.', 'data-eezz-template=');
                x_elem_list   = x_element.querySelectorAll(x_source);

                for (var i = 0; i < x_elem_list.length; i++) {
                    x_elem    = x_elem_list[i];
                    x_index   = parseInt(x_elem.getAttribute('data-eezz-index'));
                    x_row_len = Math.max(x_row_len, x_index);
                }
                var x_new_row = new Array(x_row_len + 1);
                for (var i = 0; i < x_elem_list.length; i++) {
                    x_elem    = x_elem_list[i];
                    x_index   = parseInt(x_elem.getAttribute('data-eezz-index'));
                    x_new_row[x_index] = x_elem['value'];
                }
                x_json.call.args[x_key] = x_new_row;
            }
        }
    }

    if (x_json.call) {
        eezzy_get_local_values(aElement, x_json.call.args);
    }
    if (x_json.update) {
        eezzy_get_local_values(aElement, x_json.update);
    }

    if (x_json.call || x_json.update) {
        try {
            x_response = JSON.stringify(x_json);
            g_eezz_web_socket.send(x_response);
        } catch(err) {
            eezz_status('error ' + err);
        }
    }
}
