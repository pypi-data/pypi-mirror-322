"use strict";
(self["webpackChunkclimb_onyx_gui_extension"] = self["webpackChunkclimb_onyx_gui_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/agateWidget.js":
/*!****************************!*\
  !*** ./lib/agateWidget.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AgateWidget: () => (/* binding */ AgateWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var climb_agate_gui__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! climb-agate-gui */ "webpack/sharing/consume/default/climb-agate-gui/climb-agate-gui");
/* harmony import */ var climb_agate_gui__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(climb_agate_gui__WEBPACK_IMPORTED_MODULE_2__);



class AgateWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(route, s3, fw, v) {
        super();
        this.routeHandler = route;
        this.s3PathHandler = s3;
        this.fileWriter = fw;
        this.version = v;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((climb_agate_gui__WEBPACK_IMPORTED_MODULE_2___default()), { httpPathHandler: this.routeHandler, s3PathHandler: this.s3PathHandler, fileWriter: this.fileWriter, extVersion: this.version }));
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI),
/* harmony export */   requestAPIResponse: () => (/* binding */ requestAPIResponse)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}, param = ['', ''], param2 = ['', ''], agate = false) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'climb-onyx-gui', endPoint);
    const url = new URL(requestUrl);
    if (param[0] !== '') {
        url.searchParams.append(param[0], param[1]);
    }
    if (param2[0] !== '') {
        url.searchParams.append(param2[0], param2[1]);
    }
    if (agate)
        url.searchParams.append("agate", "true");
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(url.toString(), init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
async function requestAPIResponse(endPoint = '', init = {}, param = ['', ''], agate = false) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'climb-onyx-gui', endPoint);
    const url = new URL(requestUrl);
    if (param[0] !== '') {
        url.searchParams.append(param[0], param[1]);
    }
    if (agate)
        url.searchParams.append("agate", "true");
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(url.toString(), init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.NetworkError(error);
    }
    return response;
}


/***/ }),

/***/ "./lib/icon.js":
/*!*********************!*\
  !*** ./lib/icon.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   dnaIcon: () => (/* binding */ dnaIcon),
/* harmony export */   innerJoinIcon: () => (/* binding */ innerJoinIcon),
/* harmony export */   openFileIcon: () => (/* binding */ openFileIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_dna_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./../style/icons/dna.svg */ "./style/icons/dna.svg");
/* harmony import */ var _style_icons_inner_join_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../style/icons/inner_join.svg */ "./style/icons/inner_join.svg");
/* harmony import */ var _style_icons_open_file_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../style/icons/open_file.svg */ "./style/icons/open_file.svg");




const dnaIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'climb-onyx-gui:dna',
    svgstr: _style_icons_dna_svg__WEBPACK_IMPORTED_MODULE_1__
});
const innerJoinIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'climb-onyx-gui:inner-join',
    svgstr: _style_icons_inner_join_svg__WEBPACK_IMPORTED_MODULE_2__
});
const openFileIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'climb-onyx-gui:open-file',
    svgstr: _style_icons_open_file_svg__WEBPACK_IMPORTED_MODULE_3__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/htmlviewer */ "webpack/sharing/consume/default/@jupyterlab/htmlviewer");
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _onyxWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./onyxWidget */ "./lib/onyxWidget.js");
/* harmony import */ var _agateWidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./agateWidget */ "./lib/agateWidget.js");
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");
/* harmony import */ var _openS3FileWidget__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./openS3FileWidget */ "./lib/openS3FileWidget.js");









/**
 * Initialization data for the climb-onyx-gui extension.
 */
