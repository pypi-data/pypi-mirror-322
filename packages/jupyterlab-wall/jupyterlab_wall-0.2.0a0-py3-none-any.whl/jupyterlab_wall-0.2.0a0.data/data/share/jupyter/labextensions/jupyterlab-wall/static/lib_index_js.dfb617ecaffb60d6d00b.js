"use strict";
(self["webpackChunkjupyterlab_wall"] = self["webpackChunkjupyterlab_wall"] || []).push([["lib_index_js"],{

/***/ "./lib/alertHeader.js":
/*!****************************!*\
  !*** ./lib/alertHeader.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AlertHeader: () => (/* binding */ AlertHeader)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_jupyterlab_wall_warning_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/jupyterlab_wall_warning.svg */ "./style/jupyterlab_wall_warning.svg");
/* harmony import */ var _style_jupyterlab_wall_menu_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/jupyterlab_wall_menu.svg */ "./style/jupyterlab_wall_menu.svg");






const alertIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
    name: 'jupyterlab-wall:alert',
    svgstr: _style_jupyterlab_wall_warning_svg__WEBPACK_IMPORTED_MODULE_4__
});
const menuIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
    name: 'jupyterlab-wall:menu',
    svgstr: _style_jupyterlab_wall_menu_svg__WEBPACK_IMPORTED_MODULE_5__
});
class AlertHeader extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(alerts, manager) {
        super({ node: document.createElement('div') });
        this.addAlert = async (_, m) => {
            if (this.findAlertIndex(m) > -1) {
                console.error(`attempting to add duplicate value ${m.getID()}`);
                return Promise.resolve();
            }
            if (this.findAlertIndex(m) === -1) {
                this.alerts.push(m);
                this.alerts.sort((a, b) => {
                    if (a.getPriority() < b.getPriority()) {
                        return -1;
                    }
                    else {
                        return 1;
                    }
                });
                this.setActiveAlert(0);
            }
            return Promise.resolve();
        };
        this.removeAlert = async (_, m) => {
            if (this.alerts.length === 0) {
                console.error('trying to remove from an empty array');
                return Promise.resolve();
            }
            const i = this.findAlertIndex(m);
            if (i === -1) {
                console.error(`${m.getID()} not found for removal`);
                return;
            }
            else if (i < this.alerts.length) {
                this.alerts.splice(i, 1);
            }
            if (this.alerts.length > 0) {
                this.setActiveAlert(0);
            }
            else {
                this.close();
                this.dispose();
            }
            return Promise.resolve();
        };
        this._alertDismissed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this.id = `jp-jupyterlab-wall-alert-header-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4()}`;
        this.addClass('jp-jupyterlab-wall-header');
        this.title.label = 'JupyterLab Alert';
        this.title.caption = alerts[0].getMessage();
        this.alerts = Array.from(alerts);
        this.activeAlert = 0;
        this.nextAlert = this.alerts.length === 1 ? 0 : 1;
        this.manager = manager;
        this.manager.attachHeader(this);
        this.manager.alertAddedSignal.connect(this.addAlert, this);
        this.manager.alertRemovedSignal.connect(this.removeAlert, this);
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('jp-jupyterlab-wall-header-icon');
        alertIcon.element({ container: alertDiv });
        this.alertMessageOuterDiv = document.createElement('div');
        this.alertMessageOuterDiv.classList.add('jp-jupyterlab-wall-header-message');
        this.alertMessageDiv = document.createElement('p');
        this.alertMessageOuterDiv.append(this.alertMessageDiv);
        this.sidePanel = document.createElement('div');
        this.sidePanel.classList.add('jp-jupyterlab-wall-header-sidepanel');
        this.sidePanelButtonDiv = document.createElement('div');
        this.sidePanelButtonDiv.classList.add('jp-jupyterlab-wall-header-button-outer');
        this.sidePanelButtonDiv.onclick = () => {
            this.sidePanel.classList.toggle('jp-jupyterlab-wall-header-sidepanel-open');
        };
        this.sidePanelOpenButton = document.createElement('div');
        this.sidePanelOpenButton.classList.add('jp-jupyterlab-wall-header-button');
        this.sidePanelOpenButton.classList.add('jp-icon-selectable-inverse');
        menuIcon.element({ container: this.sidePanelOpenButton });
        this.sidePanelButtonDiv.append(this.sidePanelOpenButton);
        const alertMenu = document.createElement('ul');
        alertMenu.classList.add('jp-jupyterlab-wall-header-menu');
        const alertCloseListItem = document.createElement('li');
        this.alertCloseLabel = document.createElement('span');
        const alertCloseIcon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.closeIcon.element();
        alertCloseIcon.classList.add('jp-jupyterlab-wall-header-menu-item-icon');
        alertCloseListItem.classList.add('jp-jupyterlab-wall-header-menu-item');
        alertCloseListItem.onclick = async () => {
            try {
                this._alertDismissed.emit(this.alerts[this.activeAlert]);
            }
            catch (e) {
                console.error('Failed to get active alert and send dismissed signal');
                console.error(e);
            }
        };
        alertCloseListItem.append(alertCloseIcon);
        alertCloseListItem.append(this.alertCloseLabel);
        this.alertSwitchListItem = document.createElement('li');
        this.alertSwitchListItem.classList.add('jp-jupyterlab-wall-header-menu-item');
        this.alertSwitchListItem.onclick = () => {
            this.setActiveAlert(this.nextAlert);
        };
        const iconString = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.fastForwardIcon.svgstr
            .replace('width="24"', 'width="16"')
            .replace('height="24"', 'height="16"');
        const alertSwitchIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
            name: 'jupyterlab-wall:next-alert',
            svgstr: iconString
        });
        const alertSwitchIconElement = alertSwitchIcon.element();
        alertSwitchIconElement.classList.add('jp-jupyterlab-wall-header-menu-item-icon');
        this.alertSwitchListItem.append(alertSwitchIconElement);
        this.alertSwitchLabel = document.createElement('span');
        this.alertSwitchLabel.textContent = '';
        this.alertSwitchListItem.append(this.alertSwitchLabel);
        const alertActiveCountsListItem = document.createElement('div');
        alertActiveCountsListItem.classList.add('jp-jupyterlab-wall-header-menu-item');
        const alertActiveCountsIcon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.blankIcon.element();
        alertActiveCountsIcon.classList.add('jp-jupyterlab-wall-header-menu-item-icon');
        this.alertActiveCountsLabel = document.createElement('span');
        alertActiveCountsListItem.append(alertActiveCountsIcon);
        alertActiveCountsListItem.append(this.alertActiveCountsLabel);
        alertMenu.append(alertCloseListItem);
        alertMenu.append(this.alertSwitchListItem);
        alertMenu.append(alertActiveCountsListItem);
        this.sidePanel.append(alertMenu);
        this.setActiveAlert(0);
        this.node.append(alertDiv);
        this.node.append(this.alertMessageOuterDiv);
        this.node.append(this.sidePanelButtonDiv);
        this.node.append(this.sidePanel);
    }
    get alertDismissed() {
        return this._alertDismissed;
    }
    getAlerts() {
        return Array.from(this.alerts);
    }
    dispose() {
        super.dispose();
        this.manager.detachHeader(this);
        this.manager.alertRemovedSignal.disconnect(this.addAlert, this);
        this.manager.alertAddedSignal.disconnect(this.removeAlert, this);
    }
    setActiveAlert(i) {
        const lastActive = this.activeAlert;
        if (i > -1 && i < this.alerts.length) {
            this.activeAlert = i;
            if (i === this.alerts.length - 1) {
                this.nextAlert = 0;
            }
            else {
                this.nextAlert = i + 1;
            }
            const message = this.alerts[this.activeAlert].getMessage();
            const alertType = this.alerts[this.activeAlert].getType();
            const nextType = this.alerts[this.nextAlert].getType();
            this.alertMessageDiv.setAttribute('title', message);
            this.alertMessageDiv.textContent = `${this.alerts[this.activeAlert].getMessage()} - ${this.alerts[this.activeAlert].getStartDateTime()}`;
            this.alertCloseLabel.textContent = `Dismiss ${alertType}`;
            if (this.alerts.length > 1) {
                if (lastActive !== this.activeAlert) {
                    // replace the node to reset the message animation
                    this.alertMessageOuterDiv.removeChild(this.alertMessageDiv);
                    void this.alertMessageDiv.offsetWidth;
                    this.alertMessageOuterDiv.append(this.alertMessageDiv);
                }
                // make sure display:none is removed
                this.alertSwitchListItem.style.display = '';
                this.alertSwitchLabel.textContent = `View ${nextType}`;
                this.alertActiveCountsLabel.textContent = `${this.alerts.length} alerts`;
            }
            else {
                // hide the switch message item if there is only one message
                this.alertSwitchListItem.style.display = 'none';
                this.alertSwitchLabel.textContent = '';
                this.alertActiveCountsLabel.textContent = `${this.alerts.length} alert`;
            }
        }
        else {
            console.error(`${i} out of range for this.alerts in setActiveAlert`);
        }
        this.update();
    }
    findAlertIndex(alert) {
        for (let i = this.alerts.length - 1; i >= 0; i--) {
            if (this.alerts[i].getID() === alert.getID()) {
                return i;
            }
        }
        return -1;
    }
}


