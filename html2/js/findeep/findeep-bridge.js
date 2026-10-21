/**
 * CMS findeep 전용 스크립트 대체 브릿지
 * - 라이브: /findeep/d3.bubblecloud.js, /findeep/js/img_tools.js, /findeep/js/default.js 등
 * - DNS/로컬: 공개 배포되지 않은 자산 대신 no-op / 가드 제공
 */
(function (global) {
  "use strict";

  if (typeof global.bubbleCloud !== "function") {
    global.bubbleCloud = function bubbleCloud(target) {
      var el = typeof target === "string" ? document.querySelector(target) : target;
      if (el) el.innerHTML = "";
    };
  }

  if (typeof global.getTfModel !== "function") {
    global.getTfModel = function getTfModel() {
      return Promise.reject(new Error("TensorFlow image model unavailable (CMS /findeep/js/tf required)"));
    };
  }

  if (typeof global.getImgVector !== "function") {
    global.getImgVector = function getImgVector() {
      return Promise.reject(new Error("getImgVector unavailable (CMS /findeep/js/img_tools.js required)"));
    };
  }

  ["readIDB", "writeIDB", "updateIDB", "deleteIDB"].forEach(function (name) {
    if (typeof global[name] !== "function") {
      global[name] = function () { return null; };
    }
  });

  if (typeof global.readFileAsync !== "function") {
    global.readFileAsync = function readFileAsync(file) {
      return new Promise(function (resolve, reject) {
        var reader = new FileReader();
        reader.onload = function () { resolve(reader.result); };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    };
  }
})(typeof window !== "undefined" ? window : this);