const plugin = {
    id: 'climb-onyx-gui-extension:plugin',
    description: 'JupyterLab extension for the Onyx Graphical User Interface',
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher, _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.IHTMLViewerTracker],
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager],
    activate: (app, palette, documentManager, launcher, htmlTracker) => {
        console.log('JupyterLab extension @climb-onyx-gui is activated!');
        const docs_command = 'docs_extension';
        const onyx_command = 'onyx_extension';
        const agate_command = 'agate_extension';
        const s3_command = 's3_onyx_extension';
        const category = 'CLIMB-TRE';
        let version = '';
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('version')
            .then(data => {
            version = data['version'];
            console.log(`JupyterLab extension version: ${version}`);
        })
            .catch(_ => { });
        const httpPathHandler = async (route) => {
            return (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPIResponse)('reroute', {}, ['route', route]);
        };
        const httpAgatePathHandler = async (route) => {
            return (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPIResponse)('reroute', {}, ['route', route], true);
        };
        const s3PathHandler = async (path) => {
            return (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('s3', {}, ['s3location', path]).then(data => {
                documentManager.open(data['temp_file']);
            });
        };
        const fileWriteHandler = async (path, content) => {
            return (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('file-write', {
                body: JSON.stringify({ content: content }),
                method: 'POST'
            }, ['path', path]).then(data => {
                documentManager.open(data['path']);
            });
        };
        app.commands.addCommand(docs_command, {
            label: 'CLIMB-TRE Documentation',
            caption: 'CLIMB-TRE Documentation',
            icon: _icon__WEBPACK_IMPORTED_MODULE_5__.dnaIcon,
            execute: () => {
                // Open link in new tab
                window.open('https://climb-tre.github.io/');
            }
        });
        // Create a single widget
        let widget;
        app.commands.addCommand(onyx_command, {
            label: 'Onyx',
            caption: 'Onyx',
            icon: _icon__WEBPACK_IMPORTED_MODULE_5__.innerJoinIcon,
            execute: () => {
                if (!widget || widget.disposed) {
                    const content = new _onyxWidget__WEBPACK_IMPORTED_MODULE_6__.OnyxWidget(httpPathHandler, s3PathHandler, fileWriteHandler, version);
                    content.addClass('onyx-Widget');
                    widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                    widget.title.label = 'Onyx';
                    widget.title.closable = true;
                }
                if (!tracker.has(widget)) {
                    tracker.add(widget);
                }
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
            }
        });
        // Create a single agate widget
        let agate_widget;
        app.commands.addCommand(agate_command, {
            label: 'Agate',
            caption: 'Agate',
            icon: _icon__WEBPACK_IMPORTED_MODULE_5__.dnaIcon,
            execute: () => {
                if (!agate_widget || agate_widget.disposed) {
                    const content = new _agateWidget__WEBPACK_IMPORTED_MODULE_7__.AgateWidget(httpAgatePathHandler, s3PathHandler, fileWriteHandler, version);
                    content.addClass('agate-Widget');
                    agate_widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                    agate_widget.title.label = 'Agate';
                    agate_widget.title.closable = true;
                }
                if (!agate_tracker.has(agate_widget)) {
                    agate_tracker.add(agate_widget);
                }
                if (!agate_widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(agate_widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(agate_widget.id);
            }
        });
        app.commands.addCommand(s3_command, {
            label: 'Open S3 Document',
            caption: 'Open S3 Document',
            icon: _icon__WEBPACK_IMPORTED_MODULE_5__.openFileIcon,
            execute: () => {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    body: new _openS3FileWidget__WEBPACK_IMPORTED_MODULE_8__.OpenS3FileWidget(),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'GO' })],
                    focusNodeSelector: 'input',
                    title: 'Open S3 Document'
                })
                    .then(result => {
                    if (result.button.label === 'Cancel') {
                        return;
                    }
                    if (!result.value) {
                        return;
                    }
                    const s3_link = result.value;
                    s3PathHandler(s3_link).catch(reason => {
                        console.error(`The climb-onyx-gui server extension appears to be missing.\n${reason}`);
                    });
                })
                    .catch(reason => {
                    console.error(`The climb-onyx-gui server extension appears to be missing.\n${reason}`);
                });
            }
        });
        palette.addItem({ command: docs_command, category: category });
        palette.addItem({ command: onyx_command, category: category });
        palette.addItem({ command: s3_command, category: category });
        if (launcher) {
            launcher.add({ command: docs_command, category: category });
            launcher.add({ command: onyx_command, category: category });
            launcher.add({ command: s3_command, category: category });
        }
        httpAgatePathHandler("").then(data => {
            if (data.status == 200) {
                palette.addItem({ command: agate_command, category: category });
                if (launcher)
                    launcher.add({ command: agate_command, category: category });
            }
        });
        if (htmlTracker) {
            htmlTracker.widgetAdded.connect((sender, panel) => {
                panel.trusted = true;
            });
        }
    }
};
const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({
    namespace: 'climb-onyx-gui'
});
const agate_tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({
    namespace: 'climb-agate-gui'
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/onyxWidget.js":
/*!***************************!*\
  !*** ./lib/onyxWidget.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   OnyxWidget: () => (/* binding */ OnyxWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var climb_onyx_gui__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! climb-onyx-gui */ "webpack/sharing/consume/default/climb-onyx-gui/climb-onyx-gui");
/* harmony import */ var climb_onyx_gui__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(climb_onyx_gui__WEBPACK_IMPORTED_MODULE_2__);



class OnyxWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(route, s3, fw, v) {
        super();
        this.httpPathHandler = route;
        this.s3PathHandler = s3;
        this.fileWriter = fw;
        this.version = v;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((climb_onyx_gui__WEBPACK_IMPORTED_MODULE_2___default()), { httpPathHandler: this.httpPathHandler, s3PathHandler: this.s3PathHandler, fileWriter: this.fileWriter, extVersion: this.version }));
    }
}