/***/ }),

/***/ "./lib/alertManager.js":
/*!*****************************!*\
  !*** ./lib/alertManager.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ACTIVE_ALERTS: () => (/* binding */ ACTIVE_ALERTS),
/* harmony export */   AlertManager: () => (/* binding */ AlertManager),
/* harmony export */   DISMISSED_ALERTS: () => (/* binding */ DISMISSED_ALERTS),
/* harmony export */   TRIGGER_COMMANDS: () => (/* binding */ TRIGGER_COMMANDS)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _alertMessage__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./alertMessage */ "./lib/alertMessage.js");
/* harmony import */ var _alertHeader__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./alertHeader */ "./lib/alertHeader.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");






// state string keys for saving and fetching saved alerts
const ACTIVE_ALERTS = 'jupyterlab-wall:activeAlerts';
const DISMISSED_ALERTS = 'jupyterlab-wall:dismissedAlerts';
/* JupyterLab commands that correspond to MainAreaWidget tab creation */
const TRIGGER_COMMANDS = [
    'code-viewer:open',
    'console:open',
    'console:create',
    'docmanager:clone',
    'docmanager:new-untitled',
    'docmanager:open',
    'fileeditor:create-new',
    'fileeditor:create-new-markdown-file',
    'launcher:create',
    'notebook:create-new',
    'terminal:create-new'
];
class AlertManager extends Object {
    constructor(app, state) {
        super();
        this._alertAddedSignal = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._alertRemovedSignal = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._handleIncomingAlerts = async () => {
            const serviceAlerts = await this._getServiceAlerts();
            // get the current active alerts in widgets
            const prevServiceAlerts = await this._getSavedAlerts(ACTIVE_ALERTS);
            // exit if nothing to do
            if (serviceAlerts.length === 0 && prevServiceAlerts.length === 0) {
                return;
            }
            const dismissedAlerts = await this._getSavedAlerts(DISMISSED_ALERTS);
            // clean out obsolete alerts from widgets
            prevServiceAlerts.forEach(value => {
                for (let i = serviceAlerts.length - 1; i >= 0; i--) {
                    if (value.getID() === serviceAlerts[i].getID()) {
                        return;
                    }
                }
                for (let i = dismissedAlerts.length - 1; i >= 0; i--) {
                    if (value.getID() === dismissedAlerts[i].getID()) {
                        return;
                    }
                }
                this._alertRemovedSignal.emit(value);
            });
            // clean out dismissed alerts that are no longer active
            const updatedDismissedAlerts = Array.from(dismissedAlerts).filter(value => {
                for (let i = serviceAlerts.length - 1; i >= 0; i--) {
                    if (serviceAlerts[i].getID() === value.getID()) {
                        return true;
                    }
                }
                return false;
            });
            await this._saveAlerts(updatedDismissedAlerts, DISMISSED_ALERTS);
            // drop pre-existing and dismissed alerts before sending
            const existingTabAlerts = Array.from(serviceAlerts).filter(value => {
                for (let i = updatedDismissedAlerts.length - 1; i >= 0; i--) {
                    if (updatedDismissedAlerts[i].getID() === value.getID()) {
                        return false;
                    }
                }
                for (let i = prevServiceAlerts.length - 1; i >= 0; i--) {
                    if (prevServiceAlerts[i].getID() === value.getID()) {
                        return false;
                    }
                }
                return true;
            });
            // save the current set of alerts to state
            await this._saveAlerts(serviceAlerts, ACTIVE_ALERTS);
            for (const value of existingTabAlerts) {
                this._alertAddedSignal.emit(value);
                await this._handleNewHeaders();
                this._sendNotification(value);
            }
            return Promise.resolve();
        };
        this.app = app;
        this.state = state;
        this.stateMutex = new _utils__WEBPACK_IMPORTED_MODULE_2__.Mutex();
        this.pollInterval = 5000 + Math.floor(Math.random() * 1001);
        this.app.commands.commandExecuted.connect(async (_, args) => {
            // make sure new tabs opened after alerts have started will get a header
            if (TRIGGER_COMMANDS.indexOf(args.id) > -1) {
                await args.result;
                await this._handleNewHeaders();
            }
            return Promise.resolve(args);
        });
    }
    getPollInterval() {
        return this.pollInterval;
    }
    async watchAlertStatus() {
        setInterval(this._handleIncomingAlerts, this.pollInterval);
    }
    get alertAddedSignal() {
        return this._alertAddedSignal;
    }
    get alertRemovedSignal() {
        return this._alertRemovedSignal;
    }
    attachHeader(h) {
        h.alertDismissed.connect(this._dismissAlert, this);
    }
    detachHeader(h) {
        h.alertDismissed.disconnect(this._dismissAlert, this);
    }
    async _handleNewHeaders() {
        // get the current active alerts in widgets
        const serviceAlerts = await this._getSavedAlerts(ACTIVE_ALERTS);
        // exit if nothing to do
        if (serviceAlerts.length === 0) {
            return;
        }
        // clean out dismissed alerts that are no longer active
        const dismissedAlerts = await this._getSavedAlerts(DISMISSED_ALERTS);
        // drop any dismissed alerts from incoming alerts for widgets
        const newTabAlerts = Array.from(serviceAlerts).filter(value => {
            for (let i = dismissedAlerts.length - 1; i >= 0; i--) {
                if (dismissedAlerts[i].getID() === value.getID()) {
                    return false;
                }
            }
            return true;
        });
        if (newTabAlerts.length === 0) {
            return;
        }
        const shell = this.app.shell;
        const widgets = shell.widgets();
        let w = null;
        const processWidgets = () => {
            w = widgets.next().value;
            try {
                console.log(w);
                if (w instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget &&
                    !w.isDisposed &&
                    w.contentHeader.widgets.length === 0) {
                    // create a new widget with current alerts
                    const widget = new _alertHeader__WEBPACK_IMPORTED_MODULE_3__.AlertHeader(newTabAlerts, this);
                    w.contentHeader.direction = 'left-to-right';
                    w.contentHeader.addWidget(widget);
                }
            }
            catch (reason) {
                console.error(`Unexpected error adding alert to tab.\n${reason}`);
            }
            if (w !== undefined) {
                setTimeout(processWidgets, 1);
            }
        };
        processWidgets();
        return Promise.resolve();
    }
    async _getServiceAlerts() {
        // fetch alert status from the backend service
        return (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('should_alert').then(async (result) => {
            try {
                if (result === null || result === undefined) {
                    return [];
                }
                const alertMessages = [];
                for (const k in result.data) {
                    if (result.data[k]['active']) {
                        const message = new _alertMessage__WEBPACK_IMPORTED_MODULE_5__.AlertMessage(k, result.data[k].message, result.data[k].priority, result.data[k].start);
                        alertMessages.push(message);
                    }
                }
                return alertMessages;
            }
            catch (e) {
                console.error('should_alert request failed');
                console.error(e);
                return [];
            }
        });
    }
    async _dismissAlert(_, m) {
        const dismissedAlerts = await this._getSavedAlerts(DISMISSED_ALERTS);
        dismissedAlerts.push(m);
        await this._saveAlerts(dismissedAlerts, DISMISSED_ALERTS);
        this._alertRemovedSignal.emit(m);
        return Promise.resolve();
    }
    async _getSavedAlerts(alertsKey) {
        return this.state
            .fetch(alertsKey)
            .then(alertsValue => {
            if (alertsValue === undefined) {
                return [];
            }
            const alertsJSON = JSON.parse(JSON.stringify(alertsValue));
            const alerts = [];
            for (const k in alertsJSON) {
                alerts.push(new _alertMessage__WEBPACK_IMPORTED_MODULE_5__.AlertMessage(alertsJSON[k].type, alertsJSON[k].message, alertsJSON[k].priority, alertsJSON[k].start));
            }
            return alerts;
        })
            .catch(e => {
            console.error(`_fetchAlerts(${alertsKey}) fetch failed`);
            console.error(e);
            return [];
        });
    }
    async _saveAlerts(alerts, alertsKey) {
        await this.stateMutex.lock();
        const alertsJSON = {};
        alerts.forEach(value => (alertsJSON[value.getID()] = value.toJSON()));
        const result = await this.state
            .save(alertsKey, alertsJSON)
            .then(_ => {
            return true;
        })
            .catch(e => {
            console.error(`_saveAlerts(${alerts}, ${alertsKey}) error`);
            console.error(e);
            return false;
        });
        this.stateMutex.unlock();
        return Promise.resolve(result);
    }
    _sendNotification(data) {
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.warning('Alert - ' +
            data.getMessage() +
            '     ' +
            data.getStartDateTime().toISOString());
    }
}


/***/ }),

