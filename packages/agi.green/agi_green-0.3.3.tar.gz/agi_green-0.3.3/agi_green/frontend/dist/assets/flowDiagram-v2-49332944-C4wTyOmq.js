import { p as parser$1, f as flowDb } from "./flowDb-d35e309a-CacdSHqK.js";
import { f as flowRendererV2, g as flowStyles } from "./styles-7383a064-BD6g6a6I.js";
import { t as setConfig } from "./index-0VOmjb1o.js";
import "./graph-EGokPMbj.js";
import "./layout-DmNyk2Dj.js";
import "./index-8fae9850-BTVU0iyw.js";
import "./clone-DZ6fHa5-.js";
import "./edges-d417c7a0-CiTwUnI4.js";
import "./createText-423428c9-DW8obWQJ.js";
import "./line-BrrJS_hU.js";
import "./array-DgktLKBx.js";
import "./path-Cp2qmpkd.js";
import "./channel-C_ojnRxt.js";
const diagram = {
  parser: parser$1,
  db: flowDb,
  renderer: flowRendererV2,
  styles: flowStyles,
  init: (cnf) => {
    if (!cnf.flowchart) {
      cnf.flowchart = {};
    }
    cnf.flowchart.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    setConfig({ flowchart: { arrowMarkerAbsolute: cnf.arrowMarkerAbsolute } });
    flowRendererV2.setConf(cnf.flowchart);
    flowDb.clear();
    flowDb.setGen("gen-2");
  }
};
export {
  diagram
};
//# sourceMappingURL=flowDiagram-v2-49332944-C4wTyOmq.js.map