/***/ }),

/***/ "./lib/openS3FileWidget.js":
/*!*********************************!*\
  !*** ./lib/openS3FileWidget.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   OpenS3FileWidget: () => (/* binding */ OpenS3FileWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

class OpenS3FileWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        const body = document.createElement('div');
        const existingLabel = document.createElement('label');
        existingLabel.textContent = 'S3 file name:';
        const input = document.createElement('input');
        input.value = '';
        input.placeholder = 's3://example-bucket/example-file.html';
        body.appendChild(existingLabel);
        body.appendChild(input);
        super({ node: body });
    }
    get inputNode() {
        return this.node.getElementsByTagName('input')[0];
    }
    getValue() {
        return this.inputNode.value;
    }
}


/***/ }),

/***/ "./style/icons/dna.svg":
/*!*****************************!*\
  !*** ./style/icons/dna.svg ***!
  \*****************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\" width=\"256\" height=\"256\" viewBox=\"0 0 256 256\" xml:space=\"preserve\">\r\n\r\n<defs>\r\n</defs>\r\n<g style=\"stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;\" transform=\"translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)\" >\r\n\t<path fill=\"#d63384\" d=\"M 73.352 33.287 c -1.16 0 -2.35 -0.064 -3.563 -0.193 c -0.824 -0.088 -1.42 -0.827 -1.332 -1.651 c 0.088 -0.825 0.841 -1.413 1.65 -1.333 c 7.211 0.774 13.366 -0.99 17.333 -4.956 c 0.586 -0.586 1.535 -0.586 2.121 0 s 0.586 1.536 0 2.121 C 85.631 31.205 79.962 33.287 73.352 33.287 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 26.214 90 c -0.384 0 -0.768 -0.146 -1.061 -0.439 c -0.586 -0.586 -0.586 -1.535 0 -2.121 c 5.682 -5.683 6.724 -15.295 2.858 -26.374 C 24.045 49.694 24.94 39.392 30.467 32.8 c 4.991 -5.954 13.106 -8.365 22.838 -6.79 c 0.818 0.132 1.374 0.903 1.241 1.721 s -0.907 1.366 -1.72 1.241 c -8.652 -1.401 -15.775 0.645 -20.061 5.755 c -4.831 5.762 -5.531 15.001 -1.92 25.35 c 4.259 12.209 2.958 22.955 -3.57 29.483 C 26.982 89.854 26.598 90 26.214 90 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 42.32 64.459 c -1.732 0 -3.535 -0.144 -5.399 -0.434 c -0.818 -0.128 -1.379 -0.895 -1.251 -1.713 c 0.127 -0.819 0.897 -1.372 1.713 -1.252 c 8.575 1.34 15.636 -0.731 19.881 -5.823 c 4.804 -5.764 5.493 -14.99 1.892 -25.314 c -4.259 -12.21 -2.958 -22.956 3.57 -29.483 c 0.586 -0.586 1.535 -0.586 2.121 0 s 0.586 1.536 0 2.121 c -5.682 5.682 -6.724 15.294 -2.859 26.374 c 3.958 11.344 3.076 21.631 -2.419 28.224 C 55.577 61.946 49.567 64.459 42.32 64.459 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 1.5 65.286 c -0.384 0 -0.768 -0.146 -1.061 -0.439 c -0.586 -0.586 -0.586 -1.535 0 -2.121 c 5.047 -5.047 12.812 -7.013 21.865 -5.536 c 0.817 0.134 1.372 0.904 1.239 1.722 c -0.134 0.818 -0.907 1.372 -1.722 1.239 c -8.073 -1.316 -14.914 0.35 -19.26 4.696 C 2.268 65.14 1.884 65.286 1.5 65.286 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 61.713 51.758 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 38.685 29.351 c -0.586 -0.585 -0.586 -1.536 0 -2.121 c 0.586 -0.586 1.535 -0.586 2.121 0 l 21.968 21.968 c 0.586 0.586 0.586 1.535 0 2.121 C 62.48 51.611 62.097 51.758 61.713 51.758 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 50.258 63.213 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 27.229 40.806 c -0.586 -0.585 -0.586 -1.536 0 -2.121 c 0.586 -0.586 1.535 -0.586 2.121 0 l 21.968 21.968 c 0.586 0.586 0.586 1.535 0 2.121 C 51.025 63.066 50.642 63.213 50.258 63.213 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 82.111 31.79 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 58.646 8.946 c -0.586 -0.585 -0.586 -1.536 0 -2.121 c 0.586 -0.586 1.535 -0.586 2.121 0 l 22.404 22.405 c 0.586 0.585 0.586 1.536 0 2.121 C 82.879 31.644 82.495 31.79 82.111 31.79 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path fill=\"#d63384\" d=\"M 29.133 84.769 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 5.667 61.925 c -0.586 -0.586 -0.586 -1.535 0 -2.121 s 1.535 -0.586 2.121 0 l 22.405 22.404 c 0.586 0.586 0.586 1.535 0 2.121 C 29.9 84.622 29.517 84.769 29.133 84.769 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10;  fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n</g>\r\n</svg>";

/***/ }),