/***/ "./lib/alertMessage.js":
/*!*****************************!*\
  !*** ./lib/alertMessage.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AlertMessage: () => (/* binding */ AlertMessage),
/* harmony export */   AlertMessageJSON: () => (/* binding */ AlertMessageJSON)
/* harmony export */ });
class AlertMessage {
    constructor(alert, msg, priority, start) {
        this.alertType = alert;
        this.message = msg;
        this.priority = priority;
        this.start = new Date(start);
        this.alertID = this.alertType + '_' + this.start.toISOString();
    }
    getType() {
        return this.alertType;
    }
    getMessage() {
        return this.message;
    }
    getPriority() {
        return this.priority;
    }
    getStartDateTime() {
        return this.start;
    }
    getID() {
        return this.alertID;
    }
    toJSON() {
        return new AlertMessageJSON(this.alertType, this.message, this.priority, this.start.toISOString());
    }
}
class AlertMessageJSON {
    constructor(type, message, priority, start) {
        this.type = type;
        this.message = message;
        this.priority = priority;
        this.start = start;
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
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab_wall', // API Namespace
    endPoint);
    let response;
    try {
        console.log(requestUrl);
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.error(error);
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


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
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _alertManager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./alertManager */ "./lib/alertManager.js");




/**
 * Initialization data for the jupyterlab-wall extension.
 */
const plugin = {
    id: 'jupyterlab-wall:plugin',
    description: 'A JupyterLab extension.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.IStateDB],
    activate: async (app, palette, state) => {
        console.log('JupyterLab extension jupyterlab-wall is activated!');
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyterlab_wall server extension appears to be missing.\n${reason}`);
        });
        try {
            const manager = new _alertManager__WEBPACK_IMPORTED_MODULE_3__.AlertManager(app, state);
            await manager.watchAlertStatus();
        }
        catch (e) {
            console.error(e);
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Mutex: () => (/* binding */ Mutex)
/* harmony export */ });
// Basic locking mechanism to avoid race conditions
class Mutex {
    constructor() {
        this.locked = false;
    }
    lock() {
        return new Promise(resolve => {
            if (this.locked) {
                setTimeout(() => this.lock().then(resolve), 100);
            }
            else {
                this.locked = true;
                resolve();
            }
        });
    }
    unlock() {
        this.locked = false;
    }
}


/***/ }),

/***/ "./style/jupyterlab_wall_menu.svg":
/*!****************************************!*\
  !*** ./style/jupyterlab_wall_menu.svg ***!
  \****************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\">\n  <g class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\">\n    <path d=\"M 4 6 H 20 V 4 H 20 L 4 4\"/>\n    <path d=\"M 4 12 H 20 V 10 H 20 L 4 10\"/>\n    <path d=\"M 4 18 H 20 V 16 H 20 L 4 16\"/>\n  </g>\n</svg>";

/***/ }),

/***/ "./style/jupyterlab_wall_warning.svg":
/*!*******************************************!*\
  !*** ./style/jupyterlab_wall_warning.svg ***!
  \*******************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<svg width=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n    <path d=\"M3 18L10 4C10 3 13 3 13 4L20 18C20.5 19 20 21 18 21H5C3.5 21 2 19.75 3 18Z\" stroke=\"#000000\" fill=\"#eed202\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>\n    <circle cx=\"11.5\" cy=\"17\" r=\"1\" fill=\"#000000\"/>\n    <path d=\"M11.5 10L11.5 14\" stroke=\"#000000\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>\n</svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.dfb617ecaffb60d6d00b.js.map