/* This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
* Copyright © Nastaran Saffaryazdi 2021
*
* Octopus Sensing Visualizer is a free software: you can redistribute it and/or modify it under the
* terms of the GNU General Public License as published by the Free Software Foundation,
*  either version 3 of the License, or (at your option) any later version.
*
* Octopus Sensing Visualizer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
* See the GNU General Public License for more details.
*
 You should have received a copy of the GNU General Public License along with Octopus Sensing Visualizer.
* If not, see <https://www.gnu.org/licenses/>.
*/
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
// data to be sent to the POST request
export function fetchServerData(window_size, start_time) {
    var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p;
    return __awaiter(this, void 0, void 0, function* () {
        const post_data = {
            window_size: window_size,
            start_time: start_time,
        };
        const body = {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(post_data),
        };
        const response = yield fetch('http://' + window.location.host + '/api/get_data', body);
        if (!response.ok) {
            return Promise.reject('Could not fetch data from the server: ' + response.statusText);
        }
        const jsonResponse = yield response.json();
        const data = {
            eeg: (_a = jsonResponse.eeg) !== null && _a !== void 0 ? _a : null,
            gsr: (_b = jsonResponse.gsr) !== null && _b !== void 0 ? _b : null,
            ppg: (_c = jsonResponse.ppg) !== null && _c !== void 0 ? _c : null,
            powerBands: (_d = jsonResponse.power_bands) !== null && _d !== void 0 ? _d : null,
            deltaBand: (_e = jsonResponse.delta_band) !== null && _e !== void 0 ? _e : null,
            thetaBand: (_f = jsonResponse.theta_band) !== null && _f !== void 0 ? _f : null,
            alphaBand: (_g = jsonResponse.alpha_band) !== null && _g !== void 0 ? _g : null,
            betaBand: (_h = jsonResponse.beta_band) !== null && _h !== void 0 ? _h : null,
            gammaBand: (_j = jsonResponse.gamma_band) !== null && _j !== void 0 ? _j : null,
            gsrPhasic: (_k = jsonResponse.gsr_phasic) !== null && _k !== void 0 ? _k : null,
            gsrTonic: (_l = jsonResponse.gsr_tonic) !== null && _l !== void 0 ? _l : null,
            hr: (_m = jsonResponse.hr) !== null && _m !== void 0 ? _m : null,
            hrv: (_o = jsonResponse.hrv) !== null && _o !== void 0 ? _o : null,
            breathingRate: (_p = jsonResponse.breathing_rate) !== null && _p !== void 0 ? _p : null,
        };
        return data;
    });
}
export function fetchServerMetadata() {
    var _a, _b, _c, _d;
    return __awaiter(this, void 0, void 0, function* () {
        const response = yield fetch('http://' + window.location.host + '/api/get_metadata');
        if (!response.ok) {
            return Promise.reject('Could not fetch data from the server: ' + response.statusText);
        }
        const jsonResponse = yield response.json();
        const metadata = {
            dataLength: (_a = jsonResponse.data_length) !== null && _a !== void 0 ? _a : null,
            enabledGraphs: (_b = jsonResponse.enabled_graphs) !== null && _b !== void 0 ? _b : null,
            eegChannels: (_c = jsonResponse.eeg_channels) !== null && _c !== void 0 ? _c : null,
            samplingRates: (_d = jsonResponse.sampling_rate) !== null && _d !== void 0 ? _d : null,
        };
        return metadata;
    });
}
//# sourceMappingURL=services.js.map