/***/ "./style/icons/inner_join.svg":
/*!************************************!*\
  !*** ./style/icons/inner_join.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" enable-background=\"new 0 0 24 24\" height=\"24px\" viewBox=\"0 0 24 24\" width=\"24px\" fill=\"#d63384\"><g><rect fill=\"none\" height=\"24\" width=\"24\"/></g><g><ellipse cx=\"12\" cy=\"12\" rx=\"3\" ry=\"5.74\"/><g><path d=\"M9.04,16.87C8.71,16.95,8.36,17,8,17c-2.76,0-5-2.24-5-5s2.24-5,5-5c0.36,0,0.71,0.05,1.04,0.13 c0.39-0.56,0.88-1.12,1.49-1.63C9.75,5.19,8.9,5,8,5c-3.86,0-7,3.14-7,7s3.14,7,7,7c0.9,0,1.75-0.19,2.53-0.5 C9.92,17.99,9.43,17.43,9.04,16.87z\"/></g><path d=\"M16,5c-0.9,0-1.75,0.19-2.53,0.5c0.61,0.51,1.1,1.07,1.49,1.63C15.29,7.05,15.64,7,16,7c2.76,0,5,2.24,5,5s-2.24,5-5,5 c-0.36,0-0.71-0.05-1.04-0.13c-0.39,0.56-0.88,1.12-1.49,1.63C14.25,18.81,15.1,19,16,19c3.86,0,7-3.14,7-7S19.86,5,16,5z\"/></g></svg>";

/***/ }),

/***/ "./style/icons/open_file.svg":
/*!***********************************!*\
  !*** ./style/icons/open_file.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" enable-background=\"new 0 0 24 24\" height=\"24px\" viewBox=\"0 0 24 24\" width=\"24px\" fill=\"#d63384\"><g><rect fill=\"none\" height=\"24\" width=\"24\"/></g><g><path d=\"M14,2H6C4.9,2,4,2.9,4,4v16c0,1.1,0.89,2,1.99,2H15v-8h5V8L14,2z M13,9V3.5L18.5,9H13z M17,21.66V16h5.66v2h-2.24 l2.95,2.95l-1.41,1.41L19,19.41l0,2.24H17z\"/></g></svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.99ca47bebe5dfc073a39.js.map