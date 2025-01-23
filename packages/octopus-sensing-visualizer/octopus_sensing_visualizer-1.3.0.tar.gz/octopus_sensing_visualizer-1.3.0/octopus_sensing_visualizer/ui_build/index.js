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
import { Chart, LineController, BarController, BarElement, LinearScale, Title, CategoryScale, PointElement, LineElement, } from 'chart.js';
// To make Charts tree-shakeable, we need to register the components we're using.
Chart.register(BarController, BarElement, LineController, BarController, LinearScale, Title, CategoryScale, PointElement, LineElement);
import { fetchServerData, fetchServerMetadata } from './services';
import { charts, createCharts, updateChart, clearCharts } from './chart';
let playFlag = false;
let window_size = 3;
let dataLength = 3;
function makeCanvas(id, htmlClass) {
    return `
<div class="chart-container">
  <canvas id="${id}" class="${htmlClass}" />
</div>
`;
}
function onWindowSizeChange() {
    const windowSizeBox = document.getElementById('window-size-box');
    window_size = parseInt(windowSizeBox.value);
    const slider = document.getElementById('slider');
    slider.max = (dataLength - window_size + 1).toString();
}
function onPlayPauseClick() {
    const playPauseButton = document.getElementById('play-pause-button');
    if (playFlag == true) {
        playFlag = false;
        playPauseButton.textContent = '\ue019';
    }
    else {
        playFlag = true;
        playPauseButton.textContent = '\ue01a';
    }
    console.log('playpause button is clicked');
}
function onResetClick() {
    playFlag = false;
    const playPauseButton = document.getElementById('play-pause-button');
    playPauseButton.textContent = '\ue01a';
    const slider = document.getElementById('slider');
    slider.value = '0';
    console.log('reset button is clicked');
    clearCharts();
}
export function onSliderChange(sliderAmount) {
    return __awaiter(this, void 0, void 0, function* () {
        // TODO: Draw messages in place of the chart when no data was available.
        const start_time = Number.parseInt(sliderAmount);
        const data = yield fetchServerData(window_size, start_time);
        if (charts.eeg != null) {
            if (data.eeg) {
                const eegData = data.eeg;
                charts.eeg.forEach((chart, idx) => {
                    var _a;
                    if (eegData.length > idx) {
                        updateChart(chart, eegData[idx], start_time);
                    }
                    else {
                        console.error(`Not enough data! charts: ${(_a = charts.eeg) === null || _a === void 0 ? void 0 : _a.length} data: ${eegData.length}`);
                    }
                });
            }
        }
        if (charts.gsr != null) {
            if (data.gsr) {
                updateChart(charts.gsr, data.gsr, start_time);
            }
        }
        if (charts.ppg != null) {
            if (data.ppg) {
                updateChart(charts.ppg, data.ppg, start_time);
            }
        }
        console.log(data.powerBands);
        if (charts.powerBands != null) {
            if (data.powerBands) {
                console.log(data.powerBands);
                updateChart(charts.powerBands, data.powerBands, start_time);
            }
        }
        if (charts.deltaBand != null) {
            if (data.deltaBand) {
                updateChart(charts.deltaBand, data.deltaBand, start_time);
            }
        }
        if (charts.thetaBand != null) {
            if (data.thetaBand) {
                updateChart(charts.thetaBand, data.thetaBand, start_time);
            }
        }
        if (charts.alphaBand != null) {
            if (data.alphaBand) {
                updateChart(charts.alphaBand, data.alphaBand, start_time);
            }
        }
        if (charts.betaBand != null) {
            if (data.betaBand) {
                updateChart(charts.betaBand, data.betaBand, start_time);
            }
        }
        if (charts.gammaBand != null) {
            if (data.gammaBand) {
                updateChart(charts.gammaBand, data.gammaBand, start_time);
            }
        }
        if (charts.gsrPhasic != null) {
            if (data.gsrPhasic) {
                updateChart(charts.gsrPhasic, data.gsrPhasic, start_time);
            }
        }
        if (charts.gsrTonic != null) {
            if (data.gsrTonic) {
                updateChart(charts.gsrTonic, data.gsrTonic, start_time);
            }
        }
        if (charts.hr != null) {
            if (data.hr) {
                updateChart(charts.hr, data.hr, start_time);
            }
        }
        if (charts.hrv != null) {
            if (data.hrv) {
                updateChart(charts.hrv, data.hrv, start_time);
            }
        }
        if (charts.breathingRate != null) {
            if (data.breathingRate) {
                updateChart(charts.breathingRate, data.breathingRate, start_time);
            }
        }
    });
}
function initControls() {
    try {
        const slider = document.getElementById('slider');
        slider.value = '0';
        slider.min = '0';
        slider.max = (dataLength - window_size + 1).toString();
        slider.step = '1';
        slider.onchange = () => onSliderChange(slider.value);
        const windowSizeBox = document.getElementById('window-size-box');
        windowSizeBox.min = '1';
        windowSizeBox.max = dataLength.toString();
        windowSizeBox.value = '3';
        windowSizeBox.onchange = () => onWindowSizeChange();
        const playPauseButton = document.getElementById('play-pause-button');
        playPauseButton.textContent = '\ue01a';
        playFlag = false;
        playPauseButton.onclick = () => onPlayPauseClick();
        const resetButton = document.getElementById('reset-button');
        resetButton.onclick = () => onResetClick();
    }
    catch (error) {
        // TODO: Show a notification or something
        console.error(error);
    }
}
function changeSliderValue() {
    if (playFlag == true) {
        const slider = document.getElementById('slider');
        const sliderAmount = Number.parseInt(slider.value) + 1;
        slider.value = sliderAmount.toString();
        onSliderChange(slider.value);
    }
}
function makeHtml(metaData) {
    return __awaiter(this, void 0, void 0, function* () {
        let pageHtml = '<div id="signal-container">';
        if (metaData.enabledGraphs.some((x) => x == 'gsr')) {
            pageHtml += '<div class="title">GSR</div>';
            pageHtml += makeCanvas('gsr', 'big-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'gsr_phasic')) {
            pageHtml += '<div class="title">GSR Phasic</div>';
            pageHtml += makeCanvas('gsr_phasic', 'big-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'gsr_tonic')) {
            pageHtml += '<div class="title">GSR Tonic</div>';
            pageHtml += makeCanvas('gsr_tonic', 'big-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'ppg')) {
            pageHtml += '<div class="title">PPG</div>';
            pageHtml += makeCanvas('ppg', 'big-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'eeg')) {
            pageHtml += '<div class="title">EEG</div>';
            if (metaData.eegChannels != null) {
                for (let idx = 0; idx < metaData.eegChannels.length; idx++) {
                    const id = 'eeg-' + idx;
                    pageHtml += `<div class="title">${metaData.eegChannels[idx]}</div>`;
                    pageHtml += makeCanvas(id, 'big-line-chart');
                }
            }
        }
        pageHtml += '</div>';
        pageHtml += '<div id="others-container">';
        if (metaData.enabledGraphs.some((x) => x == 'hr')) {
            pageHtml += '<div class="title">HR</div>';
            pageHtml += makeCanvas('hr', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'hrv')) {
            pageHtml += '<div class="title">HRV</div>';
            pageHtml += makeCanvas('hrv', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'breathing_rate')) {
            pageHtml += '<div class="title">Breathing Rate</div>';
            pageHtml += makeCanvas('breathing_rate', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'power_bands')) {
            console.log('power bands');
            pageHtml += '<div class="title">Power Bands</div>';
            pageHtml += makeCanvas('power_bands', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'delta_band')) {
            pageHtml += '<div class="title">Delta Band</div>';
            pageHtml += makeCanvas('delta_band', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'theta_band')) {
            pageHtml += '<div class="title">Theta Band</div>';
            pageHtml += makeCanvas('theta_band', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'alpha_band')) {
            pageHtml += '<div class="title">Alpha Band</div>';
            pageHtml += makeCanvas('alpha_band', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'beta_band')) {
            pageHtml += '<div class="title">Beta Band</div>';
            pageHtml += makeCanvas('beta_band', 'small-line-chart');
        }
        if (metaData.enabledGraphs.some((x) => x == 'gamma_band')) {
            pageHtml += '<div class="title">Gamma Band</div>';
            pageHtml += makeCanvas('gamma_band', 'small-line-chart');
        }
        //pageHtml += '<div class="title">Camera</div>'
        //pageHtml += '<img id="webcam-image" src=""></img>'
        pageHtml += '</div>';
        return pageHtml;
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        const metadata = yield fetchServerMetadata();
        const pageHtml = yield makeHtml(metadata);
        dataLength = metadata.dataLength;
        const dataElement = document.getElementById('data-container');
        if (!dataElement) {
            throw new Error('Data element is null!');
        }
        dataElement.innerHTML = pageHtml;
        createCharts(metadata.enabledGraphs);
        initControls();
        setInterval(changeSliderValue, 1000);
    });
}
main();
//# sourceMappingURL=index.js.map